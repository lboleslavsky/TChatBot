#
# TChatBot 
#
# > need to train your model for running properly, 
# feel free to use the code (MIT)
#
# @author lboleslavsky, 2023
#

import gensim.models as gLoader
import random
import spacy_udpipe
import gensim
import multiprocessing
import os
from parser import IntentParser
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.utils import simple_preprocess

#
# Data with tagged documents with intents as key
#
class TaggedData(object):

    def __init__(self,data, chatbot):
        self.data=data
        self.chatbot=chatbot

    def lemmatize(self, text):
        doc=self.chatbot.nlp(text)
        lemmas=[]
        for token in doc:
            if(token.is_alpha):
                lemmas.append(token.lemma_)

        return lemmas

    def __iter__(self):
        for key in self.data:
        	for text in self.data[key]:
		        yield TaggedDocument(words=self.lemmatize(text.strip()),tags=[key])  

#
# Chatbot class, you can load and save models, and chat with it
#
class TChatBot():

    #
    # Load a chabot
    #
    # @intentFileName - file with question intents
    # @dataFileName - file with answers 
    # @structFileName - file with intent struct context
    # @doc2vecModelFileName - model file
    # @defaultPhrase - default chat phrase
    # @language - model language
    #
    def load(self, intentFileName, dataFileName, structFileName, doc2vecModelFileName, defaultPhrase, language, isTrainFingForced=False):
        parser = IntentParser()
        data = parser.parse(intentFileName)
        answers = parser.parseAnswers(dataFileName)
        structure = parser.parseStructure(structFileName)
        self.isTrainFingForced=isTrainFingForced
        self.language = language
        self.contexts = []
        self.actionHandlers = []
        self.init(data, answers, structure, doc2vecModelFileName, defaultPhrase)

    #
    # Initialize chatbot and load model by language
    #
    def init(self, data, answers, structure, doc2vecModelFileName, defaultPhrase):
        self.answers = answers
        self.structure = structure        
        self.nlp = spacy_udpipe.load(self.language)
        self.tagged_data = TaggedData(data, self)
        self.defaultPhrase = defaultPhrase

        if not self.isTrainFingForced:
            self.model = gLoader.Doc2Vec.load("models/"+self.language+"_"+doc2vecModelFileName)         
        else:
            print("Traing model...")
            self.trainAndSaveModel(doc2vecModelFileName)
            print("OK - Model trained.")
    #
    # Method to train and save a model to file 
    #    
    def trainAndSaveModel(self, fileName):
        cores = multiprocessing.cpu_count()

       
        self.model = Doc2Vec(vector_size=200, workers=cores, min_count=1, window=3, negative=5)        
        self.model.build_vocab(self.tagged_data)
        self.model.train(self.tagged_data, total_examples=self.model.corpus_count, epochs=500)       
        
        if not os.path.exists('models'):
            os.makedirs('models')
        
        self.model.save("models/"+self.language+"_"+fileName)

    #
    # MEthod to set action handlers
    #
    def setActionHandlers(self, actionHandlers):
        self.actionHandlers = actionHandlers

    #
    # Method to force action handlers to intents
    #
    def actionSlot(self, message, intent):
        for handler in self.actionHandlers:
            r = handler.action(self, message, intent)
            if r != None:
                return r

        return None

    #
    # Adding answers to intent
    #
    def addMessage(self, key,  message):
        if key not in self.answers:
            self.answers[key] = []

        else:
            self.answers[key].append(message)

    #
    # Select array with answers associated with required intent key
    #
    def getMessagesByKey(self, key):

        if key in self.answers:
            return self.answers[key]

        return None

    #
    # Method to parse to lemmas from a sentence, and creating new vector for comparsion to similar ones
    #
    def getCategory(self, sentence):
        
        tokens=self.tagged_data.lemmatize(sentence)
        
        print(tokens)
        
        vector = self.model.infer_vector(tokens)

        index = self.model.dv.most_similar([vector], topn = 10)
        key = index[0][0]
        k = "undefined"
        if self.isInContext(key):
            k = key
        return k

    #
    # Method to determine, if intent is in the required context
    #
    def isInContext(self, key):
        if key in self.structure:
            for item in self.structure[key]:
                if item in self.contexts:
                    return True
                else:
                    return False
        return True

    #
    # Method to connect a callback to message response
    #
    def getCallbackResponse(self, message, callback):
        r = self.getResponse(message)
        callback(r)
        return r

    #
    # Method to retrieve a chatbot response to current message
    #
    def getResponse(self, message):

        if(len(message) < 2):
            return self.defaultPhrase

        c = self.getCategory(message)
        self.contexts.append(c)

        x = self.actionSlot(message, c)
        if x != None:
            return x
        if c in self.answers:
            return random.choice(self.getMessagesByKey(c))

        else:
            return self.defaultPhrase

