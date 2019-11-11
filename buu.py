import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

class Campus:	
	def getAll():
		return [{ "name": "บางแสน","campusid": 1}, {"name": "จันทบุรี","campusid": 2}, {"name": "สระแก้ว","campusid": 2} ]
	
class Room:
	def __init__(self, campusid, buildingCode):
		self.campusid = campusid
		self.buildingCode = buildingCode	
		self._cookie,self._semester = self._getData()
		today = datetime.now().date()
		year = str(today.year + 543)
		startWeek = (today - timedelta(days=today.weekday())).strftime("%d/%m/") + year

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
		print(room)

room =  Room(1,"if")
room.getAll()