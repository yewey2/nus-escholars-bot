class Player:
    def __init__(self, username, angel=None, mortal=None):
        self.username = username
        self.angel = angel
        self.mortal = mortal
        self.chat_id = None
    
    def get_username(self):
        return self.username

    def get_chat_id(self):
        return self.chat_id
    
    def set_chat_id(self, chat_id):
        self.chat_id = chat_id

    def get_angel(self):
        if self.angel:
            return self.angel
        print("Angel is not found!")

    def get_mortal(self):
        if self.mortal:
            return self.mortal
        print("Mortal is not found!")

    def set_angel_mortal(self, angel, mortal):
        self.angel = angel
        self.mortal = mortal
