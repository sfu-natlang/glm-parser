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

if (args.append == "0"):
    fTable = open(os.path.join(args.res, "log_summary.md"), "w")
    fTable.write("|Data|Machine|Branch|Learner|Feature Generator|Parser|Iteration|Training Time|Feature Count|Unlabeled Accuracy|Unlabeled Attachment Accuracy|\n")
    fTable.write("|---|---|---|---|---|---|---|---|---|---|---|\n")
else:
    fTable = open(os.path.join(args.res, "log_summary.md"), "a")


def leaveBlank(filled, index):
    for i in range(index-1, -1, -1):
        if filled[i]:
            break;
        if (index == 0):
            fTable.write("|")
        fTable.write("|");
        filled[i] = True;

for root, dirs, files in os.walk(args.src):
    for name in files:
        filled = [False, False, False, False, False, False, False, False, False, False, False]
        flagCmd = False;
        if len(name.split('.')) > 1 and name.split('.')[1] == "md":
            continue
        fTable.write("|" + name.split('.')[0] + "|")
        filled[0] = True
        fSrc = open(os.path.join(root, name), "r")
        for line in fSrc:
            line = line.strip()
            if line.startswith("Machine"):
                leaveBlank(filled, 1)
                fTable.write(line.split(" ")[1] + "|")
                filled[1] = True
            if line.startswith("Branch"):
                leaveBlank(filled, 2)
                fTable.write(line.split(" ")[1] + "|")
                filled[2] = True

            if flagCmd:
                parameters = line.split(" ")
                for index, obj in enumerate(parameters):
                    if obj.startswith("--learner"):
                        leaveBlank(filled, 3)
                        fTable.write(obj.split("=")[1] + "|")
                        filled[3] = True
                        break
                for index, obj in enumerate(parameters):
                    if obj.startswith("--fgen"):
                        leaveBlank(filled, 4)
                        fTable.write(obj.split("=")[1] + "|")
                        filled[4] = True
                        break
                for index, obj in enumerate(parameters):
                    if obj.startswith("--parser"):
                        leaveBlank(filled, 5)
                        fTable.write(obj.split("=")[1] + "|")
                        filled[5] = True
                        break
                for index, obj in enumerate(parameters):
                    if obj == "-i":
                        leaveBlank(filled, 6)
                        fTable.write(parameters[index + 1] + "|")
                        filled[6] = True
                        flagCmd = False
                        break

            if "Command" in line:
                flagCmd = True

            if "training time" in line.lower():
                leaveBlank(filled, 7)
                fTable.write(line.split(" ")[-1] + "|")
                filled[7] = True
            if "feature count" in line.lower():
                leaveBlank(filled, 8)
                fTable.write(line.split(" ")[-1] + "|")
                filled[8] = True
            if "unlabeled accuracy" in line.lower():
                leaveBlank(filled, 9)
                splitLine = line.split(" ")
                for index, obj in enumerate(splitLine):
                    if (obj.lower() == "accuracy:"):
                        fTable.write(splitLine[index + 1] + "|")
                filled[9] = True
            if "unlabeled attachment accuracy" in line.lower():
                leaveBlank(filled, 10)
                for index, obj in enumerate(splitLine):
                    if (obj.lower() == "accuracy:"):
                        fTable.write(splitLine[index + 1] + "|")
                filled[10] = True

        leaveBlank(filled, 11)
        fTable.write("\n");

        fSrc.close()

fTable.close()
