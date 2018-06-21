import requests
import re
import twitter
import logging

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
    twitter_api = twitter.Api(consumer_key=credentials.get_consumer_key(),
                              consumer_secret=credentials.get_consumer_secret(),
                              access_token_key=credentials.get_access_token_key(),
                              access_token_secret=credentials.get_access_token_secret())

    # Parse Dictionary
    dictionary = open('./dictionary/google-10000-english.txt').read().split('\n')

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
    for word in dictionary:
        match = re.search(word, babel['text'])

        if match:
            found_words.append(match.group(0))

    if len(found_words) > 0:
        longest_words = sorted(found_words, key=len)[-1:-4:-1]  # Longest 3 Words
        logging.info('Longest Words: {words}'.format(words=longest_words))

    # Post a Tweet
    hashtags = ['#libraryofbabel', '#babeldictionary']
    tweet = "\U0001f4da {title} \n\n Total Words: {total_words}\n \U0001f947 {first}\n \U0001f948 " \
            "{second}\n \U0001f949 {third} \n\n \U0001f517 {url} {hashtags}" \
        .format(title=babel['title'], total_words=len(list(filter(lambda x: len(x) >= 3, found_words))),
                first=longest_words[0], second=longest_words[1], third=longest_words[2], url=request.url,
                hashtags=' '.join(hashtags))

    # twitter_api.PostUpdate(status=tweet)


if __name__ == '__main__':
    main()
