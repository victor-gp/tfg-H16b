#!/bin/bash

# submit a SLURM job with directives based on your environment variables

# the envs are: job (path to the job config to compute, required), tasks, cpus, gpus, time.
# a full job script including those variables is written to jobs/minotauro_job.cmd and then
# submited with mnsubmit

# check the current user-defined value for those environment variables with
# $ env | grep -e job -e tasks -e cpus -e gpus -e time

set -e

if [ -z "$job" ]; then
   echo "mt_submit: env \$job is required!"
   exit 1
elif ! [ -f "$job" ]; then
   echo "mt_submit: env \$job must be a path to a job config file."
   exit 1
fi

JOB_CONFIG=$job
TOTAL_TASKS=${tasks:-1}
CPUS_PER_TASK=${cpus:-1}
GPUS_PER_NODE=${gpus:-4}
WALL_CLOCK_LIMIT=${time:-00:20:00}


validate_num() {
   env_name=$1
   value=$2

   if ! [[ $value =~ ^[0-9]+$ ]]; then
      echo "mt_submit: invalid value for env \$$env_name: ‘$value’."
      exit 1
   fi
}

validate_num "tasks" "$TOTAL_TASKS"
validate_num "cpus" "$CPUS_PER_TASK"
validate_num "gpus" "$GPUS_PER_NODE"

if ! [[ $WALL_CLOCK_LIMIT =~ ^[0-9][0-9]:[0-9][0-9]:[0-9][0-9]$ ]]; then
   echo "mt_submit: invalid value for env \$time: ‘$WALL_CLOCK_LIMIT’."
   exit 1
fi


module purge; module load K80 impi/2018.1 mkl/2018.1 cuda/8.0 CUDNN/7.0.3 python/3.6.3_ML


JOB_NAME=$(basename "$JOB_CONFIG" .yaml)
DATE_TIME=$(date +"%Y%m%dT%H%M%S")

cat > jobs/minotauro_job.cmd <<CMD_FILE
#!/bin/bash
# @ job_name= $JOB_NAME
# @ initialdir= .
# @ output= slurm/$DATE_TIME-$JOB_NAME-%j.out
# @ error= slurm/$DATE_TIME-$JOB_NAME-%j.err
# @ total_tasks= $TOTAL_TASKS
# @ cpus_per_task= $CPUS_PER_TASK
# @ gpus_per_node= $GPUS_PER_NODE
# @ wall_clock_limit = $WALL_CLOCK_LIMIT
srun python3 -m app.cli compute -j $JOB_CONFIG
CMD_FILE

mnsubmit jobs/minotauro_job.cmd
