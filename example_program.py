# This is an example program to illustrate the use of 
# the job array submission script `generic_mk.py`.
# This program saves the output of the multiplication 
# of two floats `p1` and `p2` in a file.
# It takes in three arguments - two of which are floats `p1` and `p2`,
# and the third one is a string containing the 
# directory in which to save the output. 
# The idea is to illustrate how to submit this job for a table of 
# values of `p1` and `p2`, which is shown in `generic_mk.py`

import argparse
import pathlib
parser = argparse.ArgumentParser()
parser.add_argument("--p1",type=float,default=1.0,choices=[1.0,2.0], help="value of param1")
parser.add_argument("--p2",type=float,default=4.0,choices=[4.0,5.0], help="value of param2")
parser.add_argument("--dir",type=str, default="data",help="path to data")
args = parser.parse_args()
p1 = args.p1
p2 = args.p2
parent_dir = args.dir
print("p1 = ",p1)
print("p2 = ",p2)
## Perform the computations with these parameters, in this case, multiplication.
answer = p1*p2
## Optionally save the result of this computation in a directory dedicated to these parameters
data_dir = "{}/p1_{:.1f}/p2_{:.1f}".format(parent_dir,p1,p2)
## The following command will recursively create all the directories needed.
pathlib.Path(data_dir).mkdir(parents=True, exist_ok=True)
with open("{}/answer.txt".format(data_dir), "w") as f:
    f.write("The answer is {:.1f}.\n".format(answer))
