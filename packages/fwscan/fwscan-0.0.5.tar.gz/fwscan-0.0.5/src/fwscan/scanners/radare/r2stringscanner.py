import os
import r2pipe
import shutil
import errno

from fwscan.utils.console import console
from scanfs.fsscanner import FileSystemScanner

class RadareStringScanner(FileSystemScanner):
    def __init__(
        self,
        ifolder,
        ofolder: str,
        result_file="strings.csv",
        fformat: str = "json",
        plot=False,
    ) -> None:
        super().__init__(ifolder)
        self.ifolder = ifolder
        self.ofolder = ofolder
        self.result_file = ofolder + "/" + result_file
        self.fformat = fformat
        self.plot = plot

    def fire_command(self):
        if self.setup_output_folder():
            self.strings_inside_elfs()

    def setup_output_folder(self):
        try:
            os.mkdir(self.ofolder)
            console.print("[green]Created output folder: " + self.ofolder)
        except OSError as e:
            if e.errno == errno.EEXIST:
                choice = console.input(
                    "[bold red]Output folder exists. Do you want to delete and recreate? (y/N): "
                )
                if choice == "Y" or choice == "y":
                    console.print(f"[red bold]Deleting existing folder: {self.ofolder}")
                    shutil.rmtree(self.ofolder, ignore_errors=True)
                    os.makedirs(self.ofolder, exist_ok=True)
                    console.print(f"[green]Created fresh output folder: {self.ofolder}")
                    return True
                else:
                    console.print("[green]Keeping folder safe")
                    return False
        return True

    def extract_string(self, path):
        strings_list = []
        r2 = r2pipe.open(path)
        stringsj = r2.cmdj("izj")
        
        for string in stringsj:
            strings = string['string']
            strings_list.append(strings)
        return strings_list

    def r2string_dump(self, fpath, node):
        """
        Perform string scan on ELF and dump results in a file

        Args:
            result_fpath (str): Store results in this file path
            callback (function): Function called when the elf file type
            is found
        """
        try:
            path = os.path.join(fpath, node.name)
            
            strings_list = self.extract_string(path)
            self.fd.write(str(strings_list))
            self.fd.write("\n")
        except Exception as e:
            console.print("[red bold]An exception occurred: " + str(e))


    def strings_inside_elfs(self):
        """
        Extracts strings from ELF files

        Args:
            filename (str): Filename to store the results of checksec in JSON
            fformat
        """
        self.fd = open(self.result_file, "w")
        # self.fd.write("strings,FILE")
        # self.fd.write("\n")
        with console.status(f"Scanning files ...", spinner="arrow3"):
            self.scan_for_elfs(self.r2string_dump)
        self.fd.close()