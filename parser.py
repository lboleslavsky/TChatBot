#
# TChatBot 
#
# > need to train your model for running properly, 
# feel free to use the code (MIT)
#
# @author lboleslavsky, 2023
#

import os

#
# Parse intents (for question and answers)
#
class IntentParser():
    def parse(self, fileName):
        f = open(fileName, "r")
        messages = {}
        lines = f.readlines()
        for line in lines:
            tokens = line.split("\t")
            tokens[0] = tokens[0].strip()
            if tokens[0] not in messages:
                messages[tokens[0]] = []

            messages[tokens[0]] = tokens[1:-1]

        f.close()
        #print("parsed intents: "+str(len(messages)))
        return messages

    def parseAnswers(self, fileName):
        f = open(fileName, "r")
        messages = {}
        lines = f.readlines()
        for line in lines:
            tokens = line.split("\t")
            tokens[0] = tokens[0].strip()
            if tokens[0] not in messages:
                messages[tokens[0]] = []

            messages[tokens[0]].append(tokens[1])

        f.close()
        #print("answers: "+str(len(messages)))
        return messages

    def parseStructure(self, fileName):
        f = open(fileName, "r")
        structure = {}
        lines = f.readlines()
        for line in lines:
            tokens = line.split("\t")
            tokens[0] = tokens[0].strip()
            if tokens[0] not in structure:
                structure[tokens[0]] = []

            structure[tokens[0]].append(tokens[1].strip())

        f.close()
        #print("structure: "+str(len(structure)))
        return structure
