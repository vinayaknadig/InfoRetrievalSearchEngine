
class Posting:
    doc_id;
    freq;
    tf_idf_score;

    def __init__(self, id, frequency, tf_id):
        self.doc_id = id;
        self.freq = frequency;
        self.tf_idf_score = tf_id;
    
    def getDocId(self):
        return self.doc_id;

    def getFreq(self):
        return self.freq;

    def getTfIdfScore(self):
        return self.tf_idf_score;

    