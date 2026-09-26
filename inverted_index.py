from collections import defaultdict

from preprocessing import preprocess_text


def build_inverted_index(df):

    # Dictionary:
    # word -> list of BugIDs

    index = defaultdict(list)

    for _, row in df.iterrows():

        bug_id = row["BugID"]

        # Combine all searchable fields
        text = (
            str(row["ErrorName"]) + " " +
            str(row["Language"]) + " " +
            str(row["Description"]) + " " +
            str(row["Cause"]) + " " +
            str(row["Solution"]) + " " +
            str(row["Keywords"])
        )

        # Preprocess document
        words = preprocess_text(text)

        # Add BugID for every word
        for word in words:

            if bug_id not in index[word]:

                index[word].append(bug_id)

    return index