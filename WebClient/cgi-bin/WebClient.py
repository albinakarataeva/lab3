# -*- coding: utf-8 -*-

import os, sys, re, codecs, binascii, cgi, cgitb, datetime, pickle
from msg import *

cgitb.enable()
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())

class Messenger:
	def __init__(self, q):
		self.q = q
		Message.ClientID = int(q.getvalue('ClientID', 0))
		if Message.ClientID == 0:
			Message.SendMessage(M_BROKER, M_INIT)
		self.MessageText = ''
		self.msg = ''

	def PrintPage(self):
		print(f"""Content-type: text/html; charset=utf-8

<html><head><title>Messages</title></head>
<body style="display: flex; justify-content: center; margin-bottom: 30%">
<form method = "post" action=/cgi-bin/WebClient.py name=msgform style = "display: flex; justify-content: center; 
flex-direction: column">
<input type=hidden name=type value="send">
<input type=hidden name=msg value={self.msg}>
<input type=hidden name=ClientID value="{Message.ClientID}">
<div>
<input type=text 
	name=message
	value="{self.MessageText}"
	style=  "width: 250px; height: 50px; border-radius: 5px" 
		placeholder = "Введите сообщение">
<input type = text
       name = id
	   style=  "width: 250px; height: 50px; border-radius: 5px" 
		placeholder = "Введите ID">
</div>
<br>
<div>
<input type=submit 
	value="Send"
	style=  "width: 250px; height: 50px; border-radius: 5px" >
<input type=button 
	value="Get"	
	style=  "width: 250px; height: 50px; border-radius: 5px" 
	onclick="document.forms.msgform.type.value='get'; document.forms.msgform.submit();"
		 >
</div>
<div style ="margin-top: 25px; font-size: 20px">
<span>Ваш ID = {Message.ClientID}</span>
<span>Входящие = {self.msg}</span>
</div>
</form>
</body></html>
	""")


	def MsgSend(self):
		id = ''
		try:
			id = int(self.q.getvalue('id'))
		except:
			id = 10
		Message.SendMessage(M_ALL, M_DATA, self.q.getvalue('message'))

		
	def MsgGet(self):
		m = Message.SendMessage(M_BROKER, M_ALLDATA)
		if m.Header.Type == M_DATA:
			self.msg = ', '.join(m.Data.split(':::::::'))


def main():
	q = cgi.FieldStorage( environ={'REQUEST_METHOD':'POST'})
	m = Messenger(q)

	MENU = {
		'send':	m.MsgSend,
		'get':  m.MsgGet,
	}
    

	try:
		MENU[q.getvalue('type')]()
	except Exception as e:
		pass

	m.PrintPage()
        
main()
