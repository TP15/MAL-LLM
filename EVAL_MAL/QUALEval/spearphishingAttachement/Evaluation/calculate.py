import json

def calculate_evaluation_metrics(file_path):
    """
    Calculates evaluation metrics based on the provided JSON file.

    The JSON file is expected to have the following structure:
    {
        "matched_aspects": [
            {"reference_aspect_id": 0, "generated_aspect_id": 2, "confidence_score": 0.95, ...},
            ...
        ],
        "unmatched_aspects_list_a": [
            {"id": 6, ...},
            ...
        ],
        "unmatched_aspects_list_b": [
            {"id": 0, ...},
            ...
        ]
    }

    Metrics calculated:
    - Number of matched aspects
    - Number of unmatched aspects in list A (assumed reference)
    - Number of unmatched aspects in list B (assumed generated)
    - Precision
    - Recall
    - F1-score
    - Average confidence score for matched aspects
    """
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: The file {file_path} is not a valid JSON file.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while reading the file: {e}")
        return None

    matched_aspects = data.get("matched_aspects", [])
    unmatched_aspects_list_a = data.get("unmatched_aspects_list_a", [])
    unmatched_aspects_list_b = data.get("unmatched_aspects_list_b", [])

    num_matched_aspects = len(matched_aspects)
    num_unmatched_a = len(unmatched_aspects_list_a)
    num_unmatched_b = len(unmatched_aspects_list_b)

    # True Positives (TP) = Number of matched aspects
    tp = num_matched_aspects
    # False Negatives (FN) = Number of unmatched aspects in list A (ground truth aspects not found in generated)
    fn = num_unmatched_a
    # False Positives (FP) = Number of unmatched aspects in list B (generated aspects not found in ground truth)
    fp = num_unmatched_b

    # Precision = TP / (TP + FP)
    if (tp + fp) == 0:
        precision = 0.0
    else:
        precision = tp / (tp + fp)

    # Recall = TP / (TP + FN)
    if (tp + fn) == 0:
        recall = 0.0
    else:
        recall = tp / (tp + fn)

    # F1-score = 2 * (Precision * Recall) / (Precision + Recall)
    if (precision + recall) == 0:
        f1_score = 0.0
    else:
        f1_score = 2 * (precision * recall) / (precision + recall)

    total_confidence_score = 0
    num_confidence_scores = 0
    for aspect in matched_aspects:
        if "confidence_score" in aspect:
            total_confidence_score += aspect["confidence_score"]
            num_confidence_scores += 1

    if num_confidence_scores == 0:
        avg_confidence_score = 0.0
    else:
        avg_confidence_score = total_confidence_score / num_confidence_scores

    metrics = {
        "Number of Matched Aspects (TP)": tp,
        "Number of Unmatched Aspects in List A (FN)": fn,
        "Number of Unmatched Aspects in List B (FP)": fp,
        "Precision": precision,
        "Recall": recall,
        "F1-Score": f1_score,
        "Average Confidence Score of Matched Aspects": avg_confidence_score
    }

    return metrics

if __name__ == "__main__":
    # Assuming 'Prompt3b_Result.json' is in the same directory as the script
    # If not, provide the full path to the file.
    file_path = '/Users/thomaspathe/Desktop/EVAL_MAL/QUALEval/spearphishingAttachement/Evaluation/Prompt3b_Result.json'
    evaluation_results = calculate_evaluation_metrics(file_path)

    if evaluation_results:
        print("\nEvaluation Metrics:")
        for metric_name, metric_value in evaluation_results.items():
            print(f"- {metric_name}: {metric_value:.4f}" if isinstance(metric_value, float) else f"- {metric_name}: {metric_value}")

        print("\nNote:")
        print("List A is assumed to be the reference/ground truth.")
        print("List B is assumed to be the generated/predicted output.")
        print("Precision = TP / (TP + FP)")
        print("Recall = TP / (TP + FN)")
        print("F1-Score = 2 * (Precision * Recall) / (Precision + Recall)")