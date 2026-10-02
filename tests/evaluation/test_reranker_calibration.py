from pathlib import Path

from tests.evaluation.reranker_calibration_cases import (
    RERANKER_CALIBRATION_CASES,
)
from src.retriever.document_retriever import retrieve_candidates
from src.reranker.cross_encoder_reranker import CrossEncoderReranker


def normalize_source(source: str) -> str:
    return Path(source).name


def test_reranker_calibration():
    model = CrossEncoderReranker()

    relevant_scores = []
    irrelevant_scores = []

    print("\n" + "=" * 100)
    print("RERANKER PRODUCTION-PATH CALIBRATION")
    print("=" * 100)

    for case in RERANKER_CALIBRATION_CASES:
        candidates = retrieve_candidates(
            query=case["query"],
            k=5,
        )

        ranked_results = model.rerank(
            query=case["query"],
            candidates=candidates,
            top_n=None,
        )

        expected_source = normalize_source(
            case["source"]
        )

        print("\n" + "-" * 100)
        print(f"Question: {case['query']}")
        print(
            f"Calibration target: {expected_source}"
        )
        print(
            f"Expected relevant: {case['relevant']}"
        )

        target_found = False

        for rank, result in enumerate(
            ranked_results,
            start=1,
        ):
            source = normalize_source(
                result.document.metadata.get(
                    "source",
                    "",
                )
            )

            score = result.rerank_score

            is_target = source == expected_source

            print(
                f"  Rank {rank} | "
                f"target={is_target} | "
                f"source={source} | "
                f"score={score}"
            )

            if is_target:
                target_found = True

                if score is None:
                    continue

                if case["relevant"]:
                    relevant_scores.append(score)
                else:
                    irrelevant_scores.append(score)

        if case["relevant"]:
            assert target_found, (
                "Expected relevant source was not "
                f"retrieved for: {case['query']}"
            )

    print("\n" + "=" * 100)
    print("CALIBRATION SUMMARY")
    print("=" * 100)

    print(
        f"Relevant samples: "
        f"{len(relevant_scores)}"
    )

    print(
        f"Irrelevant samples: "
        f"{len(irrelevant_scores)}"
    )

    if relevant_scores:
        print(
            f"Lowest relevant score: "
            f"{min(relevant_scores):.6f}"
        )

        print(
            f"Average relevant score: "
            f"{sum(relevant_scores) / len(relevant_scores):.6f}"
        )

    if irrelevant_scores:
        print(
            f"Highest irrelevant score: "
            f"{max(irrelevant_scores):.6f}"
        )

        print(
            f"Average irrelevant score: "
            f"{sum(irrelevant_scores) / len(irrelevant_scores):.6f}"
        )

    assert relevant_scores