"""This module provides game player2 class.

  Typical usage example:

    player2 = Player2(BroadClass(name="player2", mark="O"))
    player2.start()
"""

from concurrent.futures import ThreadPoolExecutor
from socket import socket, AF_INET, SOCK_STREAM
from time import sleep
from tkinter import NORMAL

from constant import *
from gameboard import BoardClass


class Player2:

    def __init__(self) -> None:
        """Game player2 is a socket server,accept player1's connection,it process game data received from player1 and
        also send game data to player1


        :param board: use to record game statics,such as palyers name,move position,win/tie/loose number and so on
        """
        self.name = "player2"
        self.player1 = ""
        self.mark = "O"
        self.player1Mark = "X"
        self.thread_pool = ThreadPoolExecutor(3)
        self.conn = None
        self.board = self.Player2Window(parent=self)
        self.board.show()

    def start(self, host, port) -> None:

        s = socket(AF_INET, SOCK_STREAM)
        s.bind((host, port))
        s.listen(128)
        self.board.fireGevent(type=UPDATEGAMESBOARD, args={'status': STARTED})
        res = ""
        while True:
            conn, addr = s.accept()
            self.conn = conn
            self.board.fireGevent(type=UPDATEGAMESBOARD, args={'status': NEWCONN})
            while True:
                try:
                    data = conn.recv(1024)
                    datastr = data.decode("utf-8")
                    print('recive:', datastr)
                    self.board.fireGevent(type=UPDATEGAMESBOARD, args={'status': 'recive:%s' % datastr})
                    res = self.dealRequest(datastr, conn)
                    if res == "Fun Times":
                        break
                except OSError as e:
                    self.dealError(e)
                    break
            conn.close()
            if res == "Fun Times":
                break
        s.close()
        sleep(10)
        self.board.quit()

    def dealRequest(self, data: str, conn: socket) -> str:
        kv = data.split(",")
        cmd = kv[0]
        val = kv[1]
        if cmd == "Name":
            self.player1 = val
            self.board.fireGevent(type=SETPLAYERSNAME,
                                  args={'name': self.name})
            cmd = "Name,%s" % self.name
            conn.send(cmd.encode('utf-8'))
            self.board.fireGevent(type=UPDATEGAMESBOARD, args={'status': P2WAITING})
        elif cmd == "Move":
            self.board.fireGevent(type=UPDATEGAMESBOARD,
                                  args={'status': PLAYING, 'isbt': True, 'index': int(val), 'mark': self.player1Mark})
            self.board.setLastplayer(self.player1)
        elif cmd == "Play Again":
            self.updGameResult(val)
            self.board.printStats()
            self.board.resetGameBoard()
        elif cmd == "Fun Times":
            self.updGameResult(val)
            self.board.printStats()
        return cmd

    def sendCmd(self, cmd):
        self.conn.send(cmd.encode('utf-8'))
        self.board.setLastplayer(self.name)
        self.board.fireGevent(type=UPDATEGAMESBOARD, args={'status': P2WAITING})

    def dealError(self, e) -> None:
        errmsg = 'OS error!%s' % e
        print(errmsg)
        self.board.fireGevent(type=UPDATEGAMESBOARD, args={'status': errmsg})
        self.board.resetGameBoard()
        self.board.updError()

    def updGameResult(self, val):
        if val == "win":
            self.board.updLooses()
        elif val == "tie":
            self.board.updTies()
        elif val == "loose":
            self.board.updWins()

    class Player2Window(BoardClass):

        def __init__(self, who: int = 2, parent=None) -> None:
            super().__init__(mark="O", who=who, parent=parent)

        def startPlayer2(self) -> None:
            try:
                self.parent.start(self.getHost(), int(self.getPort()))
            except OSError as e:
                self.parent.dealError(e)
                self.buttonServ.configure(state=NORMAL)

        def startPlayer1(self) -> None:
            pass


def main() -> None:
    player2 = Player2()
    # player2.start()


if __name__ == '__main__':
    main()
