import urllib.request
import json

auth = "?access_token=TOKEN"

class User:
	def __init__(self, username):
		self.username = username
		self.location = None
		self.followers = []
		self.fols_2nd_degree = []
	# END init

	def get_location(self):
		url = ("https://api.github.com/users/"+self.username+auth)
		req = urllib.request.Request(url)
		with urllib.request.urlopen(req) as resp:
			s = resp.read()
		user_json = json.loads(s)
		#try:
		#	message = user_json["message"]
		#	print(message)
		#	return
		#except:
		self.location = user_json["location"]
		# END try
	# END get_location

	def get_followers(self):
		url = ("https://api.github.com/users/"+self.username+"/followers"+auth)
		req = urllib.request.Request(url)
		with urllib.request.urlopen(req) as resp:
			s = resp.read()
		fol_list = json.loads(s)
		#try:
		#	message = fol_list["message"]
		#	print(message)
		#	return
		#except:
		for fol_json in fol_list:
			name = fol_json["login"]
			u = User(name)
			u.get_location()
			if u.location is not None:
				self.followers.append(u)
		# END for
	# END get_followers

	def get_2nd_deg_fols(self):
		for f in self.followers:
			f.get_followers()
			for f2 in f.followers:
				self.fols_2nd_degree.append((f,f2))
# END User

def main():
	start = User("sastaffo")
	start.get_location()
	print(start.username, ">", start.location)
	start.get_followers()
	for f in start.followers:
		print(f.username, ">", f.location)
	start.get_2nd_deg_fols()
	for tuple in start.fols_2nd_degree:
		print(tuple[0].username, ">", tuple[1].username, ">", tuple[1].location)
	# END for
# END main

if __name__ == '__main__':
	main()
# END if
