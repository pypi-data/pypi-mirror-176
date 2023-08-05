"""Command-line utility."""
import argparse
import logging
import pathlib
import shutil
import sys

from typing import Generator, List, Optional

from sextant import log, module, dependency


DEPFILE = "package.json"


class ChartsCollection:
    """Manages a charts collection"""

    def __init__(self, modules_dir: str, charts_dir: str):
        self.registry = module.registry_from_path(modules_dir)
        self.path = pathlib.Path(charts_dir)

    def chart(self, chart_name: str) -> "Chart":
        """Fetches a specific chart"""
        pkgfile = self.path / chart_name / DEPFILE
        if not pkgfile.exists():
            raise KeyError(f"Could not find packagefile '{pkgfile}' chart '{chart_name}'")
        return Chart(self.registry, pkgfile)

    def charts(self) -> Generator["Chart", None, None]:
        """Returns all charts in the collection.

        This means all directories that are at the first level
        of the fs tree and contain a package.json file
        """
        for chartpath in self.path.rglob(DEPFILE):
            yield Chart(self.registry, chartpath)

    def query(self, query: str) -> List["Chart"]:
        """Query the chart collection for charts including a specific module."""
        self._check_query_format(query)
        results = []
        for chart in self.charts():
            try:
                if chart.depends_on(query):
                    results.append(chart)
            except dependency.DependencyError as exc:
                log.error("Chart %s has dependency problems: %s", chart, exc)
        return results

    def _check_query_format(self, query: str):
        # Check parameters
        try:
            base, _ = query.split(":")
            _, _ = base.split(".")
        except ValueError as exc:
            raise RuntimeError("The query needs to be in the format: namespace.module:version") from exc


class Chart:
    """Manages chart vendorization."""

    BUNDLE_DIR = "templates/vendor"

    def __init__(self, registry: module.Registry, packagefile: pathlib.Path):
        self.registry = registry
        self.chart_dir = packagefile.parent
        self.vendor_dir = self.chart_dir / self.BUNDLE_DIR
        self.package = dependency.Package(self.registry, str(packagefile))

    def create_lock(self, force: bool):
        """Create a lockfile to freeze the dependencies."""
        self.package.lock(force)

    def vendor(self, force: bool):
        """Creates a bundle of all modules required by the chart, and saves it
        to a vendor directory."""
        self.vendor_dir.mkdir(exist_ok=True)
        for mod in self.package.get(force):
            target = self.vendor_dir / mod.path.parent.name / mod.path.name
            target.parent.mkdir(exist_ok=True)
            if not force and self._is_fresh(target):
                log.debug("Not updating module %s as the its file is newer than the lockfile.", mod)
                continue
            log.info("Copying %s => %s", mod.path, target)
            shutil.copy(str(mod.path), str(target))

    def _is_fresh(self, target: pathlib.Path) -> bool:
        return target.exists() and self.package.lockfile.stat().st_mtime <= target.stat().st_mtime

    def __str__(self) -> str:
        """String representation"""
        return self.chart_dir.name

    def depends_on(self, query: str) -> bool:
        """Checks if the chart depends on a module, directly or indirectly."""
        for mod in self.package.get():
            if f"{mod.namespace}.{mod.name}:{mod.version}" == query:
                return True
        return False


def argparser():
    """Get the argument parser for the command line"""
    parser = argparse.ArgumentParser(prog="sextant", description="Tool to manage template libraries for helm charts")
    parser.add_argument("--modulepath", default="./modules", help="the directory where the modules are located.")
    parser.add_argument("--debug", action="store_true", help="output debug logging.")
    action = parser.add_subparsers(dest="action", required=True)
    # Command 1: bundle charts
    bundle = action.add_parser("vendor", help="allows to package your dependencies in a vendored file")
    bundle.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Re-create the lockfile and the bundle even if not necessary.",
    )
    bundle.add_argument(
        "chartdir",
        metavar="CHART_DIRECTORY",
        help="the directory where the chart's package.json file is located.",
    )
    # Command 2: search modules in charts
    search = action.add_parser(
        "search",
        help="search all charts in a directory for dependencies on a specific module",
    )
    search.add_argument("chartdir", metavar="CHARTS_DIRECTORY", help="the directory tree to search into")
    search.add_argument(
        "query", metavar="NAMESPACE.MODULE:VERSION", help="the module to search. Only exact matches for now."
    )
    # Command 3: update a specific module to the latest version in the specified chart tree
    update = action.add_parser("update", help="update a module version across a directory of charts.")
    update.add_argument("chartdir", metavar="CHARTS_DIRECTORY", help="the directory tree to update into")
    update.add_argument("module", metavar="MODULE")
    return parser


def main(args: Optional[List[str]] = None):
    """The main entrypoint."""

    if args is None:
        args = sys.argv[1:]
    params = argparser().parse_args(args)
    if params.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    what = params.action
    if what == "vendor":
        chart_path = pathlib.Path(params.chartdir)
        chartsdir = str(chart_path.parent)
    elif what is not None:
        chartsdir = params.chartdir

    charts = ChartsCollection(params.modulepath, chartsdir)

    try:
        if what == "vendor":
            charts.chart(chart_path.name).vendor(params.force)
        elif what == "search":
            results = charts.query(params.query)
            if not results:
                print(f"The query for {params.query} returned no results.")
            else:
                print(f"Charts depending on the module {params.query}:")
                print()
                for chart in results:
                    print(chart)
        elif what == "update":
            print("Sorry, not implemented yet!")
    except Exception as exc:  # pylint: disable=W0703
        log.exception(exc)
        sys.exit(1)
