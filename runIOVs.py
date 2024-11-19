#! /usr/bin/python
import os
import argparse
import time

IOV_list = (
    [
        "2023Cv123",
        "2023Cv4",
        "2023D",
    ]
    + [
        file.replace(".txt", "").replace("mcFiles_", "")
        for file in os.listdir("input_files/")
        if "Summer23MG_" in file and "all" not in file
    ]
    + [
        file.replace(".txt", "").replace("mcFiles_", "")
        for file in os.listdir("input_files/")
        if "Summer23MGBPix_" in file and "all" not in file
    ]
    + [
        file.replace(".txt", "").replace("mcFiles_", "")
        for file in os.listdir("input_files/")
        if "2023P8" in file and "BPix" not in file and "all" not in file
    ]
    + [
        file.replace(".txt", "").replace("mcFiles_", "")
        for file in os.listdir("input_files/")
        if "2023P8-BPix" in file and "all" not in file
    ]
        + [
        "2022C",
        "2022D",
        "2022E",
        "2022F",
        "2022G",
    ]
    + [
        file.replace(".txt", "").replace("mcFiles_", "")
        for file in os.listdir("input_files/")
        if "Summer22MG_" in file and "all" not in file
    ]
    + [
        file.replace(".txt", "").replace("mcFiles_", "")
        for file in os.listdir("input_files/")
        if "Summer22EEMG_" in file and "all" not in file
    ]
    + [
        file.replace(".txt", "").replace("mcFiles_", "")
        for file in os.listdir("input_files/")
        if "2022P8" in file and "all" not in file
    ]
    + [
        file.replace(".txt", "").replace("mcFiles_", "")
        for file in os.listdir("input_files/")
        if "2022EEP8" in file and "all" not in file
    ]

)

# IOV_list = ["Summer22EEMG_4","Summer22EEMG_5", "Summer22EEMG_6"]

# resources for slurm
res_iovs = {
    # dataset: [memory, hours, days]
    "2023Cv123": [3, 2, ""],  # [10, 0, "3-"],
    "2023Cv4": [5, 12, ""],  # [10, 0, "3-"],
    "2023D": [5, 12, ""],  # [10, 0, "3-"],
    "2022C": [5, 12, ""],
    "2022D": [5, 12, ""],
    "2022E": [5, 12, ""],
    "2022F": [5, 12, ""],
    "2022G": [5, 12, ""],
    "2022C_ZB": [5, 12, ""],
    "2022D_ZB": [5, 12, ""],
    "2022E_ZB": [5, 12, ""],
    "2022F_ZB": [5, 12, ""],
    "2022G_ZB": [5, 12, ""],
}
res_iovs.update(
    {
        file.replace(".txt", "").replace("mcFiles_", ""): (
            [6, 6, ""] #if "BPix" not in file else [3, 2, ""]
        )
        for file in os.listdir("input_files/")
        if ("mcFiles_" in file) and "all" not in file
    }
)

run3_23 = [x for x in IOV_list if "23" in x]
run3_22 = [x for x in IOV_list if "22" in x]

parser = argparse.ArgumentParser(description="Run all IOVs")

parser.add_argument("-i", "--IOV_list", required=True)
parser.add_argument("-v", "--version", required=True)
parser.add_argument("-l", "--local", default=False, action="store_true", help="Run locally in the background")
parser.add_argument("-d", "--debug", default=False, action="store_true", help="Run locally printing the log")
parser.add_argument("--max_files", default=9999)
parser.add_argument("-p", "--pnetreg", default=False, action="store_true")
parser.add_argument("-n", "--neutrino", default=False, action="store_true")
parser.add_argument("-c", "--closure", default=False, action="store_true")
parser.add_argument("-f", "--fast", default=False, action="store_true")
args = parser.parse_args()

if "23" in args.IOV_list:
    IOV_list = run3_23
elif "22" in args.IOV_list:
    IOV_list = run3_22
elif args.IOV_list and "all" not in args.IOV_list:
    IOV_list = args.IOV_list
print("IOVs to run: ", IOV_list)


if (args.version) and ("test" not in args.IOV_list):
    version = args.version

if args.max_files and ("test" not in args.IOV_list):
    max_files = args.max_files

# Check that the version directory exists, if not create it
if not os.path.exists("rootfiles/" + version):
    os.makedirs("rootfiles/" + version)

if not os.path.exists("logs/" + version):
    os.makedirs("logs/" + version)

pnetreg = args.pnetreg
if "pnetreg" in version:
    pnetreg = True

neutrino = args.neutrino
if "neutrino" in version:
    neutrino = True

closure = args.closure
if "closure" in version:
    closure = True


if not args.fast:
    # choose if pnetreg or pnetregneutrino
    with open("GamHistosFill.C", "r") as file:
        filedata = file.read()

    if pnetreg and not neutrino:
        print("Setting up PNetReg without neutrino")
        if "// #define PNETREG\n" in filedata:
            print("uncommenting PNETREG")
            filedata = filedata.replace("// #define PNETREG\n", "#define PNETREG\n")
        if not "// #define PNETREGNEUTRINO\n" in filedata:
            print("commenting PNETREGNEUTRINO")
            filedata = filedata.replace(
                "#define PNETREGNEUTRINO\n", "// #define PNETREGNEUTRINO\n"
            )
    elif pnetreg and neutrino:
        print("Setting up PNetReg with neutrino")
        if "// #define PNETREGNEUTRINO\n" in filedata:
            print("uncommenting PNETREGNEUTRINO")
            filedata = filedata.replace(
                "// #define PNETREGNEUTRINO\n", "#define PNETREGNEUTRINO\n"
            )
        if not "// #define PNETREG\n" in filedata:
            print("commenting PNETREG")
            filedata = filedata.replace("#define PNETREG\n", "// #define PNETREG\n")
    else:
        print("Using standard jet pT")
        if not "// #define PNETREG\n" in filedata:
            print("commenting PNETREG")
            filedata = filedata.replace("#define PNETREG\n", "// #define PNETREG\n")
        if not "// #define PNETREGNEUTRINO\n" in filedata:
            print("commenting PNETREGNEUTRINO")
            filedata = filedata.replace(
                "#define PNETREGNEUTRINO\n", "// #define PNETREGNEUTRINO\n"
            )

    # find line that starts with bool CLOSURE_L2L3RES
    for line in filedata.split("\n"):
        if line.startswith("bool CLOSURE_L2L3RES"):
            if closure:
                print("Setting CLOSURE_L2L3RES to true")
                line_new = f"bool CLOSURE_L2L3RES = true;"
            else:
                print("Setting CLOSURE_L2L3RES to false")
                line_new = f"bool CLOSURE_L2L3RES = false;"
            break
    # modify line
    filedata = filedata.replace(line, line_new)

    # print(filedata[:700])

    with open("GamHistosFill.C", "w") as file:
        file.write(filedata)

    time.sleep(10)

    # uncomment GPU
    with open("mk_GamHistosFill.C", "r") as file:
        filedata = file.read()

    if "// #define GPU" in filedata:
        print("uncommenting GPU")
        filedata = filedata.replace("// #define GPU", "#define GPU")

    with open("mk_GamHistosFill.C", "w") as file:
        file.write(filedata)

    time.sleep(10)

    # clean and make
    os.system("make clean")
    os.system("make")

    # comment GPU
    with open("mk_GamHistosFill.C", "r") as file:
        filedata = file.read()

    filedata = filedata.replace("#define GPU", "// #define GPU")
    print("commenting GPU")

    with open("mk_GamHistosFill.C", "w") as file:
        file.write(filedata)
    time.sleep(10)


for iov in IOV_list:
    print("Process GamHistFill.C+g for IOV " + iov)

    if args.local:
        os.system(
            "nohup time root -l -b -q 'mk_GamHistosFill.C(\""
            + iov
            + '","'
            + version
            + "\")' > logs/"
            + version
            + "/log_"
            + iov
            + "_"
            + version
            + ".log &"
        )
    elif args.debug:
        os.system(
            "time root -l -b -q 'mk_GamHistosFill.C(\""
            + iov
            + '","'
            + version
            + "\")' "
        )
    else:
        os.system(
            f"sbatch --job-name=gamjet_{iov}_{version} -p {'long' if (res_iovs[iov][1] > 12 or res_iovs[iov][2]) else 'standard'} --time={res_iovs[iov][2]}0{res_iovs[iov][1]}:00:00 --ntasks=1 --cpus-per-task=1 --mem={res_iovs[iov][0]}gb --output=logs/{version}/log_{iov}_{version}.log submit_slurm.sh {iov} {version}"
        )

    print(f" => Follow logging with 'tail -f logs/{version}/log_{iov}_{version}.log'")
