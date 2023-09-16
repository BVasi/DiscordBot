import random

greetings = ["Hello", "Hi", "Hey", "Ahoy", "Howdy"]
roll = "roll"

class responseManager():
    def __init__(self, message):
        self.message = message

    def __shouldGreet(self) -> bool:
        loweredMessageContent = self.message.content.lower()
        for greeting in greetings:
            if greeting.lower() == loweredMessageContent:
                return True
        return False

    def handleResponse(self) -> str:
        messageAuthor = str(self.message.author)
        if self.__shouldGreet():
            return greetings[random.randint(0, len(greetings) - 1)] + ", " + messageAuthor
        
        if self.message.content.lower() == roll:
            return str(random.randint(1, 6))