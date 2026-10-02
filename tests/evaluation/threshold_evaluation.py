from pathlib import Path

from src.config.settings import (
    TOP_K_RESULTS,
)
from src.retriever.document_retriever import retrieve_candidates
from src.reranker.cross_encoder_reranker import CrossEncoderReranker
from tests.evaluation.retrieval_questions import (
    EVALUATION_QUESTIONS,
)


THRESHOLDS = [
    0.0001,
    0.001,
    0.003,
    0.005,
    0.010,
    0.020,
    0.030,
    0.040,
]


reranker = CrossEncoderReranker()


def normalize_source(source: str) -> str:
    return Path(source).name


def evaluate_question(
    case: dict,
    threshold: float,
) -> dict:

    candidates = retrieve_candidates(
        query=case["question"],
        k=TOP_K_RESULTS,
    )

    ranked_results = reranker.rerank(
        query=case["question"],
        candidates=candidates,
        top_n=TOP_K_RESULTS,
    )

    filtered_results = [
        result
        for result in ranked_results
        if (
            result.rerank_score is not None
            and result.rerank_score >= threshold
        )
    ]

    retrieved_sources = {
        normalize_source(
            result.document.metadata.get(
                "source",
                "",
            )
        )
        for result in filtered_results
    }

    expected_sources = {
        normalize_source(source)
        for source in case["expected_sources"]
    }

    should_retrieve = case["should_retrieve"]

    if should_retrieve:
        passed = bool(
            retrieved_sources & expected_sources
        )
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
        retrieved = len(
            result["retrieved_sources"]
        ) > 0

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

    accuracy = (
        true_positive + true_negative
    ) / total

    return {
        "threshold": threshold,
        "true_positive": true_positive,
        "true_negative": true_negative,
        "false_positive": false_positive,
        "false_negative": false_negative,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }


if __name__ == "__main__":

    results = []

    for threshold in THRESHOLDS:
        result = evaluate_threshold(
            threshold
        )

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
            f"{result['threshold']:<12.4f}"
            f"{result['accuracy']:<12.2%}"
            f"{result['precision']:<12.2%}"
            f"{result['recall']:<12.2%}"
            f"{result['f1']:<12.2%}"
        )