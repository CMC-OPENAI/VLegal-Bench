MODEL_NAME="SeaLLMs/SeaLLMs-v3-1.5B-Chat"
MAX_MODEL_LEN=18080

CUDA_VISIBLE_DEVICES=4 \
vllm serve \
    "$MODEL_NAME" \
    --port 8010 \
    --seed 42 \
    --gpu-memory-utilization 0.8 \
    --max-model-len "$MAX_MODEL_LEN" \
    --tensor_parallel_size 1 \
    --chat_template None \
    --max_num_seqs 256 \
    --tool-call-parser None \
    --trust-remote-code \
    --async-scheduling \
    # --disable-custom-kernels
    # --enable-auto-tool-choice \
    


    
