RAG_EVALUATION_DATASET = [
    {
        "question": "What is the maximum marks for the BCS-011 examination?",
        "expected_answer": "100 marks",
        "expected_sources": [
            "05._June_2012  BCS-011 IGNOUAssignmentGuru.com.pdf",
        ],
        "should_retrieve": True,
    },
    {
        "question": "How long is the BCS-011 examination?",
        "expected_answer": "3 hours",
        "expected_sources": [
            "05._June_2012  BCS-011 IGNOUAssignmentGuru.com.pdf",
        ],
        "should_retrieve": True,
    },
    {
        "question": "What is the weightage of the BCS-011 examination?",
        "expected_answer": "75%",
        "expected_sources": [
            "05._June_2012  BCS-011 IGNOUAssignmentGuru.com.pdf",
        ],
        "should_retrieve": True,
    },
    {
        "question": "How many marks does question number 1 carry in BCS-011?",
        "expected_answer": "40 marks",
        "expected_sources": [
            "05._June_2012  BCS-011 IGNOUAssignmentGuru.com.pdf",
        ],
        "should_retrieve": True,
    },
    {
        "question": "What is IATA Annual?",
        "expected_answer": "IATA Annual General Meeting",
        "expected_sources": [
            "agm69-resolution-passenger-rights.pdf",
        ],
        "should_retrieve": True,
    },
    {
        "question": "What does the IATA Annual General Meeting address?",
        "expected_answer": "passenger rights",
        "expected_sources": [
            "agm69-resolution-passenger-rights.pdf",
        ],
        "should_retrieve": True,
    },
    {
        "question": "What is the population of Japan?",
        "expected_answer": None,
        "expected_sources": [],
        "should_retrieve": False,
    },
    {
        "question": "What is IIITE?",
        "expected_answer": None,
        "expected_sources": [],
        "should_retrieve": False,
    },
]