# import firebase_admin
# from firebase_admin import db
import json
import string
#  from newsapi import NewsApiClient
from newsapi.newsapi_client import NewsApiClient
from pandas import json_normalize
from bs4 import BeautifulSoup
import requests
import copy
import random  # required for choosing a random response
import pickle  # Python object serialization
import numpy as np
import nltk  # natural language tool kit
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD
import tensorflow as tf


class Model:
    def __init__(self):
        # self.cred_obj = firebase_admin.credentials.Certificate(
        #     r"docs/files/ctextinct-firebase-adminsdk-xnpem-e13f73b9d2.json")
        # self.default_app = firebase_admin.initialize_app(self.cred_obj, {
        #     'databaseURL': "https://ctextinct-default-rtdb.europe-west1.firebasedatabase.app/"
        # })
        # self.main_ref = db.reference("/")  # setting reference to the root of the table
        self.main_target = {}
        self.trained_model = load_model("docs/files/chatbot.h5")
        self.tagList = pickle.load(open("docs/files/tagList.pk1", "rb"))
        self.wordList = pickle.load(open("docs/files/wordList.pk1", "rb"))  # read binary
        self.intents_dictionary = json.loads(open("docs/files/intents.json").read())
        # cybersecurityforum.json or intents.json
        self.lemmatizer = WordNetLemmatizer()  # calling the wordNetLemmatizer constructor
        # the lemmatizer will reduce the word to its stem. For example, work, working, worked, works is all the same
        # stem word as "work". Wordnet is an large, freely and publicly available lexical database for the
        # English language aiming to establish structured semantic relationships between words.
        print("Model Initialised")

    # def write_to_database(self):
    #     self.main_ref = db.reference("/")
    #     self.main_target = self.main_ref.get()
    #     self.main_ref.set({
    #         "News":
    #             {
    #                 "Article": -1
    #             }
    #     })
    #     ref = db.reference("/News/Article")
    #
    #     # with statement automatically closes the file handler
    #     with open(r"docs/files/feedback_responses.json", "r") as file_handler:
    #         file_contents = json.load(file_handler)  # convert json to python dictionary
    #     print(file_contents)
    #     for key, value in file_contents.items():
    #         ref.push().set(value)
    #
    # def update_database(self):
    #     for key, value in self.main_target.items():
    #         if value["Author"] == "J.R.R. Tolkien":
    #             value["Price"] = 90
    #             self.main_ref.child(key).update({"Price": 80})
    #
    # def retrieve_data_from_database(self):
    #     ref = db.reference("/Books/Best_Sellers/")
    #     print(ref.order_by_child("Price").get())
    #     ref.order_by_child("Price").limit_to_last(1).get()
    #     ref.order_by_child("Price").limit_to_first(1).get()
    #     ref.order_by_child("Price").equal_to(80).get()
    #
    # def delete_data_from_database(self):
    #     ref = db.reference("/Books/Best_Sellers")
    #     for key, value in self.main_target.items():
    #         if value["Author"] == "J.R.R. Tolkien":
    #             ref.child(key).set({})

    @staticmethod
    def connect_to_news_api():
        newsapi = NewsApiClient(
            api_key='1fa3d77b9ae7460c833ef91fe447eca4')  # generated my own api key by registering
        country = "gb"
        category = "technology"
        top_titles = newsapi.get_top_headlines(category=category,
                                               language='en', country=country)
        top_titles = json_normalize(top_titles['articles'])  # top_headlines organised in json format
        print(top_titles)
        new_df = top_titles[["title", "url"]]  # grabbing each top titles' title and urls
        dic = new_df.set_index('title')['url'].to_dict()
        return dic
        # creating dictionary with the value being the url and the title as the key

    # "https://cybersecurityforum.com/cybersecurity-faq/"
    @staticmethod
    def cyber_security_forum_parser(url):
        url = url
        filename = url.split("/")[2].split(".")[
                       0] + ".json"  # will return file name cybersecurityforum.json
        forum_question_class_name = "faq-question"
        forum_answer_class_name = "faq-answer"

        fake_browser = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0'}
        response = requests.get(url, headers=fake_browser)  # get all the text from specified url

        parser = BeautifulSoup(response.content, features="html.parser")
        # save content of forum into variable parser aby using the html parser in BeautifulSoup()

        questions = [q.text.strip() for q in
                     parser.find_all("div", class_=forum_question_class_name)]
        # a single trailing underscore as seen above is used by convention to avoid conflicts with Python keywords.
        answers = [q.text.strip() for q in
                   parser.find_all("div", class_=forum_answer_class_name)]
        # all questions and answers from each div is collected as a list
        dataset_dict = dict(tag="", patterns=[], responses=[])
        # I will need to manually edit the resulting file with reasonable tags for each question
        intents = []
        # using zip to join the question and answer lists together
        for q, a in zip(questions, answers):
            temp = copy.deepcopy(
                dataset_dict)  # deepcopy is a method of the module copy in python that allowed
            # me to do an independent copy of the dictionary instead of just referencing it
            get_letters = string.ascii_lowercase  # get all possible letters
            temp["tag"] = ''.join(random.choice(get_letters) for i in range(15))  # create random characters for the tag
            temp["patterns"].append(q)  # here i am filling the empty lists with the questions
            temp["responses"].append(a)
            intents.append(temp)

        intents_dict = {"intents": intents}

        with open("docs/files/" + filename, "w") as f:
            json.dump(intents_dict, f, indent=2, sort_keys=False)  # indent by 4 spaces and do not sort the keys

    def training_model(self):
        # physical_devices = tf.config.list_physical_devices('CPU')
        # tf.config.experimental.set_memory_growth(physical_devices[0], True)
        # used when training using CUDA and NVIDIA Graphics card.
        self.intents_dictionary = json.loads(open("docs/files/intents.json").read())
        # created 3 empty lists and the letters this program will ignore
        wordList_t = []
        tagList_t = []
        documentList_t = []  # this list will be used for the linked tokenized words and tags
        ignoredCharList_t = ["?", "!", ",", "."]
        # I am iterating over the intents
        for intent in self.intents_dictionary["intents"]:
            # for each of the patterns, the below will tokenize the sentences.
            # Meaning the sentences will split into words.
            for pattern in intent["patterns"]:
                listOfWords = nltk.word_tokenize(pattern)
                wordList_t.extend(listOfWords)
                documentList_t.append((listOfWords, intent["tag"]))
                # for each tag discovered, if not added to the classes list yet, it becomes added.
                if intent["tag"] not in tagList_t:
                    tagList_t.append(intent["tag"])

        print(documentList_t)  # testing purposes
        # replacing the contents of wordList with a lemmatized version excluding the "ignore_letters"
        wordList_t = [self.lemmatizer.lemmatize(eachWord) for eachWord in wordList_t if
                      eachWord not in ignoredCharList_t]

        # to eliminate the duplicates and sort the list
        wordList_t = sorted(set(wordList_t))
        tagList_t = sorted(set(tagList_t))
        print(wordList_t)  # testing purposes
        print(tagList_t)  # testing purposes
        # Next, I am saving the data into files. Pickling is a way to convert a python object (list, dict, etc.) into a
        # character stream. The idea is that this character stream contains all the information necessary to
        # reconstruct the object in another python script.
        pickle.dump(wordList_t, open("docs/files/wordList.pk1", "wb"))  # write binary
        pickle.dump(tagList_t, open("docs/files/tagList.pk1", "wb"))

        # The above organised data is not yet numerical, which is what we need for a machine learning algorithm.
        # The below code assigns 0 or 1 to each of the words depending on
        training = []
        outputEmpty = [0] * len(tagList_t)  # as many 0 as there are tags
        # turning our data into Matrices, (harder than image data (because RGB uses numbers))
        for document in documentList_t:  # document = (array,tag) array is made up of words from a "pattern"
            bag = []  # bag of words model used here--- the inputs of 1s & 0s into the machine learning algorithm
            wordPatterns = document[0]  # each document is a list of (pattern and related tag)
            wordPatterns = [self.lemmatizer.lemmatize(eachWord.lower()) for eachWord in wordPatterns]
            # if a word in wordlist is equal to word in wordPatterns than add 1 to bag, if not add 0.
            for eachWord in wordList_t:
                bag.append(1) if eachWord in wordPatterns else bag.append(0)

            outputRow = list(outputEmpty)  # copying outputEmpty into OutputRow.
            outputRow[tagList_t.index(document[1])] = 1  # The output row is the "Prediction" of the related tag
            training.append([bag, outputRow])  # example: bag(10100010101000000000100001001000) outputRow(000010000)
            # how many words relate to a certain tag
        # preprocessing the data
        random.shuffle(training)
        training = np.array(training)  # converting to numpy array

        trainX = list(training[:, 0])  # train the words
        trainY = list(training[:, 1])  # train the tags


        # Start of building Neural Network model
        # Keras need to know the shape of their inputs in order to be able to create their weights.
        # the shape of the weights depends on the shape of the inputs
        model_t = Sequential()  # single input, will get single output, before moving to next input. this has 5 layers.
        model_t.add(Dense(128, input_shape=(len(trainX[0]),), activation="relu"))  # 128 nodes in first layer
        model_t.add(Dropout(0.5))
        model_t.add(Dense(64, activation="relu"))  # using relu to decide which neurons are activated for each layer
        model_t.add(Dropout(0.5))
        model_t.add(Dense(len(trainY[0]), activation="softmax"))  #
        # SGD stands for Stochastic gradient descent (optimizer)
        # model.compile specifies network configurations
        sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)  # lr = learning rate
        model_t.compile(loss="categorical_crossentropy", optimizer=sgd, metrics=["accuracy"])
        # train model and save in a Hierarchical Data Format file
        hist = model_t.fit(np.array(trainX), np.array(trainY), epochs=200, batch_size=5, verbose=1)
        print(model_t.weights)
        print(model_t.summary())
        model_t.save("docs/files/chatbot.h5", hist)
        print("Done")

    # this function tokenizes each word in the sentence and lemmatizes it.
    def cleanup_sentence(self, sentence):
        sentence_words = nltk.word_tokenize(sentence)
        sentence_words = [self.lemmatizer.lemmatize(eachWord) for eachWord in sentence_words]
        return sentence_words

    # convert a sentence into Bag of Words. A list of 0s or 1s to indicate if a word is there or not.
    def bag_of_words(self, sentence):
        sentence_words = self.cleanup_sentence(sentence)
        bag = [0] * len(self.wordList)
        for x in sentence_words:
            for i, thisWord in enumerate(self.wordList):
                if thisWord == x:
                    bag[i] = 1
        return np.array(bag)

    # for predicting the tag based on the sentence inputted
    def predict_tag(self, sentence):
        bag_of_w = self.bag_of_words(sentence)  # this will be inputted into the neural network
        result_tag = self.trained_model.predict(np.array([bag_of_w]))[0]  # 0 added to match the format
        print("Result tag after going through trained model: " + str(result_tag))
        ERROR_THRESHOLD = 0.0025  # should set it to 0.25 but testing
        percentage_res = [[i, r] for i, r in enumerate(result_tag) if r > ERROR_THRESHOLD]
        percentage_res.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in percentage_res:
            return_list.append({"intent": self.tagList[r[0]], "probability": str(r[1])})
        print("PREDICT TAG : " + str(return_list))
        return return_list

    # for giving a response
    def get_response(self, intents_list, intents_json):
        result_response = ""
        tag = intents_list[0]["intent"]  # only choose the first tag (one with the highest percentage)
        list_of_intents = intents_json["intents"]
        # Go through all intents in original json file and find the intent with the matching tag, choose random answer
        for i in list_of_intents:
            if i["tag"] == tag:
                result_response = random.choice(i["responses"])
                break
        print("from GETRESPONSE def: "+ result_response)
        return result_response

    def ask_question(self, user_question):
        if user_question == "":
            user_question = "Hi"
        ints = self.predict_tag(user_question)
        response = self.get_response(ints, self.intents_dictionary)
        print("From model response : "+ response)
        return response