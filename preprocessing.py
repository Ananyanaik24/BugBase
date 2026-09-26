import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Stop words
stop_words = set(stopwords.words("english"))

# Stemmer
stemmer = PorterStemmer()


def preprocess_text(text):
    """
    Performs:
    1. Lowercase conversion
    2. Punctuation removal
    3. Tokenization
    4. Stop-word removal
    5. Stemming
    """

    # Convert to string
    text = str(text)

    # Lowercase
    text = text.lower()

    # Remove punctuation
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)

    # Tokenization
    words = text.split()

    # Remove stop words
    words = [
        word for word in words
        if word not in stop_words
    ]

    # Stemming
    words = [
        stemmer.stem(word)
        for word in words
    ]

    return words


# Test the preprocessing
if __name__ == "__main__":

    text = "Java Null Pointer Errors!"

    print("Original Text:")
    print(text)

    print("\nProcessed Text:")
    print(preprocess_text(text))