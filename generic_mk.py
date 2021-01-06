## This is a sample python script to submit a paramater sweep of jobs.
## Made for use on:
##  A) Brandeis HPCC which uses the SLURM workload manager.
##  B) Brandeis HPC (old cluster) which uses the Sun Grid Engine.
##  C) The XSEDE machines 'Expanse' and 'STAMPEDE2'.
##  -> Contributions from others for compatibility with other clusters are welcome!

## It essentially creates a unique temporary bash script for each parameter value, submits the job using sbatch, and deletes the script. 
from subprocess import call, Popen
from itertools import product
import os
## Setting up argparse ##
## This is to specify which server we are running the script on. ##
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--server", default="hpcc", choices=[
                    "local", "hpc", "hpcc", "stampede2", "expanse"], help="Name of server (local/hpc/hpcc/stampede2/expanse)")
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
    uname = "kdfjlas"
    parentfolder = "/work/05636/{}/stampede2".format(uname)
elif(server == 'expanse'):
    parentfolder = "/expanse/lustre/scratch/{}/temp_project".format(uname)
##
## This sample is a sweep over two parameters, but can be easily extended to however many parameters.
param1 = [1.0,2.0,3.0]
param2 = [4.0,5.0,6.0,7.0]
job_name = 'test'
job_num = 1 # To keep track of the total number of jobs, if needed.
for (p1,p2) in product(param1,param2):
    ## Define the command to execute to run the code
    exec_cmd = "python3 example_program.py --p1 {0:.1f} --p2 {1:.1f} --dir {2}".format(
        p1, p2, parentfolder)

    script_n = "script_{0}_{1}.sh".format(
        server, job_num)  # Name of bash script
    if(server=="local"):
        # Run the program  
        Popen("{}".format(exec_cmd).split())
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
        ## Run the program 
        script += "srun " + exec_cmd
        ## Write contents to a bash script
        with open(script_n,'w') as g:
            g.write(script)
        ## Submit the specific job using sbatch    
        call(["sbatch", script_n])
        ## Delete the temporary script. Save one of them to check if it looks okay
        if(job_num!=1): os.remove(script_n)
    elif(server=="hpc"):
        ## Some lines in the bash script are going to be independent of the parameters.
        ## I have stored them in a separate file called sun_grid_common_lines.txt, but they can be included here too.
        with open ('sun_grid_common_lines.txt','r') as f:
            qsub_base = f.read()
        ## Now we add a parameter-specific job name, for instance "test__{p1}_{p2}"
        script = "#$ -N {0}_{1:.1f}_{2:.1f}\n".format(job_name,p1,p2)
        script += qsub_base
        ## Loading the essential modules (in this case, python3 anaconda) on the cluster, if required.
        script += "module load PYTHON3 \n"
        ## Run the program - "{program_to_run}"
        script += exec_cmd
        ## Write contents to a bash script
        ## Submit the specific job using qsub    
        with open(script_n,'w') as g:
            g.write(script)
        call(["qsub", script_n])
        ## Delete the temporary script. Save one of them to check if it looks okay
        if(job_num!=1): os.remove(script_n)
    elif(server == "stampede2"):
        ## Some lines in the bash script are going to be independent of the parameters.
        ## I have stored them in a separate file called stampede2_common_lines.txt, but they can be included here too.
        with open('stampede2_common_lines.txt', 'r') as f:
            commonlines = f.read()
        script = commonlines
        ## Now we add a parameter-specific job name, for instance "test__{p1}_{p2}"
        script += "\n#SBATCH --job-name={0}\n".format(job_name)
        script += "\n#SBATCH -o %x.o"
        script += "\n#SBATCH -e %x.e"
        # script += "\nexport OMP_NUM_THREADS=64\n"
        ## Loading the essential modules (in this case, python3 anaconda) on the cluster, if required.
        script += "\nmodule load python3\n"
        script += "\nexho $SLURM_JOB_ID\n"
        ## Run the program 
        script += exec_cmd
        ## Write contents to a bash script
        with open(script_n, 'w') as g:
            g.write(script)
        ## Submit the specific job using sbatch
        call(["sbatch", script_n])
        ## Delete the temporary script. Save one of them to check if it looks okay
        if(job_num != 1):
            os.remove(script_n)
    elif(server == "expanse"):
        ## Some lines in the bash script are going to be independent of the parameters.
        ## I have stored them in a separate file called expanse_common_lines.txt, but they can be included here too.
        with open('expanse_common_lines.txt', 'r') as f:
            commonlines = f.read()
        script = commonlines
        ## Now we add a parameter-specific job name, for instance "test__{p1}_{p2}"
        # script += "\n#SBATCH --job-name={0}_{1:.1f}_{2:.1f}\n".format(job_name,p1,p2)
        script += "\n#SBATCH -N 1"
        script += "\n#SBATCH --ntasks-per-node=1"
        script += "\n#SBATCH --job-name={0}\n".format(job_name)
        script += "\n#SBATCH -o %x.o"
        script += "\n#SBATCH -e %x.e"

## Loading the essential modules (in this case, python3 anaconda) on the cluster, if required.
        script += "\nmodule load cpu"
        ## Run the program 
        script += exec_cmd
        ## Write contents to a bash script
        with open(script_n, 'w') as g:
            g.write(script)
        # Submit the specific job using sbatch
        call(["sbatch", script_n])
        # Delete the temporary script. Save one of them to check if it looks okay
        if(job_num != 1):
            os.remove(script_n)

    job_num +=1