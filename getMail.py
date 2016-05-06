import sys
import imaplib
import email
import email.header
import datetime
import os

outputDir = "updates/"

# Use 'INBOX' to read inbox.  Note that whatever folder is specified, 
# after successfully running this script all emails in that folder 
# will be marked as read.
EMAIL_FOLDER = "INBOX"

class Mail():

	EMAIL_ACCOUNT = ""
	password = ""
	outputDir = "/updates"
	M = None
	def __init__(self, usern, pas):
		global EMAIL_ACCOUNT
		global password
		global M
		EMAIL_ACCOUNT = usern
		password = pas
		
		M = imaplib.IMAP4_SSL('imap.gmail.com')

		try:
			global EMAIL_ACCOUNT
			global password
			rv, data = M.login(EMAIL_ACCOUNT, password)
		except imaplib.IMAP4.error:
			print ("LOGIN FAILED!!! ")
			sys.exit(1)

		rv, mailboxes = M.list()
		rv, data = M.select(EMAIL_FOLDER)
		
		

	def process_mailbox(self):
		"""
		Do something with emails messages in the folder.  
		For the sake of this example, print some headers.
		"""
		action = ""
		rv, data = M.search(None, "ALL")
		if rv != 'OK':
			print("No messages found!")
			return
		for num in data[0].split():
			
			rv, data = M.fetch(num, '(RFC822)')
			if rv != 'OK':
				print("ERROR getting message", num)
				return
			if type(data[0][1]) is int:
				continue
			msg = email.message_from_bytes(data[0][1])
			hdr = email.header.make_header(email.header.decode_header(msg['Subject']))
			subject = str(hdr)
			if subject != "action":
				continue
			# Now convert to local date-time
			tmp = data[0][1]
			msg=email.message_from_string(tmp.decode("utf-8") )
			if msg.get_content_maintype() == 'multipart': 
				for part in msg.walk():       
					if part.get_content_type() == "text/plain":
						body = part.get_payload(decode=True).decode("utf-8")
						action = body
					if part.get('Content-Disposition') is not None:
						action = "update"
						filename = part.get_filename()
						att_path = os.path.join(outputDir, filename)
						fp = open(att_path, 'wb')
						fp.write(part.get_payload(decode=True))
						fp.close()
			M.store(num, '+FLAGS', '\\Deleted')
		M.expunge()	
		return action
		
	def run(self):
		return self.process_mailbox()
		
		
		
	def exit(self):
		M.close()
		M.logout()
		