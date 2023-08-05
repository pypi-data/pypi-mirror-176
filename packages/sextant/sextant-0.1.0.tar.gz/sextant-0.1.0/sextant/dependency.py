"""
Simple dependency resolver. It is simplified by the fact our modules have well defined dependencies.

SPDX-License-Identifier: GPL-3.0-or-later
"""
import json
import pathlib
from typing import List, Optional

from sextant import log
from sextant.module import Module, Registry


class DependencyError(Exception):
    """Special exception for dependencies errors."""


class Dependency:
    """Graph edge for the dependency tree"""

    def __init__(self, module: Module, root: Optional["Dependency"]):
        self.root = root
        self.module = module
        self.branches: List["Dependency"] = []

    def is_compatible(self, other: "Dependency") -> bool:
        """Check if two modules are compatible."""
        if self == other:
            return True
        if self.module.namespace != other.module.namespace:
            return True
        if self.module.name != other.module.name:
            return True
        # The modules are different, but they have same module and namespace.
        # This means they're on differing versions. Are those compatible?
        # Modules make the promise of not being incompatible
        # across patch versions.
        # NOTE: given how the Package class works, if this method is called
        # from there, this condition will always be false as the code should
        # always select the same exact patch version.
        if self.module.version[:3] == other.module.version[:3]:
            return True
        return False

    def __eq__(self, other):
        return self.module == other.module

    def __str__(self) -> str:
        if self.root is None:
            return str(self.module)
        # Here we try to avoid the inception of "required by".
        # TODO: maybe go check the original rootless object and create a chain
        return f"{self.module} (required by {self.root.module})"


class Package:
    """Package dependencies for"""

    def __init__(self, registry: Registry, filename: str):
        self.package_modules: List[Dependency] = []
        self.registry = registry
        self.path = pathlib.Path(filename)
        if not self.path.exists():
            raise RuntimeError(f"Dependency file {self.path} does not exist.")
        self.lockfile = self.path.with_suffix(".lock")
        self.modules: List[str] = json.loads(self.path.read_bytes())

    def get(self, force: bool = False) -> List[Module]:
        """Get all the modules from the dependency tree."""
        # First let's check if the lockfile exists
        if not force and self.lockfile.exists():
            return self._read_lockfile()
        self._fetch_dependencies(*self.modules, root=None)
        self._check_dependencies()
        self._write_lockfile()
        return [el.module for el in self.package_modules]

    def lock(self, force: bool = False):
        """Just generate the lockfile"""
        if not force and self.lockfile.exists():
            log.info("Lockfile already exists and --force wasn't specified, not overwriting.")
            return
        self._fetch_dependencies(*self.modules, root=None)
        self._check_dependencies()
        self._write_lockfile()

    def _read_lockfile(self) -> List[Module]:
        try:
            lock = json.loads(self.lockfile.read_bytes())
        except json.decoder.JSONDecodeError as exc:
            raise DependencyError("The lockfile {self.lockfile} contains invalid json data.") from exc
        # If the lockfile is valid, we just need to read the lockfile to load the correct
        # modules.
        out = []
        for mod in lock:
            mods = self.registry.query(**mod)
            if len(mods) != 1:
                raise DependencyError("The lockfile doesn't specify the modules correctly, please regenerate it.")
            out.append(mods[0])
        return out

    def _write_lockfile(self):
        outdata = []
        for dependency in self.package_modules:
            module = dependency.module
            outdata.append(
                {
                    "namespace": module.namespace,
                    "module": module.name,
                    "version": module.version,
                }
            )
        log.debug("Writing module dependencies to %s", self.lockfile)
        self.lockfile.write_text(json.dumps(outdata, indent=4), encoding="utf-8")

    def _fetch_dependencies(self, *modules: str, root: Optional[Dependency] = None):
        """Given a list of modules, recursively fetch dependencies from a registry"""
        # Container of the needed modules
        for mod in modules:
            log.debug("Fetching dependency for %s (from %s)", mod, root)
            try:
                base, version = mod.split(":")
                namespace, module = base.split(".")
            except ValueError as exc:
                raise DependencyError(f"dependency '{mod}' is not in the format 'namespace.module:version'") from exc
            all_matching = self.registry.query(namespace=namespace, module=module, version=version)
            if not all_matching:
                msg = f"could not find the module {mod}"
                if root is not None:
                    msg += f" (required by {root.module})"
                raise DependencyError(msg)
            # Now we get the highest matching version, then see if it's alread in our package.
            to_add = all_matching[0]
            for to_check in all_matching[1:]:
                if to_check.is_newer(to_add):
                    to_add = to_check
            obj = Dependency(to_add, root)
            # We already added this module, so:
            # 1 - do not add it again
            # 2 - go to the next dependency
            # This will work because we consider two dependencies to be
            # equal if their module is equal.
            if obj in self.package_modules:
                continue
            # If we already are requiring the same module, but
            if root is not None:
                root.branches.append(obj)
            self.package_modules.append(obj)
            # Call myself recursively for the dependencies of this module
            # The maximum theoretical recursion depth is the total number of modules we have.
            # when we'll have 1000 modules and this will hit the python recursion limit, we'll rewrite sextant in
            # a language that optimizes tail recursion.
            self._fetch_dependencies(*to_add.dependencies, root=obj)

    def _check_dependencies(self):
        """Check dependencies."""
        # This is a brute-force process.
        # Again, this is ok until we have too many dependencies.
        for i, dep in enumerate(self.package_modules):
            reminder = i + 1
            for other in self.package_modules[reminder:]:
                if not dep.is_compatible(other):
                    raise DependencyError(f"Module {dep} is incompatible with module {other}")
