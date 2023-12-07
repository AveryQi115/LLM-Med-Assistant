#!/bin/bash

# Define the command to be executed in the loop

command="torchrun --nproc_per_node 1 extract/process_prompt.py $1 \
    --ckpt_dir /home/yifengw2/llama-2/llama/llama-2-7b-chat/ \
    --tokenizer_path /home/yifengw2/llama-2/llama/tokenizer.model \
    --max_seq_len 4096 --max_batch_size 4"

$command