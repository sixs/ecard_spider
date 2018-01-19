#-*-coding:utf-8 -*-	
import requests
import json
import time
from bs4 import BeautifulSoup
import re
import pymysql 

def main():
	class ecard:

		# 用户参数
		session = requests.Session()
		number = ''	# 学号
		passwd = ''	# 密码
		account = ''	# 一卡通卡号

		# 数据库参数
		db_user = ''	# 数据库user
		db_pw = ''	# 数据库密码
		db_host = ''	# host
		db_port = 3306	# 端口
		db_name = ''	# 数据库名
		db_table = ''	# 表名

		def __init__(self):		# 初始化

			# 获取验证码，由于重新登录验证码仍然可用，故验证码设为全局变量
			checkCodeUrl = 'http://116.57.72.198/getCheckpic.action?rand='+str(int(time.time()*1000))
			req1 = self.session.get(checkCodeUrl)
			fp = open('./checkCode.jpg','wb')
			fp.write(req1.content)
			fp.close()
			self.checkCode = input('输入验证码:')

			# 登录
			self.lastLogin = (time.time())
			self.loginIn()

			# 23：00-07：00时间段不监控
			while(True):
				if(int(time.strftime("%H"))>=7 and int(time.strftime("%H"))<=23):
					self.checkLogin()
					self.todayAccount()
					time.sleep(10)
				else:
					time.sleep(28800)

		def checkLogin(self):	# 每小时重新登录一次
			timestamp = (time.time())
			if (timestamp-self.lastLogin)>=3600:
				print(time.strftime("%Y-%m-%d %H:%M:%S"),"重新登录")
				self.lastLogin = timestamp
				self.loginOut()
				self.loginIn()

		# 登录
		def loginIn(self):

			loginUrl = 'http://116.57.72.198/loginstudent.action'
			headers = {
				'Host':'116.57.72.198',
				'Origin':'http://116.57.72.198',
				'Referer':'http://116.57.72.198/homeLogin.action',
				'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
			}
			data = {
				'name':self.number,
				'loginType':'2',
				'userType':'1',
				'passwd':self.passwd,
				'rand':self.checkCode,
				'imageField.x':'38',
				'imageField.y':'9'
			}
			req2 = self.session.post(url=loginUrl,headers=headers,data=data)
			print(req2.text)

		# 基本信息
		def getInfo(self):
			infoUrl = 'http://116.57.72.198/accountcardUser.action'
			headers = {
				'Host':'116.57.72.198',
				'Origin':'http://116.57.72.198',
				'Referer':'http://116.57.72.198/accountleftFrame.action',
				'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
			}
			req3 = self.session.get(url=infoUrl)
			print(req3.text)

		# 提取出消费的详情信息
		def getAccountInfo(self,html):
			soup = BeautifulSoup(html,'html.parser')
			trs = soup.findAll(name = 'tr',attrs = {'class':re.compile(r'listbg(.*)')})
			if len(trs):
				for tr in trs:
					accountInfo = []
					accountInfo.append(number)
					tds = tr.select('td')
					for i in range(0,len(tds)):
						accountInfo.append(tds[i].text.strip()) 
					# 存入数据库
					self.storage(accountInfo)
				return True
			else:
				return False

		# 今日消费
		def todayAccount(self):
			todayUrl = 'http://116.57.72.198/accounttodatTrjnObject.action'
			headers = {
				'Host':'116.57.72.198',
				'Origin':'http://116.57.72.198',
				'Referer':'http://116.57.72.198/accounttodayTrjn.action',
				'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
			}
			data = {
				'account':self.account,
				'inputObject':'all',
				'Submit':'+%C8%B7+%B6%A8+'
			}
			req4 = self.session.post(url=todayUrl,headers=headers,data=data)
			self.getAccountInfo(req4.text)

		# 获取历史消费
		def historyAccount(self,inputStartDate,inputEndDate):

			url1 = 'http://116.57.72.198/accounthisTrjn.action'
			headers = {
				'Host':'116.57.72.198',
				'Referer':'http://116.57.72.198/accountleftFrame.action'
			}
			req5 = self.session.get(url1,headers=headers)
			soup = BeautifulSoup(req5.text,'html.parser')
			url2 = 'http://116.57.72.198' + soup.select('form')[0]['action']

			headers = {
				'Host':'116.57.72.198',
				'Origin':'http://116.57.72.198',
				'Referer':'http://116.57.72.198/accounthisTrjn.action'
			}
			data = {
				'account':self.account,
				'inputObject':'all',
				'Submit':'+%C8%B7+%B6%A8+'
			}
			req6 = self.session.post(url=url2,headers=headers,data=data)
			soup = BeautifulSoup(req6.text,'html.parser')
			url3 = 'http://116.57.72.198' + soup.select('form')[0]['action']

			headers = {
				'Host':'116.57.72.198',
				'Origin':'http://116.57.72.198',
				'Referer':url2
			}
			data = {
				'inputStartDate':inputStartDate,
				'inputEndDate':inputEndDate
			}
			req7 = self.session.post(url=url3,headers=headers,data=data)
			soup = BeautifulSoup(req7.text,'html.parser')
			url4 = 'http://116.57.72.198' + soup.select('form')[0]['action']

			headers = {
				'Host':'116.57.72.198',
				'Origin':'http://116.57.72.198',
				'Referer':'http://116.57.72.198/accounttodayTrjn.action',
				'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
			}
			data = {}
			req8 = self.session.post(url=url4,headers=headers,data=data)
			
			html = req8.text
			pageNum = 1

			while(True):
				if(self.getAccountInfo(html)):
					pageNum += 1

					url5 = 'http://116.57.72.198/accountconsubBrows.action'
					headers = {
						'Host':'116.57.72.198',
						'Origin':'http://116.57.72.198',
						'Referer':url4
					}
					data = {
						'inputStartDate':inputStartDate,
						'inputEndDate':inputEndDate,
						'pageNum':str(pageNum)
					}
					req9 = self.session.post(url=url5,headers=headers,data=data)
					html = req9.text
					if(pageNum == 5):
						break
				else:
					break

		# 存入数据库
		def storage(self,info):
			connection = pymysql.connect(user=self.db_user, passwd=self.db_pw, host=self.db_host,
				port=self.db_port, unix_socket='/var/run/mysqld/mysqld.sock', db=self.db_name,
				use_unicode=True, charset="utf8") 
			# 执行sql语句
			try:
				cursor = connection.cursor()
				sql1 = "SELECT * FROM "+ self.db_table +" where paydate='"+info[1]+"'"
				cursor.execute(sql1)
				# 获取查询结果
				if(cursor.fetchone()):
					msg = '已经存在'
					print(msg)

				else:
					print(info,'插入数据库成功')
					# 执行sql语句，进行查询
					sql2 = "INSERT INTO `"+ self.db_table +"`(`number`, `paydate`, `paytype`, `payloc`, `account`, \
					`paycount`, `balance`, `payindex`, `status`) VALUES ('"+info[0]+"','"+info[1]+"','"+ \
					info[2]+"','"+info[3]+"','"+info[4]+"',"+info[5]+","+info[6]+","+info[7]+",'"+info[8]+"')"
					cursor.execute(sql2)
				# 没有设置默认自动提交，需要主动提交，以保存所执行的语句
				connection.commit()
				cursor.close()
			 
			finally:
			    connection.close();

		def loginOut(self):
			loginOutUrl = 'http://116.57.72.198/loginout.action'
			req = self.session.get(loginOutUrl,allow_redirects=False)

	ecard = ecard()

if __name__ == '__main__':
	main()

