import json

def calculate_evaluation_metrics(file_path):
    """
    Calculates evaluation metrics from a JSON file containing matched and unmatched aspects.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict: A dictionary containing the calculated metrics (Precision, Recall, F1-Score,
              Average Confidence Score, number of matched aspects,
              number of unmatched reference aspects, and number of unmatched generated aspects).
              Returns None if the file cannot be processed.
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

    matched_aspects = data.get("matched_aspects", [])
    unmatched_aspects_a = data.get("unmatched_aspects_a", [])  # Reference aspects not matched
    unmatched_aspects_b = data.get("unmatched_aspects_b", [])  # Generated aspects not matched

    num_matched = len(matched_aspects)
    num_unmatched_a = len(unmatched_aspects_a) # Corresponds to False Negatives for recall
    num_unmatched_b = len(unmatched_aspects_b) # Corresponds to False Positives for precision

    # Calculate Precision
    # Precision = TP / (TP + FP)
    # TP = num_matched
    # FP = num_unmatched_b (generated aspects that were not in reference)
    if (num_matched + num_unmatched_b) > 0:
        precision = num_matched / (num_matched + num_unmatched_b)
    else:
        precision = 0.0

    # Calculate Recall
    # Recall = TP / (TP + FN)
    # TP = num_matched
    # FN = num_unmatched_a (reference aspects that were not generated)
    if (num_matched + num_unmatched_a) > 0:
        recall = num_matched / (num_matched + num_unmatched_a)
    else:
        recall = 0.0

    # Calculate F1-Score
    if (precision + recall) > 0:
        f1_score = 2 * (precision * recall) / (precision + recall)
    else:
        f1_score = 0.0

    # Calculate Average Confidence Score
    total_confidence = 0
    if num_matched > 0:
        for aspect in matched_aspects:
            total_confidence += aspect.get("confidence_score", 0)
        average_confidence = total_confidence / num_matched
    else:
        average_confidence = 0.0

    metrics = {
        "num_matched_aspects": num_matched,
        "num_unmatched_reference_aspects (FN)": num_unmatched_a,
        "num_unmatched_generated_aspects (FP)": num_unmatched_b,
        "precision": precision,
        "recall": recall,
        "f1_score": f1_score,
        "average_confidence_score": average_confidence
    }

    return metrics

if __name__ == "__main__":
    # Assuming 'Prompt3b_Result.json' is in the same directory as the script
    file_to_evaluate = "/Users/thomaspathe/Desktop/EVAL_MAL/QUALEval/supplyChainCompromise/Evaluation/Prompt3b_Result.json"
    results = calculate_evaluation_metrics(file_to_evaluate)

    if results:
        print(f"\nEvaluation Metrics for: {file_to_evaluate}")
        print("--------------------------------------------------")
        print(f"Number of Matched Aspects: {results['num_matched_aspects']}")
        print(f"Number of Unmatched Reference Aspects (FN for Recall): {results['num_unmatched_reference_aspects (FN)']}")
        print(f"Number of Unmatched Generated Aspects (FP for Precision): {results['num_unmatched_generated_aspects (FP)']}")
        print(f"Precision: {results['precision']:.4f}")
        print(f"Recall: {results['recall']:.4f}")
        print(f"F1-Score: {results['f1_score']:.4f}")
        print(f"Average Confidence Score of Matched Aspects: {results['average_confidence_score']:.4f}")
        print("--------------------------------------------------")

        # Explanation based on the provided PDF (ExPerT framework)
        print("\nMetric Interpretation (based on common evaluation practices like in ExPerT [cite: 1]):")
        print("- Precision measures how many of the generated aspects (from 'Prompt3b_Result.json') are relevant (i.e., match reference aspects).")
        print("- Recall measures how many of the reference aspects were successfully identified or generated.")
        print("- F1-Score is the harmonic mean of Precision and Recall, providing a single score that balances both.")
        print("- The 'unmatched_aspects_a' in your JSON correspond to aspects in the reference that the generation missed (False Negatives in a typical IR sense).")
        print("- The 'unmatched_aspects_b' in your JSON correspond to aspects the generation produced but were not in the reference (False Positives).")