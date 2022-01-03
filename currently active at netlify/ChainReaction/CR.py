import socket,thread,signal,time,game
from collections import deque
from game import Game
PORT = 12347
game_state=0 #0->no game going on.. 1 -> game is going on..
cur_users_turn=0 #cur_users in the game...
#game_grid
user_names=[]
cur_users=[]
is_not_out=[]
users_left=0

lkup={'def':'def'}	
MsgQueue={ 'def':deque()}
Cols={}

MovesQueue = {}


Def_Cols=['#FF0000','#00FF00','#0000FF','#FFFF00','#00FFFF','#AABBCC','#0A0B0C','#C8B9AA','#671234','#ABCD01']
HTML_User_List='$'
Bad_Request = 0

def listener():
	while 1:
		s=raw_input()
		if s=="R":
			game_reset()
		elif s=="S":
			start_the_game()


def game_reset():
	global cur_users
	global game_state	
	global grid
	grid = [[0]*10]*10
	game_state=0
	logmsg("Game is reset","System")
	broad_cast("Game over!")
	command("+")
	cur_users=[]
	print "Command called!"

def broad_cast(msg,allv=0):
	global cur_users
	global MsgQueue
	if allv==0:
		for user in cur_users:
			MsgQueue[user].append('System: '+msg)
	else:
		#send to every-one...
		for user in MsgQueue:
			MsgQueue[user].append('System: '+msg)


def command(msg):
	global MsgQueue
	global cur_users
	
	for user in cur_users:
		MsgQueue[user].append(msg)
		if msg=="+":
			print user,"->",MsgQueue[user]


def start_the_game():
	#time.sleep(10)
	global cur_users_turn
	global is_not_out
	global users_left

	users_left=len(cur_users)
	is_not_out = [1]*len(cur_users)
	broad_cast('The game has started!!')
	game_state=1
	cur_id = user_names.index(cur_users[cur_users_turn])
	cur_users_turn = (cur_users_turn+1)%len(cur_users)
	msg='*'+str(cur_id)
	for user in cur_users:
		MsgQueue[user].append(msg)

def getColor(n):
	return Def_Cols[n-1]


def extractData(req):
	tmp = req.split('\r\n\r\n')
	dat = ''
	if len(tmp)>1:
		dat = tmp[1]
	hdr = tmp[0].split('\r\n')[0]
	#print '**',hdr
	hdr = hdr.split(' ')
	if len(hdr)!=3:
		Bad_Request=1
		return ('','','')
	tmp = hdr[1].split('/')[-1]
	
	if tmp=="":
		tmp="/"
	return (hdr[0],tmp,dat)

def makeResponse(dat,typ='text/html'):
	return 'HTTP/1.1 200 OK\r\nContent-type: '+typ+'\r\nContent-length: '+str(len(dat))+'\r\n\r\n'+dat

def verifyAddress(addr):
	name=''
	try:
		name = lkup[addr]
	except KeyError:
		#get a user-name from him...
		fd = open('auth.html','r')
		st = fd.read()
		return makeResponse(st)
	return ''

def invalidRequest(conn):
	conn.send(makeResponse('<h1>Invalid request!!</h1>'))
	conn.close()

def checkConnection(st,conn):
	if "X-Forwarded-For" in st:
		#the request was from a proxy-server..
		conn.send(makeResponse("<p>Please use Direct Connection!</p>"));
		conn.close();
		return 1
	else:
		return 0
		
def sendMove(st):
	global MovesQueue
	global user_names
	for user in user_names:
		MovesQueue[user].append(st)

def logmsg(msg, src):
#	print MsgQueue
	print src,":",msg

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0',PORT))
s.listen(1000)
thread.start_new_thread(listener ,())

while 1:
	conn,addr = s.accept()
	src_ip_address = addr[0]

	#print MsgQueue
	#print cur_users

	st = conn.recv(1024)
	if checkConnection(st,conn)==1:
		logmsg("Direct Connection",src_ip_address)
		continue
	#print st
	Bad_Request=0
	typ, resrce, dat = extractData(st)
	if Bad_Request:
		logmsg("Invalid Request",src_ip_address)
		invalidRequest(conn)
		continue

	#print "Headers:",typ,"Resource:",resrce,"Data:",dat,"From:",src_ip_address
	
	if typ=="GET":
		st = verifyAddress(src_ip_address)
		#addrVerified = 0
		if "ico" in resrce:
			conn.close()
			continue
		if len(st):#get a user-name...
			logmsg("Authenticating...",src_ip_address)
			conn.send(st)
			conn.close()
			continue
		#check if its for a resource...
		if resrce=="/":#send the game page...
			st = open('CR.html','r').read()
			logmsg("Sending Base File...",lkup[src_ip_address])
			conn.send(makeResponse(st))

		elif "ico" in resrce:
			conn.close()
			continue

		elif "." in resrce:
			if resrce[0]=='/':
				resrce = resrce[1:]
			try:
				st = open(resrce,'r').read()
			except IOError:
				invalidRequest(conn)
				continue
			typ = "text/html"
			if "png" in resrce:
				typ = "image/png"
			elif "js" in resrce:
				typ = "application/javascript"
			elif "css" in resrce:
				typ = "text/css"
			conn.send(makeResponse(st,typ))
			logmsg("Sending Support Files...",lkup[src_ip_address])
		elif resrce=="uname":
			#print src_ip_address,lkup[src_ip_address]
			try:
				k=lkup[src_ip_address]
			except KeyError:
				invalidRequest(conn)
				continue
			conn.send(lkup[src_ip_address]+"|"+str(user_names.index(lkup[src_ip_address])))
			logmsg("Sending user-name...",lkup[src_ip_address])
			#print 'Added Uname!'
		elif resrce=="join":
			#request by the user to join the game...
			valid=1
			try:
				k=lkup[src_ip_address]
			except KeyError:
				valid=0
			if valid==0 or game_state==1:
				invalidRequest(conn)
				continue
			if game_state==1:
				conn.send(makeResponse("Game already started! Try next game."))
				logmsg("Game Request during the game...",lkup[src_ip_address])
			if lkup[src_ip_address] not in cur_users:
				cur_users.append(lkup[src_ip_address])
				broad_cast(cur_users[-1]+' joined the game!',1)
				conn.send(makeResponse("Successfully added!"))
				logmsg("Added to the game list...",lkup[src_ip_address])
				#if len(cur_users)>1:
				#	broad_cast('Game starts in a 30 seconds!')
				#	thread.start_new_thread( start_the_game ,())
			else:
				conn.send(makeResponse("Already added!"))
				logmsg("Duplicate Request...",lkup[src_ip_address])
		elif resrce[0]=="M":#somebody made a move..
			command(resrce);
			logmsg("Made a move.."+resrce[1:],lkup[src_ip_address])
			while is_not_out[cur_users_turn]==0:
				cur_users_turn = (cur_users_turn+1)%len(cur_users)

			cur_id = user_names.index(cur_users[cur_users_turn])
			tmpName = cur_users[cur_users_turn]
			cur_users_turn = (cur_users_turn+1)%len(cur_users)
			sendMove('*'+str(cur_id))
			logmsg("Turn to move...",tmpName)
			conn.send("-")
		elif resrce=="finish":
			broad_cast(lkup[src_ip_address]+" is out!",1);
			logmsg("Out of the Game...",lkup[src_ip_address])
			is_not_out[cur_users.index(lkup[src_ip_address])]=0
			users_left-=1
			if users_left==1:
				while is_not_out[cur_users_turn]==0:
					cur_users_turn = (cur_users_turn+1)%len(cur_users)
				broad_cast(cur_users[cur_users_turn]+" wins the game...!")
				logmsg("Wins the game...",cur_users[cur_users_turn])
				game_reset()
			#cur_users.remove(lkup[src_ip_address])
		elif resrce=="X":
			st = '-'
			if len(MovesQueue[lkup[src_ip_address]]) > 0:
				st = MovesQueue[lkup[src_ip_address]].popleft()
				logmsg("Sent the move..."+st, lkup[src_ip_address])
			conn.send(st)
		else:
			#protocol to execute the ajax requests...
			st = "-"
			#print '**',resrce,'**'
			if len(MsgQueue[resrce])>0:
				st = MsgQueue[resrce].popleft()
				logmsg("Sent the message..."+st, lkup[src_ip_address])
			conn.send(st)
	elif typ=="POST":
	#post request... only in case of a new user-name & chat...
		if resrce=="auth":
			#this is to grab the user-name...
			if len(dat)==0:
				invalidRequest(conn)
			else:
				#split the data.. format:u_name=comment
				dat = dat.split("=")
				#add the addr,name pair...
				lkup[src_ip_address] = dat[1]
				#create a new msg queue...
				MsgQueue[dat[1]] = deque()
				MovesQueue[dat[1]] = deque()
				#give a new color to the user...
				Cols[dat[1]] = getColor(len(lkup)-1)
				user_names.append(dat[1])
				prv_strs=""
				#append the msg regarding the current list of users so far..
				MsgQueue[dat[1]].append(HTML_User_List)
				#generate the current user <p> tag...
				cur_usr = '<p style="color:'+Cols[dat[1]]+'">'+dat[1]+'</p>'
				HTML_User_List += cur_usr#update the user-list
				for i in MsgQueue:
					if i=='def':
						continue
					MsgQueue[i].append('$'+cur_usr)#notify each user with the newly added user...
				for i in MsgQueue['def']:#now send all the prev-msgs of chat to this new user...
					prv_strs += i +'<br/>'
				prv_strs = prv_strs[:-5]
				MsgQueue[dat[1]].append(prv_strs)#here is where we are adding the prev list of messages...
				logmsg("Re-directing the user...", lkup[src_ip_address])
				#now redirect the client to "/".. to access the main game..
				conn.send("HTTP/1.1 302 Found\r\nLocation: /\r\n\r\n")
		elif resrce=="comment":
			#code for chat...
			dat = dat.split("=")
			usr = "<b>"+dat[0]+":</b> "
			logmsg("commented "+dat[1], lkup[src_ip_address])
			for i in MsgQueue:
				MsgQueue[i].append(usr+dat[1])
			conn.send("-")
	else:
		invalidRequest(conn)
	conn.close()