from ctextinct.controller import Controller
import argparse

trainUpdate = argparse.ArgumentParser(description="Train specific file")
parserAndTrain = argparse.ArgumentParser(description="Parse a specific forum online and train chatbot with that data.")
trainUpdate.add_argument("-f", "--fileName", type=str, metavar="",
                         help="Please specify the exact name of the jason file containing the training data")
parserAndTrain.add_argument("-u", "--url", type=str, metavar="",
                            help="Please specify the exact URL of the forum you would like to parse")
args = trainUpdate.parse_args()
args2 = parserAndTrain.parse_args()


def train(fileName):
    train_bot = Controller()
    train_bot.train_model(fileName)


def parse_and_train(url):
    train_bot = Controller()
    train_bot.parse_cyber_security_forum_and_replace_training_data(url)


def main():
    cyber_chatbot = Controller()
    print("main object initialised")
    cyber_chatbot.main()


if __name__ == "__main__":
    main()
if __name__ == "train":
    train(args.fileName)
if __name__ == "parse_and_forum":
    parse_and_train(args2.url)
else:
    print('This module cannot be imported or used by another module. Please run code from app.py file')
