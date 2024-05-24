#! /usr/bin/python
import os
import argparse

# Run BCDEF first in case using global fit 'dofsrcombo' option
# IOV_list= ['BCDEF','B','C','D','E','F']
# IOV_list= ['2018ABCD','2018A','2018B','2018C','2018D']
# IOV_list= ['2017P8','2017B','2017C','2017D','2017E','2017F','2016P8APV']
# IOV_list= ['2016GH','2016BCDEF','2016BCD','2016EF']
# IOV_list= ['2016BCDEF','2016GH','2016BCD','2016EF']
# IOV_list= ['2018P8','2018A','2018B','2018C','2018D1','2018D2']
# IOV_list= ['2018D1','2018D2']
# IOV_list= ['2016P8','2016BCD','2016EF','2016FGH']
# IOV_list= ['2016P8','2016QCD','2016FGH']
# IOV_list= ['2016P8','2016BCD','2016EF','2016FGH',
#           '2017P8','2017B','2017C','2017D','2017E','2017F']
# IOV_list= ['2016BCD','2016EF','2016FGH',
#           '2017B','2017C','2017D','2017E','2017F']
# IOV_list= ['2017C']
# IOV_list= ['2016P8','2017P8']
# IOV_list= ['2016P8APV']

##################
# Run 2 IOV list #
##################
# IOV_list= ['2016P8','2016QCD','2016BCD','2016EF',
#           '2016APVP8','2016APVQCD','2016FGH',
#           '2017P8','2017QCD','2017B','2017C','2017D','2017E','2017F',
#           '2018P8','2018QCD','2018A1','2018A2','2018B','2018C',
#           '2018D1','2018D2','2018D3','2018D4']
# IOV_list= ['2018A1','2018A2','2018D3','2018D4']
# version = 'v19'

##################
# Run 3 IOV list #
##################
# IOV_list= ['2022C','2022D',
IOV_list = [
    "2022P8",
    "2022QCD",
    "2022C",
    "2022D",
    "2022EEP8",
    "2022EEQCD",
    "2022E",
    "2022F",
    "2022G",
    "2023B",
    "2023Cv123",
    "2023Cv4",
    "2023D",
]  # 2024B-PromptReco-v1
version = "w11"


IOV_list = [
    "2023Cv123",
    "2023Cv4",
    "2023D",
    "2023P8-BPix",
    "2023P8",
    "Summer23MG_1",
    "Summer23MG_2",
    "Summer23MG_3",
    "Summer23MG_4",
    "Summer23MG_5",
    "Summer23MG_6",
    "Summer23MGBPix_1",
    "Summer23MGBPix_2",
    "Summer23MGBPix_3",
    "Summer23MGBPix_4",
]

res_iovs = {
    # dataset: [memory, hours, days]
    "2023Cv123": [10, 0, "3-"],
    "2023Cv4": [10, 0, "3-"],
    "2023D": [10, 0, "3-"],
    "2023P8-BPix": [10, 0, "3-"],
    "2023P8": [10, 0, "3-"],
    "Summer23MG_1": [10, 0, "3-"],
    "Summer23MG_2": [10, 0, "3-"],
    "Summer23MG_3": [10, 0, "3-"],
    "Summer23MG_4": [10, 0, "3-"],
    "Summer23MG_5": [10, 0, "3-"],
    "Summer23MG_6": [10, 0, "3-"],
    "Summer23MGBPix_1": [10, 0, "3-"],
    "Summer23MGBPix_2": [10, 0, "3-"],
    "Summer23MGBPix_3": [10, 0, "3-"],
    "Summer23MGBPix_4": [10, 0, "3-"],
}

parser = argparse.ArgumentParser(description="Run all IOVs")

# The user can pass the IOV list, version, max number of files as an argument
parser.add_argument("-i", "--IOV_list", nargs="+", default=[])
parser.add_argument("-v", "--version", default=version)
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
if not os.path.exists('rootfiles/'+version):
    os.makedirs('rootfiles/'+version)

if not os.path.exists("logs/" + version):
    os.makedirs("logs/" + version)

# os.system("rm *.so *.d *.pcm")
# os.system("root -l -b -q mk_CondFormats.C")
for iov in IOV_list:
    print("Process GamHistFill.C+g for IOV " + iov)
    # os.system("ls -ltrh rootfiles/GamHistosFill_mc_"+iov+".root")
    # os.system("ls -ltrh rootfiles/GamHistosFill_data_"+iov+".root")
    # os.system("ls -ltrh logs/log_"+iov+"_"+version+".txt")

    os.system("nohup time root -l -b -q 'mk_GamHistosFill.C(\""+iov+"\",\""+version+"\")' > logs/"+version+"/log_"+iov+"_"+version+".txt &")
    print(f" => Follow logging with 'tail -f logs/{version}/log_{iov}_{version}.txt'")

    # os.system(f'time root -l -b -q \'mk_GamHistosFill.C("{iov}","{version}")\'')
    # os.system("mkdir -p logs/" + version)
    # os.system(f"sbatch submit_slurm.sh {iov} {version}")

    # os.system(f"sbatch --job-name=gamjet_analysis -p {'long' if (res_iovs[iov][1] > 12 or res_iovs[iov][2]) else 'standard'} --time={res_iovs[iov][2]}0{res_iovs[iov][1]}:00:00 --ntasks=1 --cpus-per-task=1 --mem={res_iovs[iov][0]}gb --output=logs/{version}/gamjet_analysis_{iov}_{version}_%j.log submit_slurm.sh {iov} {version}")


#    os.system("fs flush")
#    wait()
#    time.sleep(sleep_time)
