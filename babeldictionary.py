import requests
import twitter
import logging
import sys
import watchtower

from datetime import datetime
from credentials import TwitterCredentials
from lxml import html

# Logging Config
logging.basicConfig(level=logging.INFO, format='[Babel Dictionary][%(levelname)s] %(asctime)s: %(message)s')
logger = logging.getLogger(__name__)
logger.addHandler(watchtower.CloudWatchLogHandler())


# noinspection PyTypeChecker
def main():
    """
    Main Function
    """

    # API Setup (Twitter)
    logger.info('Initializing Twitter API')
    credentials = TwitterCredentials('./twitter_secrets.json')
    twitter_api = twitter.Api(consumer_key=credentials.get_consumer_key(),
                              consumer_secret=credentials.get_consumer_secret(),
                              access_token_key=credentials.get_access_token_key(),
                              access_token_secret=credentials.get_access_token_secret())

    # Parse Dictionary
    with open('./dictionary/words_alpha.txt', encoding='utf-8') as file:
        dictionary = set(file.read().split())

    # Request Library of Babel Page & Parse
    logger.info('Requesting Library of Babel Page')

    try:
        request = requests.get('https://libraryofbabel.info/random.cgi?', timeout=5)
    except requests.exceptions.RequestException as error:
        logger.error(error)
        sys.exit(1)

    tree = html.fromstring(request.content)

    babel = {
        'title': tree.xpath('//h3[1]/text()')[0],
        'text': tree.xpath('//pre[@id="textblock"]/text()')[0]
    }

    found_words = set()

    logger.info('Searching...')
    search_start = datetime.now()
    for word in dictionary:
        if word in babel['text']:
            found_words.add(word)

    search_time = (datetime.now() - search_start).microseconds / 1000
    if len(found_words) > 0:
        longest_words = sorted(found_words, key=len, reverse=True)[1:4]  # Longest 3 Words
        logger.info('Dictionary search took {}ms...'.format(search_time))
        logger.info('Matches: {matches} - Longest Words: {words}'.format(matches=len(found_words), words=longest_words))
    else:
        logger.warning('No matches were found, did something go wrong?')

    # Post a Tweet
    hashtags = ['#libraryofbabel', '#babeldictionary']
    tweet = "\U0001f4c3 {title}\n\n" \
            "Total Words (3 letters or longer): {total_words}\n" \
            "\U0001f947 {first_word}\n" \
            "\U0001f948 {second_word}\n" \
            "\U0001f949 {third_word}\n\n" \
            "\U0001f517 {url} {hashtags}" \
        .format(title=babel['title'], total_words=len([x for x in found_words if len(x) >= 3]), first_word=longest_words[0],
                second_word=longest_words[1], third_word=longest_words[2], url=request.url, hashtags=' '.join(hashtags))

    logger.info('Posting to Twitter')
    twitter_api.PostUpdate(status=tweet)


if __name__ == '__main__':
    main()
