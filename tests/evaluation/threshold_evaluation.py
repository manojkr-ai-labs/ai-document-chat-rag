from pathlib import Path

from src.config.settings import TOP_K_RESULTS
from src.retriever.document_retriever import retrieve_documents
from tests.evaluation.retrieval_questions import EVALUATION_QUESTIONS

 
THRESHOLDS = [
    0.95,
    0.98,
    1.00,
    1.02,
    1.05,
    1.08,
    1.10,
]


def evaluate_question(case: dict, threshold: float) -> dict:
    documents = retrieve_documents(
        case["question"],
        k=TOP_K_RESULTS,
        threshold=threshold,
    )

    retrieved_sources = {
        Path(
            document.metadata.get("source", "")
        ).name
        for document in documents
    }

    expected_source = case["expected_source"]
    should_retrieve = case["should_retrieve"]

    if should_retrieve:
        passed = expected_source in retrieved_sources
    else:
        passed = len(retrieved_sources) == 0

    return {
        "passed": passed,
        "should_retrieve": should_retrieve,
        "retrieved_sources": retrieved_sources,
    }

def evaluate_threshold(threshold: float):
    print(f"\nThreshold: {threshold}")
    print("=" * 60)

    true_positive = 0
    true_negative = 0
    false_positive = 0
    false_negative = 0

    for case in EVALUATION_QUESTIONS:
        result = evaluate_question(
            case,
            threshold,
        )

        should_retrieve = result["should_retrieve"]
        retrieved = len(result["retrieved_sources"]) > 0

        if should_retrieve and retrieved:
            true_positive += 1
            status = "TP"

        elif not should_retrieve and not retrieved:
            true_negative += 1
            status = "TN"

        elif not should_retrieve and retrieved:
            false_positive += 1
            status = "FP"

        else:
            false_negative += 1
            status = "FN"

        print(
            f"{status} | "
            f"{case['question']}"
        )

   
    total = len(EVALUATION_QUESTIONS)

    precision = (
        true_positive
        / (true_positive + false_positive)
        if true_positive + false_positive
        else 0
    )

    recall = (
        true_positive
        / (true_positive + false_negative)
        if true_positive + false_negative
        else 0
    )

    f1 = (
        2 * precision * recall
        / (precision + recall)
        if precision + recall
        else 0
    )

    return {
        "threshold": threshold,
        "true_positive": true_positive,
        "true_negative": true_negative,
        "false_positive": false_positive,
        "false_negative": false_negative,
        "accuracy": (true_positive + true_negative) / total,
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }


        
if __name__ == "__main__":
    results = []

    for threshold in THRESHOLDS:
        result = evaluate_threshold(threshold)
        results.append(result)

    print()
    print(
        f"{'Threshold':<12}"
        f"{'Accuracy':<12}"
        f"{'Precision':<12}"
        f"{'Recall':<12}"
        f"{'F1':<12}"
    )

    print("-" * 60)

    for result in results:
        print(
            f"{result['threshold']:<12}"
            f"{result['accuracy']:<12.2%}"
            f"{result['precision']:<12.2%}"
            f"{result['recall']:<12.2%}"
            f"{result['f1']:<12.2%}"
        )