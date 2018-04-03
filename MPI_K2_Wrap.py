#from mpi4py import MPI

from glob import glob

import time as sys_time
# Import all the functions
from K2TranPixCode import *

field = 'c14'
path = '/avatar/ryanr/Data/'+field+'/'
Files = np.asarray(glob(path+'*.gz'))

save = '/avatar/ryanr/Results/'

Files = np.asarray(glob(path+'*.gz'))
# Code to remove files from the list that have already been calculated
try:
    Log = open('/avatar/ryanr/Code/shell'+ field + '.out')
    log = Log.read()
    lines  = test.split('\n')
    files = []
    for line in lines:
        if '/avatar/ryanr/Data/' in line:
            files.append(line)
    for j in range(len(files)):
        Files = np.delete(Files,np.where(files[j] in Files))
except (FileNotFoundError):
    pass

dims = int(len(Files)) # set to be length of your task
start = sys_time.time()

def print_mpi(string):
    comm = MPI.COMM_WORLD
    print("["+str(comm.Get_rank())+"] "+string)

def print_master(string):
    comm = MPI.COMM_WORLD
    if comm.Get_rank() == 0:
        print("["+str(comm.Get_rank())+"] "+string)

# init MPI

comm = MPI.COMM_WORLD
nPE = comm.Get_size()
myPE = comm.Get_rank()
print_master("Total number of MPI ranks = "+str(nPE))
comm.Barrier()


# Progress saving function

def writemyprog(filename,out):
    np.savez(filename,out)

# domain decomposition

my_start = int(myPE * (dims / nPE));
my_end   = int((myPE+1) * (dims / nPE) - 1);
# last PE gets the rest
if (myPE == nPE-1): my_end = dims-1;
print_mpi("my_start = "+str(my_start)+", my_end = "+str(my_end))

# parallel loop

filename = "my_prog_"+str(myPE).zfill(4)


for n in range(my_start, my_end+1):
    mytimestart = sys_time.time()
    
    K2TranPix(Files[n],save)
    
    mytimestop = sys_time.time()
    mytime = mytimestop-mytimestart
    #print('n=%g' %n, 'my_time=%f' %mytime)


# MPI collective communication (all reduce)

stop = sys_time.time()
print_master('Time taken=%f' %(stop-start))