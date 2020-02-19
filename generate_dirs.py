#!/usr/bin/env python

from pathlib import Path
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("infile", help="Input file")
parser.add_argument("-o", "--outdir", help="Output dir", default="./sequences")
parser.add_argument("-u", "--unique", help="Output a unique.txt listing all the unique sequences")
args = parser.parse_args()

with open(args.infile, "r") as protine_file:
    file_text = protine_file.read()

unique = dict()
unique_keys = set()
sequence_limit = {"min": 20, "max": 10000000000}

file_text = file_text.replace("\n","")[1:]
lines = file_text.split(">")

for line in lines:
    name = line.split("|")
    rest = name[1:]
    name = name[0].strip()
    #print(name)
    #print(rest)
    sequence = rest[-1][len("SEQUENCE"):].strip()
    #print(sequence)
    rest.pop()
    size = len(sequence)
    if size > sequence_limit["min"] and size < sequence_limit["max"]:
        if sequence not in unique:
            unique[sequence] = {"sequence":sequence, "rest":rest, "name": name}

print("size: {}".format(len(unique)))

if args.unique:
    unique_text = list()
    for key in unique:
        unique_text.append(">{}|{}|SEQUENCE\n{}".format(unique[key]["name"], "|".join(unique[key]["rest"]),unique[key]["sequence"]))
    with open("unique.txt", "w") as unique_handle:
        unique_handle.write("\n".join(unique_text))

for key in unique:
    entry = unique[key]
    dir = Path(args.outdir) / entry["name"]
    dir.mkdir(parents=True)
    with open(str(dir/"sequence.txt"), "w") as seq_file:
        seq_file.write("{}\n".format(entry["sequence"]))
