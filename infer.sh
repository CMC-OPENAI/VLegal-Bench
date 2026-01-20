#!/bin/bash

# ===== CONFIG =====
TASK="3.4"
TASK_FILE="${TASK//./_}"
BATCH_SIZE=1
MODEL_NAME="gemini-2.5-flash-lite"
MAX_MODEL_LEN=32768

# === New option — default false ===
USE_REMOVE_CONTENT=${USE_REMOVE_CONTENT:-false}

# ===== FILE MATCHING =====
verified_no_remove=($(ls ./${TASK}/${TASK_FILE}*verified_reformatted.jsonl 2>/dev/null | grep -v "remove_content"))
verified_remove=($(ls ./${TASK}/${TASK_FILE}*remove_content_verified_reformatted.jsonl 2>/dev/null))
no_verified=($(ls ./${TASK}/${TASK_FILE}*reformatted.jsonl 2>/dev/null | grep -v "remove_content"))

# ===== SELECT DATASET =====
if [ "$USE_REMOVE_CONTENT" = true ]; then
    echo "[INFO] USE_REMOVE_CONTENT=true → ưu tiên file remove_content"
    if [ -f "${verified_remove[0]}" ]; then
        DATASET_FILE="${verified_remove[0]}"
    else
        echo "[WARN] Không tìm thấy file remove_content, fallback sang file thường."
        DATASET_FILE="${verified_no_remove[0]}"
    fi
else
    echo "[INFO] USE_REMOVE_CONTENT=false → ưu tiên file không remove_content"
    if [ -f "${verified_no_remove[0]}" ]; then
        DATASET_FILE="${verified_no_remove[0]}"
    else
        echo "[WARN] Không có file thường, dùng file normal."
        DATASET_FILE="${no_verified[0]}"
    fi
fi

echo "[INFO] Using dataset: $DATASET_FILE"

# ===== RUN LOCAL LLM =====
python inference.py \
       --dataset_path "$DATASET_FILE" \
       --model_name "$MODEL_NAME" \
       --max_model_len "$MAX_MODEL_LEN" \
       --batch_size "$BATCH_SIZE" \