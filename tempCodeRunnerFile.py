import re
from collections import defaultdict

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

# Tokenizing text into individual chars while treating punctuation separately
def tokenize_text(text):
    # Use regular expression to separate punctuation from words
    words = re.findall(r"\w+|[^\w\s]", text, re.UNICODE)
    
    # Convert each word into characters. Punctuation is kept as standalone tokens.
    tokens = {}
    for word in words:
        if re.match(r"^\w+$", word):  # If the word is alphanumeric
            tokens[word] = [c if i == 0 else f"##{c}" for i, c in enumerate(word)]
        else:  # If the word is punctuation
            tokens[word] = [word]
    return tokens

# Getting frequencies of side-by-side chars
def get_pair_frequencies(tokens, word_freqs):
    pair_freq = defaultdict(int)
    token_freq = defaultdict(int)

    for word, split in tokens.items():
        freq = word_freqs[word]

        if len(split) == 1:
            token_freq[split[0]] += freq
            continue

        # Making pairs of the adjacent characters' freq
        for i in range(len(split) - 1):
            pair = (split[i], split[i + 1])
            token_freq[split[i]] += freq
            pair_freq[pair] += freq

        token_freq[split[-1]] += freq

    return pair_freq, token_freq

# Calculate pair frequencies based on the formula provided.
def calculate_pair_scores(pair_freq, token_freq):
    pair_scores = {}
    for (first, second), freq_pair in pair_freq.items():
        score = freq_pair / (token_freq[first] * token_freq[second])
        pair_scores[(first, second)] = score
    return pair_scores

# Merging high freq tokens
def merge_pair(tokens, best_pair, word_freqs):
    a, b = best_pair
    merged_tokens = {}

    for word, split in tokens.items():
        freq = word_freqs[word]

        if len(split) == 1:
            merged_tokens[word] = split
            continue

        i = 0
        while i < len(split) - 1:
            if split[i] == a and split[i + 1] == b:
                merge = a + b[2:] if b.startswith("##") else a + b
                split = split[:i] + [merge] + split[i + 2:]
            else:
                i += 1

        merged_tokens[word] = split

    return merged_tokens

# Main algorithm function
def word_piece_algorithm(file_path):
    # Read text
    text = read_file(file_path)

    # Pre-tokenizing into words and counting the frequency of words
    word_freqs = defaultdict(int)
    words = re.findall(r"\w+|[^\w\s]", text, re.UNICODE)  # Ensure punctuation is separated
    for word in words:
        word_freqs[word] += 1

    # Splitting into individual tokens
    tokens = tokenize_text(text)
    
    merges = [] 

    # For first 10 merges
    while len(merges) < 10:
        # Getting pair and token frequencies
        pair_freq, token_freq = get_pair_frequencies(tokens, word_freqs)
        # Get pair scores based on the provided formula
        pair_scores = calculate_pair_scores(pair_freq, token_freq)

        # Find the highest pair score
        best_pair = max(pair_scores, key=pair_scores.get)

        # Append the best pair and its score
        merges.append((best_pair, pair_scores[best_pair]))

        # Merging highest freq tokens
        tokens = merge_pair(tokens, best_pair, word_freqs)

    return merges

if __name__ == "__main__":
    file_path = "wordpiece_input.txt"

    # Calling wordpiece algorithm
    first_10_merged_pairs = word_piece_algorithm(file_path)

    # First 10 pairs and their scores
    print("First 10 pairs merged by the algorithm with their frequency scores:")
    print(first_10_merged_pairs)
    for pair, score in first_10_merged_pairs:
        print(f"Pair: {pair}, Score: {score:.6f}")
