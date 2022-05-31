from tkinter import *
from tkinter import simpledialog
from tkinter.messagebox import askyesno


class BoardClass:

    def __init__(self, mark: str) -> None:

        self.lastplayer = ""

        self.btn1 = None
        self.btn2 = None
        self.btn3 = None
        self.btn4 = None
        self.btn5 = None
        self.btn6 = None
        self.btn7 = None
        self.btn8 = None
        self.btn9 = None
        self.wins = 0
        self.ties = 0
        self.looses = 0
        self.played = 0
        self.player1 = ""
        self.player2 = ""
        self.mark = mark
        self.host = ""
        self.port = 0
        self.client = None
        self.labelWin = None
        self.labelLoose = None
        self.labelTie = None
        self.labelPlayed = None
        self.labelLastPlayer = None
        self.labelturn = None
        self.root = Tk()
        self.root.title("tic-tac-toe")
        self.root.geometry('400x300+400+182')
        self.draw()
        self.resetGameBoard()

    def draw(self):
        f0 = Frame(self.root)
        f0.grid(row=0, column=1)
        self.host = simpledialog.askstring(title="tic-tac-toe game",
                                           prompt="Please input game server's hostname/IP")
        labelHost = Label(f0, text="hostname/IP:%s" % self.host)
        labelHost.grid(row=0, column=0, sticky=NW)
        self.port = simpledialog.askinteger(title="tic-tac-toe game",
                                            prompt="Please input game server's port")
        labelPort = Label(f0, text="port:%d" % self.port)
        labelPort.grid(row=1, column=0, sticky=NW)
        name = simpledialog.askstring(title="tic-tac-toe game",
                                      prompt="Please input your name")
        labelName = Label(f0, text="Your name:%s" % name)
        if self.mark == "X":
            self.player1 = name
        if self.mark == "O":
            self.player2 = name
        labelName.grid(row=2, column=0, sticky=NW)
        self.labelWin = Label(f0, text="You wins:%d" % self.wins)
        self.labelWin.grid(row=3, column=0, sticky=NW)
        self.labelLoose = Label(f0, text="You looses:%d" % self.looses)
        self.labelLoose.grid(row=4, column=0, sticky=NW)
        self.labelTie = Label(f0, text="Game ties:%d" % self.ties)
        self.labelTie.grid(row=5, column=0, sticky=NW)
        self.labelPlayed = Label(f0, text="Total played:%d" % self.played)
        self.labelPlayed.grid(row=6, column=0, sticky=NW)
        self.labelLastPlayer = Label(f0, text="lastplayer:%s" % self.lastplayer)
        self.labelLastPlayer.grid(row=7, column=0, sticky=NW)
        self.labelturn = Label(f0, text="who's trun:")
        self.labelturn.grid(row=8, column=0, sticky=NW)

        f1 = Frame(self.root)
        f1.grid(row=0, column=0)
        self.btn1 = Button(f1, text=" ", width=10, height=5, command=self.onClickBtn1)
        self.btn1.grid(row=3, column=0)
        self.btn2 = Button(f1, text=" ", width=10, height=5, command=self.onClickBtn2)
        self.btn2.grid(row=3, column=1)
        self.btn3 = Button(f1, text=" ", width=10, height=5, command=self.onClickBtn3)
        self.btn3.grid(row=3, column=2)
        self.btn4 = Button(f1, text=" ", width=10, height=5, command=self.onClickBtn4)
        self.btn4.grid(row=4, column=0)
        self.btn5 = Button(f1, text=" ", width=10, height=5, command=self.onClickBtn5)
        self.btn5.grid(row=4, column=1)
        self.btn6 = Button(f1, text=" ", width=10, height=5, command=self.onClickBtn6)
        self.btn6.grid(row=4, column=2)
        self.btn7 = Button(f1, text=" ", width=10, height=5, command=self.onClickBtn7)
        self.btn7.grid(row=5, column=0)
        self.btn8 = Button(f1, text=" ", width=10, height=5, command=self.onClickBtn8)
        self.btn8.grid(row=5, column=1)
        self.btn9 = Button(f1, text=" ", width=10, height=5, command=self.onClickBtn9)
        self.btn9.grid(row=5, column=2)

    def resetGameBoard(self) -> None:

        self.lastplayer = self.player2
        self.labelLastPlayer['text'] = "lastplayer:%s" % self.lastplayer
        self.labelturn['text'] = "who's trun:%s" % self.player1
        self.btn1['text'] = " "
        self.btn2['text'] = " "
        self.btn3['text'] = " "
        self.btn4['text'] = " "
        self.btn5['text'] = " "
        self.btn6['text'] = " "
        self.btn7['text'] = " "
        self.btn8['text'] = " "
        self.btn9['text'] = " "
        self.btn1['state'] = NORMAL
        self.btn2['state'] = NORMAL
        self.btn3['state'] = NORMAL
        self.btn4['state'] = NORMAL
        self.btn5['state'] = NORMAL
        self.btn6['state'] = NORMAL
        self.btn7['state'] = NORMAL
        self.btn8['state'] = NORMAL
        self.btn9['state'] = NORMAL

    def show(self):
        self.root.mainloop()

    def quit(self):
        self.root.quit()

    def onClickBtn1(self) -> None:
        self.doSend("Move,1", self.btn1)

    def onClickBtn2(self) -> None:
        self.doSend("Move,2", self.btn2)

    def onClickBtn3(self) -> None:
        self.doSend("Move,3", self.btn3)

    def onClickBtn4(self) -> None:
        self.doSend("Move,4", self.btn4)

    def onClickBtn5(self) -> None:
        self.doSend("Move,5", self.btn5)

    def onClickBtn6(self) -> None:
        self.doSend("Move,6", self.btn6)

    def onClickBtn7(self) -> None:
        self.doSend("Move,7", self.btn7)

    def onClickBtn8(self) -> None:
        self.doSend("Move,8", self.btn8)

    def onClickBtn9(self) -> None:
        self.doSend("Move,9", self.btn9)

    def doSend(self, msg, btn):
        if self.mark == "X":
            if self.lastplayer != self.player1:
                self.updLastplayer(self.player1,True)
                btn['text'] = self.mark
                btn['state'] = DISABLED
                result = self.gameResult(self.mark)
                if result == "next":
                    self.client.send(msg.encode())
                else:
                    self.replay(result)
        if self.mark == "O":
            if self.lastplayer == self.player1:
                self.updLastplayer(self.player2,True)
                btn['text'] = self.mark
                btn['state'] = DISABLED
                self.client.send(msg.encode())

    def updateGamesBoard(self, btn, mark, player) -> None:
        btn['text'] = mark
        btn['state'] = DISABLED
        self.updLastplayer(player,False)
        if self.mark == "X":
            result = self.gameResult(mark)
            if mark == "O":
                if result == "win":
                    result = "loose"
            if result != "next":
                self.replay(result)

    def replay(self, data: str) -> None:
        again = self.again("Game end,you %s! Do you want play again?" % data)
        if again:
            cmd = "Play Again,%s" % data
            self.client.send(cmd.encode())
            self.computeStats(data, True)
            self.resetGameBoard()
        else:
            cmd = "Fun Times,%s" % data
            self.client.send(cmd.encode())
            self.computeStats(data, True)
            self.quit()

    def updLastplayer(self, player,send) -> None:
        self.lastplayer = player
        self.labelLastPlayer['text'] = "lastplayer:%s" % self.lastplayer
        if send:
            if self.mark == "X":
                self.labelturn['text'] = "who's trun:%s" % self.player2
            else:
                self.labelturn['text'] = "who's trun:%s" % self.player1
        else:
            if self.mark == "X":
                self.labelturn['text'] = "who's trun:%s" % self.player1
            else:
                self.labelturn['text'] = "who's trun:%s" % self.player2

    def updWins(self) -> None:
        self.wins += 1
        self.updateGamesPlayed()
        self.labelWin['text'] = "You wins:%d" % self.wins

    def updTies(self) -> None:
        self.ties += 1
        self.updateGamesPlayed()
        self.labelTie['text'] = "Game ties:%d" % self.ties

    def updLooses(self) -> None:
        self.looses += 1
        self.updateGamesPlayed()
        self.labelLoose['text'] = "You looses:%d" % self.looses

    def updateGamesPlayed(self) -> None:
        self.played += 1
        self.labelPlayed['text'] = "Total played:%d" % self.played

    def computeStats(self, val, p1) -> (str, str, str, int, int, int, int):
        if p1:
            if val == "win":
                self.updWins()
            elif val == "tie":
                self.updTies()
            elif val == "loose":
                self.updLooses()
        else:
            if val == "win":
                self.updLooses()
            elif val == "tie":
                self.updTies()
            elif val == "loose":
                self.updWins()

        return self.player1, self.player2, self.lastplayer, self.played, self.wins, self.ties, self.looses

    def isWinner(self, mark: str) -> bool:
        win = False
        # Horizontal winning condition
        if self.btn1['text'] == self.btn2['text'] and self.btn2['text'] == self.btn3['text'] and \
                self.btn1['text'] == mark:
            win = True
        elif self.btn4['text'] == self.btn5['text'] and self.btn5['text'] == self.btn6['text'] and \
                self.btn4['text'] == mark:
            win = True
        elif self.btn7['text'] == self.btn8['text'] and self.btn8['text'] == self.btn9['text'] and \
                self.btn7['text'] == mark:
            win = True
        # Vertical Winning Condition
        elif self.btn1['text'] == self.btn4['text'] and self.btn4['text'] == self.btn7['text'] and \
                self.btn1['text'] == mark:
            win = True
        elif self.btn2['text'] == self.btn5['text'] and self.btn5['text'] == self.btn8['text'] and \
                self.btn2['text'] == mark:
            win = True
        elif self.btn3['text'] == self.btn6['text'] and self.btn6['text'] == self.btn9['text'] and \
                self.btn3['text'] == mark:
            win = True
        # Diagonal Winning Condition
        elif self.btn1['text'] == self.btn5['text'] and self.btn5['text'] == self.btn9['text'] and \
                self.btn1['text'] == mark:
            win = True
        elif self.btn3['text'] == self.btn5['text'] and self.btn5['text'] == self.btn7['text'] and \
                self.btn3['text'] == mark:
            win = True

        return win

    def boardIsFull(self, mark: str) -> bool:
        full = False
        if (self.btn1['text'] != ' ' and self.btn2['text'] != ' ' and self.btn3['text'] != ' ' and
                self.btn4['text'] != ' ' and self.btn5['text'] != ' ' and self.btn6['text'] != ' ' and
                self.btn7['text'] != ' ' and self.btn8['text'] != ' ' and self.btn9['text'] != ' '):
            full = True

        return full

    def gameResult(self, mark: str) -> str:
        result = self.isWinner(mark)
        if result:
            return "win"
        elif self.boardIsFull(mark):
            return "tie"
        else:
            return "next"

    def again(self, prompt) -> bool:
        return askyesno(self.root, prompt)

    def setClient(self, client):
        self.client = client


def main() -> None:
    gui = BoardClass(mark="X")
    gui.show()


if __name__ == '__main__':
    main()
