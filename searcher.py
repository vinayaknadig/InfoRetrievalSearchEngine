from nltk.stem import PorterStemmer
import math

def main():
    stemmer = PorterStemmer()
    query = input("What would you like to search for today? ").split()
    N = 35724
    stemmed_query = [stemmer.stem(x.lower()) for x in query]
    with open("token_posting_list.txt", 'r') as readfile:
        line = readfile.readline()
        line = line.split()
        query_posting_dict = dict()
        while line:
            if line[0] in stemmed_query:
                df = len(line[1:])
                for posting in line[1:]:
                    doc_id = int(posting.split(',')[0])
                    tf = float(posting.split(',')[1])
                    tf_idf = (1+math.log(tf))*math.log(N/df)
                    if line[0] in query_posting_dict.keys():
                        query_posting_dict[line[0]].append((doc_id, tf_idf))
                    else:
                        query_posting_dict[line[0]] = [(doc_id, tf_idf)]
            line = readfile.readline()
            line = line.split()

    document_scores = dict()
    for term in stemmed_query:
        for doc_id, tfidfscore in query_posting_dict[term]:
            if doc_id not in document_scores.keys():
                document_scores[doc_id] = [0 for _ in stemmed_query]
            document_scores[doc_id][stemmed_query.index(term)] += tfidfscore

    for docid, scorelist in document_scores.items():
        normalization = math.sqrt(sum([x*x for x in scorelist]))
        count = 0
        while count < len(scorelist):
            scorelist[count] = scorelist[count] / normalization
            count += 1
    
    query_scores = []
    for term in stemmed_query:
        query_scores.append(math.log(N/len(query_posting_dict[term])))
    normalization = math.sqrt(sum([x*x for x in query_scores]))
    count = 0
    while count < len(query_scores):
        query_scores[count] = query_scores[count] / normalization
        count += 1
    
    final_scoring = dict()
    for doc_id in document_scores.keys():
        count = 0
        score = 0
        while count < len(stemmed_query):
            score += query_scores[count]*document_scores[doc_id][count]
            count += 1
        final_scoring[doc_id] = score

    all = [x for x in sorted(final_scoring.keys(), key=lambda y:final_scoring[y], reverse=True)]

    with open("doc_id_list.txt", "r") as docList:
        allcopy = all.copy()
        URLS = {}
        line = docList.readline()
        line = line.split()
        while len(allcopy) > 0:
            while int(line[0]) not in allcopy:
                line = docList.readline()
                line = line.split()
            URLS[int(line[0])] = line[1]
            allcopy.remove(int(line[0]))
            line = docList.readline()
            line = line.split()
                
    
    print("Your search results are listed below:")
    for i in range(2):
        if ((i+1)*100 >= len(all)):
            if (i*100 < len(all)):
                for id in all[i*100:]:
                    print("  " + URLS[id])
        else:
            for id in all[i*100:(i+1)*100]:
                    print("  " + URLS[id])

if __name__ == '__main__':
    main()
    