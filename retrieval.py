import re

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from preprocessing import preprocess_text
from query_expansion import expand_query


def retrieve_bugs(query, df, index, top_k=5):

    # =====================================================
    # STEP 1 - QUERY PREPROCESSING
    # =====================================================

    original_tokens = preprocess_text(query)

    # =====================================================
    # STEP 2 - QUERY EXPANSION
    # =====================================================

    expanded_tokens = expand_query(original_tokens)

    # Make sure expanded_tokens is a list
    if isinstance(expanded_tokens, str):
        expanded_tokens = preprocess_text(expanded_tokens)

    # =====================================================
    # STEP 3 - INVERTED INDEX SEARCH
    # =====================================================

    matched_terms = []

    candidate_ids = set()

    for token in expanded_tokens:

        token = str(token).lower().strip()

        if token in index:

            matched_terms.append(token)

            candidate_ids.update(index[token])

    # =====================================================
    # IF NO CANDIDATES, SEARCH ALL DOCUMENTS
    # =====================================================

    if candidate_ids:

        candidate_df = df[
            df["BugID"].isin(candidate_ids)
        ].copy()

    else:

        candidate_df = df.copy()

    # =====================================================
    # STEP 4 - CREATE SEARCHABLE DOCUMENT TEXT
    # =====================================================

    candidate_df["SearchText"] = (
        candidate_df["ErrorName"].fillna("").astype(str)
        + " "
        + candidate_df["Description"].fillna("").astype(str)
        + " "
        + candidate_df["Cause"].fillna("").astype(str)
        + " "
        + candidate_df["Solution"].fillna("").astype(str)
        + " "
        + candidate_df["Keywords"].fillna("").astype(str)
    )

    # =====================================================
    # STEP 5 - TF-IDF
    # =====================================================

    documents = candidate_df["SearchText"].tolist()

    query_text = " ".join(expanded_tokens)

    if not query_text.strip():
        query_text = query

    vectorizer = TfidfVectorizer()

    try:

        tfidf_matrix = vectorizer.fit_transform(
            documents + [query_text]
        )

        document_vectors = tfidf_matrix[:-1]
        query_vector = tfidf_matrix[-1]

        cosine_scores = cosine_similarity(
            query_vector,
            document_vectors
        ).flatten()

    except ValueError:

        cosine_scores = [0.0] * len(candidate_df)

    candidate_df["TFIDF_Cosine"] = cosine_scores

    # =====================================================
    # STEP 6 - PATTERN MATCHING
    # =====================================================

    query_lower = query.lower()

    pattern_scores = []

    for _, bug in candidate_df.iterrows():

        searchable_text = (
            str(bug["ErrorName"]) + " "
            + str(bug["Description"]) + " "
            + str(bug["Cause"]) + " "
            + str(bug["Solution"]) + " "
            + str(bug["Keywords"])
        ).lower()

        exact_match = (
            query_lower in searchable_text
        )

        individual_match = any(
            token in searchable_text
            for token in original_tokens
        )

        if exact_match:
            pattern_scores.append(1.0)

        elif individual_match:
            pattern_scores.append(0.5)

        else:
            pattern_scores.append(0.0)

    candidate_df["PatternMatch"] = [
        score > 0 for score in pattern_scores
    ]

    # =====================================================
    # STEP 7 - FINAL RELEVANCE SCORE
    # =====================================================

    candidate_df["FinalScore"] = (
        0.80 * candidate_df["TFIDF_Cosine"]
        + 0.20 * pd.Series(
            pattern_scores,
            index=candidate_df.index
        )
    )

    # =====================================================
    # STEP 8 - RANKING
    # =====================================================

    candidate_df = candidate_df.sort_values(
        by="FinalScore",
        ascending=False
    )

    # =====================================================
    # STEP 9 - TOP K RESULTS
    # =====================================================

    results = candidate_df.head(top_k).copy()

    # =====================================================
    # REMOVE TEMPORARY COLUMN
    # =====================================================

    if "SearchText" in results.columns:
        results = results.drop(
            columns=["SearchText"]
        )

    # =====================================================
    # INFORMATION FOR FRONTEND
    # =====================================================

    info = {

        "original_tokens": original_tokens,

        "expanded_tokens": expanded_tokens,

        "candidate_count": len(candidate_df),

        "matched_terms": matched_terms
    }

    return results, info


# =========================================================
# SELECT BEST SOLUTION
# =========================================================

def get_best_solution(results):

    if results is None or results.empty:
        return None

    # First row is the highest ranked result
    best_bug = results.iloc[0]

    relevance = min(
        max(
            float(best_bug["FinalScore"]) * 100,
            0
        ),
        100
    )

    return {

        "BugID": best_bug["BugID"],

        "ErrorName": best_bug["ErrorName"],

        "Language": best_bug["Language"],

        "Description": best_bug["Description"],

        "Cause": best_bug["Cause"],

        "Solution": best_bug["Solution"],

        "Keywords": best_bug["Keywords"],

        "Relevance": relevance,

        "CosineScore": float(
            best_bug["TFIDF_Cosine"]
        ) * 100,

        "PatternMatch": best_bug["PatternMatch"]
    }
def get_best_solution(results):
    """
    Selects the solution from the highest-ranked bug
    based on FinalScore (Relevance).
    """

    if results is None or results.empty:
        return None

    # Results are already sorted by FinalScore
    best_bug = results.iloc[0]

    return best_bug