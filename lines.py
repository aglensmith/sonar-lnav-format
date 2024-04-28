#!/usr/bin/python3
import sys

file = open(sys.argv[1], 'r')
for line in file:
    print('{"line": "'+ line.strip() +'"},')
file.close()