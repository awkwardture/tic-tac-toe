"""This module provides game player1 class.

  Typical usage example:

    player1 = Player1(BroadClass(mark="X"))
    player1.start()
"""
import _thread
from socket import socket, AF_INET, SOCK_STREAM

from gameboard import BoardClass


class Player1:

    def __init__(self) -> None:
        """Game player1,also a socket client,communicate to player2 by socket


        :param board: use to record game statics,such as palyers name,move action,win/tie/loose number and so on
        """
        self.mark = "X"
        self.player2Mark = "O"
        self.conn = None
        self.board = BoardClass(mark=self.mark)
        _thread.start_new_thread(self.start, ())
        self.board.show()

    def start(self) -> None:
        while True:
            try:
                self.conn = socket(AF_INET, SOCK_STREAM)
                self.conn.connect((self.board.host, self.board.port))
                self.board.setClient(self.conn)
                break
            except OSError as e:
                self.conn.close()
                errmsg = 'OS error!%s' % e
                print(errmsg)
                again = self.board.again("Connection error,do you want try again?")
                if again:
                    continue
                else:
                    self.board.quit()

        self.exchangeName(self.conn)
        while True:
            msg = self.conn.recv(1024).decode()
            if msg == 'Move,1':
                self.board.updateGamesBoard(self.board.btn1, self.player2Mark, self.board.player2)
            elif msg == 'Move,2':
                self.board.updateGamesBoard(self.board.btn2, self.player2Mark, self.board.player2)
            elif msg == 'Move,3':
                self.board.updateGamesBoard(self.board.btn3, self.player2Mark, self.board.player2)
            elif msg == 'Move,4':
                self.board.updateGamesBoard(self.board.btn4, self.player2Mark, self.board.player2)
            elif msg == 'Move,5':
                self.board.updateGamesBoard(self.board.btn5, self.player2Mark, self.board.player2)
            elif msg == 'Move,6':
                self.board.updateGamesBoard(self.board.btn6, self.player2Mark, self.board.player2)
            elif msg == 'Move,7':
                self.board.updateGamesBoard(self.board.btn7, self.player2Mark, self.board.player2)
            elif msg == 'Move,8':
                self.board.updateGamesBoard(self.board.btn8, self.player2Mark, self.board.player2)
            elif msg == 'Move,9':
                self.board.updateGamesBoard(self.board.btn9, self.player2Mark, self.board.player2)

    def exchangeName(self, conn) -> None:
        cmd = "Name,%s" % self.board.player1
        conn.send(cmd.encode())
        data = conn.recv(1024).decode()
        self.board.player2 = data.split(",")[1]


def main() -> None:
    player1 = Player1()


if __name__ == '__main__':
    main()
