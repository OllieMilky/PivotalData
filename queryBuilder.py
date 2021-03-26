import csv, nltk, time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

contentList = []
numberList = []

driver = webdriver.Firefox()

#Tweet data is loaded in from the CSV, but only the actual Tweet content
with open('tweetData.csv', encoding='mbcs') as file:
    reader = csv.reader(file)

    count = 0
    for row in reader:
        contentList.append(row[4]) # Just extract the content of each tweet, not the metadata

contentList = contentList[1:] # Remove the headings from the list

# Leading phrases loaded into phrases
with open('leadingPhrases.csv', newline='') as f:
    reader = csv.reader(f)
    phrases = list(reader)

# Function for tokenising words and looking for queries by comparing with leading phrases 
for content in contentList:
    for phrase in phrases:
        if phrase[0] in content: # If leading phrase in tweet
            tokens = nltk.word_tokenize(content) # Tokenise
            tags = nltk.pos_tag(tokens) # POS tag
            for tag in tags: # For each word/tag pair
                if tag[1] == 'CD': # If word is a number
                    print(content) # Print tweet
                    preceedingPhrase = phrase[0] +" "+ tag[0] # Create possible matching queries
                    proceedingPhrase = tag[0] +" "+ phrase[0]
                    if (preceedingPhrase in content): # Check if matching phrase is in the Tweet
                        numberList.append(content)
                    if (proceedingPhrase in content):
                        numberList.append(content)

# Inputs each query into the google search engine before returning the top URLs of search results 
numberList = set(numberList) # Removes duplicate data values
for element in numberList: # For each query 
    print(element)
    driver.get("https://www.google.com") # Go to Google
    time.sleep(2) # Wait for webpage to load
    searchBox = driver.find_element_by_name("q") # Find the search box
    searchBox.send_keys(element, Keys.ENTER) # Input element into search box
    time.sleep(2)
    posts = driver.find_elements_by_class_name("yuRUbf") # Find post results in returned HTML
    for post in posts:
        print(post.find_element_by_css_selector('a').get_attribute('href')) # Print the URL 

