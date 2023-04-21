#
# TChatBot 
#
# > need to train your model for running properly, 
# feel free to use the code (MIT)
#
# @author lboleslavsky, 2023
#

#
# Class to handle your custom actions (parse entities)
#
class ActionHandler():

    def parse():
        pass

    def action(self, chb, message, intent):
        if intent == "WhoAmI":
            print(chb.parseEntities(message))
            # return "This is some joke..."

        return None