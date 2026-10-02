from tests.evaluation.retrieval_questions import EVALUATION_QUESTIONS
from src.retriever.document_retriever import retrieve_documents


def test_retrieval():
    for case in EVALUATION_QUESTIONS:
        documents = retrieve_documents(case["question"])

        sources = {
            document.metadata.get("source", "")
            for document in documents
        }

        if case["should_retrieve"]:
            assert any(
                expected_source in source
                for expected_source in case["expected_sources"]
                for source in sources
            ), (
                f"Expected source not retrieved for: "
                f"{case['question']}"
            )

        else:
            assert len(documents) == 0, (
                f"Unexpected documents retrieved for: "
                f"{case['question']}"
            )