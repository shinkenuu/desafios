import logging
from multiprocessing import Process, Queue
from os import environ

from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from telegram.ext import CommandHandler, Updater
from twisted.internet import reactor

from redditor.spiders.popstars import PopstarsSpider
from redditor.settings import OUTPUT_FILE as CRAWLING_OUTPUT_FILE

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger()


def nothing_to_do(bot, update, args):
    """
    Handler of TelegramBot command 'NadaPraFazer'.

    Look for popular threads on `subreddits` and send their data

    :param Bot bot: Telegram Bot
    :param Update update: Telegram Update
    :param list args: subreddits to look for. Format: ['subreddit1;subreddit2', ]
    """
    logger.info('nothing_to_do invoked with args: {}'.format(str(args)))

    subreddits = args[0].split(';')

    crawl_popular_reddit_threads(subreddits=subreddits)

    text = read_crawled_threads()

    bot.send_message(chat_id=update.message.chat_id, text=text)


def setup_telegram_bot():
    """
    Setup the Telegram bot and start listening for commands.
    """
    updater = Updater(token=environ.get('TELEGRAM_TOKEN'))

    nothing_to_do_handler = CommandHandler('NadaPraFazer', nothing_to_do, pass_args=True)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(nothing_to_do_handler)

    updater.start_polling()
    logger.info('Telegram Bot setup complete')


def crawl_popular_reddit_threads(subreddits: list):
    """
    Invoke PopstarsSpider to crawl data of subreddits
    :param list subreddits: list with subreddit's names
    """
    def crawl(queue):
        """
        Crawl spider and keep thread up to listen to another messages.
        """
        try:
            runner = CrawlerRunner(get_project_settings())
            deferred = runner.crawl(PopstarsSpider, subreddits=subreddits)
            deferred.addBoth(lambda _: reactor.stop())
            reactor.run()
            queue.put(None)
        except Exception as e:
            queue.put(e)

    queue = Queue()
    process = Process(target=crawl, args=(queue,))
    process.start()
    result = queue.get()
    process.join()

    if result is not None:
        raise result


def read_crawled_threads() -> str:
    """
    Read data crawled by PopstarsSpider
    :return: str in JSON format with subreddits data
    :rtype: str
    """
    with open(CRAWLING_OUTPUT_FILE, 'r') as file:
        file_content = file.read()

    return file_content


if __name__ == '__main__':
    setup_telegram_bot()
