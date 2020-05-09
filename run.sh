#!/bin/bash
cd /Users/zoe/Documents/leon # you have to change this
echo "Running Leon"
./leon --solvers=smt-z3 --synthesis  ./testcases/synthesis/current/List/Split.scala > out.txt
x=$(cat out.txt | grep -n "========" | tail -1 | cut -f1 -d:)
x=$((x + 1)) # don't want the ==== header line
tail -n +$x out.txt > tmp.txt

echo "Wrote program to tmp.txt"
echo "Cleaning up program..."
sed 's/\[.*\] //' tmp.txt > program.scala
rm tmp.txt
echo "Wrote program to program.scala. Done."
