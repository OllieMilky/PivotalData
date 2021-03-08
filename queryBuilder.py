import csv, nltk, time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

contentList = []
numberList = []

driver = webdriver.Firefox()

with open('tweetData.csv', encoding='mbcs') as file:
    reader = csv.reader(file)

    count = 0
    for row in reader:
        contentList.append(row[4])

        if count > 1560:
            break 

        count +=1 

contentList = contentList[1:]

with open('leadingPhrases.csv', newline='') as f:
    reader = csv.reader(f)
    phrases = list(reader)

for content in contentList:
    for phrase in phrases:
        if phrase[0] in content:
            tokens = nltk.word_tokenize(content)
            tags = nltk.pos_tag(tokens)
            for tag in tags:
                if tag[1] == 'CD':
                    print(content)
                    preceedingPhrase = phrase[0] +" "+ tag[0]
                    proceedingPhrase = tag[0] +" "+ phrase[0]
                    if (preceedingPhrase in content):
                        numberList.append(content)
                    if (proceedingPhrase in content):
                        numberList.append(content)

numberList = set(numberList)
for element in numberList:
    print(element)
    driver.get("https://www.google.com")
    time.sleep(2)
    searchBox = driver.find_element_by_name("q")
    searchBox.send_keys(element, Keys.ENTER)
    time.sleep(2)
    posts = driver.find_elements_by_class_name("yuRUbf")
    for post in posts:
        print(post.find_element_by_css_selector('a').get_attribute('href'))

