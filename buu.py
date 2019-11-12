import requests, re
from datetime import datetime, timedelta
from bs4 import BeautifulSoup, Comment
import requests_cache

requests_cache.install_cache('buu_cache', backend='sqlite', expire_after=3600)

class Campus:
	def getAll():
		return [{ "name": "Bangsaen","campusid": 1}, {"name": "Juntaburi","campusid": 2}, {"name": "Srakaew","campusid": 2} ]

class Building:
	def __init__(self):   
		self._cookie = self._getData()

	def _getData(self):
		with requests_cache.disabled():
			r = requests.get("https://reg.buu.ac.th/registrar/room_time.asp")        
			cookie = r.cookies.get_dict()
			cookie['CKLANG'] = "1"
			return cookie

	def getAll(self):
		r = requests.get("https://reg.buu.ac.th/registrar/room_time.asp",cookies=self._cookie)
		soup = BeautifulSoup(r.text, 'lxml')
		item = soup.findAll("table")[4]
		building = {}
		campus = ""
		for i, row in enumerate(item.findAll('tr')):
			aux = row.findAll('td')
			if(row.has_attr('class') and "headerdetail" in row["class"]):
				campus = aux[1].text.replace("CAMPUS ","").strip()
			if(campus not in building.keys() and campus != ""):
				building[campus] = []	
			if(row.has_attr('class') and "normaldetail" in row["class"] and len(aux) == 3):
				building[campus].append({"building":aux[1].text.strip(),"name":aux[2].text.replace("\r\n"," ").strip()})
		return building
	
class Room:
	def __init__(self):   
		self._cookie,self._semester = self._getData()
		today = datetime.now().date()
		self.year = str(today.year + 543)
		self.startWeek = (today - timedelta(days=today.weekday())).strftime("%d/%m/") + self.year

	def _getData(self):
		with requests_cache.disabled():
			r = requests.get("https://reg.buu.ac.th/registrar/room_time.asp?f_cmd=1&campusid=1&bc=KB")        
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

	def getAll(self, campusid, buildingCode):
		r = requests.get("https://reg.buu.ac.th/registrar/room_time.asp?f_cmd=1&campusid={}&bc={}"
				.format(campusid, buildingCode.upper()),cookies=self._cookie)
		soup = BeautifulSoup(r.text, 'lxml')
		item = soup.find("select", attrs={"name": "roomid"})
		room = []
		for i in item:
			room.append({"name":i.string,"roomid":i.get('value')})
		return room

	def getSchedule(self, campusid, roomid):
		Postdata = {"f_cmd": 1, "campusid": campusid, "campusname": "", "bn": "",
					"acadyear": self.year, "semester": self._semester, "firstday": self.startWeek,
					"bc": "", "roomid" : roomid
		}
		r = requests.post("https://reg.buu.ac.th/registrar/room_time.asp", data = Postdata, cookies=self._cookie)
		soup = BeautifulSoup(r.text, 'lxml')
		item = soup.findAll("table")[5]
		results = util.tableParse(item)
		return results

class util:
	def tableParse(item):
		results = {}
		day = ""
		for i, row in enumerate(item.findAll('tr')):
			if(i < 2):
				continue
			aux = row.findAll('td')
			if(aux[0].string != None and aux[0].string.strip() != ""):
				day = aux[0].string.strip()
			table = []
			cur_time = 0
			for j in range(1,len(aux)-1):
				txt = aux[j].text.strip() 
				classtime = int(aux[j]["colspan"])/4		
				if(txt != ""):
					course = util.desc2Dict(txt)
					title = aux[j].find("a")
					if(title):
						course["title"] = title['title']
					else:
						course["title"] = ""
					course["start_time"] = int(cur_time + 8)
					course["end_time"] = int(cur_time + classtime + 8)
					if(aux[j].has_attr('bgcolor') and aux[j]["bgcolor"] != "#C0D0FF"):
						course["duplicate"] = True
					else:
						course["duplicate"] = False
					table.append(course)
				cur_time += classtime
			if(day not in results.keys()):
				results[day] = table    
			else:
				results[day] += table   
		return results

	def desc2Dict(txt):
		regex = r"([0-9].*)\(([0-9].*)\) ([0-9].*)\, (.*)"
		matches = re.finditer(regex, txt, re.MULTILINE)
		for matchNum, match in enumerate(matches):   
   			return {"course_code":match.group(1),"credit":match.group(2),"group":match.group(3),"type":match.group(4)}
import json
if __name__ == '__main__':
	build =  Building()
	#print(json.dumps(room.getAll(1,"KB")))
	print(json.dumps(build.getAll()))