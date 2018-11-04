import urllib.request
import json

class User:
	def __init__(self, username):
		self.username = username
		self.location = None
		self.followers = []
	# END init

	def get_location(self):
		url = ("http://api.github.org/"+self.username)
		with urllib.request.urlopen(url) as resp:
			s = resp.read()
		user_json = json.loads(s)
		self.location = user_json["location"]
	# END get_location

	def get_followers(self):
		url = ("http://api.github.org/"+user+"/followers")
		with urllib.request.urlopen(url) as resp:
			s = resp.read()
		fol_list = json.loads(s)
		for fol_json in fol_list:
			name = fol_json["login"]
			u = User(name)
			u.get_location()
			self.followers.append(u)
		# END for
	# END get_followers
# END User

def main():
	start = User("sastaffo")
	start.get_location()
	printf(start.location)
	start.get_followers()
	for f in start.followers:
		print(f.username + f.location)
# END main

if __name__ == '__main__':
	main()
# END if
