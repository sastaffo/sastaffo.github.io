import urllib.request
import json

class Geocoder:
	def __init__(self):
		lines = [line.rstrip('\n') for line in open("googleAPIkey.txt")]
		self.key = lines[0]
		self.urlstem = ("https://maps.googleapis.com/maps/api/geocode/json?address=")
	# END __init__

	def get_lnglat(self, location):
		if location == "": return (0,0)

		location = str.replace(location, " ", "+")

		url = (self.urlstem+location+"&key="+self.key)
		req = urllib.request.Request(url)
		try:
			with urllib.request.urlopen(req) as resp:
				s = resp.read()
		except UnicodeEncodeError as e:
			return (0,0)

		loc_json = json.loads(s)
		results = loc_json["results"]
		status = loc_json["status"]
		if status == "OK":
			geometry = results[0]["geometry"]
			location = geometry["location"]
			latitude = location["lat"]
			longitude = location["lng"]
			return (longitude,latitude)
		else: return (0,0)
	# END get_latlng
# END Geocoder

#def main():
#	loc = "New York"
#	g = Geocoder()
#	t = g.get_latlng(loc)
#	print(""+loc+" "+str(t[0])+","+str(t[1]))
# END main

class JSONBuilder:
	def __init__(self):
		self.filename = "locations.json"
		self.opener = "{\"features\":["
		self.body = ""
		self.closer = "]}"
	# END init

	def build(self,_list):
		# takes in list of tuples (loc1,lat1,lng1,loc2,lat2,lng2)
		lines = []
		for t in _list:
			line = ( "{\"type\":\"Feature\","
					+"\"geometry\": {\"type\": \"Point\", \"name\": \""
					+t[0]+ "\", \"coordinates\": ["+str(t[1])+","+str(t[2])
					+"]},\"geometryto\": {\"type\" : \"Point\",\"name\": \""
					+t[3]+ "\", \"coordinates\": ["+str(t[4])+","+str(t[5])
					+"]}}" )
			lines.append(line)
		# END for
		delim=",\n"
		self.body = delim.join(lines)
		self.write()
	# END build

	def write(self):
		file = open(self.filename, "w+")
		json = (""+self.opener+self.body+self.closer)
		file.write(json)
		file.close()

# END JSONBuilder

def main():
	j = JSONBuilder()
# END main

if __name__ == '__main__':
	main()
