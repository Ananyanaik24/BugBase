import pandas as pd
from retrieval import retrieve_bugs


def evaluate(df, index):

    # Test queries with expected BugIDs
    test_queries = [
        ("java null pointer", 1),
        ("python index error", 31),
        ("python key error", 32),
        ("java array index", 2),
        ("java class not found", 3),
        ("java stack overflow", 4),
        ("java syntax error", 5),
        ("python indentation error", 33),
        ("python syntax error", 34),
        ("python type error", 35),
        ("c segmentation fault", 61),
        ("c buffer overflow", 62),
        ("c memory leak", 63),
        ("c++ segmentation fault", 91),
        ("c++ memory leak", 92),
        ("c++ compilation error", 93),
        ("web 404 error", 121),
        ("web 500 server error", 122),
        ("web cors error", 123),
        ("web timeout", 124)
    ]

    k = 5

    rows = []
    total_relevant = 0
    total_retrieved_relevant = 0

    for query, expected_id in test_queries:

        try:
            results, info = retrieve_bugs(
                query,
                df,
                index,
                k
            )

            retrieved_ids = results["BugID"].tolist()

        except Exception:
            retrieved_ids = []

        found = expected_id in retrieved_ids

        if found:
            total_retrieved_relevant += 1

        total_relevant += 1

        precision = 1 / k if found else 0
        recall = 1 if found else 0

        if precision + recall > 0:
            f1 = (
                2 * precision * recall /
                (precision + recall)
            )
        else:
            f1 = 0

        rows.append({
            "Query": query,
            "Expected BugID": expected_id,
            "Retrieved BugIDs": ", ".join(
                str(x) for x in retrieved_ids
            ),
            "Found in Top 5": "✓ Yes" if found else "✗ No",
            "Precision": round(precision, 3),
            "Recall": round(recall, 3),
            "F1 Score": round(f1, 3)
        })

    # Overall metrics
    overall_precision = (
        total_retrieved_relevant /
        (total_relevant * k)
    )

    overall_recall = (
        total_retrieved_relevant /
        total_relevant
    )

    if overall_precision + overall_recall > 0:

        overall_f1 = (
            2 *
            overall_precision *
            overall_recall /
            (overall_precision + overall_recall)
        )

    else:

        overall_f1 = 0

    table = pd.DataFrame(rows)

    return {
        "precision": overall_precision,
        "recall": overall_recall,
        "f1": overall_f1,
        "hits": total_retrieved_relevant,
        "total": total_relevant,
        "table": table
    }