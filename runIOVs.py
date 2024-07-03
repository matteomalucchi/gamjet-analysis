#! /usr/bin/python
import os
import argparse

version = "w11"

IOV_list = [
    # "2023Cv123",
    # "2023Cv4",
    # "2023D",
    # "2023P8-BPix",
    # "2023P8",
    # "Summer23MG_1",
    "Summer23MG_2",
    # "Summer23MG_3",
    # "Summer23MG_4",
    # "Summer23MG_5",
    "Summer23MG_6",
    # "Summer23MGBPix_1",
    # "Summer23MGBPix_2",
    # "Summer23MGBPix_3",
    # "Summer23MGBPix_4",
]

res_iovs = {
    # dataset: [memory, hours, days]
    "2023Cv123": [5, 12, ""],#[10, 0, "3-"],
    "2023Cv4": [5, 12, ""],#[10, 0, "3-"],
    "2023D": [5, 12, ""],#[10, 0, "3-"],
    "2023P8-BPix": [10, 0, "3-"],
    "2023P8": [10, 0, "3-"],
    "Summer23MG_1": [10, 0, "3-"],
    "Summer23MG_2": [10, 0, "3-"],
    "Summer23MG_3": [5, 12, ""],#[10, 0, "3-"],
    "Summer23MG_4": [5, 12, ""],#[10, 0, "3-"],
    "Summer23MG_5": [5, 12, ""],#[10, 0, "3-"],
    "Summer23MG_6": [5, 12, ""],#[10, 0, "3-"],
    "Summer23MGBPix_1": [10, 0, "3-"],
    "Summer23MGBPix_2": [10, 0, "3-"],
    "Summer23MGBPix_3": [5, 12, ""],#[10, 0, "3-"],
    "Summer23MGBPix_4": [5, 12, ""],#[10, 0, "3-"],
}

parser = argparse.ArgumentParser(description="Run all IOVs")

# The user can pass the IOV list, version, max number of files as an argument
parser.add_argument("-i", "--IOV_list", nargs="+", default=[])
parser.add_argument("-v", "--version", default=version)
parser.add_argument("-l", "--local", default=False, action="store_true")
parser.add_argument("--max_files", default=9999)
args = parser.parse_args()

if args.IOV_list and "all" not in args.IOV_list:
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

# os.system("rm *.so *.d *.pcm")
# os.system("root -l -b -q mk_CondFormats.C")
for iov in IOV_list:
    print("Process GamHistFill.C+g for IOV " + iov)
    # os.system("ls -ltrh rootfiles/GamHistosFill_mc_"+iov+".root")
    # os.system("ls -ltrh rootfiles/GamHistosFill_data_"+iov+".root")
    # os.system("ls -ltrh logs/log_"+iov+"_"+version+".log")

    # os.system(f'time root -l -b -q \'mk_GamHistosFill.C("{iov}","{version}")\'')
    # os.system("mkdir -p logs/" + version)
    # os.system(f"sbatch submit_slurm.sh {iov} {version}")

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
    else:
        os.system(
            f"sbatch --job-name=gamjet_{iov}_{version} -p {'long' if (res_iovs[iov][1] > 12 or res_iovs[iov][2]) else 'standard'} --time={res_iovs[iov][2]}0{res_iovs[iov][1]}:00:00 --ntasks=1 --cpus-per-task=1 --mem={res_iovs[iov][0]}gb --output=logs/{version}/log_{iov}_{version}.log submit_slurm.sh {iov} {version}"
        )

    print(f" => Follow logging with 'tail -f logs/{version}/log_{iov}_{version}.log'")


#    os.system("fs flush")
#    wait()
#    time.sleep(sleep_time)
