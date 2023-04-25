#
# TChatBot 
#
# > need to train your model for running properly, 
# feel free to use the code (MIT)
#
#
# Model translator: 
# usage: python3 model_translator.py <input file> <output file> <language>
#
# @author lboleslavsky, 2023
#

import os
import sys 
from googletrans import Translator

class ModelTranslator:
    
    def __init__(self, limit):
        self.TRANSLATE_LIMIT=limit

    def load(self, fileName):
        f = open(fileName, "r")
        self.messages = {}
        self.intents={}
        keys={}

        lines = f.readlines()
        request = ""
        i=0

        for line in lines:
            tokens = line.split("\t")
            key = tokens[0].strip()
            
            text="^^".join(tokens[1:-1])            
            
            if key not in keys:
                keys[key]="["+str(i)+" $]"
                self.intents[keys[key]]=key

            self.messages[i] = keys[key]+" "+text+"\n"           
            i+=1

        f.close()
        
        return request

    def process(self, text):
        for key in self.intents:
            #print(key+">"+self.intents[key])
            text = text.replace(key, self.intents[key]+"\t")

        text =  text.replace("^^","\t")    
        return text

    def translate(self, fileName, language):
        
        self.load(fileName)
        request = ""
        response = ""
        cnt=0
        i=0
        #TODO!
        translator = Translator()

        for key in self.messages:
            i+=1; 
            cnt += len(self.messages[key])
            request+=self.messages[key]

            if cnt>self.TRANSLATE_LIMIT or i>=len(self.messages):
                print("Translating chunk of data...")
                response += translator.translate(request, dest=language).text
                cnt=0
                request=""  

        output = self.process(response)
        
        return output

    def save(self, fileName, text):
        f = open(fileName, "w")
        f.write(text)



translator = ModelTranslator(2500)
text = translator.translate(sys.argv[1],sys.argv[3])
translator.save(sys.argv[2],text)

print(text)

