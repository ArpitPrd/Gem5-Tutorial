#!/bin/bash

CPUS=(O3 TIMING)
FREQS=(600MHz 800MHz 1000MHz 1200MHz 1400MHz 1600MHz 1800MHz 2000MHz 2200MHz 2400MHz 2600MHz 2800MHz 3000MHz 3200MHz 3300MHz)
MEMS=(DDR3 HBM)
mode=a
gcc -O3 mm.c -o mm
for cpu in "${CPUS[@]}"; do
  for freq in "${FREQS[@]}"; do
    for mem in "${MEMS[@]}"; do
      time \
      /home/arpit/Desktop/iitd/sem_7/COL718/projects/gem5/build/X86/gem5.opt \
        --outdir="out/${cpu}_${freq}_${mem}_out" \
        ./config_script.py \
        --cpu_type="$cpu" \
        --cpu_freq="$freq" \
        --mem_type="$mem" \
        --cache_type=MESITwoLevelCacheHierarchy \
        --mem_size=2GiB \
        --mode=$mode
    done
  done
done