import os
import sys
import yaml
import boto3
import shutil
import zipfile
from pathlib import Path

#
# Copyright (c) 2021 Pharmacelera S.L.
# All rights reserved.
#
# Description: Support functions for experiment post-processing
#


class Colors:
    BOLD = "\033[1m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    UNDERLINE = "\033[4m"


class Utils:
    # statics - - - - -
    out: str = "outputs"
    inputs: str = "inputs"
    result: str = "results.txt"
    log_file: str = "experiment.log"
    coef_file: str = "experiment.coef"

    def get_arg(self):
        """
        Parse binary name from the shell.
        """
        args = sys.argv
        if len(args) < 2:
            print("Please enter the binary name to upload: (pharmscreen or pharmqsar)")
            sys.exit()
        binary = args[1]
        if binary != "pharmscreen" and binary != "pharmqsar":
            print("Incorrect name, please use: (pharmscreen or pharmqsar)")
            sys.exit()
        return binary

    def get_name(self, command):
        """Extract experiment name from command line"""
        if command:
            command = command.split(" ")
            index = command.index("--name") + 1
            return command[index]
        return None

    def best_model_selector(self, folder_path, statics, config=None):
        """Unzip all output files and list all log files,
        then parse line by line to extract the best component among all experiments
        """
        all_components = []
        self.best = statics["MODEL_NAME"]
        self.upload = statics["UPLOAD_S3"]
        if self.upload == True:
            self.s3_bucket = statics["S3_BUCKET"]
            self.s3_folder = statics["S3_FOLDER"]
        outputs = os.path.join(folder_path, self.out, self.best)
        results = os.path.join(folder_path, self.best)
        Path(results).mkdir(parents=True, exist_ok=True)
        result_file = open(os.path.join(results, self.result), "w")
        result_file.write(self.copyright())
        self.unzip_results(outputs)
        for root, _, files in os.walk(outputs):
            path = root.split(os.sep)
            vs_files = []
            for f in files:
                if f.endswith((".pdb", ".va0", ".coef")):
                    vs_files = files
            for file in vs_files:
                if file == self.log_file:
                    result_file.write(os.path.basename(root) + "\n")
                    filename = os.path.join("/".join(path), file)
                    best_q2 = 0.0
                    best_r2 = 0.0
                    num = 0
                    with open(filename, "r+") as f:
                        for line in f:
                            if line.startswith("test r2="):
                                r2 = float(line.split(" ")[2])
                                test_r2 = r2 if r2 > 0 else best_r2
                            if line.startswith("q2="):
                                q2 = float(line.split(" ")[1])
                                if q2 > best_q2 and (q2 - best_q2) > 0.01:
                                    best_q2 = q2
                                    num = next(f).split(" ")[-1].strip()
                                    best_r2 = test_r2
                    all_components.append(
                        {
                            "q2": best_q2,
                            "r2": best_r2,
                            "sum": best_q2 + best_r2,
                            "n": num,
                            "folder": path[-1],
                        }
                    )
                    result_file.write(
                        f"Best q2: {best_q2}\
                        \nBest r2: {best_r2}\
                        \nNumber of components: {num}\n"
                    )
        sorted_by_q2 = sorted(all_components, key=lambda k: k["q2"], reverse=True)
        sorted_by_r2 = sorted(all_components, key=lambda k: k["r2"], reverse=True)
        index_sum = sys.maxsize
        selected = {}
        for q2_index, content in enumerate(sorted_by_q2):
            r2_index = next((i for (i, d) in enumerate(sorted_by_r2) if d["r2"] == content["r2"]), None)
            qr_sum = q2_index + r2_index
            if qr_sum < index_sum:
                index_sum = qr_sum
                selected = sorted_by_q2[q2_index]
            elif qr_sum == index_sum:
                q2_index = q2_index - 1 if selected["sum"] > sorted_by_q2[q2_index]["sum"] else q2_index
                selected = sorted_by_q2[q2_index]
        result_file.write(self.headline())
        result_file.write(self.get_row(selected))
        result_file.close()
        if self.upload == True and selected:
            folder = selected["folder"]
            self.create_next_yaml(selected, config, statics)
            self.prepare_files_and_upload(folder_path, folder)
        self.remove_uncompressed()

    def create_next_yaml(self, selected, config, statics):
        """Manual customization of new yaml config for next experiments."""
        name = selected["folder"]
        chosen_exp = [e for e in config.values() if e["name"] == name].pop()
        best_model = {**chosen_exp, **statics}
        chosen_exp.pop("tmols", None)
        chosen_exp.pop("sdthr", None)
        chosen_exp.pop("ncomp", None)
        chosen_exp.pop("field1", None)
        chosen_exp.pop("field2", None)
        chosen_exp.pop("field3", None)
        chosen_exp.pop("field4", None)
        chosen_exp.pop("norm", None)
        chosen_exp.pop("invdistproj", None)
        chosen_exp["mode"] = "predict"
        if best_model.get("charges", None):
            chosen_exp["charges"] = best_model.get("charges")
        chosen_exp["logp"] = best_model.get("logp", "userdefined")
        chosen_exp["repcomp"] = selected["n"]
        chosen_exp["files"]["repcoef"] = "inputs/experiment.coef"
        chosen_exp["files"]["repgrid"] = "inputs/grid_out.pdb"
        if "actv" in chosen_exp["files"]:
            del chosen_exp["files"]["actv"]
        exp_num = 1
        exp1 = {}
        prep_exp = [e for e in config.values() if e["name"] == chosen_exp["files"]["input"][4:-4]]
        if prep_exp:
            prep_exp = prep_exp.pop()
            if "ref" in prep_exp["files"]:
                prep_exp["files"]["ref"] = prep_exp["files"]["ref"].replace("tmp/", "inputs/tmp/")
            exp1 = {"experiment" + str(exp_num): prep_exp}
            exp_num += 1
        exp2 = {"experiment" + str(exp_num): chosen_exp}
        with open("custom.yaml", "w") as file:
            self.new_yaml_data = {**exp1, **exp2}
            yaml.dump(
                self.new_yaml_data,
                file,
            )

    def unzip_results(self, outputs):
        folder, _, filenames = next(os.walk(outputs))
        for f in filenames:
            if f.endswith(".zip"):
                with zipfile.ZipFile(os.path.join(folder, f)) as zipped:
                    path = os.path.join(outputs, f.split(".")[0])
                    Path(path).mkdir(parents=True, exist_ok=True)
                    zipped.extractall(path)

    def prepare_files_and_upload(self, path, folder):
        for root, _, files in os.walk(os.path.join(path, self.out, self.best, folder)):
            for file in files:
                if file.endswith((".coef", ".pdb", ".log")):
                    dest = file
                    if file.endswith(".coef"):
                        dest = self.coef_file
                    shutil.copyfile(os.path.join(root, file), os.path.join(path, self.best, dest))
        shutil.move(os.path.join(path, "custom.yaml"), os.path.join(path, self.best, "custom.yaml"))
        try:
            shutil.move(os.path.join(path, "tmp"), os.path.join(path, self.best, "tmp"))
        except Exception:
            pass
        shutil.make_archive(self.best, "zip", os.path.join(path, self.best))
        shutil.rmtree(os.path.join(path, self.best), ignore_errors=True)
        self.upload_s3(path, self.best)

    def upload_s3(self, path, file):
        if self.upload:
            file = file + ".zip"
            s3 = boto3.resource("s3")
            s3.Bucket(self.s3_bucket).upload_file(file, self.s3_folder + "/" + file)
            print("Uploaded to S3")

    def get_row(self, selected):
        return f"Experiment folder: {selected.get('folder'), None}\
                \nBest q2: {selected.get('q2'), None}\
                \nBest test r2: {selected.get('r2', None)}\
                \nNumber of components: {selected.get('n')} \n\n"

    def remove_uncompressed(self):
        outputs = os.path.join(self.out, self.best)
        for path in Path(outputs).glob("**/*"):
            if path.is_dir():
                shutil.rmtree(path)

    @staticmethod
    def headline():
        return "\n" + "-" * 30 + "Selected Configuration" + "-" * 30 + "\n"

    @staticmethod
    def copyright():
        return (
            "PHARMQSAR MODEL SELECTION\
            \nPHARMACELERA S.L.\
            \n"
            + "-" * 80
            + "\n"
        )
