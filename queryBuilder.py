import csv, nltk

contentList = []

with open('Draft1.csv', encoding='mbcs') as file:
    reader = csv.reader(file)

    count = 0
    for row in reader:
        contentList.append(row[4])

        if count > 5:
            break 

        count +=1 

print(contentList)