import re
import string

def clean_text(text):
    """Remove punctuation and convert text to lowercase."""
    return text.translate(str.maketrans('', '', string.punctuation)).lower()

def tokenize_text(text):
    """Split cleaned text into words."""
    return re.findall(r'\b\w+\b', text)

def calculate_word_frequencies(words):
    """Create a dictionary of word frequencies."""
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    return freq

def average_word_length(words):
    """Calculate average word length."""
    total_chars = sum(len(word) for word in words)
    total_words = len(words)
    return total_chars / total_words if total_words > 0 else 0

def analyze_text_file(file_path):
    """Read file and analyze its content."""
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    cleaned = clean_text(text)
    words = tokenize_text(cleaned)
    frequencies = calculate_word_frequencies(words)
    avg_length = average_word_length(words)

    return frequencies, avg_length

def display_results(frequencies, avg_length):
    print("Word Frequencies:")
    for word, freq in sorted(frequencies.items(), key=lambda x: (-x[1], x[0])):
        print(f"{word}: {freq}")
    print(f"\nAverage Word Length: {avg_length:.2f}")

# Example usage
if __name__ == "__main__":
    file_path = "sample.txt"  # Replace with your actual file
    try:
        freqs, avg = analyze_text_file(file_path)
        display_results(freqs, avg)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
