from configparser import ConfigParser
import tweepy
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


class SimpleTwitterBot:
    def __init__(self):  # Coleta os dados para acessar o twitter
        config = ConfigParser()
        config.read(os.path.join(__location__, '.config'))
        consumer_key = config['TWITTER']['consumer_key']
        consumer_secret = config['TWITTER']['consumer_secret']
        access_token = config['TWITTER']['token']
        access_token_secret = config['TWITTER']['secret']

        # Realiza a conexão ao twitter
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)

    def tweet(self, string):
        self.api.update_status(string)


if __name__ == "__main__":
    bot = SimpleTwitterBot()
    bot.tweet("teste")
