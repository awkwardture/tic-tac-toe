"""This module provides game player2 class.

  Typical usage example:

    player2 = Player2(BroadClass(name="player2", mark="O"))
    player2.start()
"""
import _thread
from socket import socket, AF_INET, SOCK_STREAM

from gameboard import BoardClass


class Player2:

    def __init__(self) -> None:
        """Game player2 is a socket server,accept player1's connection,it process game data received from player1 and
        also send game data to player1


        :param board: use to record game statics,such as palyers name,move position,win/tie/loose number and so on
        """
        self.mark = "O"
        self.player1Mark = "X"
        self.board = BoardClass(mark=self.mark)
        _thread.start_new_thread(self.start, ())
        self.board.show()

    def start(self) -> None:

        s = socket(AF_INET, SOCK_STREAM)
        s.bind((self.board.host, self.board.port))
        s.listen(128)
        res = ""
        while True:
            conn, addr = s.accept()
            self.board.setClient(conn)
            while True:
                try:
                    datastr = conn.recv(1024).decode()
                    print('recive:', datastr)
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
        self.board.quit()

    def dealRequest(self, data: str, conn: socket) -> str:
        kv = data.split(",")
        cmd = kv[0]
        val = kv[1]
        if cmd == "Name":
            self.board.player1 = val
            cmd = "Name,%s" % self.board.player2
            conn.send(cmd.encode('utf-8'))
        elif cmd == "Move":
            if val == "1":
                self.board.updateGamesBoard(self.board.btn1, self.player1Mark, self.board.player1)
            elif val == "2":
                self.board.updateGamesBoard(self.board.btn2, self.player1Mark, self.board.player1)
            elif val == "3":
                self.board.updateGamesBoard(self.board.btn3, self.player1Mark, self.board.player1)
            elif val == "4":
                self.board.updateGamesBoard(self.board.btn4, self.player1Mark, self.board.player1)
            elif val == "5":
                self.board.updateGamesBoard(self.board.btn5, self.player1Mark, self.board.player1)
            elif val == "6":
                self.board.updateGamesBoard(self.board.btn6, self.player1Mark, self.board.player1)
            elif val == "7":
                self.board.updateGamesBoard(self.board.btn7, self.player1Mark, self.board.player1)
            elif val == "8":
                self.board.updateGamesBoard(self.board.btn8, self.player1Mark, self.board.player1)
            elif val == "9":
                self.board.updateGamesBoard(self.board.btn9, self.player1Mark, self.board.player1)
        elif cmd == "Play Again":
            self.board.computeStats(val, False)
            self.board.resetGameBoard()
        elif cmd == "Fun Times":
            self.board.computeStats(val, False)
            self.board.quit()
        return cmd

    def dealError(self, e) -> None:
        errmsg = 'OS error!%s' % e
        print(errmsg)
        self.board.resetGameBoard()


def main() -> None:
    player2 = Player2()


if __name__ == '__main__':
    main()
