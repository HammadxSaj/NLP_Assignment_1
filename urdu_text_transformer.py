from transformers import AutoTokenizer

# Load a pretrained transformer model 
tokenizer = AutoTokenizer.from_pretrained("bert-base-multilingual-cased")

def read_urdu_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

def tokenize_urdu_with_transformer(text):
    tokens = tokenizer.tokenize(text)
    return tokens

def write_tokens_to_file(tokens, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for token in tokens:
            file.write(token + '\n')

if __name__ == "__main__":
    # Define file paths
    input_file_path = "urdu_text_input.txt"
    output_file_path = "urdu_tokens_output_transformer.txt"
    
    urdu_text = read_urdu_text(input_file_path)

    tokens = tokenize_urdu_with_transformer(urdu_text)

    write_tokens_to_file(tokens, output_file_path)

    print("Tokenization complete using Transformer model. Tokens have been written to", output_file_path)