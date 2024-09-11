import re
from collections import defaultdict

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    #print(text)
    return text

#tokenizing text into individiual chars.
def tokenize_text(text):
    words = text.split()
    # the line below converts each word into characters. Except first character, rest have ## added.
    tokens = {word: [c if i == 0 else f"##{c}" for i, c in enumerate(word)] for word in words}
    #print(tokens)
    return tokens

#getting frequencies of sidebyside chars
def get_pair_frequencies(tokens, word_freqs):
    pair_freq = defaultdict(int)
    token_freq = defaultdict(int)
    #print(tokens)

    for word, split in tokens.items():
        freq = word_freqs[word]
        #print(freq)
        #print(split)

        if len(split) == 1:
            token_freq[split[0]] += freq
            continue

        #making pairs of the adjacent characters' freq
        for i in range(len(split) - 1):
            pair = (split[i], split[i + 1])
            token_freq[split[i]] += freq
            pair_freq[pair] += freq

        token_freq[split[-1]] += freq

    # print(pair_freq)
    # print("split here")
    # print(token_freq)

    return pair_freq, token_freq

#Calc pair freqs based on the formula provided.
def calculate_pair_scores(pair_freq, token_freq):
    pair_scores = {}
    for (first, second), freq_pair in pair_freq.items():
        score = freq_pair / (token_freq[first] * token_freq[second])
        pair_scores[(first, second)] = score
    return pair_scores

# ,erging high freq tokens
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

#Main algorithm function
def word_piece_algorithm(file_path):
    # Read text
    text = read_file(file_path)
    #print(text)

    # pre-tokenizing into words and counting the freq of words
    word_freqs = defaultdict(int)
    for word in text.split():
        word_freqs[word] += 1
    #print(word_freqs)

    #splitting into individual tokens
    tokens = tokenize_text(text)
    
    merges = [] 

    # for first 10 merges
    while len(merges) < 10:
        # Getting pair and token frequencies
        pair_freq, token_freq = get_pair_frequencies(tokens, word_freqs)
        #get pair scores based on provided formula
        pair_scores = calculate_pair_scores(pair_freq, token_freq)

        # simple max func to find highest pair score
        best_pair = max(pair_scores, key=pair_scores.get)

        merges.append(best_pair)

        #merging hghihest freq tokens
        tokens = merge_pair(tokens, best_pair, word_freqs)

    return merges

if __name__ == "__main__":
    file_path = "wordpiece_input.txt"

    # calling wordpiece algo.
    first_10_merged_pairs = word_piece_algorithm(file_path)

    # first 10 pairs
    print("First 10 pairs merged by the algorithm:")
    for pair in first_10_merged_pairs:
        print(pair)