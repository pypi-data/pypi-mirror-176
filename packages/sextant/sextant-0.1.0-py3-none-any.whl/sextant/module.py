"""
Classes to interact with chart modules.

SPDX-License-Identifier: GPL-3.0-or-later
"""

from dataclasses import dataclass
import pathlib
from typing import List, Optional

import json

from sextant import log


def registry_from_path(path_str: str) -> "Registry":
    """Given a Path, find all modules under it."""
    path = pathlib.Path(path_str)
    modules = []
    for modulepath in path.rglob("module.json"):
        modinfo = json.loads(modulepath.read_text())
        namespace = modulepath.parent.name
        for module in modulepath.parent.glob("*.tpl"):
            try:
                modname, fullversion = module.stem.split("_")
            except ValueError:
                log.warning("could not load file '%s': invalid name. Skipping")
                continue
            deps = []
            found = False
            for mod in modinfo["modules"]:
                if modname == mod["name"] and fullversion[:3] == mod["version"]:
                    try:
                        deps = mod["depends"]
                    except KeyError:
                        deps = []
                    found = True
                    break
            if not found:
                log.warning(
                    "could not find %s.%s:%s in the modules.json file",
                    namespace,
                    modname,
                    fullversion,
                )
                continue
            modules.append(Module(namespace, modname, fullversion, deps, module))
    return Registry(modules)


class Registry:
    """A registry of all modules."""

    def __init__(self, modules: List["Module"]):
        self._modules = modules

    @property
    def namespaces(self) -> List[str]:
        """Returns a list of namespaces found in this registry"""
        return list({mod.namespace for mod in self._modules})

    @property
    def modules(self) -> List[str]:
        """Returns a list of modules found in this registry, in the format namespace.module:version"""
        return [str(mod) for mod in self._modules]

    def query(
        self,
        namespace: Optional[str] = None,
        module: Optional[str] = None,
        version: Optional[str] = None,
    ) -> List["Module"]:
        """Get modules based on an optional set of filters."""
        # Early optimization is the root of all evil.
        # This code is inefficient but, short of having thousands of modules, it's good enough.
        query_results = []
        for mod in self._modules:
            if namespace is not None and mod.namespace != namespace:
                continue
            if module is not None and mod.name != module:
                continue
            if version is not None and not mod.version_matches(version):
                continue
            query_results.append(mod)
        return query_results


@dataclass(frozen=True)
class Module:
    """Represents a single module"""

    namespace: str
    name: str
    version: str
    dependencies: List[str]
    path: pathlib.Path

    def version_matches(self, ver: str) -> bool:
        """Find if this module matches  a version string"""
        return ver == self.version[: len(ver)]

    def matches(self, dep: str) -> bool:
        """Find if this module matches a dependency"""
        return str(self)[:-2] == dep

    def __str__(self) -> str:
        """String representation."""
        return f"{self.namespace}.{self.name}:{self.version}"

    def is_newer(self, other: "Module") -> bool:
        """Returns true if this module is newer than other, false otherwise."""
        major, minor, patch = self.version.split(".")
        o_major, o_minor, o_patch = other.version.split(".")
        if int(major) > int(o_major):
            return True
        if int(minor) > int(o_minor):
            return True
        if int(patch) > int(o_patch):
            return True
        return False
