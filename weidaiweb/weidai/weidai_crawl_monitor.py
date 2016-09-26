# coding: utf-8
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import sys
import os
import datetime
import time
import subprocess
import csv
import codecs
import MySQLdb as mdb
import datetime

reload(sys)
sys.setdefaultencoding("utf-8")

class SendErrorMail(object):
	def __init__(self):
		self.mailto_list = ["wangmaoxuwj29775@touna.cn"]
		self.mail_host = "smtp.touna.cn"    
		self.mail_user = "wangmaoxuwj29775@touna.cn"  
		self.mail_pass = "Wj29775" 
		self.content = self.read_error_from_file()
		#print(self.content)

	def read_error_from_file(self):
		with open('weidaiweb.log', 'rb') as f:
			content = f.readlines()[300:]
		return "".join(content)

	def send_mail(self, sub='微贷网抓取异常'):
		me = "weidaiweb_crawl" + "<" + self.mail_user + ">"
		to_list = self.mailto_list
		msg = MIMEText(self.content, _subtype='plain', _charset='utf-8')
		msg['Subject'] = sub    
		msg['From'] = me
		msg['To'] = ";".join(to_list)
		try:
			server = smtplib.SMTP()
			server.connect(self.mail_host)
			server.login(self.mail_user, self.mail_pass)
			server.sendmail(me, to_list, msg.as_string())
			server.close()
			return True
		except Exception, e:
			print str(e)
			return False

class DetectorError(object):
	def __init__(self):
		self.now = datetime.datetime.now().strftime("%Y-%m-%d")+"%"
		#self.now = "2016-08-20%"
		print(self.now)
	
	def monitor(self):
		try:
			conn = mdb.connect(host="10.0.4.123", user="root", passwd="root123", db="weidai_db", port=3306)
			cur = conn.cursor()
			count = cur.execute(" select title, loan_number, amount_of_subject, rate_of_return, \
							deadline, repayment_ways, release_date, progress_width,  source_of_stores, \
							user_sex, marriage, native_place, repayment_periods, stay_still, \
							number_of_overdue, vehicle_brand, license_plate_number, revenue_passenger_kilometers, \
							purchasing_price, collateral_value, verifytime, audit_instructions from zhibiao_info  where release_date like %s ", self.now)
			if count < 1:
				SendErrorMail().send_mail()
		except mdb.Error,e:
			print "Mysql Error %d: %s" % (e.args[0], e.args[1])

if __name__ == '__main__':
	DetectorError().monitor()
