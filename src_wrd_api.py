from fastapi import FastAPI
from pydantic import BaseModel
from collections import Counter
import re
from typing import List

# Define the FastAPI app
app = FastAPI()

# Input model for the API
class WordSchemaRequest(BaseModel):
    pattern: str

# Load vocabulary file (assumed to be in the same directory as the script)
def load_vocabulary(file_path: str) -> List[str]:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return [line.strip().lower() for line in file.readlines()]
    except FileNotFoundError:
        raise FileNotFoundError(f"Vocabulary file '{file_path}' not found.")

# Match words against the pattern
def match_pattern(words: List[str], pattern: str) -> List[str]:
    # Convert pattern to a regex
    regex = '^' + pattern.replace('-', '.') + '$'
    return [word for word in words if re.match(regex, word, re.IGNORECASE)]

# Analyze character frequency
def analyze_characters(words: List[str]) -> List[str]:
    # Flatten all characters into a single list
    characters = [char for word in words for char in word]
    # Count occurrences of each character
    most_common = Counter(characters).most_common(5)
    return [char for char, _ in most_common]

# Get all unique characters in the matched words
def get_unique_characters(words: List[str]) -> List[str]:
    return sorted(set(char for word in words for char in word))

@app.post("/find_words/")
def find_words(request: WordSchemaRequest):
    # Load vocabulary
    vocabulary_file = "voc_ita.txt"
    try:
        vocabulary = load_vocabulary(vocabulary_file)
    except FileNotFoundError as e:
        return {"error": str(e)}

    # Match words
    matching_words = match_pattern(vocabulary, request.pattern)

    # Analyze characters
    popular_characters = analyze_characters(matching_words)

    # Get all unique characters
    unique_characters = get_unique_characters(matching_words)

    return {
        "pattern": request.pattern,
        "matching_words_count": len(matching_words),
        "matching_words": matching_words,
        "popular_characters": popular_characters,
        "all_characters": unique_characters
    }

#For local testing, uncomment the following lines:
if __name__ == "__main__":
    # Allow testing via user input
    print("--- Test Find Words API Locally ---")
    pattern = input("Enter pattern (e.g., M----E or MA-A-E): ")
    vocabulary_file = "voc_ita.txt"

    try:
        vocabulary = load_vocabulary(vocabulary_file)
        matching_words = match_pattern(vocabulary, pattern)
        popular_characters = analyze_characters(matching_words)
        unique_characters = get_unique_characters(matching_words)

        print(f"Pattern: {pattern}")
        print(f"Number of matching words: {len(matching_words)}")
        print(f"Matching words: {matching_words}")
        print(f"Most popular characters: {popular_characters}")
        print(f"All characters: {unique_characters}")
    except FileNotFoundError as e:
        print(f"Error: {e}")
