import Skype4Py
import time
import json
import rubles
import kt_utils
import requests

with open('data/users.json') as f:
    db = json.load(f)


class Bank(object):

    def __init__(self):
        self.skype = Skype4Py.Skype()
        if self.skype.Client.IsRunning == False:
            self.skype.Client.Start()
        self.skype.Attach()
        self.skype.OnMessageStatus = self.RunFunction

        self.listen = False
        self.start = time.clock()
        self.mode = ''
        self.context = ''
        self.accounts = db['accounts']
        self.key = 'dc6zaTOxFJmzC'

    def RunFunction(self, Message, Status):
        if Status == 'SENT' or Status == 'RECEIVED':
            cmd = Message.Body.split(' ')[0]
            if cmd in self.functions.keys():
                self.context = Message
                self.functions[cmd](self)
            elif self.listen:
                self.ParseAnswer(Message, Message.Body)

    def parseanswer(self, Message, query):
        pass
    
    def giftrans(self):
        search = self.context.Body.split(' ')[1]
        r = requests.get("http://api.giphy.com/v1/gifs/translate?s=" + search + "&api_key=" + self.key + "&limit=1")
        info = r.json()
        try:
            url = info['data']['url']
        except TypeError:
            self.context.Chat.SendMessage('/me [CamelBot]: Too Complicated of a Gif Search i am in beta , you dun almost crashed me , if sean did not put any error checking!')
            return
        self.context.Chat.SendMessage('/me [CamelBot]: gif translation for ' + search + ' is ' + url)
      
        

    def create(self):
        new = rubles.rubles(self.context.FromHandle, 100)
        if not kt_utils.check(self.context.FromHandle):
            new.openaccount()
            new.saveaccount()
            self.context.Chat.SendMessage('/me [The Kondor Treasury]: User: ['
                     + self.context.FromHandle
                    + '] Thank you for choosing us as your bank , please accept 100 rubles for creating a new account with us today!'
                    )
        else:
            self.context.Chat.SendMessage('/me [The Kondor Treasury]: User: ['
                     + self.context.FromHandle
                    + '] i see you already have an account with us')

    def delete(self):
        rub = rubles.rubles(self.context.FromHandle, 0)
        try:
            rub.deleteaccount()
            rub.saveaccount()
            self.context.Chat.SendMessage('/me [The Kondor Treasury]: User: '
                     + self.context.FromHandle
                    + ' [Account Status]: Suspended')
        except KeyError:
            self.context.Chat.SendMessage('/me [The Kondor Treasury]: User: '
                     + self.context.FromHandle
                    + ' [Account Status]: Not Found')

    def balance(self):
        rub = rubles.rubles(self.context.FromHandle, '')
        try:
            self.context.Chat.SendMessage('/me [The Kondor Treasury]: User: '
                     + self.context.FromHandle + ' [Balance]: '
                    + str(self.accounts[self.context.FromHandle]) + 'rB'
                    )
        except KeyError:
            self.context.Chat.SendMessage('/me [The Kondor Treasury]: We could not find that account on file or you do not have an account with us yet.'
                    )
            return

    def payto(self):
        try:
            r = self.context.Body.split(' ')[1]
        except IndexError:
            self.context.Chat.SendMessage('/me [CamelBot]: Please use proper syntax !pay [Account] [Money]'
                    )
            return
        try:
            a = self.context.Body.split(' ')[2]
        except IndexError:
            self.context.Chat.SendMessage('/me [CamelBot]: Please use proper syntax !pay [Account] [Money]'
                    )
            return
        if not kt_utils.check(r):
            self.context.Chat.SendMessage('/me [The Kondor Treasury]: We could not find that account on file.'
                    )
        elif int(a) < 0:
            self.context.Chat.SendMessage('/me [The Kondor Treasury]: Invalid Numbers, please use postive intergers only.'
                    )
        elif int(a) > self.accounts[self.context.FromHandle]:
            self.context.Chat.SendMessage('/me [The Kondor Treasury]: User: '
                     + self.context.FromHandle
                    + ' you have\n [Status] Insufficient Funds for this transfer'
                    )
        else:
            rub = rubles.rubles(self.context.FromHandle, 0)
            self.accounts[self.context.FromHandle] -= int(a)
            self.accounts[r] += int(a)
            self.context.Chat.SendMessage('/me [The Kondor Treasury]: User: '
                     + self.context.FromHandle + ' wrote a check to '
                    + r + ' for [Money]: ' + a + 'rB')
            rub.saveaccount()
            

    functions = {
        '!createaccount': create,
        '!balance': balance,
        '!deleteaccount': delete,
        '!pay':        payto,
        '@GifTrans':  giftrans,
        }


if __name__ == '__main__':
    Fuck = Bank()
    while True:
        time.sleep(1)