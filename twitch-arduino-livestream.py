import serial, time
import config
import requests
from twitch import TwitchClient
CLIENT_ID = config.CLIENT_ID
OAUTH_ID = config.OAUTH_ID
USERNAME = config.USERNAME
SERIAL_PORT = config.SERIAL_PORT
BAUD_RATE = config.BAUD_RATE
TIMEOUT = config.TIMEOUT
INTERVAL = config.INTERVAL
user_id = None
client = TwitchClient(CLIENT_ID, OAUTH_ID)
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)
follows_channelname = []           #channel names of followed channels
follows_userids = []               #user IDs of followed channels
streams_online = []                #user IDs of live channels
streams_new = []                   #user IDs of live channels that the user hasn't been notified of yet
streams_old = []                   #user IDs of live channels that the user has already been notified of

def login():
	global user_id
	users = client.users.translate_usernames_to_ids(USERNAME)
	for user in users:
		user_id = user.id

def getfollows(): #gets followed channels and puts them into a list
	global follows_channelname
	del follows_channelname[:]
	e = client.users.get_follows(user_id)
	for i in range(len(e)): #gets the channel name
		follows_channelname.insert(i, e[i]['channel']['name'])

def getids(): #gets followed channels' user IDs and puts them into a list
	global follows_userids
	del follows_userids[:]
	for i in range(len(follows_channelname)):
		users = client.users.translate_usernames_to_ids(follows_channelname[i])
		for user in users:
			follows_userids.insert(i, user.id)

def update_online(): #takes every channel that is online from the follows_userids list and puts them into the streams_online list
	global streams_online
	del streams_online[:]
	for i in range(len(follows_userids)):
		e = client.streams.get_stream_by_user(follows_userids[i])
		if e is not None:
			streams_online.insert(i, follows_userids[i])

def update_new(): #checks for any new live channels, and if there's any, sends a notification through the serial port and puts them in the streams_old list
	print('Checking for streams...')
	global streams_new
	streams_new = streams_online
	if streams_new:
		while streams_new:
			if streams_new[0] not in streams_old:
				e = client.streams.get_stream_by_user(streams_new[0])
				time.sleep(2)
				try:
					ser.write(b'%r' % (e['channel']['display_name']))
				except serial.serialutil.SerialException:	
					print('Serial exception occurred, trying again...')
				print('%s is live!' % (e['channel']['display_name']))
				streams_old.insert(0, streams_new[0])
			del streams_new[0]

def update_old(): #checks if the channels are still online, if not, removes them from the list
	global streams_old
	if streams_old:
		for i in range(len(streams_old)):
			try:
				for i in range(len(streams_old)):
					if streams_old[i]:
						e = client.streams.get_stream_by_user(streams_old[i])
						if e is None:
							del streams_old[i]
			except IndexError:
				pass


def main(e):
	print('Serial port on %s open.' % (config.SERIAL_PORT))
	print('Logging in as %s...' % (USERNAME))
	login();
	print('Login successful!')
	while True:
		try:
			getfollows();
			getids();
			update_online();
			update_new();
			update_old();
		except requests.exceptions.HTTPError:
			print('Internal server error, trying again...')
		time.sleep(e)

if __name__ == '__main__':
	main(INTERVAL);