from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common import exceptions
from selenium.webdriver.common.keys import Keys
import time
import pandas

#List of terms to be searched for on Twitter. These can be changed to suit subject matter
searchTerms = ['COVID', 'Vaccine', 'COVID19', 'coronavirus', 'COVID-19']

url = 'https://twitter.com/login' # First navigation to Twitter
driver = webdriver.Firefox() #Can be edited if using Chrome etc 

#Used to derive the searching page while inputting the search terms as a hashtag
def base_url(
    hashtag): return "https://twitter.com/search?q=lang%3Aen%20%23{}&src=typed_query&f=live".format(hashtag)

#Function for trawling through the HTML of the page and collecting the correct elements
def getTweetData(card, term):

    # Username
    Username = card.find_element_by_xpath('.//span').text
    Username = Username.encode('ascii', 'ignore') # Usernames can contain strange characters so encoded to basic chars
    print()
    Username = str(Username).replace("b'", "") #Replace strange chars
    Username = str(Username).replace("\\n", "")
    Username = Username[:-1] #Remove final username character added by Twitter
    # print(Username)

    # Twitter Handle
    Handle = card.find_element_by_xpath('.//span[contains(text(), "@")]').text
    # print(Handle)

    # Postdate
    PostDate = card.find_element_by_xpath(
        './/time').get_attribute('datetime')
    print(PostDate)

    # Content
    Comment = card.find_element_by_xpath('.//div[2]/div[2]/div[1]').text
    Response = card.find_element_by_xpath('.//div[2]/div[2]/div[2]').text
    Content = Comment + Response
    Content = Content.encode('ascii', 'ignore')

    Content = str(Content).replace("b'", "")
    Content = str(Content).replace("b\"", "")
    Content = str(Content).replace("\\n", "")
    Content = Content[:-1]
    # print(Content)

# Reply count
    ReplyCount = card.find_element_by_xpath(
        './/div[@data-testid="reply"]').text
    print(ReplyCount)

# Retweet count
    RetweetCount = card.find_element_by_xpath(
        './/div[@data-testid="retweet"]').text
    print(RetweetCount)

# Likes count
    LikesCount = card.find_element_by_xpath('.//div[@data-testid="like"]').text
    print(LikesCount)

#Data is then stored in a list before being returned
    tweet = (term, Username, Handle, PostDate, Content,
             ReplyCount, RetweetCount, LikesCount)
    return tweet

#Function for inputting a new search term and scrolling down
def scrapePage(localUrl, n, term, tweetData):
    driver.get(localUrl) # Access search URL
    driver.implicitly_wait(5) # Wait for page to load
    driver.find_element_by_link_text('Latest').click() # Navigate to 'latest' tab
    data = []
    tweet_ids = set() 
    last_pos = driver.execute_script("return window.pageYOffset;") # Find last scrolling position
    scrolling = True
    scrollNo = 0

    while scrolling: # Continue to scroll, loading new Tweets
        cards = driver.find_elements_by_xpath('//div[@data-testid="tweet"]') # Finds each tweet
        for card in cards: # For each loaded tweet
            data = getTweetData(card, term)
            if data: # If successful 
                tweet_id = ''.join(data)
                if tweet_id not in tweet_ids: # Used to check that Tweets aren't being added more than once
                    tweet_ids.add(tweet_id)
                    tweetData.append(data)

        scrollAttempt = 0
        while True:
            # check scroll position
            driver.execute_script(
                'window.scrollTo(0, document.body.scrollHeight);')
            scrollNo += 1
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" + str(scrollNo))
            if scrollNo >= n: # Value of n can be changed to scroll more than once per search
                scrolling = False
                break
            time.sleep(3)
            curr_position = driver.execute_script("return window.pageYOffset;") # Continue to scroll
            if last_pos == curr_position:
                scrollAttempt += 1
                if scrollAttempt >= 3:
                    scrolling = False
                    break
                else:
                    time.sleep(3)
            else:
                last_pos = curr_position
                break
    return(tweetData)

#Function for saving the tweets to a CSV. The commented out line is for use when an empty csv is being used/first set up
def saveTweets(searchTerms, n):
    tweetList = []
    for term in searchTerms:
        print()
        print('Scraping for #{}'.format(term))
        tweetList = scrapePage(base_url(term), n, term, tweetList)
    df = pandas.DataFrame(tweetList) # Pandas used to store tweets in a dataframe
    # df.to_csv('tweetData.csv', encoding='utf-8', index=False, header=[
    #           "Search Term", "Username", "Handle", "PostDate", "Content", "Comments", "Retweets", "Likes"])
    old = pandas.read_csv('tweetData.csv', header=None)
    old = old.append(df, ignore_index=True)
    new = old.drop_duplicates() # Duplicate tweets removed
    new.to_csv('tweetData.csv', # New information stored in CSV format
               encoding='utf-8', index=False)

#Function used to wait while the web pages are allowed to load
def waiting_function(by_variable, attribute):
    try:
        WebDriverWait(driver, 20).until(
            lambda x: x.find_element(by=by_variable, value=attribute))
    except (NoSuchElementException, TimeoutException):
        print(' {} {} not found'.format(by_variable, attribute))
        exit()

#Main function - logs into Twitter and then continues to scrape tweets indefinitely
if __name__ == '__main__':
    driver.get(url)

    waiting_function('name', 'session[username_or_email]')
    email = driver.find_element_by_name('session[username_or_email]')
    password = driver.find_element_by_name('session[password]')
    email.send_keys('LaneTrance') # Username, can be edited
    password.send_keys('PivotalData', Keys.ENTER) # Password for account, can be edited

    while True:
        saveTweets(searchTerms, 1) # The number '1' can be changed so that you can scroll more than once per search
    driver.quit()
