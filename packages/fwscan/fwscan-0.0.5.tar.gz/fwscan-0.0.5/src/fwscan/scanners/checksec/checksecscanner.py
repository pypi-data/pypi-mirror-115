import logging

from fwscan.utils.console import console
from fwscan.scanners.checksec.checksechelper import CheckSecHelper

log = logging.getLogger(__name__)


class ChecksecScanner(object):
    """Scanner for extracting, processing and visualizing
    protections in binaries

    Dependencies:
        pip install checksec

    Examples usages:
    Scan folder /usr/bin and store results in folder output:
        fwscan checksec scan /usr/bin output

    Scan with plots:
        fwscan checksec scan /usr/bin output --plot

    For more help:
        fwscan checksec --help
        fwscan checksec scan --help
    """

    def __init__(self, verbose=False, plot=False):
        """
        Parameters
        ----------
        verbose : boolean, optional
            Enable verbose logging

        plot : boolean, optional
            Enable generation of plots
        """
        self.verbose = verbose
        self.plot = plot
        if verbose:
            log.setLevel(logging.DEBUG)

    def scan(self, ifolder, ofolder):
        """
        Scan for ELF binaries in the folder, extracts protection features
        and stores result in output file. Optionally generates plots for
        each protection features.

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
        css = CheckSecHelper(ifolder, ofolder, fformat="csv", plot=self.plot)
        css.fire_command()