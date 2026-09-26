# Query expansion dictionary

synonyms = {

    "npe": [
        "null",
        "pointer",
        "exception",
        "null pointer exception"
    ],

    "crash": [
        "runtime",
        "error",
        "failure"
    ],

    "bug": [
        "error",
        "issue"
    ],

    "segfault": [
        "segmentation",
        "fault"
    ],

    "outofbounds": [
        "array",
        "index",
        "bounds"
    ],

    "memory": [
        "heap",
        "allocation",
        "leak"
    ],

    "divzero": [
        "division",
        "zero",
        "arithmetic"
    ]
}


def expand_query(words):

    expanded_words = list(words)

    for word in words:

        if word in synonyms:

            expanded_words.extend(
                synonyms[word]
            )

    # Remove duplicate words
    expanded_words = list(
        dict.fromkeys(expanded_words)
    )

    return expanded_words