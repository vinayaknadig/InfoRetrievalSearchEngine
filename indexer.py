from postings import Posting
from tokenizer import Tokenizer
import os

def main():
    count = 0
    doc_id_dict = {}
    token_postings = {}
    for directory_path, directory_name, filename in os.walk("Dev"):
        for file in filename:
            if file.endswith('.json'):
                print(file)
                doc_id_dict[count] = file
                token_obj = Tokenizer(directory_path + "/" + file)
                tokens = token_obj.tokenize()
                token_freq = token_obj.computeWordFrequencies(tokens)
                for token in token_freq.keys():
                    if token not in token_postings.keys():
                        token_postings[token] = []
                    token_postings[token].append(Posting(count, token_freq[token], 0))
                count += 1
    
    with open("output.txt", "w") as file_to_write:
        for token, post_list in token_postings.items():
            file_to_write.write(token)
            for post in post_list:
                file_to_write.write(" " + str(post.getDocId()) + "," + str(post.getFreq()))
            file_to_write.write("\n")



if __name__ == '__main__':
    main()
