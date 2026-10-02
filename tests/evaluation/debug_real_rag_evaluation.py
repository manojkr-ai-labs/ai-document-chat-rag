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

        result = answer_question(question)

        answer = result.get("answer", "")
        citations = result.get("citations", [])

        print("\nACTUAL ANSWER:")
        print(answer)

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

                print(
                    f"    content: "
                    f"{citation.get('content')}"
                )

        # --------------------------------------------------
        # Answer correctness
        # --------------------------------------------------

        if case["should_retrieve"]:
            answer_correct = evaluate_answer(
                generated_answer=answer,
                expected_answer=expected_answer,
            )
        else:
            answer_correct = (
                not citations
            )

        print(
            f"\nANSWER CORRECT: "
            f"{answer_correct}"
        )

        # --------------------------------------------------
        # Citation correctness
        # --------------------------------------------------

        citation_correct = False

        if citations and expected_sources:
            cited_source = citations[0].get(
                "source",
                "",
            )

            citation_correct = evaluate_citation(
                cited_source=cited_source,
                expected_sources=expected_sources,
            )

        print(
            f"CITATION CORRECT: "
            f"{citation_correct}"
        )

        # --------------------------------------------------
        # Faithfulness
        # --------------------------------------------------

        context_parts = []

        for citation in citations:
            content = citation.get("content")

            if content:
                context_parts.append(content)

        context = "\n".join(context_parts)

        print("\nFAITHFULNESS CONTEXT:")

        if context:
            print(context)
        else:
            print(
                "  No citation content available."
            )

        if context:
            faithfulness_score = (
                evaluate_claim_faithfulness(
                    answer=answer,
                    context=context,
                )
            )
        else:
            faithfulness_score = 0.0

        print(
            f"\nFAITHFULNESS SCORE: "
            f"{faithfulness_score:.2%}"
        )