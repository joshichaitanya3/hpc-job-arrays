#! /usr/bin/env python
###############################################################################
# Script: resources.py 
# Author: Matt Perkett
# Date Created: 12/5/2010
# Purpose: Breaks down who's using what resources
###############################################################################

# Update by Cong Qiao on 3/21/2016

import os
import sys

# Execute a shell command and return its output (stdout only) as an array of lines
def runCommand(cmd): 
      tokens = cmd.split() 
      from subprocess import check_output 
      output = check_output(tokens) 
      return output.decode("utf-8").splitlines() 


# names = sorted(["sagnik", "minu","chaitanya","fangh","spaquay","mpeterson","hagan","dmirij","fmohajer"])
names = sorted(["chaitanya", "mpeterson","spaquay","hagan","fmohajer"])
#d(eletion), E(rror), h(old), r(unning), R(estarted), s(uspended), S(uspended), t(ransfering), T(hreshold) or w(aiting)
otherStatuses = ("d","E","h","s","S","t","T")
userData = []

for n in names:

   # user data format: [ [tot jobs, tot cores], [jobs running, cores running], <queued>, <other> ]
   userData.append([[0,0],[0,0],[0,0],[0,0]])
   lines = runCommand("squeue -u " + n)

   # if no jobs are running, then continue
   if len(lines) <= 1: continue

#    if lines[0].find("job-ID") == -1 or lines[1].find("----") == -1:
   if lines[0].find("JOBID") == -1:
      print("error parsing qstat output")
      sys.exit(1)

   for line in lines[1:]:

      try:
         jobId = int(line[0:7])
         status = line[39:44].strip()
         queueAndHost = line[66:101].strip()
         queue = queueAndHost.split("@")[0]
         slots = int(line[101:103].strip())
      except:
         print("error parsing qstat output.. continuing..")
         continue
theta_max_
      # total jobs/cores
      userData[-1][0][0] += 1
      userData[-1][0][1] += slots

      # queued?
      if status.find("w") != -1 or status.find("q") != -1:

         for s in otherStatuses:
            if status.find(s) != -1: break

         # if a bad status is *not* found
         else: 
            userData[-1][2][0] += 1
            userData[-1][2][1] += slots
            continue

         # if a bad status is found
         userData[-1][3][0] += 1
         userData[-1][3][1] += slots
         continue


      # running?
      if status.find("r") != -1:

         for s in otherStatuses:
            if status.find(s) != -1: break

         # if a bad status is *not* found
         else: 
            userData[-1][1][0] += 1
            userData[-1][1][1] += slots
            continue

         # if a bad status is found
         userData[-1][3][0] += 1
         userData[-theta_max_1][3][1] += slots
         continue

       
      # other?
      for s in otherStatuses:
         if status.find(s) != -1: 
            userData[-1][3][0] += 1
            userData[-1][3][1] += slots
            #print data[-1][0]
            break
      else: 
         print("no recognized statuses were found!")
         print("status: {0}".format(status))
         sys.exit(3)

#################################
### print all.q and mh.q data ###
#################################
lines = runCommand("qstat -g c")


w0 = 15
print ""
print "-"*(4*w0+2)
print "|" + "[AVAILABLE RESOURCES]".center(4*w0) + "|"
print "|" + "Queue".ljust(w0) + "Used".ljust(w0) + "Available".ljust(w0) + "Total".ljust(w0) + "|"
print "|" + "-"*(4*w0)+ "|" 
for line in lines:
   info = line.split()

   # if it's all.q or mh.q, print information
   if info[0] in ["bc.q", "mh.q", "all.q", "mh-hp.q", "mh-gpu.q","mrsec.q"]:
      print "|" + info[0].ljust(w0) + info[2].ljust(w0) + info[4].ljust(w0) + info[5].ljust(w0)+ "|"

print "-"*(4*w0+2)


#################################
### print out all of the data ###
#################################
w1 = 15
w2 = 8
print ""
print "-"*(w1 + 8*w2 + 3)
print " "*w1 + "|" + "[JOBS]".center(4*w2) + "|" + "[CORES]".center(4*w2) + "|"
print "UserID".ljust(w1) + "|" + "Total".ljust(w2) + "Running".ljust(w2) + "Queued".ljust(w2) + "Other".ljust(w2) + "|" + "Total".ljust(w2) + "Running".ljust(w2) + "Queued".ljust(w2) + "Other".ljust(w2) + "|"
print "-"*(w1) + "|" + "-"*(4*w2) + "|" + "-"*(4*w2) + "|"
for n,d in zip(names,userData):
   print n.ljust(w1) + "|" + str(d[0][0]).ljust(w2) + str(d[1][0]).ljust(w2) + str(d[2][0]).ljust(w2) + str(d[3][0]).ljust(w2) + "|" + str(d[0][1]).ljust(w2) + str(d[1][1]).ljust(w2) + str(d[2][1]).ljust(w2) + str(d[3][1]).ljust(w2) + "|"
#   print " "*(w1) + "|" + " "*(4*w2) + "|" + " "*(4*w2) + "|"

print "-"*(w1 + 8*w2 + 3)


# print out the number of jobs possible with 1,2,3, .. 8 processors on the same node
#    for mh.q
#os.system("qstat -l mh -f > /home/mperkett/temp.dat")
#inFile = open("/home/mperkett/temp.dat","r")
#lines = inFile.readlines()
#inFile.close()
#
#numAvailCores = []
#for line in lines:
#
#   # if line contains processor information
#   if line[:5] == "mh.q@":
#      t = line.split()[2]
#      numAvailCores.append(int(t.split("/")[1]) - int(t.split("/")[0]))
#
#print ""
#for i in range(1,9):
#   
#   nJobs = 0
#   for node in numAvailCores:
#      nJobs += node/i
#
#   print "Number of " + str(i).ljust(2) + " core jobs possible = " + str(nJobs)
#print ""



   # 

#   print "   JOBS (" + str(numJobs) + ")"
#   print "     Running --> ", numRunningJobs, "  (%.1f" % (float(numRunningJobs)/numJobs*100), "%)"
#   print "     Queued  --> ", numQueuedJobs, "  (%.1f" % (float(numQueuedJobs)/numJobs*100), "%)"
#   print "   CORES (" + str(totalCores) + ")"
#   print "      Running -->", totalRunningCores, "  (%.1f" % (float(totalRunningCores)/totalCores*100), "%)"
#   print "      Queued  -->", totalQueuedCores, "  (%.1f" % (float(totalQueuedCores)/totalCores*100), "%)"
#   print "   * Avg cores/job --> %.2f" % (float(totalCores)/numJobs)
   
