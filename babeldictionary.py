import requests
import re
import twitter
import logging

from datetime import datetime
from credentials import TwitterCredentials
from lxml import html

# Logging Config
logging.basicConfig(level=logging.INFO, format='[Babel Dictionary][%(levelname)s] %(asctime)s: %(message)s')


def main():
    """
    Main Function
    """

    # API Setup (Twitter)
    logging.info('Initializing Twitter API')
    credentials = TwitterCredentials('./twitter_secrets.json')
    TwitterAPI = twitter.Api(consumer_key=credentials.get_consumer_key(),
                             consumer_secret=credentials.get_consumer_secret(),
                             access_token_key=credentials.get_access_token_key(),
                             access_token_secret=credentials.get_access_token_secret())

    # Parse Dictionary
    with open('./dictionary/words_alpha.txt') as file:
        dictionary = set(file.read().split('\n'))

    # Request Library of Babel Page & Parse
    logging.info('Requesting Library of Babel Page')
    request = requests.get('https://libraryofbabel.info/random.cgi?')

    if not request.ok:
        logging.ERROR('The request could not be completed...')
        raise requests.ConnectionError('The request could not be completed!')

    logging.info('Request Success!')
    tree = html.fromstring(request.content)

    babel = {
        'title': tree.xpath('//h3[1]/text()')[0],
        'text': tree.xpath('//pre[@id="textblock"]/text()')[0]
    }

    found_words = []

    logging.info('Searching...')
    search_start = datetime.now()
    for word in dictionary:
        if word in babel['text']:
            found_words.append(word)

    search_time = (datetime.now() - search_start).microseconds
    if len(found_words) > 0:
        longest_words = sorted(found_words, key=len)[-1:-4:-1]  # Longest 3 Words
        logging.info('Dictionary search took {}ms...'.format(search_time))
        logging.info('Matches: {matches} - Longest Words: {words}'.format(matches=len(found_words), words=longest_words))
    else:
        logging.warning('No matches were found, did something go wrong?')

    # Post a Tweet
    hashtags = ['#libraryofbabel', '#babeldictionary']
    tweet = "\U0001f4c3 {title}\n\n" \
            "Total Words (3 letters or longer): {total_words}\n" \
            "\U0001f947 {first_word}\n" \
            "\U0001f948 {second_word}\n" \
            "\U0001f949 {third_word}\n\n" \
            "\U0001f517 {url} {hashtags}" \
        .format(title=babel['title'], total_words=len(list(filter(lambda x: len(x) >= 3, found_words))),
                first_word=longest_words[0], second_word=longest_words[1], third_word=longest_words[2], url=request.url,
                hashtags=' '.join(hashtags))

    print(tweet)

    logging.info('Posting to Twitter')
    TwitterAPI.PostUpdate(status=tweet)


if __name__ == '__main__':
    main()
