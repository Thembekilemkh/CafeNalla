import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart


class Email():
	def __init__(self, **kwargs):
		print("__init__")
		email_V = False
		valid_email = kwargs["emailQ"]
		connection=kwargs["connection"]

		self.receiver = kwargs["email"]
		self.sender = "thembekile47@gmail.com"
		
		try:
			email_good = self.check_email(self.receiver)

			if email_good == True:
				self.domain = self.get_provider(self.receiver)
				valid_email.put(True)
				email_V = True
			else:
				valid_email.put(False)

		except Exception as e:
			valid_email.put(False)
			print("Invalid email: ", str(e))

		if email_V == True:
			try:
				self.server = smtplib.SMTP(f"smtp.{self.domain}.com", 587)
				self.server.starttls()
				self.server.login(self.sender, "onth zqve ynde ncie")
				connection.put(True)
			except Exception as e:
				connection.put(False)
				print("Failed connection: ", str(e))

	def prep_email(self, **kwargs):
		email_sent = kwargs["email_sent"]
		try:
			message = kwargs["message"]
			subject = kwargs["subject"]
			self.mail_message(subject, message)
			email_sent.put(True)
			
		except Exception as e:
			print("Failed to send email: ", str(e))
			email_sent.put(False)

	def mail_message(self, subject, message):
		msg = MIMEMultipart()
		msg["From"] = "Cafe Nalla App"
		msg["To"] = self.receiver
		msg["Subject"] = subject 

		msg.attach(MIMEText(message, "plain"))

		text = msg.as_string()
		self.server.sendmail(self.sender, self.receiver, text)

	def get_provider(self, email):
		provider = ""
		i = -1 
		start_capture = False

		while i < 0:
			letter = email[i]

			if letter == "@":
				start_capture = False
				break

			if start_capture == True:
				provider = provider+letter

			if letter == ".":
				if email[i+1:-1] == "co":
					start_capture = True
				else:
					pass
			else:
				pass

			i = i-1
		return provider[::-1]

	def check_email(self, email):
		got_at = False
		got_com = False

		for letter in email:
			if letter == "@":
				got_at = True
				break

		if got_at == True:
			if email[-4:] == ".com":
				got_com = True
			else:
				return False
		else:
			return False

		return got_com