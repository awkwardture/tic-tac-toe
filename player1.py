"""This module provides game player1 class.

  Typical usage example:

    player1 = Player1(BroadClass(mark="X"))
    player1.start()
"""

from concurrent.futures import ThreadPoolExecutor
from socket import socket, AF_INET, SOCK_STREAM
from time import sleep
from tkinter import simpledialog, Tk, NORMAL
from tkinter.messagebox import askyesno

from constant import *
from gameboard import BoardClass


class Player1:

    def __init__(self) -> None:
        """Game player1,also a socket client,communicate to player2 by socket


        :param board: use to record game statics,such as palyers name,move action,win/tie/loose number and so on
        """
        self.mark = "X"
        self.player2 = ""
        self.player2Mark = "O"
        self.conn = None
        self.thread_pool = ThreadPoolExecutor(3)
        self.board = self.Player1Window(parent=self)
        self.board.show()

    def start(self, host, port) -> None:
        try:
            self.conn = socket(AF_INET, SOCK_STREAM)
            self.conn.connect((host, port))
            self.board.fireGevent(type=UPDATEGAMESBOARD, args={'status': CONNECTED})
        except OSError as e:
            self.conn.close()
            errmsg = 'OS error!%s' % e
            print(errmsg)
            self.board.fireGevent(type=UPDATEGAMESBOARD, args={'status': errmsg})

            again = self.board.again("Connection error,do you want try again?")
            if again:
                raise e
            else:
                raise RuntimeError('Game end')
        try:
            self.exchangeName(self.conn)
        except Exception as e:
            self.dealError(e)

    def sendCmd(self, cmd):
        self.board.setLastplayer(self.board.getPlayersname())
        result = self.board.gameResult(self.mark)
        print("dddddddddddddd====", result)
        if result == "next":
            self.conn.send(cmd.encode('utf-8'))
            self.board.fireGevent(type=UPDATEGAMESBOARD, args={'status': P1WAITING})
            data = self.conn.recv(1024)
            datastr = data.decode("utf-8")
            print('recive:%s' % datastr)
            self.dealRequest(datastr)
            p2result = self.board.gameResult(self.player2Mark)
            if p2result != "next":
                self.updGameResult(p2result)
                result = p2result
                if p2result == "win":
                    result = "loose"
                self.replay(result, self.conn)
            else:
                self.board.fireGevent(type=UPDATEGAMESBOARD, args={'status': PLAYING})
        else:
            self.replay(result, self.conn)

    def updGameResult(self, val) -> None:
        if val == "win":
            self.board.updLooses()
        elif val == "tie":
            self.board.updTies()
        elif val == "loose":
            self.board.updWins()

    def replay(self, data: str, conn: socket) -> None:
        # res = ""
        again = self.board.again("Game end,you %s! Do you want play again?" % data)
        if again:
            cmd = "Play Again,%s" % data
            conn.send(cmd.encode('utf-8'))
            self.board.printStats()
            self.board.resetGameBoard(enable=True)
        else:
            cmd = "Fun Times,%s" % data
            conn.send(cmd.encode('utf-8'))
            # res = "break"
            self.board.printStats()
            sleep(10)
            self.board.quit()
        # return res

    def dealError(self, e) -> None:
        errmsg = 'OS error!%s' % e
        print(errmsg)
        self.board.fireGevent(type=UPDATEGAMESBOARD, args={'status': errmsg})
        state = True
        if self.conn.fileno() < 0:
            state = False
        self.board.resetGameBoard(enable=state)
        self.board.updError()
        errmsg = "{}".format(e)
        if errmsg == "Game end":
            self.board.quit()

    def exchangeName(self, conn) -> None:
        name = self.board.askPlayerName()
        self.board.fireGevent(type=SETPLAYERSNAME, args={'name': name})
        cmd = "Name,%s" % name
        conn.send(cmd.encode('utf-8'))
        data = conn.recv(1024)
        datastr = data.decode("utf-8")
        print('recive:', datastr)
        self.board.fireGevent(type=UPDATEGAMESBOARD, args={'status': 'recive:%s' % datastr})
        self.dealRequest(datastr)

    def dealRequest(self, data: str) -> None:
        kv = data.split(",")
        cmd = kv[0]
        val = kv[1]
        if cmd == "Name":
            self.player2 = val
            self.board.fireGevent(type=UPDATEGAMESBOARD, args={'status': PLAYING})
        elif cmd == "Move":
            p2index = int(val)
            self.board.setLastplayer(self.player2)
            self.board.fireGevent(type=UPDATEGAMESBOARD,
                                  args={'status': 'recive:%s' % data, 'isbt': True, 'index': p2index,
                                        'mark': self.player2Mark})
            while self.board.buttons[p2index]['text'] != self.player2Mark:
                sleep(1)

    class Player1Window(BoardClass):

        def __init__(self, who: int = 1, parent=None) -> None:
            super().__init__(mark="X", who=who, parent=parent)

        def startPlayer1(self) -> None:
            try:
                self.parent.start(self.getHost(), int(self.getPort()))
            except Exception as e:
                self.parent.dealError(e)
                self.buttonConnect.configure(state=NORMAL)

        def startPlayer2(self) -> None:
            pass

        def again(self, prompt) -> bool:
            return askyesno(self.root, prompt)

        def askPlayerName(self) -> str:
            newWin = Tk()
            newWin.withdraw()
            newWin.geometry('370x330+400+182')
            name = simpledialog.askstring(title="tic-tac-toe game",
                                          prompt="What's your name?", parent=newWin)
            newWin.destroy()
            return name


def main() -> None:
    player1 = Player1()
    # player1.start()


if __name__ == '__main__':
    main()
