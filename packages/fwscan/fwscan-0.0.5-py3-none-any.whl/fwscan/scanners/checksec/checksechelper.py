from scanfs.fsscanner import FileSystemScanner
import os
import subprocess
import seaborn as sns
import subprocess
import errno
import shutil
import matplotlib.pyplot as plt
import pandas as pd
from pycaret.anomaly import *


from fwscan.utils.console import console
from scanfs.fsscanner import FileSystemScanner


class CheckSecHelper(FileSystemScanner):
    def __init__(
        self,
        ifolder,
        ofolder: str,
        result_file="output.csv",
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
            self.checksec_on_elfs()
            if self.plot:
                self.generate_plots()

    def checksec_dump(self, fpath, node):
        """
        Perform checksec and dump results in a file

        Args:
            result_fpath (str): Store results in this file path
            callback (function): Function called when the elf file type
            is found
        """
        try:
            path = os.path.join(fpath, node.name)
            completed_process = subprocess.run(
                ["checksec", "--format=" + str(self.fformat), "--file=" + str(path)],
                capture_output=True,
                check=True,
            )
            self.fd.write(completed_process.stdout.decode("utf-8"))
            self.fd.write("\n")
        except Exception as e:
            console.print("[red bold]An exception occurred: " + str(e))

    def checksec_on_elfs(self):
        """
        Checks the security features enabled on elf

        Args:
            filename (str): Filename to store the results of checksec in JSON
            fformat
        """
        self.fd = open(self.result_file, "w")
        self.fd.write(
            "RELRO,CANARY,NX,PIE,RPATH,RUNPATH,Symbols,FORTIFY,Fortified,Fortifiable,FILE"
        )
        self.fd.write("\n")
        with console.status(f"Scanning files ...", spinner="arrow3"):
            self.scan_for_elfs(self.checksec_dump)
        self.fd.close()

    def find_anomaly(self, df):
        # intialize the setup
        checksec_ano = setup(df, session_id=5555, normalize=True, verbose=False)
        # create a model
        knn = create_model("knn")
        knn_df = assign_model(knn)

        # plot a model
        plot_model(knn, feature="FILE")
        plot_model(knn, plot="umap", feature="FILE")

        # create a model
        iforest = create_model("iforest")
        iforest_df = assign_model(iforest)

        # plot a model
        plot_model(iforest, feature="FILE")
        plot_model(iforest, plot="umap", feature="FILE")

    def generate_plots(self):
        plots_path = self.ofolder + "/plots"
        os.makedirs(plots_path, exist_ok=True)

        df = pd.read_csv(self.result_file)
        console.print("[bold red]Samples from the data frame")
        console.print(df.head(5))

        console.print("[bold green]Generating interesting plots for you!!!")
        with console.status(f"[magenta]Generating plots ...", spinner="arrow3"):
            for key in df.keys():
                console.print(key)
                figure = df[key].value_counts().plot(kind="bar").get_figure()
                figure.savefig(
                    plots_path + "/" + key + ".svg",
                    format="svg",
                    dpi=600,
                    pad_inches=0.5,
                )
                figure.clear()
                figure = sns.countplot(x=key, data=df).get_figure()
                figure.savefig(
                    plots_path + "/sns_" + key + ".svg",
                    format="svg",
                    dpi=600,
                    pad_inches=0.5,
                )
                figure.clear()

        with console.status(f"[magenta]Generating scatter plots ...", spinner="arrow3"):
            for key in df.keys():
                figure.clear()
                figure = sns.scatterplot(data=df, x=key, y=df.keys()[-1]).get_figure()
                figure.savefig(
                    plots_path + "/scat_" + key + ".svg",
                    format="svg",
                    dpi=600,
                    pad_inches=0.5,
                )

        figure.clear()
        figure = sns.pairplot(df)
        figure.savefig(
            plots_path + "/pairplot.svg",
            format="svg",
            dpi=600,
            pad_inches=0.5,
        )

        with console.status(f"[magenta]Finding anomaly ...", spinner="arrow3"):
            self.find_anomaly(df)

        console.print("[green bold]All plots generated in folder: " + plots_path)

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
