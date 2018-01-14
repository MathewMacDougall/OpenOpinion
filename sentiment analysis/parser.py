
import json
from subprocess import call
from sys import argv
import time

if len(argv) == 2:
    input_file = open('input.txt', 'w')
    input_file.write(argv[1])
    input_file.close()

    call(['java', '-cp', '"*"', '-Xmx2g', 'edu.stanford.nlp.pipeline.StanfordCoreNLP', '-annotators', 'tokenize,ssplit,parse,pos,sentiment', '-file', 'input.txt', '-outputFormat', 'json'])



json_file = open('input.txt.json').read()
data = json.loads(json_file)['sentences']

nouns = []
sentenceSentimentScore = []

for sentence in data:
    words = str(sentence['parse']).split()
    if '(NNP' in words:
        noun = words[words.index('(NNP')+1:[words.index(x) for x in words if x.endswith('))')][0]+1]
        if '(NNP' in noun:
            noun.remove('(NNP')
        noun = ' '.join(noun).replace(')', '')
        nouns.append(noun)

    sentenceSentimentScore.append(int(sentence['sentimentValue']) * (sentence['sentiment'] == 'Negative' and -1 or 1))

print nouns
print sentenceSentimentScore
