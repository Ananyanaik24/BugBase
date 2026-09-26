def generate_solution(query, user_question, best_bug):
    """
    Generates a simple local AI-style response using
    the highest-ranked bug from the IR system.

    No external API is used.
    """

    if best_bug is None:
        return """
### 🤖 AI Solution Assistant

I could not find a sufficiently relevant bug in the database.

Try searching with more specific keywords such as:
- null pointer
- memory leak
- segmentation fault
- syntax error
- file not found
"""

    # Get information from the best-ranked bug
    error_name = str(best_bug.get("ErrorName", "Unknown Error"))
    description = str(best_bug.get("Description", "No description available"))
    cause = str(best_bug.get("Cause", "Cause not available"))
    solution = str(best_bug.get("Solution", "Solution not available"))
    language = str(best_bug.get("Language", "Unknown"))

    # Relevance score
    if "FinalScore" in best_bug:
        relevance = float(best_bug["FinalScore"]) * 100
    else:
        relevance = 0

    # User question handling
    question = str(user_question).strip()

    if question:
        question_text = (
            f"Your question: **{question}**\n\n"
        )
    else:
        question_text = ""

    response = f"""
### 🤖 AI Solution Assistant

**Based on your search:** `{query}`

{question_text}

#### 🔍 Best Matching Bug

**{error_name}**  
**Language:** {language}  
**Relevance:** {relevance:.1f}%

---

#### 📌 Problem

{description}

#### ⚠️ Possible Cause

{cause}

#### 💡 Recommended Solution

{solution}

---

### ⭐ Why this solution was selected

This solution comes from the **highest-ranked result** returned by the
Information Retrieval system.

The ranking considers:

- **TF-IDF**
- **Cosine Similarity**
- **Pattern Matching**
- **Final Relevance Score**

The bug with the highest final relevance score is selected as the
**Best Recommended Solution**.
"""

    return response