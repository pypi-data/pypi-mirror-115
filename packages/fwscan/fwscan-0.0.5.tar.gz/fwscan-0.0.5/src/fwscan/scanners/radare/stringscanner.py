import logging

from fwscan.utils.console import console
from fwscan.scanners.radare.r2stringscanner import RadareStringScanner

log = logging.getLogger(__name__)


class RadareELFScanner(object):
    def scan(args, ifolder, ofolder):
        """
        Scan for ELF binaries using radare2 and extract following artifacts:
            1. Strings

        Parameters
        ----------
        ifolder : string
            Target (input) folder to scan
        ofolder : string
            Output folder to store the results & plots
        """
        console.print(
            f"[bold green] :mag: Scanning folder: [bold magenta]{ifolder}[/bold magenta]"
        )
        print("Input Folder: " + ifolder)
        print("Output Folder: " + ofolder)
        rss = RadareStringScanner(ifolder, ofolder)
        rss.fire_command()