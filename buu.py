import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup, Comment

class Campus:	
	def getAll():
		return [{ "name": "บางแสน","campusid": 1}, {"name": "จันทบุรี","campusid": 2}, {"name": "สระแก้ว","campusid": 2} ]
	
class Room:
	def __init__(self, campusid, buildingCode):
		self.campusid = campusid
		self.buildingCode = buildingCode	
		self._cookie,self._semester = self._getData()
		today = datetime.now().date()
		self.year = str(today.year + 543)
		self.startWeek = (today - timedelta(days=today.weekday())).strftime("%d/%m/") + self.year

	def _getData(self):
		r = requests.get("https://reg.buu.ac.th/registrar/room_time.asp?f_cmd=1&campusid=1&bc={}".format(self.buildingCode))		
		cookie = r.cookies.get_dict()
		cookie['CKLANG'] = "1"
		soup = BeautifulSoup(r.text, 'lxml')
		item = soup.find("select", attrs={"name": "roomid"})
		item = soup.find("font", attrs={"color": "#800000"})
		for i in item:
			if(i.name == None):
				val = i.string.strip()
				if(len(val) < 4 and val != "/" and len(val) > 0):
					return cookie, val	

	def getAll(self):
		r = requests.get("https://reg.buu.ac.th/registrar/room_time.asp?f_cmd=1&campusid={}&bc={}"
				.format(self.campusid, self.buildingCode.upper()),cookies=self._cookie)
		soup = BeautifulSoup(r.text, 'lxml')
		item = soup.find("select", attrs={"name": "roomid"})
		room = []
		for i in item:
			room.append({"name":i.string,"roomid":i.get('value')})
		return room

	def getSchedule(self,roomid):
		Postdata = {"f_cmd": 1, "campusid": self.campusid, "campusname": "", "bn": "",
					"acadyear": self.year, "semester": self._semester, "firstday": self.startWeek,
					"bc": "KB", "roomid" : roomid
		}
		proxy = {"http":"http://127.0.0.1:8888","https":"https://127.0.0.1:8888"}
		r = requests.post("https://reg.buu.ac.th/registrar/room_time.asp", data = Postdata, cookies=self._cookie,proxies=proxy,verify=False)
		soup = BeautifulSoup(r.text, 'lxml')
		item = soup.findAll("table")[5]
		results = {}
		for i, row in enumerate(item.findAll('tr')):
			aux = row.findAll('td')
			results[aux[0].string] = aux[1].string

		print(results)
		#print(item)

if __name__ == '__main__':
	room =  Room(1,"if")
	room.getSchedule("4235")