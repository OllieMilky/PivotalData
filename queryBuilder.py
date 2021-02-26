import csv
import nltk
import pandas

contentList = []
queryPhrases = []

with open('tweetData.csv', encoding='mbcs') as file:
    reader = csv.reader(file)

    count = 0
    for row in reader:
        # print(row)
        contentList.append(row[4])

contentList = contentList[1:]
# print(contentList)

for content in contentList:
    tokens = nltk.word_tokenize(content)
    tags = nltk.pos_tag(tokens)
    for tag in tags:
        if tag[1] == 'CD':
            print(tag)
            phrases = pandas.read_csv('leadingPhrases.csv')
            for phrase in phrases:
                if phrase in content:
                    queryPhrases.append(content)

print(queryPhrases)
