## This is a sample python script to submit a paramater sweep of jobs.
## Made for use on:
##  A) Brandeis HPCC which uses the SLURM workload manager.
##  B) Brandeis HPC (old cluster) which uses the Sun Grid Engine.
##  -> XSTREAM and STAMPEDE2 compatibility coming up.
##  -> Contributions from others for compatibility with other clusters are welcome!

## It essentially creates a unique temporary bash script for each parameter value, submits the job using sbatch, and deletes the script. 
import numpy as np
from subprocess import call, Popen
from itertools import product
import os
## Setting up argparse ##
## This is to specify which server we are running the script on. ##
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-s","--server", default="hpcc", choices=["local","hpc","hpcc","stampede2","xstream"], help="Name of server (local/hpc/hpcc/stampede2/xstream)")
## Change the default username according to what you want. ##
parser.add_argument("-u","--username", default="chaitanya",help="Username corresponding to the server")
args = parser.parse_args()
server = args.server
uname = args.username
## Directory Structure ##
## parentfolder is the filesystem destination. Change it if changing servers. ##
if(server=='local'):
    parentfolder = "data"
elif(server=='hpc'):
    parentfolder = "/data/netapp/{}".format(uname)
elif(server=='hpcc'):
    parentfolder="/work/{}".format(uname)
elif(server=='stampede2'):
    # stampede2 has obscure usernames, and I won't remember them.
    # So I am redifining it here.
    uname = "tg849351"
    parentfolder = "/work/05636/{}/stampede2".format(uname)
elif(server=='xstream'):
    parentfolder = "/cstor/xsede/users/{}".format(uname)
##
## This sample is a sweep over two parameters, but can be easily extended to however many parameters.
param1 = [1.0,2.0,3.0]
param2 = [4.0,5.0,6.0,7.0]
job_name = 'test'
job_num = 1 # To keep track of the total number of jobs, if needed.
for (p1,p2) in product(param1,param2):
    if(server=="local"):
        #  
        Popen("python3 stupid_program.py --p1 {0:.1f} --p2 {1:.1f} --dir {2}".format(p1,p2,parentfolder).split())
    elif(server=="hpcc"):
        ## Some lines in the bash script are going to be independent of the parameters.
        ## I have stored them in a separate file called slurm_common_lines, but they can be included here too.
        with open ('slurm_common_lines.txt','r') as f:
            commonlines = f.read()
        script = commonlines
        ## Now we add a parameter-specific job name, for instance "test__{p1}_{p2}"
        script += "\n#SBATCH --job-name={0}_{1:.1f}_{2:.1f}\n".format(job_name,p1,p2)
        ## Loading the essential modules (in this case, python3 anaconda) on the cluster, if required.
        script += "\nmodule load share_modules/ANACONDA/5.3_py3\n"
        ## Run the program with current parameters - "srun {program_to_run}"
        script += "srun python3 stupid_program.py --p1 {0:.1f} --p2 {1:.1f} --dir {2}".format(p1,p2,parentfolder)
        ## Write contents to a bash script
        with open("slurm_script.sh",'w') as g:
            g.write(script)
        ## Submit the specific job using sbatch    
        call(["sbatch", "slurm_script.sh"])
        ## Delete the temporary script. Save one of them to check if it looks okay
        if(job_num!=1): os.remove("slurm_script_test.sh")
    elif(server=="hpc"):
        with open ('sun_grid_common_lines.txt','r') as f:
            qsub_base = f.read()
        qsub = "#$ -N {0}_{1:.1f}_{2:.1f}\n".format(job_name,p1,p2)
        qsub += qsub_base
        qsub += "module load PYTHON3 \n"
        qsub += "python3 stupid_program.py --p1 {0:.1f} --p2 {1:.1f} --dir {2}".format(p1,p2,parentfolder)
        with open("sun_grid_script",'w') as g:
            g.write(qsub)
        call(["qsub", "sun_grid_script"])
        os.remove("sun_grid_script")
    job_num +=1