from postings import Posting
from tokenizer import Tokenizer
import os
from nltk.stem import PorterStemmer
import json
import math
import sys
from simhash import Simhash # https://leons.im/posts/a-python-implementation-of-simhash-algorithm/ - Used this version of Simhash to compare similarities of sites

def main():
    count = 0
    doc_id_dict = {}
    token_postings = {}
    partialnum = 0
    stemmer = PorterStemmer()
    hash_values = set()
    for directory_path, directory_name, filename in os.walk("Dev"):
        for file in filename:
            if file.endswith('.json'):
                print(file)
                json_obj = open(directory_path + "/" + file, 'r')
                content = json.load(json_obj)
                token_obj = Tokenizer(directory_path + "/" + file)
                tokens = token_obj.tokenize()
                hash_no = Simhash(tokens).value
                if len(tokens) > 50 and hash_no not in hash_values:
                    hash_values.add(hash_no)
                    doc_id_dict[count] = content['url']
                    token_freq = token_obj.computeWordFrequencies(tokens)
                    for token in token_freq.keys():
                        stemmed_token = stemmer.stem(token)
                        if stemmed_token not in token_postings.keys():
                            token_postings[stemmed_token] = []
                        token_postings[stemmed_token].append(Posting(count, token_freq[token], 0))
                    count += 1
                if sys.getsizeof(token_postings) >= 5000000:
                    filename = "partial" + str(partialnum) + '.txt'
                    print(filename)
                    partialnum += 1
                    with open(filename, "w") as file_to_write:
                        for token, post_list in sorted(token_postings.items(), key= lambda x: x):
                            file_to_write.write(token)
                            for post in post_list:
                                file_to_write.write(" " + str(post.getDocId()) + "," + str(post.getFreq()))
                            file_to_write.write("\n")
                    token_postings.clear()


    openfiles = dict()
    for i in range(partialnum):
        filename = r"Partial Indices/partial" + str(i) + '.txt'
        openfiles[i] = open(filename, "r")
    
    past_word = ""
    with open("token_posting_list.txt", "w") as file_to_write:
        fileobj = [x for x in sorted(openfiles.items(), key=lambda x:see_line(x[1])) if see_line(x[1])!='zzzzzzzzzzzzzzzzzz']
        while len(fileobj)>0:
            line = fileobj[0][1].readline().split()
            openfiles[fileobj[0][0]] = fileobj[0][1]
            if line[0] == past_word:
                for posting_pair in line[1:]:
                    file_to_write.write(" " + posting_pair)
            else:
                past_word = line[0]
                file_to_write.write("\n")
                file_to_write.write(line[0])
                for posting_pair in line[1:]:
                    file_to_write.write(" " + posting_pair)
            fileobj = [x for x in sorted(openfiles.items(), key=lambda x:see_line(x[1])) if see_line(x[1])!='zzzzzzzzzzzzzzzzzz']

    with open("doc_id_list.txt", "w") as doc_id_file:
        for id, url in doc_id_dict.items():
            doc_id_file.write(str(id) + " " + str(url) + "\n")


def see_line(file):
    current_position = file.tell()
    text = file.readline()
    file.seek(current_position)
    if text:
        return text
    else:
        return 'zzzzzzzzzzzzzzzzzz'

if __name__ == '__main__':
    main()
