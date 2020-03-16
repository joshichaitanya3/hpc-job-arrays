# hpc_job_arrays
Python script to submit jobs to computing clusters using SLURM / Sun Grid Engine.

*generic_mk.py* : This is an example python script to submit multiple jobs which run the same code with different input parameters. This is ideal for parameter sweeps.

OPTIONS:

**-s, --server=<name_of_server>**

Specify the name of server. Default is hpcc. Other options are local and hpc as of now. xstream, and stampede2 coming up soon.

**-u, --username=<user_name>**

Specify your username on the server. This will be used to determine the directory on that server where the data will be stored.

## Demo using an example

*example_program.py* : This is our computation script. It takes two numbers `p1` and `p2` as its input parameters, calculates their product, and saves the answer in a file.

OPTIONS:

**--p1 <value_of_p1>**

Specify the value of `p1` (float). Default is `1.0`. Choices are `[1.0,2.0]`.

**--p2 <value_of_p2>**

Specify the value of `p2` (float). Default is `4.0`. Choices are `[4.0,5.0]`.

**--dir <path/to/work/directory>**

Specify the path to the parent directory where data is to be stored. Usually this would be the $WORK directory. Default is "data" (`./data`).

 The choices for `p1` and `p2` are restricted just so that you can test large parameter sweeps without printing large amount of data (the script will just break if the values aren't one of the choices). The output is printed in a text file in the directory `"dir/p1_{value of p1}/p2_{value of p2}"`. The `"dir"` is the parent data directory.


There are usually some common lines in the bash scripts that do not depend on the parameters, like the nodes to be used, or the email id to be used, etc. I have made text files to store these lines for simplicity.

*slurm_common_lines* : This one contains the common bash script lines for the new HPCC which uses SLURM

*sun_grid_common_lines* : This one contains the common bash script lines for the old cluster which uses the Sun Grid Engine.
