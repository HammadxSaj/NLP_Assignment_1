import re
from collections import defaultdict


def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read().lower()
    # Clean the text by removing non-alphabetic characters
    text = re.sub(r'[^a-z\s]', '', text)
    return text


def tokenize_text(text):
    words = text.split()
    # Each word becomes a list of characters
    tokens = [list(word) for word in words]
    return tokens


def get_pair_frequencies(tokens):
    pair_freq = defaultdict(int)
    token_freq = defaultdict(int)

    for token_list in tokens:
        # Count frequency of each token
        for token in token_list:
            token_freq[token] += 1

        # Count frequency of each pair of adjacent tokens
        for i in range(len(token_list) - 1):
            pair = (token_list[i], token_list[i + 1])
            pair_freq[pair] += 1
    # print(token_freq)
    # print("THIS IS SEPERATION")
    # print(pair_freq)
    return pair_freq, token_freq


def calculate_pair_scores(pair_freq, token_freq):
    pair_scores = {}
    for (first, second), freq_pair in pair_freq.items():
        score = freq_pair / (token_freq[first] * token_freq[second])
        pair_scores[(first, second)] = score
    return pair_scores


def merge_pair(tokens, pair_to_merge):
    merged_tokens = []
    first, second = pair_to_merge
    pair_str = first + second

    for token_list in tokens:
        merged_token_list = []
        skip_next = False
        for i in range(len(token_list)):
            if skip_next:
                skip_next = False
                continue

            if i < len(token_list) - 1 and token_list[i] == first and token_list[i + 1] == second:
                merged_token_list.append(pair_str)
                skip_next = True
            else:
                merged_token_list.append(token_list[i])

        merged_tokens.append(merged_token_list)

    #print(merged_tokens)
    return merged_tokens

def word_piece_algorithm(file_path, num_merges=10):
    # Read and preprocess the text
    text = read_file(file_path)

    tokens = tokenize_text(text)

    #print(tokens)

    merged_pairs = []

    for _ in range(num_merges):

        pair_freq, token_freq = get_pair_frequencies(tokens)

        pair_scores = calculate_pair_scores(pair_freq, token_freq)

        best_pair = max(pair_scores, key=pair_scores.get)

        # Append the pair to the merged pairs list
        merged_pairs.append(best_pair)

        # Merge the best pair in tokens
        tokens = merge_pair(tokens, best_pair)

    #print("pairscores:", pair_scores)
    return merged_pairs


if __name__ == "__main__":
    # Specify the file path to your text file here
    file_path = "wordpiece_input.txt"
    first_10_merged_pairs = word_piece_algorithm(file_path)
    print("First 10 pairs merged by the algorithm:")
    for pair in first_10_merged_pairs:
        print(pair)
