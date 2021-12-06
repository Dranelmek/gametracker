from tkinter import *
from functools import partial
import sqlite3
import subprocess
import threading
import time

conn = sqlite3.connect("WastedOnGames.db")
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS TimeWasted
				(GameID integer,
				Date Date,
				TimeWasted text,
				FOREIGN KEY (GameID) REFERENCES GAMES(GameID))
				""")

cursor.execute("""CREATE TABLE IF NOT EXISTS GAMES
				(GameID integer PRIMARY KEY AUTOINCREMENT,
				Game Text,
				subprocessProcessName Text)
				""")
conn.commit()


class window:
    def __init__(self, master, title):
        self.master = master
        self.master.geometry("350x250")
        self.master.title(title)

    def makeLabel(self, text, x, y, fg="black"):
        self.label = Label(self.master, text=text, fg=fg)
        self.label.pack()
        self.label.place(x=x, y=y)
        return self.label

    def makeButton(self, text, x, y, command):
        self.button = Button(self.master, text=text, command=command)
        self.button.pack()
        self.button.place(x=x, y=y)
        return self.button

    def makeEntry(self, x, y, bd=3):
        self.entry = Entry(self.master, bd=bd)
        self.entry.pack()
        self.entry.place(x=x, y=y)
        return self.entry


class game:
    def __init__(self, master):
        Window = window(master, "Game Tracker")
        self.master = master

        self.gameButtonArr = []

        menu = Menu(self.master)
        self.master.config(menu=menu)
        # Creating the settings menu at the top
        settings = Menu(menu)
        menu.add_cascade(label="Settings", menu=settings)
        settings.add_command(label="Add new game", command=self.addNewGame)

        # Fetch the number of games and list of games user has
        numberGames = self.getNumberGames()
        listGames = self.getListGames()
        # Create buttons for each game
        for i in range(numberGames):
            self.gameButtonArr.append(Window.makeButton(listGames[i], 10, 40 * i, partial(self.activate, i)))
        Window.makeButton("Sonar", 80, 40, self.activateAll)

    def addNewGame(self):
        new = Toplevel(self.master)
        addNewGameGUI = window(new, "Add New Game")
        addNewGameGUI.makeLabel("Enter name of new game to add to tracker", 10, 10)
        self.entry = addNewGameGUI.makeEntry(10, 40)
        self.button = addNewGameGUI.makeButton("get", 120, 40,self.getEntry)

    def getEntry(self):
        # Need help with this - currently cant return the value as i have nowhere to store it
        entry = self.entry.get()
        if entry == "":
            return "No input"
        return entry

    def getButton(self, button):
        return button.cget('text')

    def activate(self, button):
        # Activate the system to look for this particular game
        # Fetches the game based off of the button pressed
        gameName = self.getButton(self.gameButtonArr[button])
        var = self.getExeName(gameName)

        var = str(var)
        var = var.replace('(', '')
        var = var.replace(')', '')
        var = var.replace(',', '')
        self.waitForGame(var)

        s = subprocess.check_output('tasklist', shell=True)
        while var.encode() in s:
            s = subprocess.check_output('tasklist', shell=True)

    def activateAll(self):
        # activate the system to look for all games in list
        self.waitForGameDefault()
        print("Checking for all games")

    def waitForGame(self, game):
        s = subprocess.check_output('tasklist', shell=True)
        notRunning = True

        while notRunning:
            if game.encode() in s:
                notRunning = False
                print(game, " Has been detected")

    def waitForGameDefault(self):
        s = subprocess.check_output('tasklist', shell=True)
        notRunning = True

    def getExeName(self, gameName):
        # Fetches the exe name of the game
        cursor.execute("SELECT subprocessProcessName FROM GAMES WHERE Game=?", (gameName,))
        name = cursor.fetchone()
        return name

    def getNumberGames(self):
        # this will include the DB connection to get the number of games
        cursor = conn.cursor()
        sql_query = ("""SELECT COUNT(GameID)
					FROM GAMES
				""")
        cursor.execute(sql_query)
        data = cursor.fetchall()
        data = str(data)
        data = data.replace('(', '')
        data = data.replace(',', '')
        data = data.replace(')', '')
        data = data.replace('[', '')
        data = data.replace(']', '')
        return int(data)

    def getListGames(self):
        # Gets the list of games from db
        sql_query = ("""SELECT 
					Game
					FROM GAMES
				""")

        cursor.execute(sql_query)
        data = cursor.fetchall()
        return data

    def addGameToDatabase(self, game):
        # Inserts new game into database
        sql = "INSERT into GAMES (Game) values (?)"
        cursor.execute(sql, game)
        conn.commit()
        cursor.close()
        return "Game added successfully"


class myThread(threading.Thread):
    
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.exitFlag = 0

    def run(self):
        print("Starting " + self.name)
        self.print_time(self.name, 5, self.counter)
        print("Exiting " + self.name)

    def print_time(self,threadName, counter, delay):
        while counter:
            if self.exitFlag:
                threadName.exit()
            time.sleep(delay)
            print("%s: %s" % (threadName, time.ctime(time.time())))
            counter -= 1


def main():
    root = Tk()
    app = game(root)
    root.mainloop()


if __name__ == "__main__":
    main()
