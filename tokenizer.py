import json
import re
from lxml import etree
import lxml.html

class Tokenizer:
    file = ""

    def __init__(self, filename):
        self.file = filename
    
    def tokenize(self) -> list:
        to_return = []
        try:
            json_obj = open(self.file, "r")
            content = json.load(json_obj);
            doc = lxml.html.document_fromstring(content["content"])
            lines = doc.text_content().split()
            for word in lines:
                word = word.lower()
                tokens = re.split('[^a-z0-9]', word)
                for x in tokens:
                    if re.match('^[a-z]+$', x) or re.match('^[0-9]+$', x):
                        to_return.append(x)
            json_obj.close()
        except FileNotFoundError:
            print("File not found. Please try again.")
        except ValueError:
            print(self.file)
        except etree.ParserError:
            print(self.file)
        
        return to_return

    def computeWordFrequencies(self, tokens) -> {str:int}:
        to_return = {}
        already_done = set()
        for token in tokens:
            if token in already_done:
                to_return[token] += 1
            else:
                to_return[token] = 1
                already_done.add(token)
        return to_return