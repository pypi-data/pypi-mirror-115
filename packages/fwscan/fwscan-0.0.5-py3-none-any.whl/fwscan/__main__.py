"""Command-line interface."""
import fire
import logging
from fwscan.scanners.radare.r2stringscanner import RadareStringScanner
from fwscan.scanners.radare.stringscanner import RadareELFScanner

from fwscan.utils.console import console

from fwscan.scanners.checksec.checksecscanner import ChecksecScanner


# Logging setup
logging.basicConfig(
    level=logging.INFO,
    filename="/tmp/fwscan.log",
    format="%(asctime)s %(levelname)s:%(message)s",
)


def main() -> None:
    """fwscan."""
    checksec_scanner = ChecksecScanner()
    radare_elf_scanner = RadareELFScanner()

    # Register commands
    fire.Fire({"r2": RadareELFScanner, "checksec": ChecksecScanner})


if __name__ == "__main__":
    main(prog_name="fwscan")  # pragma: no cover
