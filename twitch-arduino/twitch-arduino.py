import serial, time
from twitch import TwitchClient
CLIENT_ID = 
OAUTH_ID = 
USER_ID = 
SERIAL_PORT = 
BAUD_RATE = 
TIMEOUT = 
INTERVAL = 
client = TwitchClient(CLIENT_ID, OAUTH_ID)
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=TIMEOUT)
follows_displayname = []           #display names of followed channels
follows_channelname = []           #channel names of followed channels
follows_userids = []               #user IDs of followed channels
streams_online = []                #user IDs of live channels
streams_new = []                   #user IDs of live channels that the user hasn't been notified of yet
streams_old = []                   #user IDs of live channels that the user has already been notified of

def getfollows(): #gets followed channels and puts them into a list
	del follows_displayname[:]
	del follows_channelname[:]
	e = client.users.get_follows(USER_ID)
	for i in range(len(e)): #gets the display name
		follows_displayname.insert(i, e[i]['channel']['display_name'])
	for i in range(len(e)): #gets the channel name
		follows_channelname.insert(i, e[i]['channel']['name'])

def getids(): #gets followed channels' user IDs and puts them into a list
	del follows_userids[:]
	for i in range(len(follows_displayname)):
		users = client.users.translate_usernames_to_ids(follows_channelname[i])
		for user in users:
			follows_userids.insert(i, user.id)

def update_online(): #takes every channel that is online from the follows_userids list and puts them into the streams_online list
	del streams_online[:]
	for i in range(len(follows_userids)):
		e = client.streams.get_stream_by_user(follows_userids[i])
		if e is not None:
			streams_online.insert(i, follows_userids[i])

def update_new(): #checks for any new live channels, and if there's any, sends a notification through the serial port and puts them in the streams_old list
	streams_new = streams_online
	if streams_new:
		for i in range(len(streams_new)):
			if streams_new[i] not in streams_old:
				e = client.streams.get_stream_by_user(streams_new[i])
				time.sleep(2)
				ser.write(b'%r' % (e['channel']['display_name']))
				streams_old.insert(i, streams_new[i])
				del streams_new[i]

def update_old(): #checks if the channels are still online, if not, removes them from the list
	if streams_old:
		for i in range(len(streams_old)):
			e = client.streams.get_stream_by_user(streams_old[i])
			if e is None:
				del streams_old[i]

def init():
	getfollows();
	getids();

def main(e):
	while True:
		init();
		update_online();
		update_new();
		update_old();
		time.sleep(e)

if __name__ == '__main__':
	main(INTERVAL);
