#!/bin/bash
# @ job_name= heatmap_demo
# @ initialdir= .
# @ output= slurm/20201220T131218-heatmap_demo-%j.out
# @ error= slurm/20201220T131218-heatmap_demo-%j.err
# @ total_tasks= 1
# @ cpus_per_task= 1
# @ gpus_per_node= 4
# @ wall_clock_limit = 00:20:00
srun python3 -m app.cli compute -j jobs/heatmap_demo.yaml
