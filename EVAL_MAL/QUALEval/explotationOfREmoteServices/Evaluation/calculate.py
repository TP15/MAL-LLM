import json

def calculate_metrics_from_json(file_path):
    """
    Calculates precision, recall, and F1-score from a JSON file
    containing matched and unmatched aspects.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict: A dictionary containing precision, recall, and F1-score.
              Returns None if the file cannot be processed or if
              necessary keys are missing.
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
        print("Error: JSON content is not a dictionary.")
        return None

    matched_aspects = data.get('matched_aspects')
    unmatched_aspects_list_a = data.get('unmatched_aspects_list_a') # Assuming List A is reference/ground truth
    unmatched_aspects_list_b = data.get('unmatched_aspects_list_b') # Assuming List B is the generated output

    if matched_aspects is None or unmatched_aspects_list_a is None or unmatched_aspects_list_b is None:
        print("Error: One or more required keys ('matched_aspects', 'unmatched_aspects_list_a', 'unmatched_aspects_list_b') are missing from the JSON file.")
        return None

    if not isinstance(matched_aspects, list) or \
       not isinstance(unmatched_aspects_list_a, list) or \
       not isinstance(unmatched_aspects_list_b, list):
        print("Error: 'matched_aspects', 'unmatched_aspects_list_a', or 'unmatched_aspects_list_b' is not a list.")
        return None

    true_positives = len(matched_aspects)
    false_negatives = len(unmatched_aspects_list_a) # Aspects in reference but not matched in generated
    false_positives = len(unmatched_aspects_list_b) # Aspects in generated but not matched in reference

    print(f"True Positives (TP): {true_positives}")
    print(f"False Negatives (FN): {false_negatives}")
    print(f"False Positives (FP): {false_positives}")

    # Calculate Precision
    if (true_positives + false_positives) == 0:
        precision = 0.0
        print("Warning: (TP + FP) is zero, setting precision to 0.0")
    else:
        precision = true_positives / (true_positives + false_positives)

    # Calculate Recall
    if (true_positives + false_negatives) == 0:
        recall = 0.0
        print("Warning: (TP + FN) is zero, setting recall to 0.0")
    else:
        recall = true_positives / (true_positives + false_negatives)

    # Calculate F1-Score
    if (precision + recall) == 0:
        f1_score = 0.0
        print("Warning: (Precision + Recall) is zero, setting F1-score to 0.0")
    else:
        f1_score = 2 * (precision * recall) / (precision + recall)

    metrics = {
        'precision': precision,
        'recall': recall,
        'f1_score': f1_score
    }

    return metrics

if __name__ == '__main__':
    # Assuming the JSON file "Prompt3b_Result.json" is in the same directory as the script
    file_name = "/Users/thomaspathe/Desktop/EVAL_MAL/QUALEval/explotationOfREmoteServices/Evaluation/Prompt3b_Result.json"
    
    print(f"Calculating metrics from: {file_name}\n")
    
    calculated_metrics = calculate_metrics_from_json(file_name)

    if calculated_metrics:
        print("\nCalculated Metrics:")
        print(f"  Precision: {calculated_metrics['precision']:.4f}")
        print(f"  Recall:    {calculated_metrics['recall']:.4f}")
        print(f"  F1-Score:  {calculated_metrics['f1_score']:.4f}")