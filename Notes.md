## Links 

| Title | Link |
| --- | --- |
The tutorial | https://www.youtube.com/watch?v=npbMXXoKltg
Github repo to gem5 codesapce tut| https://github.com/gem5-hpca-2023/gem5-tutorial-codespace
Github repo to gem5 | https://github.com/gem5/gem5


Compilation Script for making static libraries : 
gcc hello.c -o hello.1 -static -static-libgcc

## Requirements

- (codespaces is nothing but VMs by github to run codes, built on docker)
- gem5 github repo


## Where to start

- read the gem5 doc and get a code implemented by it
- read about various performance metrics online and from the book
- implement matrix multiplication code
- generate a library for plotting various plots (general purpose codes that are required)
    - title, x-axis, y-axis etc..

## Nomenclature

- Host: Hardware on which sims running on 
- Guest: 
    - Code running on sim hardware
    - OS running on sim hardware guest OS
    - gem5 is simulating hardware
- simulator's code: runs natively to emulate the hardware on actial hardware
- Simulator's performance: time to run the simulation on the host wallclock as time you percieve it
- Simulated Performacne: time predicted by the simulator

- setting up these binary workloads is a pain (dont attempt it): these are disk images
- board.set_workload - is like the software on which the simulation is supposed to run
- obtain_resource - downloads the files needed to run the specific workload
- for: board.set_workload(obtain_resouces("x86-ubuntu-18.04-boot")), basically means for an x86 machine we get OS of Ubuntu whose version is 18.04 (dont know what boot is)
- resources file of gem5 contains all of them, all the images have an id and copy and use them
- SE FS mode
- It is like on top of the 
- Ticks: (Not cycles) smallest unit of time in the simulation specific for tgem5 purposes, frequency of processor in terms of ticks (too much goes in a cycle to encompensate)
    - ewvents queue is sorted by ticks
- any, json extentions are hardcopies of whatever has been simulated
- config.json: values of everything, if the system does not work out
- stats.txt 
    - simsecond
    - simticks
    - l1 cost controller
    - host time secs and simseconds are so different because
    - 10 ** 12 ticks = 1 sec
    - (lot fo them)

- use /home/arpit/Desktop/iitd/sem_7/COL718/projects/gem5/configs/common/Options.py to find what options can be added to the se file
- simulated perf > simultors performance

## General Pointers

- .git/pbjects/pack/pack has multiple file that can be accessed randomly and differences called delta
- .out file production may take atleast 15mins
- pre-commit hooks automating codes such as make etc.., just before commit, to maintain the sanctity of the github repo
- apropos lists all the similar commands by the name of the command
- "pipe" instruction behaves exactly like a pipeline and keeps providing plugins to the next operation whenever required
- gem5 util/pre-commit.sh has issue with the cd format recieveing more inputs than that are allowed (need to check this)
- BASH_SOURCE[0] provides the prefix to the directory (location to the directory)
- never use spaces while naming a file or a folder, causes the compiler to ditch the next word in a space (possibly thats why we could not get the cd running in the pre-commit.sh file)
- warnings in gem5 are very soft
- the number of ticks also matter for some reason
- CPU is defined in ticks per cycle
- git remote set-url <file> you can change the url where this project needs to be pushed
- events can schedule other events
- 1ps per tick = 10^12 ticks per sec
- the binary produced is wrt ISA
- inline can be used to suggest the compiler to replace a funciton call by the code itself when loops etc.. are not present (ref: https://www.geeksforgeeks.org/cpp/inline-functions-cpp/)
- gem5 script: gem5 is like a wrapper to python binary but with the fact that it aids to gem5 specific tasks
- \n starts new line for points in commenting eg currently supprot \n 1. etc..
- __main__ not supported in gem5 binary file

## Process Adopted by gem5 to run simulations

- type scons on the terminal and produce a gem5.out
- write your code that defines the entire hardware
- instead of calling python3, you call gem5 which loads OS and python on the simluated machine where the code is run. gem5 does the conversion of system level calls from the simulated machine to the host, providing one to one correspondence and hence emulation
- TODO: see if any code runs according to this logic
- TOSEE: maybe the Scons to run a matrix multiplication is different from the hello-world 
- ALL build includes all the ISAs, hence requires it for once only (it is written in the SConstruct and hence dont know how to modify it)
- gem5 is the interpreter for the special language that is based on python
- how to run a simulation: (whenver running pass the configguration script)
    - <opt file> <configuration file containing all the required set of hardware and software>

- You can set the workload from outside, however this is a binary file (check how to build it)

- clone and compile gem5
- created a simulation using a pre-built borad 
- obtained the workload needed from gem5 resources
- checked the output of gem5 simulation (I need to do this at my end)

- in m5.object there is something that is called Process: Usage:
    - process = Process(pid+x)
    - process.executable=wrkld or the binary file

- smallest unit is SimObjects
    - talk to eachother
    - events
    - schedule events, process
    - eg. can be register
    - gem5 lib of sim objects
    - CPU sim obj sends info to Mem Sim Objects

## Notes on Directory Structrure

- build/ shall be made automatically when scons is called
- there is Sconscript file in each of the sub-directory which is called for building purposes (doubtful)
- build/ has seperate directory for each set of ISAs and cache coherence policy


## Some painstaking errors

- Fixed the issue of not being able to run gem5 compiled version, becuase of using .out instead of .opt ;;
- scons ran with all the cpu cores and without running in background (either one of them can be an issue)

## File Structure Layout

- gem5
    - build/ISA/gem5.opt
    - configs/deprecated/se.py
- Gem5-Tutorial
    - config_script.py
    - binary file
    - (make calls from here to gem5)
    - Notes 
    - plots/ -> contains all the images for various plots

## some configs

All gem5 BaseCPU’s take the naming format {ISA}{Type}CPU

- Valid ISAs:
    (can use while using se.py)
    - Riscv
    - Arm
    - X86
    - Sparc
    - Power
    - Mips

- Valid CPU Types: (https://www.gem5.org/documentation/general_docs/cpu_models/SimpleCPU#timingsimplecpu)
    (can use while using se.py)
    - AtomicSimpleCPU (uses atomic memory access (?))
    - O3CPU (uses pipielining)
    - TimingSimpleCPu (uses timing memory access (?))
    - KvmCPU
    - MinorCPU

All gem5 BaseCPU’s take the naming format {ISA}{Type}CPU


## Performance Metrics that may be used

- Raw speed
- Throughput
- Latency 
- Parallelism


## How to get sir's code running

- BinaryResource to be used
- processor to be mentioned at length: processor = SimpleProcessor(cpu_type=CPUTypes.ATOMIC, num_cores=1, isa=ISA.X86)
- OS and kernel (ig) are chosen by default

## To Submit (Check before submission)

- Report:
    - Performance Variation (Grpahs + Table)

- mm.c
- Config Script file

- (For bonus you need a cross compiler)
- read about stats from here: https://www.gem5.org/documentation/learning_gem5/part1/gem5_stats/

## Did not understand but can be useful

- Trace: play-back that plays elastic probe atteached to o3 cpus

## Working on Matrix Multiplication

- can use this simple compilte method: https://vaibhaw-vipul.medium.com/matrix-multiplication-optimizing-the-code-from-6-hours-to-1-sec-70889d33dcfa
- use the method in comp arch book