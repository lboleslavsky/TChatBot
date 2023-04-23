#
# TChatBot 
#
# > need to train your model for running properly, 
# feel free to use the code (MIT)
#
# @author lboleslavsky, 2023
#

#
# Configuration class for chatbot
#
class TChatBotConfig:
    
    def __init__(self):
        
        self.FORCE_TRAIN=False
        self.INTENT_QUESTION_FILE="models/chbot1/intent_questions.txt"
        self.INTENT_ANSWERS_FILE="models/chbot1/intent_answers.txt"
        self.INTENT_CONTEXT_STRUCTURE_FILE="models/chbot1/structure.txt"
        self.MODEL_FILE="doc2vec.bin"

        # dialog start to context structure
        self.INTENT_START_DIALOG = "DialogStart" 
        self.DEFAULT_PHRASE = "What?"
        self.LANGUAGE="en"



