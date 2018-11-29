import urllib.request
import json

from helper import Geocoder
from helper import JSONBuilder

lines = [line.rstrip('\n') for line in open("token.txt")]
auth = lines[0]

geocoder = Geocoder()
jsonb = JSONBuilder()


class User:
	def __init__(self, username):
		self.username = username
		self.location = None
		self.location_tuple = (0,0)
		self.followers = []
		self.fols_2nd_degree = [] # array of tuples: (followed, follower)
		self.tuples_list = [] # array of tuples: (loc1,lat1,lng1,loc2,lat2,lng2)
	# END init

	def get_location(self):
		url = ("https://api.github.com/users/"+self.username+auth)
		req = urllib.request.Request(url)
		with urllib.request.urlopen(req) as resp:
			s = resp.read()
		user_json = json.loads(s)
		self.location = user_json["location"]
		if self.location is not None:
			self.location_tuple = geocoder.get_latlng(self.location)
	# END get_location

	def get_followers(self):
		url = ("https://api.github.com/users/"+self.username+"/followers"+auth)
		req = urllib.request.Request(url)
		with urllib.request.urlopen(req) as resp:
			s = resp.read()
		fol_list = json.loads(s)

		for fol_json in fol_list:
			name = fol_json["login"]
			u = User(name)
			u.get_location()
			if u.location_tuple != (0,0):
				self.followers.append(u)
				print('.', end='') # prints dots to show progress
		# END for
		self.makelist()
	# END get_followers

	def get_2nd_deg_fols(self):
		for f in self.followers:
			f.get_followers()
			for f2 in f.followers:
				self.fols_2nd_degree.append((f,f2))
				print('.', end='')
			# END for
			for t in f.tuples_list:
				self.tuples_list.append(t)
			# END for
		# END for
	# END get_2nd_deg_fols

	def get_all(self):
		self.get_location()
		if self.location is None:
			return
		self.get_followers()
		self.get_2nd_deg_fols()
		jsonb.build(self.tuples_list)
	# END get_all

	def makelist(self):
		self_tuple = (self.location, self.location_tuple[0], self.location_tuple[1])
		for u in self.followers:
			u_tuple = (u.location, u.location_tuple[0], u.location_tuple[1])
			self.tuples_list.append(self_tuple+u_tuple)
		# END for
	# END makelist
# END User

def main():
	username = "sastaffo"
	# lydell is a Swedish software desginer with approx 100 followers
	start = User(username)
	start.get_all()
	# END for
# END main

if __name__ == '__main__':
	main()
# END if
