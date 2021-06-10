# HPC_final_project

The codes are developed in python

Supposing you are using the Beskow, following is the tutorial about how to get these python file work for you.

[Step1] Run "parallel_solver.py" or "serial.py" to solve the equation and produce results. The commands are:
$ salloc --nodes=1 -t 01:00:00 -A edu21.DD2356 -C Haswell
$ srun -n 1 python3 parallel_solver.py

If you want to run "parallel_solver.py", make sure to run the command "$ module load mpi4py/3.0.2/py37" before executing the file.

If you want to run "parallel_solver.py" using more than 64 processes, for example, 256 processes, 1 node is no more enough for so many process, so you need to modify the first two commands into:
$ salloc --nodes=8 -t 01:00:00 -A edu21.DD2356 -C Haswell
$ srun -n 256 --ntasks-per-node=32 python3 parallel_solver.py

When the program is completed, you will see two newly generated folders: "scalingTestResults" and "heatResults"



[Step2] Run the single-process program code, "plotcoolwarm.py", to see the resulting heat picture:
$ srun -n 1 python3 plotcoolwarm.py



[Step3] Modify the parameters, e.g. the value of the variables "dx (should==dy)" in "parallel_solver.py", and the number of processes, to see different results and performance. Run the single-process program file, "scalingTest_resultShower.py", to see the execution time of the calculation part of the multi-process program code, "parallel_solver.py"
$ srun -n 1 python3 scalingTest_resultShower.py



[Step4] Run the multi-process program code, "monitor_parallel_solver.py", to record the time stamps right before/after the "req.wait()". For example, if you want to use 256 processes, you need to run the commands:
$ salloc --nodes=8 -t 01:00:00 -A edu21.DD2356 -C Haswell
$ srun -n 256 --ntasks-per-node=32 python3 monitor_parallel_solver.py

After it is completed, you will see two newly generated folders, "heatResults" and "timeRecords".



[Step5] Run the single-process program code, "visualizer.py", to see the idle-period plot.



[Step6*] If you want to test whether the "visualizer.py" produce expected results, you can run the multi-process program code, "visualizationTester.py". It is recommended to look into the code of the "visualizationTester.py" file and do some modification.


