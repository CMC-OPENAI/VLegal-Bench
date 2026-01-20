import json
import re
import traceback
from typing import List, Dict, Tuple
import os
from rouge_score import rouge_scorer
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from openai import OpenAI
import ast
import logging
from collections import defaultdict

task_type_mapping = {
    '1_1': 'multiple_choices',
    '1_2': 'multiple_choices',
    '1_3': 'multiple_choices',
    '1_4': 'multiple_choices',
    '1_5': 'multiple_choices',
    '2_1': 'multiple_choices',
    '2_2': 'multiple_choices',
    '2_3': 'generation',
    '2_4': 'multiple_choices',
    '2_5': 'multiple_choices',
    '3_1': 'multiple_choices',
    '3_2': 'multiple_choices',
    '3_3': 'multiple_choices',
    '3_4': 'multiple_choices_imbalance',
    '3_5': 'multiple_choices',
    '4_1': 'generation',
    '4_2': 'generation',
    '4_3': 'generation',
    '5_1': 'multiple_choices',
    '5_2': 'multiple_choices',
    '5_3_legal_ethics_cases': 'multiple_choices',
    '5_3_law_vs_ethics': 'multiple_choices',
    '5_4': 'multiple_choices'
}
def parse_triplets(answer_text):
    """Parse the string response into a list of tuples
    
    Args:
        answer_text: String containing list of tuples in various formats
    
    Returns:
        List of tuples: [("entity1", "relation", "entity2"), ...]
    """
    # Handle None or empty input
    if not answer_text or (isinstance(answer_text, str) and not answer_text.strip()):
        logging.warning("Empty or None input provided to parse_triplets")
        return []
    
    # Convert to string if not already
    answer_text = str(answer_text)
    
    try:
        # Clean up newlines before attempting parse
        if "\n" in answer_text:
            answer_text = answer_text.replace("\n", " ")
        
        # First, try to parse using ast.literal_eval (for proper Python format)
        parsed = ast.literal_eval(answer_text)
        
        # Ensure it's a list of tuples
        if isinstance(parsed, list):
            result = []
            for item in parsed:
                if isinstance(item, tuple) and len(item) == 3:
                    result.append(item)
                elif isinstance(item, list) and len(item) == 3:
                    result.append(tuple(item))
                elif isinstance(item, str) and '+' in item:
                    # Handle "entity1 + relation + entity2" format
                    parts = [part.strip() for part in item.split('+')]
                    if len(parts) == 3:
                        result.append(tuple(parts))
            return result
        return []
        
    except (ValueError, SyntaxError, TypeError) as e:
        logging.warning(f"Failed to parse with ast.literal_eval: {e}. Trying fallback patterns...")
        
        # Fallback: Try to extract tuples from various formats
        try:
            # First, try to parse "entity1 + relation + entity2" format
            # Handle quoted format: "entity1 + relation + entity2"
            plus_pattern_quoted = r'["\']([^"\']+?)\s*\+\s*([^"\']+?)\s*\+\s*([^"\']+?)["\']'
            matches = re.findall(plus_pattern_quoted, answer_text)
            
            if matches:
                result = [tuple(item.strip() for item in match) for match in matches]
                logging.info(f"Parsed {len(result)} triplets using quoted plus-separated pattern")
                return result
            
            # Try without quotes for plus-separated format
            # This pattern looks for text + text + text where text doesn't contain special chars
            plus_pattern_unquoted = r'([^+,\[\]"\'\n]+?)\s*\+\s*([^+,\[\]"\'\n]+?)\s*\+\s*([^+,\[\]"\'\n]+?)(?=\s*[,\]\n]|$)'
            matches = re.findall(plus_pattern_unquoted, answer_text)
            
            if matches:
                result = [tuple(item.strip() for item in match) for match in matches]
                logging.info(f"Parsed {len(result)} triplets using unquoted plus-separated pattern")
                return result
            
            # Pattern to match standard tuple format: (text, text, text)
            # With or without surrounding list brackets
            pattern = r'\(\s*([^,)]+?)\s*,\s*([^,)]+?)\s*,\s*([^)]+?)\s*\)'
            matches = re.findall(pattern, answer_text)
            
            if matches:
                result = [tuple(item.strip().strip('"\'') for item in match) for match in matches]
                logging.info(f"Parsed {len(result)} triplets using standard tuple pattern")
                return result
            
            # Try pattern with double quotes
            pattern_quoted = r'\(\s*"([^"]+)"\s*,\s*"([^"]+)"\s*,\s*"([^"]+)"\s*\)'
            matches = re.findall(pattern_quoted, answer_text)
            
            if matches:
                result = [tuple(match) for match in matches]
                logging.info(f"Parsed {len(result)} triplets using double-quoted pattern")
                return result
            
            # Try pattern with single quotes
            pattern_single = r"\(\s*'([^']+)'\s*,\s*'([^']+)'\s*,\s*'([^']+)'\s*\)"
            matches = re.findall(pattern_single, answer_text)
            
            if matches:
                result = [tuple(match) for match in matches]
                logging.info(f"Parsed {len(result)} triplets using single-quoted pattern")
                return result
            
            # Last resort: Try to find any pattern with 3 elements separated by commas
            # This is very permissive and should be last
            simple_pattern = r'([^,\[\]()]+),\s*([^,\[\]()]+),\s*([^,\[\]()]+)'
            matches = re.findall(simple_pattern, answer_text)
            
            if matches:
                # Filter out matches that are too short or look invalid
                result = []
                for match in matches:
                    cleaned = tuple(item.strip().strip('"\'') for item in match)
                    # Validate that all parts have reasonable content
                    if all(len(part) > 0 for part in cleaned):
                        result.append(cleaned)
                
                if result:
                    logging.info(f"Parsed {len(result)} triplets using simple comma-separated pattern")
                    return result
            
            logging.error(f"No triplets found in response: {answer_text[:200]}...")
            return []
            
        except Exception as e:
            logging.error(f"Failed to parse triplets with fallback patterns: {e}")
            logging.debug(f"Problematic input: {answer_text[:200]}...")
            return []
class Prediction: 
    """
    Class to handle inference process and store predictions.
    """
    def __init__(self, data_file: str, reasoning: bool = False):
        """
        Initialize Prediction class with models and data file.
        Args:
            models (Dict[object, Tuple[str, str]]): List of model to use for inference. Need to specify 'type' (either 'api' or 'local_host') and 'name' for each model.
            data_file (str): Path to the JSONL file containing data for testing. Each data entry should contain 'instruction' and 'ground_truth' fields. Other fields depend on the specific task.
        """
        self.data_file = data_file
        self.data = []
        # Open and read the JSONL file
        with open(self.data_file, 'r', encoding='utf-8') as f:
            self.data.extend([json.loads(line) for line in f.readlines()])
        file_name = os.path.basename(self.data_file)
        self.task = "_".join(file_name.split("_")[:2])
        print(self.task)
        if self.task == "5_3":
            if "legal_ethics_cases" in file_name:
                self.task = "5_3_legal_ethics_cases"
            elif "law_vs_ethics" in file_name:
                self.task = "5_3_law_vs_ethics"
        print(f"Loaded {len(self.data)} entries for task {self.task}")
        
        self.reasoning = reasoning
        print(f"Reasoning set to {self.reasoning}")
    
    def preprocess_input(self, input_data: Dict) -> Tuple[str, str]:
        """
        Preprocess input data before feeding into the model. For each task, need to customized this method.
        Args:
            input_data (Dict): A single data entry from the dataset.
        Returns:
            Tuple[str, str]: Preprocessed input string for the model and the ground truth answer.
        """
        if self.task in ["1_1", "1_2", "1_3", "1_4", "1_5", "2_1", "2_2", "2_5", "3_1", "3_5", "5_1", "5_2", "5_3_legal_ethics_cases", "5_3_law_vs_ethics", "5_4"]:
            instruction = input_data['instruction'].lower()
            question = input_data['question']
            choices = input_data['answers']
            ground_truth = input_data['ground_truth']
            return f"{instruction}\n{question}\n{choices}", ground_truth
    
        elif self.task == "3_4": 
            instruction = input_data['instruction'].lower()
            question = input_data['question']
            ground_truth = input_data['ground_truth']
            return f"{instruction}\n{question}", ground_truth
        
        elif self.task == "2_3":
            instruction = input_data['instruction']
            document = input_data['document']
            ground_truth = input_data['answer']
            return f"{instruction}\n{document}", ground_truth
        
        elif self.task == "2_4":
            instruction = input_data['instruction']
            description = input_data['description']
            court_judgement = input_data['court_judgement']
            ground_truth = input_data['ground_truth']
            return f"{instruction}\n{description}\n{court_judgement}", ground_truth
        
        elif self.task == "3_2": 
            instruction = input_data['instruction']
            description = input_data['description']
            choices = input_data['answers']
            ground_truth = input_data['ground_truth']
            return f"{instruction}\n{description}\n{choices}", ground_truth
        
        elif self.task == "3_3":
            instruction = input_data['instruction']
            question = input_data['question']
            choices = input_data['answers']
            ground_truth = input_data['ground_truth']
            return f"{instruction}\n{question}\n{choices}", ground_truth
        
        elif self.task == "4_1":
            instruction = input_data['instruction']
            content = input_data['content']
            ground_truth = input_data['ground_truth']
            return f"{instruction}\n{content}", ground_truth
        
        elif self.task in ["4_3", "4_2"]:
            instruction = input_data['instruction']
            question = input_data['question']
            ground_truth = input_data['answer']
            return f"{instruction}\n{question}", ground_truth        
    
    def parse_output(self, raw_output: str) -> str:
        """
        Parse raw model output to extract the final answer. For each task, need to customized this method.
        Args:
            raw_output (str): Raw output string from the model.
        Returns:
            str: Parsed final answer.
        """
        if self.task in ["1_1", "1_3", "1_4", "1_5", "2_1", "2_2", "3_1", "3_2", "3_3", "3_5", "5_1", "5_2", "5_3_legal_ethics_cases", "5_3_law_vs_ethics", "5_4"]: 
            # Validate: must be exactly A, B, C, or D
            if raw_output.upper() in ['A', 'B', 'C', 'D']:
                return raw_output.upper()
            
            # Try to extract if response contains other text
            match = re.search(r'\b([ABCD])\b', raw_output, re.IGNORECASE)
            if match:
                extracted = match.group(1).upper()
                logging.warning(f"Extracted '{extracted}' from response: {raw_output}")
                return extracted
        
        elif self.task == "1_2": 
            # Validate: must be exactly A, B, C, D, E, or F
            if raw_output.upper() in ['A', 'B', 'C', 'D', 'E', 'F']:
                return raw_output.upper()
            
            # Try to extract if response contains other text
            match = re.search(r'\b([ABCDEF])\b', raw_output, re.IGNORECASE)
            if match:
                extracted = match.group(1).upper()
                logging.warning(f"Extracted '{extracted}' from response: {raw_output}")
                return extracted
            
        elif self.task == "2_3": 
            # Parse the response into list of tuples
            parsed_answer = parse_triplets(raw_output)
            if not parsed_answer:
                logging.warning(f"No valid triplets parsed from response: {raw_output}")
                return None
            return parsed_answer
        
        elif self.task == "2_4":
            # Validate: must be exactly Đúng or Sai
            if raw_output.upper() in ['ĐÚNG', 'SAI']:
                return raw_output.capitalize()
            
            # Try to extract if response contains other text
            match = re.search(r'\b(Đúng|Sai)\b', raw_output, re.IGNORECASE)
            if match:
                extracted = match.group(1).capitalize()
                logging.warning(f"Extracted '{extracted}' from response: {raw_output}")
                return extracted
        
        elif self.task == "3_4": 
            # Validate: must be exactly CÓ or KHÔNG
            if raw_output.upper() in ['CÓ', 'KHÔNG']:
                return raw_output.capitalize()
            
            # Try to extract if response contains other text
            match = re.search(r'\b(Có|Không)\b', raw_output, re.IGNORECASE)
            if match:
                extracted = match.group(1).capitalize()
                logging.warning(f"Extracted '{extracted}' from response: {raw_output}")
                return extracted
        
        elif self.task == "2_5": 
            # Validate: must be combination of A, B, C, or D
            if all(char in ['A', 'B', 'C', 'D', ',',' ', '[', ' ]'] for char in raw_output.upper()):
                return raw_output.upper().strip("[]").split(",")
            # Try to extract if response contains other text
            matches = re.findall(r'\b([ABCD])\b', raw_output, re.IGNORECASE)
            if matches:
                extracted = [m.upper() for m in matches]
                logging.warning(f"Extracted '{extracted}' from response: {raw_output}")
                return extracted
        elif self.task in ["4_1", "4_3", "4_2"]:
            return raw_output.strip()
    
    def parse_output_with_reasoning(self, raw_output: str, max_retries: int=3) -> str: 
        """
        Parse raw model output to extract the final answer (with reasoning). For each task, need to customized this method.
        Args:
            raw_output (str): Raw output string from the model.
        Returns:
            str: Parsed final answer.
        """
        for attempt in range(max_retries):
            # Extract content within <output> ... </output>. 
            try:
                match = re.search(r'<output>(.*?)</output>', raw_output, re.DOTALL | re.IGNORECASE)
                if match:
                    extracted = match.group(1).capitalize()
                    logging.warning(f"Extracted '{extracted}' from response: {raw_output}")
                    return self.parse_output(extracted)
                else: 
                    logging.warning(f"Attempt {attempt + 1}: Could not find <output> tags in response, retrying...")
            except Exception as e:
                logging.error(f"Attempt {attempt + 1} failed: {str(e)}")
        logging.error(f"Fail to parse output after {max_retries} attempts")
        return None

    def parse_thinking(self, raw_output: str, max_retries: int=3) -> str: 
        """
        Parse raw model output to extract the final answer (with reasoning). For each task, need to customized this method.
        Args:
            raw_output (str): Raw output string from the model.
        Returns:
            str: Parsed final answer.
        """
        for attempt in range(max_retries):
            # Extract content within <output> ... </output>. 
            try:
                match = re.search(r'<think>(.*?)</think>', raw_output, re.DOTALL | re.IGNORECASE)
                if match:
                    extracted = match.group(1).capitalize()
                    logging.warning(f"Extracted thinking: '{extracted}' from response: {raw_output}")
                    return extracted
                else: 
                    logging.warning(f"Attempt {attempt + 1}: Could not find <think> tags in response, retrying...")
            except Exception as e:
                logging.error(f"Attempt {attempt + 1} failed: {str(e)}")
        logging.error(f"Fail to parse thinking after {max_retries} attempts")
        return None
    
    def get_few_shot_examples(self, k: int = 3) -> List[Dict]:
        """
        Get k few-shot examples and gather them together.
        Args:
            k (int): Number of few-shot examples to retrieve.
        Returns:
            List[Dict]: A list of few-shot examples.
        """
        return self.data[:k]
    
    def export_predictions(self, predictions: Dict[str, List[str]], output_dir: str = "./predictions"):
        """
        Export predictions to JSONL files, one for each model.
        Args:
            predictions (Dict[str, List[str]]): A dictionary mapping model names to their list of predictions.
            output_dir (str): Directory to save the prediction files.
        """
        os.makedirs(output_dir, exist_ok=True)
        for model_name, preds in predictions.items():
            output_file = os.path.join(output_dir, f"{self.task}_{model_name}_predictions.jsonl")
            with open(output_file, 'w', encoding='utf-8') as f:
                for pred in preds:
                    f.write(json.dumps(pred, ensure_ascii=False) + "\n")
    
class Metrics: 
    """
    Class to compute evaluation metrics for model predictions.
    With multiple choices task: accuracy, precision, recall, f1-score.
    With generative task: BLEU, ROUGE.
    """
    def __init__(self, result_path: str):
        """
        Initialize Metrics class with the path to the result file.
        Args:
            result_path (str): Path to the JSONL file containing model predictions and references. The JSONL file should contains entries with 'prediction' and 'ground_truth' fields.
        """
        self.result_path = result_path
        self.data = []
        # Open and read the JSONL file
        with open(self.result_path, 'r', encoding='utf-8') as f:
            self.data.extend([json.loads(line) for line in f.readlines()])
        # Check if data contains essential fields
        assert all('prediction' in item and 'ground_truth' in item for item in self.data), "Each entry must contain 'prediction' and 'ground_truth' fields."
        # Check for task type 
        file_name = os.path.basename(self.result_path)
        task = "_".join(file_name.split("_")[:2])
        if task == "5_3":
            if "legal_ethics_cases" in file_name:
                task = "5_3_legal_ethics_cases"
            elif "law_vs_ethics" in file_name:
                task = "5_3_law_vs_ethics"
        assert task in task_type_mapping, f"Task {task} not recognized in task_type_mapping. Please rename the result file in format <task>_results.jsonl"
        self.task_type = task_type_mapping[task]
        print(f"Detected task type: {self.task_type}")
        if self.task_type == 'multiple_choices':
            self.metrics = ['accuracy', 'precision', 'recall', 'f1-score']
        elif self.task_type == 'generation':
            self.metrics = ['BLEU', 'ROUGE']
        elif self.task_type == "multiple_choices_imbalance":
            self.metrics = ['Macro-F1']

    def calculate_accuracy(self) -> float:
        """
        Calculate accuracy for both:
        - single-choice questions (e.g., "A")
        - multi-multiple-choice questions (e.g., ["A", "C"])

        A prediction is correct if the sets match exactly.
        """
        def normalize(x):
            """Normalize answers into a set of uppercase option letters."""
            if isinstance(x, list):
                return {str(i).strip().upper() for i in x}

            if isinstance(x, str):
                # Remove punctuation and split by space/comma
                cleaned = (
                    x.replace(",", " ")
                    .replace("[", " ")
                    .replace("]", " ")
                    .replace("'", " ")
                    .replace('"', " ")
                    .strip()
                    .upper()
                )
                parts = cleaned.split()

                # If user writes "AC" with no spaces → treat as characters
                if len(parts) == 1 and len(parts[0]) > 1:
                    return set(parts[0])  # e.g., "AC" → {"A","C"}

                return set(parts)  # "A C" → {"A", "C"}

            return set()  # default fallback

        correct = 0

        for item in self.data:
            pred = normalize(item.get("prediction", ""))
            truth = normalize(item.get("ground_truth", ""))

            if pred == truth:
                correct += 1

        total = len(self.data)
        return correct / total if total > 0 else 0.0
    
    def calculate_precision(self) -> float:
        """
        Calculate precision for multiple choices task.
        Returns:
            float: Precision score.
        """
        res = 0.0
        total_predicted_positives = 0
        for item in self.data:
            ground_truth = item['ground_truth'] if isinstance(item['ground_truth'], list) else [item['ground_truth']]
            prediction = item['prediction'] if isinstance(item['prediction'], list) else [item['prediction']]
            hyp_set = set([h.strip() for h in prediction])
            ref_set = set([str(r).strip() for r in ground_truth])
            print(ref_set)
            true_positives = len(hyp_set.intersection(ref_set))
            predicted_positives = len(hyp_set)
            if predicted_positives == 0:
                continue
            res += true_positives / predicted_positives
            total_predicted_positives += 1
        return res / total_predicted_positives if total_predicted_positives > 0 else 0.0
    
    def calculate_recall(self) -> float:
        """
        Calculate recall for multiple choices task.
        Returns:
            float: Recall score.
        """
        res = 0.0
        total_actual_positives = 0
        for item in self.data:
            ground_truth = item['ground_truth'] if isinstance(item['ground_truth'], list) else [item['ground_truth']]
            prediction = item['prediction'] if isinstance(item['prediction'], list) else [item['prediction']]
            hyp_set = set([h.strip() for h in prediction])
            ref_set = set([str(r).strip() for r in ground_truth])
            
            true_positives = len(hyp_set.intersection(ref_set))
            actual_positives = len(ref_set)
            if actual_positives == 0:
                continue
            res += true_positives / actual_positives
            total_actual_positives += 1
        return res / total_actual_positives if total_actual_positives > 0 else 0.0
    def calculate_f1_score(self) -> float:
        """
        Calculate F1-score for multiple choices task.
        Returns:
            float: F1-score.
        """
        precision = self.calculate_precision()
        recall = self.calculate_recall()
        if precision + recall == 0:
            return 0.0
        return 2 * (precision * recall) / (precision + recall)

    def calculate_weighted_macro_f1_score(self) -> float:
        """
        Calculate weighted Macro-F1 score
        - class "không" has weight = 3
        - other classes have weight = 1
        """

        tp = defaultdict(int)
        fp = defaultdict(int)
        fn = defaultdict(int)

        # 1. Accumulate TP / FP / FN per class
        for item in self.data:
            # Normalize to capitalized strings
            ground_truth = [s.capitalize() for s in (item['ground_truth'] if isinstance(item['ground_truth'], list) else [item['ground_truth']])]
            prediction = [s.capitalize() for s in (item['prediction'] if isinstance(item['prediction'], list) else [item['prediction']])]
            ref_set = set(str(r).strip() for r in ground_truth)
            hyp_set = set(h.strip() for h in prediction)

            for label in hyp_set:
                if label in ref_set:
                    tp[label] += 1
                else:
                    fp[label] += 1

            for label in ref_set:
                if label not in hyp_set:
                    fn[label] += 1

        all_labels = set(tp.keys()) | set(fp.keys()) | set(fn.keys())
        
        map = dict()
        for label in all_labels:
            precision = tp[label] / (tp[label] + fp[label]) if (tp[label] + fp[label]) > 0 else 0.0
            recall = tp[label] / (tp[label] + fn[label]) if (tp[label] + fn[label]) > 0 else 0.0

            if precision + recall == 0:
                f1 = 0.0
            else:
                f1 = 2 * precision * recall / (precision + recall)
            map[label] = f1

        map = dict(sorted(map.items()))
        return map
        
    def calculate_bleu(self) -> float:
        """
        Calculate BLEU score for generative task.
        Returns:
            float: BLEU score.
        """
        total_bleu = 0.0
        smoothie = SmoothingFunction().method4
        for sample in self.data:
            reference = sample['ground_truth']
            candidate = sample['prediction']
            if isinstance(reference, list):
                reference = " ".join(" ".join(ref) if isinstance(ref, list) else ref for ref in reference)
            if isinstance(candidate, list):
                candidate = " ".join(" ".join(cand) if isinstance(cand, list) else cand for cand in candidate)
            # Tokenize (split by spaces)
            ref_tokens = reference.lower().split()
            cand_tokens = candidate.lower().split()
            bleu_score = sentence_bleu([ref_tokens], cand_tokens, smoothing_function=smoothie)
            total_bleu += bleu_score
        return total_bleu / len(self.data) if len(self.data) > 0 else 0.0
    def calculate_rouge(self) -> float:
        """
        Calculate ROUGE score for generative task.
        Returns:
            float: ROUGE score.
        """  
        total_f1 = 0.0      
        for sample in self.data:
            reference = sample['ground_truth']
            candidate = sample['prediction']
            if isinstance(reference, list):
                reference = " ".join(" ".join(ref) if isinstance(ref, list) else ref for ref in reference)
            if isinstance(candidate, list):
                candidate = " ".join(" ".join(cand) if isinstance(cand, list) else cand for cand in candidate)
            scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
            scores = scorer.score(reference.lower(), candidate.lower())
            f1_score = scores['rougeL'].fmeasure
            total_f1 += f1_score
        return total_f1 / len(self.data) if len(self.data) > 0 else 0.0
    def eval(self):
        """
        Interface for evaluation. Call eval methods for different metrics here.
        """
        results = {}
        if self.task_type == 'multiple_choices':
            results['accuracy'] = self.calculate_accuracy()
            results['precision'] = self.calculate_precision()
            results['recall'] = self.calculate_recall()
            results['f1-score'] = (2 * results['precision'] * results['recall']) / (results['precision'] + results['recall']) if (results['precision'] + results['recall']) > 0 else 0.0
        elif self.task_type == 'generation':
            results['BLEU'] = self.calculate_bleu()
            results['ROUGE'] = self.calculate_rouge()
        elif self.task_type == 'multiple_choices_imbalance':
            results['Macro-F1'] = self.calculate_weighted_macro_f1_score()
        return results

def main(): 
    test_dir = [
        "./1.1/1_1_legal_entity_recognition_dataset_reformatted.jsonl"
    ]
    for file in test_dir:
        predictor = Prediction(data_file=file)
        print(predictor.data)

if __name__ == "__main__":
    main()