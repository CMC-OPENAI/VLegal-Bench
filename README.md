# VLegal-Bench

A comprehensive Vietnamese legal benchmark dataset for evaluating Large Language Models (LLMs) on various legal NLP tasks.

## 📋 Table of Contents

- [Overview](#overview)
- [Dataset Structure](#dataset-structure)
- [Task Categories](#task-categories)
- [Installation](#installation)
- [Usage](#usage)
- [Evaluation](#evaluation)

---

## 🎯 Overview

This benchmark contains 22 legal tasks organized into 5 main categories, covering key aspects of legal language understanding and generation in Vietnamese. Task 5.3 is divided into 2 subtasks with separate folders. Each task folder contains:
- **Dataset file(s)**: `.jsonl` format containing questions and ground truth answers
- **Prompt file**: `prompt_X_Y.py` defining the evaluation prompt and format, with `X.Y` is task id defined below.

---

## 📁 Dataset Structure

```
vlegal-bench/
├── 1.1/  # Legal Entity Recognition
│   ├── 1_1.jsonl
│   └── prompt_1_1.py
├── 1.2/  # Legal Topic Classification
├── 1.3/  # Legal Concept Recall
├── 1.4/  # Article Recall
├── 1.5/  # Legal Schema Recall
├── 2.1/  # Relation Extraction
├── 2.2/  # Legal Element Recognition
├── 2.3/  # Legal Graph Structuring
├── 2.4/  # Judgement Verification
├── 2.5/  # User Intent Understanding
├── 3.1/  # Article/Clause Prediction
├── 3.2/  # Legal Court Decision Prediction
├── 3.3/  # Multi-hop Graph Reasoning 
├── 3.4/  # Conflict & Consistency Detection 
├── 3.5/  # Penalty / Remedy Estimation
├── 4.1/  # Legal Document Summarization
├── 4.2/  # Judicial Reasoning Generation
├── 4.3/  # Object Legal Opinion Generation
├── 5.1/  # Bias Detection
├── 5.2/  # Privacy & Data Protection
├── 5.3/  # Ethical Consistency Assessment
└── 5.4/  # Unfair Contract Detection 
```

---

## 📚 Task Categories

### Category 1: Recognition & Recall
- **1.1**: Legal Entity Recognition 
- **1.2**: Legal Topic Classification
- **1.3**: Legal Concept Recall
- **1.4**: Article Recall
- **1.5**: Legal Schema Recall

### Category 2: Understanding & Structuring
- **2.1**: Relation Extraction
- **2.2**: Legal Element Recognition
- **2.3**: Legal Graph Structuring
- **2.4**: Judgement Verification
- **2.5**: User Intent Understanding

### Category 3: Reasoning & Inference
- **3.1**: Article/Clause Prediction
- **3.2**: Legal Court Decision Prediction
- **3.3**: Multi-hop Graph Reasoning
- **3.4**: Conflict & Consistency Detection
- **3.5**: Penalty / Remedy Estimation

### Category 4: Interpretation & Generation
- **4.1**: Legal Document Summarization
- **4.2**: Judicial Reasoning Generation
- **4.3**: Object Legal Opinion Generation

### Category 5: Ethics, Fairness & Bias
- **5.1**: Bias Detection
- **5.2**: Privacy & Data Protection
- **5.3**: Ethical Consistency Assessment
- **5.4**: Unfair Contract Detection

---

## 🛠️ Installation

### Environment Setup

```bash
pip install uv
uv venv .venv 
source .venv/bin/activate
uv sync
```

### Configure Environment Variables

Create your own .env file according to .env_example

---

## 🚀 Usage

### Option 1: Using Local VLLM Server

1. **Start VLLM Server**

```bash
# Edit MODEL_NAME in vllm_serving.sh
bash vllm_serving.sh
```

2. **Run Inference**

```bash
# Edit TASK variable in infer.sh (e.g., TASK="1.1")
bash infer.sh

# For tasks with remove_content variant (3.3, 3.4)
USE_REMOVE_CONTENT=true bash infer.sh
```

### Option 2: Using API Models (GPT, Gemini, Claude)

```bash
# For standard tasks
bash infer.sh

# For tasks with remove_content variant (3.3, 3.4)
USE_REMOVE_CONTENT=true bash infer.sh
```

### Configuration Parameters

Edit the following variables in `infer.sh`:
- `TASK`: Task number (e.g., "1.1", "3.3", "4.1")
- `MODEL_NAME`: Model to use (e.g., "gpt-4o", "gemini-2.5-flash")
- `BATCH_SIZE`: Number of samples per batch (default: 1)
- `MAX_MODEL_LEN`: Maximum context length (default: 32768)
- `USE_REMOVE_CONTENT`: Use content-removed dataset variant (true/false)

---

## 📊 Evaluation

The evaluation is automatically performed after inference. Metrics vary by task type:

### Multiple Choice Tasks (1.x, 2.x, 3.x, 5.x)
- **Accuracy**
- **Precision**
- **Recall**
- **F1-Score**

### Generation Tasks (4.x)
- **BLEU Score**
- **ROUGE Score**

Results are saved in:
```
./<task>/<task>_llm_test_results_<model_name>.json
```

### Manual Evaluation

To evaluate existing prediction files:

```python
from src.evaluation import Metrics

metrics = Metrics(result_path="./1.1/1_1_llm_test_results_model_name.json")
results = metrics.eval()
print(results)
```


## 🤝 Contributing

When adding new tasks or modifying existing ones:
1. Maintain the folder structure `X.Y/`
2. Include both dataset (`.jsonl`) and prompt (`prompt_X_Y.py`) files
3. Update this README with task description
4. Test with the evaluation pipeline

---

## 📄 License

Please refer to the repository license for usage terms and conditions.

---

## 📧 Contact

For questions or issues, please open an issue in the repository or contact the maintainers.

## 📧 Citation

```
@misc{dong2025vlegalbenchcognitivelygroundedbenchmark,
      title={VLegal-Bench: Cognitively Grounded Benchmark for Vietnamese Legal Reasoning of Large Language Models}, 
      author={Nguyen Tien Dong and Minh-Anh Nguyen and Thanh Dat Hoang and Nguyen Tuan Ngoc and Dao Xuan Quang Minh and Phan Phi Hai and Nguyen Thi Ngoc Anh and Dang Van Tu and Binh Vu},
      year={2025},
      eprint={2512.14554},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2512.14554}, 
}
```
