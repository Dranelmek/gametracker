import subprocess
import time
from time import sleep
from datetime import date

games = ['fakeValorant.exe','r5apex.exe']

# conn = sqlite3.connect("WastedOnValorant.db")
# cursor = conn.cursor()

# cursor.execute("""CREATE TABLE IF NOT EXISTS TimeWasted
# 				(GameID integer PRIMARY KEY AUTOINCREMENT,
# 				Game text,
# 				Date Date,
# 				TimeWasted text)
# 				""")
# conn.commit()

tic = 0
toc = 0




# try:
# 	playsound('Most-annoying-sound.mp3')
# except Exception as e:
# 	print(e)

def addToTable(values):
	print("data added to table was{values}")
	pass
	# sql = "INSERT into TimeWasted (Game,Date,TimeWasted) values (?,?,?)"
	#cursor.execute(sql,values)
	#conn.commit()
	#cursor.close()


def setTimer(game):
	print("...Program Detected...\n...Timer Set...")
	tic = 0
	toc = 0
	gameAdd = ""
	if game == "r5apex.exe":
		gameAdd = "ApexLegends"
	else:
		gameAdd = "Valorant"
	try:
		s = subprocess.check_output('tasklist', shell=True)
		print("game is:"+ game)
		print(game.encode() in s)
		tic = time.perf_counter()
		while  game.encode() in s and (toc-tic)//60 <60:
			s = subprocess.check_output('tasklist', shell=True)
			toc = time.perf_counter()
		if (toc-tic)//60 >= 60:
			print((toc-tic)//60,": minutes spent on "+str(gameAdd))
			timeSpent = (toc-tic)//60
			dateTime = date.today()
			dateTime = dateTime.strftime("%d/%m/%y")
			values = (gameAdd,dateTime,timeSpent)
			addToTable(values)
			try: 
				playsound('Sound/sound.wav')
			except Exception as e:
				print(e)
		else:
			toc =time.perf_counter()
			print((toc-tic)//60,": minutes spent on "+ str(gameAdd))
			timeSpent = (toc-tic)//60
			dateTime = date.today()
			dateTime = dateTime.strftime("%d/%m/%y")
			values = (gameAdd,dateTime,timeSpent)
			addToTable(values)
			k = input(str(gameAdd)+" has been closed")
	except KeyboardInterrupt:
		print("KeyboardInterrupt")
		pass


s = subprocess.check_output('tasklist', shell=True)
notRunning = True
while notRunning:
	# time.sleep(2)
	s = subprocess.check_output('tasklist', shell=True)
	if 'fakeValorant.exe'.encode() in s:
		notRunning = False
		print("fake valorant detected")
		setTimer("fakeValorant.exe")
	elif 'r5apex.exe'.encode() in s:
		notRunning = False
		setTimer("r5apex.exe")
	
