
class Posting:
    doc_id;
    freq;
    tf_idf_score;

    def __init__(self, id, frequency, tf_id):
        self.doc_id = id;
        self.freq = frequency;
        self.tf_idf_score = tf_id;

    