# HPC_final_project
the resulting heat map is stored in the folder "heatResults"

the codes are developed in python

1. To visualize the heat map, please run the python file "plotcoolwarm.py" using the command:
_______________________
$ python3 plotcoolwarm.py
-----------------------

2. To modify the parameters, e.g. Tcool, Thot, the initial heat state and the size of the rectangular pad, open the file "parallel_solver.py" or "serial.py".

3. To run the file "parallel_solver.py" or "serial.py" on Beskow, use the command:
_______________________
$ mkdir heatResults
module load mpi4py/3.0.2/py37
srun -n ? python3 parallel_solver.py
ls
tar -cvf heatResults.tar heatResults
------------------------
then, on your personal computer, locate yourself at a folder in terminal, and then type in the commands:
________________________
$ scp yuehan@t04n27.pdc.kth.se:/cfs/klemming/scratch/y/yuehan/DD2356/Project/heatResults.tar .

tar -xvf heatResults.tar
python3 plotcoolwarm.py
--------------------------


