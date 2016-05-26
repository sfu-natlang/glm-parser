import os
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--src", help="directory of log files")
parser.add_argument("--res", help="directory of the result table")
parser.add_argument("--append", help="0 = build a new talbe; 1 = append to old table")
args = parser.parse_args()

if not (args.src and args.res and args.append):
    print "invalid argument, try -h"
    sys.exit(0)

fTable = open(os.path.join(args.res, "log_summary.md"), "w")
print args.append
if (args.append == "0"):
    fTable.write("|Data|Machine|Branch|Learner|Feature Generator|Parser|Iteration|Training Time|Feature Count|Unlabeled Accuracy|Unlabeled Attachment Accuracy|\n")
    fTable.write("|---|---|---|---|---|---|---|---|---|---|---|\n")

for root, dirs, files in os.walk(args.src):
    for name in files:
        if (name.split('.')[1] == "md"):
            continue
        fTable.write("|" + name.split('.')[0] + "|")
        fSrc = open(os.path.join(root, name), "r")
        flagCmd = False
        flagRes = False
        for line in fSrc:
            line = line.strip()
            if line.startswith("Machine"):
                fTable.write(line.split(" ")[1] + "|")
            if line.startswith("Branch"):
                fTable.write(line.split(" ")[1] + "|")

            if flagCmd:
                parameters = line.split(" ")
                for index, obj in enumerate(parameters):
                    if obj.startswith("--learner"):
                        fTable.write(obj.split("=")[1] + "|")
                        break
                for index, obj in enumerate(parameters):
                    if obj.startswith("--fgen"):
                        fTable.write(obj.split("=")[1] + "|")
                        break
                for index, obj in enumerate(parameters):
                    if obj.startswith("--parser"):
                        fTable.write(obj.split("=")[1] + "|")
                        break
                for index, obj in enumerate(parameters):
                    if obj == "-i":
                        fTable.write(parameters[index + 1] + "|")
                        break
                flagCmd = False
                flagRes = True

            if line.startswith("Command"):
                flagCmd = True

            if "Training time" in line and flagRes:
                fTable.write(line.split(" ")[-1] + "|")
            if "Feature count" in line and flagRes:
                fTable.write(line.split(" ")[-1] + "|")
            if "Unlabeled accuracy" in line and flagRes:
                fTable.write(line.split(" ")[-3] + "|")
            if "Unlabeled attachment accuracy" in line and flagRes:
                fTable.write(line.split(" ")[-3] + "|")
                flagRes = False

        if not flagRes:
            fTable.write("\n")
        else:
            fTable.write(" | | | |\n")


        fSrc.close()

fTable.close()
