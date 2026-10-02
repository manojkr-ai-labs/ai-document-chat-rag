from pathlib import Path

from src.config.settings import TOP_K_RESULTS
from src.config.settings import (
    RERANK_RELEVANCE_THRESHOLD,
    RERANK_TOP_N,
)
from src.retriever.document_retriever import retrieve_candidates
from src.reranker.cross_encoder_reranker import CrossEncoderReranker
from tests.evaluation.retrieval_questions import EVALUATION_QUESTIONS

 
RERANK_THRESHOLDS = [
    0.0001,
    0.0005,
    0.001,
    0.002,
    0.005,
    0.01,
]

def evaluate_question(
    case: dict,
    reranker: CrossEncoderReranker,
    threshold: float,
) -> dict:
    candidates = retrieve_candidates(
        case["question"],
        k=TOP_K_RESULTS,
    )

    ranked = reranker.rerank(
        case["question"],
        candidates,
        top_n=RERANK_TOP_N,
    )

    relevant_results = [
        result
        for result in ranked
        if result.rerank_score is not None
        and result.rerank_score >= threshold
    ]

    retrieved_sources = {
        Path(
            result.document.metadata.get("source", "")
        ).name
        for result in relevant_results
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

def evaluate_reranking():
    reranker = CrossEncoderReranker()

    total = len(EVALUATION_QUESTIONS)

    print("\n")
    print("Reranker Threshold Evaluation")
    print("=" * 75)

    print(
        f"{'Threshold':<12}"
        f"{'Accuracy':<12}"
        f"{'Precision':<12}"
        f"{'Recall':<12}"
        f"{'F1':<12}"
    )

    print("-" * 75)

    for threshold in RERANK_THRESHOLDS:
        true_positive = 0
        true_negative = 0
        false_positive = 0
        false_negative = 0

        print(f"\nThreshold: {threshold}")

        for case in EVALUATION_QUESTIONS:
            result = evaluate_question(
                case,
                reranker,
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

        accuracy = (
            (true_positive + true_negative) / total
            if total
            else 0
        )

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

        print("-" * 60)
        print(
            f"TP={true_positive} "
            f"TN={true_negative} "
            f"FP={false_positive} "
            f"FN={false_negative}"
        )

        print(
            f"Accuracy={accuracy:.2%} | "
            f"Precision={precision:.2%} | "
            f"Recall={recall:.2%} | "
            f"F1={f1:.2%}"
        )
if __name__ == "__main__":
    evaluate_reranking()