from src.services.rag_service import answer_question

from tests.evaluation.answer_correctness import evaluate_answer
from tests.evaluation.citation_correctness import evaluate_citation
from tests.evaluation.claim_faithfulness import (
    evaluate_claim_faithfulness,
)
from tests.evaluation.rag_evaluation_dataset import (
    RAG_EVALUATION_DATASET,
)


def test_debug_real_rag_evaluation():

    print("\n" + "=" * 100)
    print("REAL RAG DEBUG EVALUATION")
    print("=" * 100)

    for index, case in enumerate(
        RAG_EVALUATION_DATASET,
        start=1,
    ):
        print("\n" + "=" * 100)
        print(f"CASE {index}")
        print("=" * 100)

        question = case["question"]
        expected_answer = case["expected_answer"]
        expected_sources = case["expected_sources"]

        print(f"\nQUESTION:")
        print(question)

        print(f"\nEXPECTED ANSWER:")
        print(expected_answer)

        print(f"\nEXPECTED SOURCES:")
        for source in expected_sources:
            print(f"  - {source}")

        # ==================================================
        # Capture actual RetrievalResult objects
        # ==================================================

        real_retriever = (
            answer_question.__globals__["retriever"]
        )

        captured_results = []

        original_retrieve = real_retriever.retrieve

        def capture_retrieve(*args, **kwargs):
            results = original_retrieve(
                *args,
                **kwargs,
            )

            captured_results.extend(results)

            return results

        real_retriever.retrieve = capture_retrieve

        try:
            result = answer_question(question)
        finally:
            real_retriever.retrieve = original_retrieve

        # ==================================================
        # Extract answer and citations
        # ==================================================

        answer = result.get("answer", "")
        citations = result.get("citations", [])

        print("\nACTUAL ANSWER:")
        print(answer)

        # ==================================================
        # Retrieved documents
        # ==================================================

        print("\nRETRIEVED DOCUMENTS:")

        if not captured_results:
            print("  No documents retrieved.")
        else:
            for rank, retrieval_result in enumerate(
                captured_results,
                start=1,
            ):
                document = retrieval_result.document

                source = document.metadata.get(
                    "source",
                    "",
                )

                page = document.metadata.get(
                    "page",
                    "",
                )

                print(f"\n  Rank {rank}")
                print(f"    Source: {source}")
                print(f"    Page: {page}")
                print(
                    f"    Rerank score: "
                    f"{retrieval_result.rerank_score}"
                )

                print("    Content:")
                print(
                    document.page_content
                )

        # ==================================================
        # Citations
        # ==================================================

        print("\nCITATIONS:")

        if not citations:
            print("  No citations returned.")
        else:
            for citation_index, citation in enumerate(
                citations,
                start=1,
            ):
                print(
                    f"\n  Citation {citation_index}:"
                )

                print(
                    f"    source: "
                    f"{citation.get('source')}"
                )

                print(
                    f"    page: "
                    f"{citation.get('page')}"
                )

        # ==================================================
        # Answer correctness
        # ==================================================

        if case["should_retrieve"]:
            answer_correct = evaluate_answer(
                generated_answer=answer,
                expected_answer=expected_answer,
            )
        else:
            answer_correct = (
                answer.strip().lower()
                in {
                    "i don't know.",
                    "i don't know",
                }
            )

        print(
            f"\nANSWER CORRECT: "
            f"{answer_correct}"
        )

        # ==================================================
        # Citation correctness
        # ==================================================

        if not case["should_retrieve"]:
            citation_correct = None

        elif citations:
            cited_source = citations[0].get(
                "source",
                "",
            )

            citation_correct = evaluate_citation(
                cited_source=cited_source,
                expected_sources=expected_sources,
            )

        else:
            citation_correct = False

        if citation_correct is None:
            print("CITATION CORRECT: N/A")
        else:
            print(
                f"CITATION CORRECT: "
                f"{citation_correct}"
            )

        # ==================================================
        # Build actual grounding context
        # ==================================================

        context_parts = [
            retrieval_result.document.page_content
            for retrieval_result in captured_results
        ]

        context = "\n".join(context_parts)

        print("\nFAITHFULNESS CONTEXT:")

        if context:
            print(context)
        else:
            print(
                "  No retrieved context available."
            )

        # ==================================================
        # Faithfulness
        # ==================================================

        if (
            case["should_retrieve"]
            and context
        ):
            faithfulness_score = (
                evaluate_claim_faithfulness(
                    answer=answer,
                    context=context,
                )
            )

            print(
                f"\nFAITHFULNESS SCORE: "
                f"{faithfulness_score:.2%}"
            )

        else:
            print(
                "\nFAITHFULNESS SCORE: N/A"
            )