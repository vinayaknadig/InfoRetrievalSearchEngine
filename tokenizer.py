import json
import re
from lxml import etree
import lxml.html
from bs4 import BeautifulSoup

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
            soup = BeautifulSoup(content['content'], 'lxml')
            for i in range(2):
                if soup.find('strong'):
                    lines.extend(soup.find('strong').text.split())
                if soup.find('title'):
                    lines.extend(soup.find('title').text.split())
                if soup.find('h1'):
                    lines.extend(soup.find('h1').text.split())
                if soup.find('h2'):
                    lines.extend(soup.find('h2').text.split())
                if soup.find('h3'):
                    lines.extend(soup.find('h3').text.split())
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