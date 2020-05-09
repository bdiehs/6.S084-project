#!/bin/bash
cd /Users/zoe/Documents/leon
echo `pwd`
# # ./leon --solvers=smt-z3 --synthesis --o=newoutput/leon.out ./testcases/synthesis/current/List/Split.scala > out.txt
x=$(cat out.txt | grep -n "========" | tail -1 | cut -f1 -d:)
echo $x
# # gets line number value, set to variable
tail -n +$x out.txt
