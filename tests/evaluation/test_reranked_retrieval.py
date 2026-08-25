from tests.evaluation.retrieval_questions import EVALUATION_QUESTIONS
from src.retriever.reranked_retriever import RerankedRetriever


retriever = RerankedRetriever()

def test_reranked_retrieval_returns_expected_sources():
    total = 0
    hits = 0
    reciprocal_ranks = []

    for case in EVALUATION_QUESTIONS:
        if not case["should_retrieve"]:
            continue

        total += 1

        results = retriever.retrieve(
            query=case["question"],
        )

        sources = [
            result.document.metadata.get("source", "")
            for result in results
        ]

        matching_ranks = [
            index + 1
            for index, source in enumerate(sources)
            if any(
                expected_source in source
                for expected_source in case["expected_sources"]
            )
        ]

        hit = bool(matching_ranks)

        if hit:
            hits += 1
            reciprocal_ranks.append(
                1 / min(matching_ranks)
            )
        else:
            reciprocal_ranks.append(0)

        assert hit, (
            f"Expected source not retrieved for: "
            f"{case['question']}"
        )

        assert all(
            result.rerank_score is not None
            for result in results
        ), (
            f"Missing rerank score for: "
            f"{case['question']}"
        )

    hit_rate = hits / total
    mrr = sum(reciprocal_ranks) / total

    print(
        f"\nReranked Retrieval Hit Rate: "
        f"{hit_rate:.2%} ({hits}/{total})"
    )

    print(
        f"Reranked Retrieval MRR: "
        f"{mrr:.4f}"
    )

    assert total > 0
def test_reranked_retrieval_rejects_irrelevant_queries():
    for case in EVALUATION_QUESTIONS:
        if case["should_retrieve"]:
            continue

        results = retriever.retrieve(
            query=case["question"],
        )

        assert results == [], (
            f"Unexpected documents retrieved for: "
            f"{case['question']}"
        )
def test_reranked_retrieval_recall_at_2():
    total = 0
    hits = 0

    for case in EVALUATION_QUESTIONS:
        if not case["should_retrieve"]:
            continue

        total += 1

        results = retriever.retrieve(
            query=case["question"],
        )

        top_2_sources = [
            result.document.metadata.get("source", "")
            for result in results[:2]
        ]

        relevant_found = any(
            expected_source in source
            for expected_source in case["expected_sources"]
            for source in top_2_sources
        )

        if relevant_found:
            hits += 1

        assert relevant_found, (
            f"Expected source not found in top-2 for: "
            f"{case['question']}"
        )

    recall_at_2 = hits / total

    print(
        f"\nReranked Retrieval Recall@2: "
        f"{recall_at_2:.2%} ({hits}/{total})"
    )

    assert total > 0

def test_reranked_retrieval_precision_at_2():
    total_precision = 0.0
    evaluated_queries = 0

    for case in EVALUATION_QUESTIONS:
        if not case["should_retrieve"]:
            continue

        evaluated_queries += 1

        results = retriever.retrieve(
            query=case["question"],
        )

        top_2_results = results[:2]

        relevant_count = 0

        print(
            f"\nQuestion: {case['question']}"
        )

        for rank, result in enumerate(
            top_2_results,
            start=1,
        ):
            source = result.document.metadata.get(
                "source",
                "",
            )

            is_relevant = any(
                expected_source in source
                for expected_source in case["expected_sources"]
            )

            if is_relevant:
                relevant_count += 1

            print(
                f"  Rank {rank} | "
                f"relevant={is_relevant} | "
                f"source={source} | "
                f"rerank_score={result.rerank_score}"
            )

        returned_count = len(top_2_results)

        assert returned_count > 0, (
            f"No results returned for: "
            f"{case['question']}"
        )

        precision_at_2 = (
            relevant_count / returned_count
        )

        print(
            f"  Precision@2: "
            f"{precision_at_2:.2%}"
        )

        total_precision += precision_at_2

    precision_at_2 = (
        total_precision / evaluated_queries
    )

    print(
        f"\nReranked Retrieval Precision@2: "
        f"{precision_at_2:.2%}"
    )

    assert evaluated_queries > 0