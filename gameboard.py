from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from time import sleep
from tkinter import *
from tkinter.scrolledtext import ScrolledText

from constant import *


class BoardClass:

    def __init__(self, title: str = "tic-tac-toe game", who: int = 2, name: str = "", mark: str = "",
                 parent=None) -> None:
        self.line = 0
        self.thread_pool = ThreadPoolExecutor(5)
        self.who = who
        self.state = INIT
        self.root = Tk()
        self.root.title(title)
        self.root.geometry('370x330+400+182')
        self.labelName = None
        self.textStatus = None
        self.entryHost = None
        self.entryPort = None
        self.buttonServ = None
        self.buttonConnect = None
        self.frameR0C1 = None
        self.parent = parent
        self.buttons = []
        self.q = Queue(maxsize=0)

        self.name = name
        self.lastplayer = ""
        self.wins = 0
        self.ties = 0
        self.looses = 0
        self.oserror = 0
        self.played = 0
        self.mark = mark

        self.draw()

    def resetGameBoard(self, enable: bool = False) -> None:
        self.buttons = []
        if enable:
            btstate = NORMAL
        else:
            btstate = DISABLED

        self.frameR0C1 = Frame(self.root, highlightbackground="blue", highlightthickness=1)
        self.frameR0C1.grid(row=0, column=1, rowspan=3, sticky=N)

        frameR0C1_R0C0 = Frame(self.frameR0C1)
        frameR0C1_R0C0.grid(row=0, column=0)
        labelTitle = Label(frameR0C1_R0C0, text="Game Board")
        labelTitle.grid(row=0, column=0)

        frameR0C1_R1C0 = Frame(self.frameR0C1)
        frameR0C1_R1C0.grid(row=1, column=0)
        index = 0
        for i in range(0, 3):
            for j in range(0, 3):
                button = Button(frameR0C1_R1C0, text=" ", command=lambda m=index: self.onClick(m), width=5, height=5,
                                state=btstate)
                self.buttons.append(button)
                button.grid(row=i, column=j)
                index += 1

    def draw(self) -> None:
        frameR0C0 = Frame(self.root)
        frameR0C0.grid(row=0, column=0, sticky=NW)

        labelHost = Label(frameR0C0, text="hostname/IP:")
        labelHost.grid(row=0, column=0, sticky=NW)
        self.entryHost = Entry(frameR0C0)
        self.entryHost.grid(row=0, column=1, sticky=NW)
        labelPort = Label(frameR0C0, text="port:")
        labelPort.grid(row=1, column=0, sticky=NW)
        self.entryPort = Entry(frameR0C0)
        self.entryPort.grid(row=1, column=1, sticky=NW)
        if self.who == 2:
            self.buttonServ = Button(frameR0C0, text="start server", command=self.onClickServ)
            self.buttonServ.grid(row=2, column=0, columnspan=2, sticky=NW)
        if self.who == 1:
            self.buttonConnect = Button(frameR0C0, text="connect server", command=self.onclickConnect)
            self.buttonConnect.grid(row=2, column=0, columnspan=2, sticky=NW)
        self.labelName = Label(frameR0C0, text="Your name:")
        self.labelName.grid(row=3, column=0, columnspan=2, sticky=NW)

        labelStatus = Label(self.root, text="Game infomations:")
        labelStatus.grid(row=1, column=0, sticky=NW)
        self.textStatus = ScrolledText(self.root, width=30, height=14)
        self.textStatus.grid(row=2, column=0, columnspan=2, sticky=NW)
        self.updateGamesBoard(STARTING)

        self.resetGameBoard()

    def show(self):
        self.root.after(0, lambda: self.dealEvent())
        self.root.mainloop()

    def dealEvent(self):
        while not self.q.empty():
            event = self.q.get()
            print("收到消息%s" % event.getType())
            if event is not None:
                self.handleEvent(event)
        self.root.after(30, lambda: self.dealEvent())

    def handleEvent(self, event):
        eType = event.getType()
        eArgs = event.getArgs()
        if eType == UPDATEGAMESBOARD:
            self.updateGamesBoard(**eArgs)
        if eType == SETPLAYERSNAME:
            self.setPlayersname(**eArgs)

    def onClickServ(self) -> None:
        self.buttonServ.configure(state=DISABLED)
        exc = self.thread_pool.submit(self.startPlayer2)
        exc.add_done_callback(self.thread_pool_callback)

    def startPlayer2(self) -> None:
        raise NotImplementedError('Please define "a startPlayer2 method"')

    def onclickConnect(self) -> None:
        self.buttonConnect.configure(state=DISABLED)
        exc = self.thread_pool.submit(self.startPlayer1)
        exc.add_done_callback(self.thread_pool_callback)

    def startPlayer1(self) -> None:
        raise NotImplementedError('Please define "a startPlayer1 method"')

    def thread_pool_callback(self, worker):
        worker_exception = worker.exception()
        if worker_exception:
            self.updateGamesBoard("Worker return exception: {}".format(worker_exception))
            if self.buttonServ is not None:
                self.buttonServ.configure(state=NORMAL)
            if self.buttonConnect is not None:
                self.buttonConnect.configure(state=NORMAL)
        errmsg = "{}".format(worker_exception)
        if errmsg == "Game end":
            self.quit()

    def quit(self):
        self.root.quit()

    def onClick(self, index: int) -> None:
        self.disableAllBt()
        exc = self.thread_pool.submit(lambda m=index: self.dealClick(m))
        exc.add_done_callback(self.thread_pool_callback)

    def dealClick(self, index: int) -> None:
        cmd = "Move,%d" % index
        self.fireGevent(type=UPDATEGAMESBOARD, args={'status': cmd, 'isbt': True, 'index': index, 'mark': self.mark})
        while self.buttons[index]['text'] != self.mark:
            sleep(1)
        self.parent.sendCmd(cmd)

    def fireGevent(self, type, args):
        self.q.put(GEvent(type=type, args=args))

    def updateGamesBoard(self, status: str, isbt: bool = False, index: int = 0, mark: str = "") -> None:
        self.line += 1
        self.state = status
        self.textStatus.insert(END, "[%d]" % self.line + status + "\n")
        self.textStatus.yview_moveto(1)
        self.textStatus.update()
        if isbt:
            self.buttons[index].configure(text=mark, state=DISABLED)
        if status == STARTED:
            self.buttonServ.configure(state=DISABLED)
            self.entryPort.configure(state=DISABLED)
            self.entryHost.configure(state=DISABLED)
        if status == CONNECTED:
            self.buttonConnect.configure(state=DISABLED)
            self.entryPort.configure(state=DISABLED)
            self.entryHost.configure(state=DISABLED)
        if status == PLAYING:
            for b in self.buttons:
                if b['text'] == " ":
                    b.configure(state=NORMAL)
                else:
                    b.configure(state=DISABLED)
        if status == P1WAITING or status == P2WAITING:
            self.disableAllBt()

    def disableAllBt(self):
        for b in self.buttons:
            b.configure(state=DISABLED)

    def getHost(self):
        return self.entryHost.get()

    def getPort(self):
        return self.entryPort.get()

    def setPlayersname(self, name: str) -> None:
        self.name = name
        self.labelName.configure(text="Your name:%s" % name)

    def getPlayersname(self) -> str:
        return self.name

    def setLastplayer(self, lastplayer: str) -> None:
        self.lastplayer = lastplayer

    def updWins(self) -> None:
        self.wins += 1
        self.updateGamesPlayed()

    def updTies(self) -> None:
        self.ties += 1
        self.updateGamesPlayed()

    def updLooses(self) -> None:
        self.looses += 1
        self.updateGamesPlayed()

    def updError(self) -> None:
        self.oserror += 1
        self.updateGamesPlayed()

    def printStats(self) -> None:
        self.updateGamesBoard(status="players name:%s" % self.name)
        self.updateGamesBoard(status="lastplayer:%s" % self.lastplayer)
        self.updateGamesBoard(status="game played:%d" % self.played)
        self.updateGamesBoard(status="game wins:%d" % self.wins)
        self.updateGamesBoard(status="game ties:%d" % self.ties)
        self.updateGamesBoard(status="game looses:%s" % self.looses)
        self.updateGamesBoard(status="game error:%s" % self.oserror)

    def updError(self) -> None:
        self.oserror += 1
        self.updateGamesPlayed()

    def updateGamesPlayed(self) -> None:
        self.played += 1

    def isWinner(self, mark: str) -> bool:
        for i in range(0, 9):
            print(i, ":", self.buttons[i]['text'])

        win = False
        # Horizontal winning condition
        if self.buttons[0]['text'] == self.buttons[1]['text'] and self.buttons[1]['text'] == self.buttons[2]['text'] and \
                self.buttons[1]['text'] == mark:
            win = True
        elif self.buttons[3]['text'] == self.buttons[4]['text'] and self.buttons[4]['text'] == self.buttons[5][
            'text'] and self.buttons[3]['text'] == mark:
            win = True
        elif self.buttons[6]['text'] == self.buttons[7]['text'] and self.buttons[7]['text'] == self.buttons[8][
            'text'] and self.buttons[6]['text'] == mark:
            win = True
        # Vertical Winning Condition
        elif self.buttons[0]['text'] == self.buttons[3]['text'] and self.buttons[3]['text'] == self.buttons[6][
            'text'] and self.buttons[0]['text'] == mark:
            win = True
        elif self.buttons[1]['text'] == self.buttons[4]['text'] and self.buttons[4]['text'] == self.buttons[7][
            'text'] and self.buttons[1]['text'] == mark:
            win = True
        elif self.buttons[2]['text'] == self.buttons[5]['text'] and self.buttons[5]['text'] == self.buttons[8][
            'text'] and self.buttons[2]['text'] == mark:
            win = True
        # Diagonal Winning Condition
        elif self.buttons[0]['text'] == self.buttons[4]['text'] and self.buttons[4]['text'] == self.buttons[8][
            'text'] and self.buttons[0]['text'] == mark:
            win = True
        elif self.buttons[2]['text'] == self.buttons[4]['text'] and self.buttons[4]['text'] == self.buttons[6][
            'text'] and self.buttons[2]['text'] == mark:
            win = True

        if win and mark == self.mark:
            self.updWins()

        return win

    def boardIsFull(self, mark: str) -> bool:
        full = False
        if (self.buttons[0]['text'] != ' ' and self.buttons[1]['text'] != ' ' and self.buttons[2]['text'] != ' ' and
                self.buttons[3]['text'] != ' ' and self.buttons[4]['text'] != ' ' and self.buttons[5]['text'] != ' ' and
                self.buttons[6]['text'] != ' ' and self.buttons[7]['text'] != ' ' and self.buttons[8]['text'] != ' '):
            full = True
        if full and mark == self.mark:
            self.updTies()
        return full

    def gameResult(self, mark: str) -> str:
        result = self.isWinner(mark)
        if result:
            return "win"
        elif self.boardIsFull(mark):
            return "tie"
        else:
            return "next"


class GEvent:
    def __init__(self, type: str, args: dict) -> None:
        self.type = type
        self.args = args

    def getType(self):
        return self.type

    def getArgs(self):
        return self.args


def main() -> None:
    gui = BoardClass()


if __name__ == '__main__':
    main()
