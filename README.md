# 6.S084-project

Final project for 6.S084. 

# Setting up Leon

Leon is at: https://github.com/epfl-lara/leon. You can mostly follow its README but there are some changes. Make sure you use the right versions of Scala for Leon and Z3. 

# Setting up Z3

Z3 is an SMT solver. There are some instructions in the Leon README but here are some more. To install Z3, follow the steps in the Leon README. Get the appropriate release for your OS at https://github.com/Z3Prover/z3/releases. The bin/ directory has the binary `z3`. `cd` into bin/ and add that to your $PATH.  

Faster than using Z3 is using the Z3 wrapper, ScalaZ3, which Leon uses (this is described in the Leon README). Follow the Leon README's instructions at 
https://github.com/epfl-lara/leon/blob/master/src/sphinx/installation.rst#building-scalaz3-and-z3-api 
which point you to ScalaZ3's README instructions. Get the release appropriate for your OS at https://github.com/epfl-lara/ScalaZ3/releases. You will need a different version of sbt than for Leon. 

In section https://github.com/epfl-lara/ScalaZ3#using-scalaz3, instead of adding the suggested code to build.sbt, add the following: 

`unmanagedJars in Compile += file("scalaz3_2.13-4.7.1.jar")` 

This is because Leon builds with an older version of sbt than ScalaZ3. 

When running `sbt +package`, some instructions about changing environment variables and installing Z3 will go by. You should add the follow lines to your bash profile: 

```
export PYTHONPATH=$PYTHONPATH:/Your/Path/Here/ScalaZ3/z3/z3-4.7.1/build/python

export DYLD_LIBRARY_PATH=$DYLD_LIBRARY_PATH:/Your/Path/Here/ScalaZ3/z3/z3-4.7.1/build
```

and run `sudo make install`.

To use the wrapper, which is the faster option, run with `--solvers=smt-z3`. For example, 
`./leon --solvers=smt-z3 ./testcases/verification/datastructures/RedBlackTree.scala`.
