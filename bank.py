import Skype4Py
import time
import json
import rubles
import kt_utils

with open('data/users.json') as f:
    db = json.load(f)

class Bank(object):
    def  __init__(self):
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
    
    
    def create(self):
	new = rubles.rubles(self.context.FromHandle, 100)
	if not kt_utils.check(self.context.FromHandle):
	    new.openaccount()
	    new.saveaccount()
	    self.context.Chat.SendMessage("/me [The Kondor Treasury]: " "User: " "["+ self.context.FromHandle + "]" " Thank you for choosing us as your bank , please accept 100 rubles for creating a new account with us today!")
	else:
	    self.context.Chat.SendMessage("/me [The Kondor Treasury]: " "User: " "["+ self.context.FromHandle + "]" " i see you already have an account with us")
    
    def delete(self):
	rub = rubles.rubles(self.context.FromHandle, 0)
	try:
	    rub.deleteaccount()
	    rub.saveaccount()
	    self.context.Chat.SendMessage("/me [The Kondor Treasury]: " "User: " + self.context.FromHandle + " [Account Status]: Suspended")
	except KeyError:
	    self.context.Chat.SendMessage("/me [The Kondor Treasury]: " "User: " + self.context.FromHandle + " [Account Status]: Not Found")
	    
    
    def balance(self):
	rub = rubles.rubles(self.context.FromHandle, '')
	self.context.Chat.SendMessage("/me [The Kondor Treasury]: " "User: " + self.context.FromHandle +  " [Balance]: " + str(self.accounts[self.context.FromHandle]) + "rB") 
	
    def payto(self):
	try:
	    r = self.context.Body.split(' ')[1]
	except IndexError:
	    self.context.Chat.SendMessage('/me [CamelBot]: Please use proper syntax !pay [Account] [Money]')
	    return
	try:
	    a = self.context.Body.split(' ')[2]
	except IndexError:
	    self.context.Chat.SendMessage('/me [CamelBot]: Please use proper syntax !pay [Account] [Money]')
	    return
	if not kt_utils.check(r):
	    self.context.Chat.SendMessage("/me [The Kondor Treasury]: We could not find that account on file.")
	elif int(a) < 0:
	    self.context.Chat.SendMessage("/me [The Kondor Treasury]: Invalid Numbers, please use postive intergers only.")
	elif int(a) > self.accounts[self.context.FromHandle]:
	    self.context.Chat.SendMessage("/me [The Kondor Treasury]: User: " + self.context.FromHandle + ' you have' '\n [Status] Insufficient Funds for this transfer')
	else:
	    rub = rubles.rubles(self.context.FromHandle, 0)
	    self.accounts[self.context.FromHandle] -= int(a)
	    self.accounts[r] += str(a)
	    self.context.Chat.SendMessage("/me [The Kondor Treasury]: User: " + self.context.FromHandle + " wrote a check to " + r + " for [Money]: " + a +'rB')
	    rub.saveaccount()

    
	
	


    functions = {
        "!createaccount":	create,
        "!balance":             balance,
        "!deleteaccount":       delete,
        "!pay":                  payto,
                }
    
if __name__ == "__main__":
    Fuck = Bank()
    while True:
	time.sleep(1)
	    
	
