from ctextinct.controller import Controller
import argparse

parserAndTrain = argparse.ArgumentParser(description="Parse a specific forum online and train chatbot with that data.")
parserAndTrain.add_argument("-u", "--url", type=str, metavar="",
                            help="Please specify the exact URL of the forum you would like to parse")
args = parserAndTrain.parse_args()


def parse_and_train(url):
    train_bot = Controller()
    train_bot.parse_cyber_security_forum_and_replace_training_data(url)


if __name__ == "parse_and_forum":
    parse_and_train(args.url)
else:
    print('This module cannot be imported or used by another module. Please run code from app.py file')
