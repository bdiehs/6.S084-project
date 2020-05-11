#!/bin/bash
cd /Users/zoe/Documents/leon # you have to change this
echo "Running Leon"
./leon --solvers=smt-z3 --synthesis  ./../6.S084-project/input_program.txt > ../6.S084-project/out.txt

cd /Users/zoe/Documents/6.S084-project
x=$(cat out.txt | grep -n "========" | tail -1 | cut -f1 -d:)
x=$((x + 1)) # don't want the ==== header line
tail -n +$x out.txt > tmp.txt

echo "Wrote program to tmp.txt"
echo "Cleaning up program..."
sed 's/\[.*\] //' tmp.txt > output_program.scala
rm tmp.txt
rm out.txt
echo "Wrote program to output_program.scala. Done."
