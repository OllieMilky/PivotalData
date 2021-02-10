import csv, nltk

contentList = []

with open('Draft1.csv', encoding='mbcs') as file:
    reader = csv.reader(file)

    count = 0
    for row in reader:
        print(row)
        contentList.append(row[4])

        if count > 1560:
            break 

        count +=1 

contentList = contentList[1:]
print(contentList)

for content in contentList:
    tokens = nltk.word_tokenize(content)
    tags = nltk.pos_tag(tokens)
    for tag in tags:
        if tag[1] == 'CD':
            print(tag)