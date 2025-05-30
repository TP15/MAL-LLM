import json

def calculate_evaluation_metrics(file_path):
    """
    Calculates evaluation metrics (precision, recall, F1-score)
    from a JSON file containing matched and unmatched aspects.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict: A dictionary containing the calculated metrics.
              Returns None if the file cannot be processed or
              if essential data is missing.
    """
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {file_path}")
        return None

    if not isinstance(data, dict):
        print("Error: JSON data is not in the expected dictionary format.")
        return None

    matched_pairs = data.get("matched_pairs", [])
    unmatched_list_a = data.get("unmatched_list_a", [])
    unmatched_list_b = data.get("unmatched_list_b", [])

    if not isinstance(matched_pairs, list) or \
       not isinstance(unmatched_list_a, list) or \
       not isinstance(unmatched_list_b, list):
        print("Error: 'matched_pairs', 'unmatched_list_a', or 'unmatched_list_b' is not a list.")
        return None

    num_matched_pairs = len(matched_pairs)
    num_unmatched_a = len(unmatched_list_a)  # Corresponds to items only in the reference set
    num_unmatched_b = len(unmatched_list_b)  # Corresponds to items only in the generated set

    # --- Precision, Recall, and F1-Score Calculation ---
    # True Positives (TP) = Number of matched pairs
    # False Positives (FP) = Number of unmatched items in the generated list (unmatched_list_b)
    # False Negatives (FN) = Number of unmatched items in the reference list (unmatched_list_a)

    tp = num_matched_pairs
    fp = num_unmatched_b
    fn = num_unmatched_a

    if (tp + fp) == 0:
        precision = 0.0
        print("Warning: Precision cannot be calculated (TP + FP = 0). Setting to 0.")
    else:
        precision = tp / (tp + fp)

    if (tp + fn) == 0:
        recall = 0.0
        print("Warning: Recall cannot be calculated (TP + FN = 0). Setting to 0.")
    else:
        recall = tp / (tp + fn)

    if (precision + recall) == 0:
        f1_score = 0.0
        print("Warning: F1-score cannot be calculated (Precision + Recall = 0). Setting to 0.")
    else:
        f1_score = 2 * (precision * recall) / (precision + recall)

    results = {
        "num_matched_pairs": num_matched_pairs,
        "num_unmatched_reference (FN)": num_unmatched_a,
        "num_unmatched_generated (FP)": num_unmatched_b,
        "precision": precision,
        "recall": recall,
        "f1_score": f1_score
    }

    return results

# --- Main execution ---
# Replace 'Prompt3b_Result.json' with the actual path to your file if it's different.
file_path = '/Users/thomaspathe/Desktop/EVAL_MAL/QUALEval/DrivebyCompromise/Evaluation/Prompt3b_Result.json'
metrics = calculate_evaluation_metrics(file_path)

if metrics:
    print("\n--- Evaluation Metrics ---")
    print(f"Number of Matched Pairs (TP): {metrics['num_matched_pairs']}")
    print(f"Number of Unmatched Reference Items (FN): {metrics['num_unmatched_reference (FN)']}")
    print(f"Number of Unmatched Generated Items (FP): {metrics['num_unmatched_generated (FP)']}")
    print(f"Precision: {metrics['precision']:.4f}")
    print(f"Recall: {metrics['recall']:.4f}")
    print(f"F1-Score: {metrics['f1_score']:.4f}")