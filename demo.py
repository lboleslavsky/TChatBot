#
# TChatBot 
#
# > need to train your model for running properly, 
# feel free to use the code (MIT)
#
# @author lboleslavsky, 2023
#

from chatbot import TChatBot
from conf import TChatBotConfig
import os

tchBot = TChatBot()
config = TChatBotConfig()

tchBot.load(config.INTENT_QUESTION_FILE, config.INTENT_ANSWERS_FILE, config.INTENT_CONTEXT_STRUCTURE_FILE, config.MODEL_FILE, config.DEFAULT_PHRASE, config.LANGUAGE, config.FORCE_TRAIN)
tchBot.contexts.append(config.INTENT_START_DIALOG)

sentence=""
while(tchBot.contexts[-1]!="CourtesyGoodBye" and tchBot.contexts[-1]!="GoodBye"):
    print(">", end=" ")
    sentence = input()
    
    print("---")
    print(tchBot.getResponse(sentence))
    print("["+tchBot.contexts[-1]+"]")
    print("---")
