#! /usr/bin/python3

import csv
import sys

csv.field_size_limit(sys.maxsize)

reader = csv.reader(sys.stdin, delimiter="\t")

for row in reader:
    if row[6] == "P":
        sys.stdout.write(row[1]+"\n")
