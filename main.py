# import packages for program
import copy, random


# class to contain all of the battleship game
class BattleshipGame:
    # function to print the board
    def print_board(self, s, board):
        # see if computer or user turn
        player = "Computer"
        if s == "u":
            player = "User"
        print("This is how the " + player + "'s board look: \n")
        # print the horiz numbers
        print("  ", end=' ')
        for i in range(10):
            print("  " + str(i + 1) + "  ", end=' ')
        print("\n")
        for i in range(10):
            # print the vertical line number
            if i != 9:
                print(str(i + 1) + "  ", end=' ')
            else:
                print(str(i + 1) + " ", end=' ')
            # print the board values
            for j in range(10):
                if board[i][j] == -1:
                    print(' ', end=' ')
                elif s == "u":
                    print(board[i][j], end=' ')
                elif s == "c":
                    if board[i][j] == "*" or board[i][j] == "$":
                        print(board[i][j], end=' ')
                    else:
                        print(" ", end=' ')
                if j != 9:
                    print(" || ", end=' ')
            print()
            # print a horizontal line at end of rows
            if i != 9:
                print("   __________________________________________________________")
            else:
                print()

                # function to let the user place the ships

    def user_place_ships(self, board, ships):
        """
        allows the user to place ships and check whether they are in valid placements
        """
        for ship in list(ships.keys()):
            # get coords and validate position
            valid = False
            while (not valid):
                self.print_board("u", board)
                print("Putting an/a " + ship + " in place")
                x, y = self.get_coor()
                ori = self.v_or_h()
                valid = self.validate(board, ships[ship], x, y, ori)
                if not valid:
                    print("A ship can't be placed there.\nPlease review the board and try once more.")
                    input("Continue by pressing enter.")
            # place the ship
            board = self.place_ship(board, ships[ship], ship[0], ori, x, y)
            self.print_board("u", board)
        input("Our ships are ready, please ENTER to go to war!")
        return board

    # let the computer place/validate ships
    def computer_place_ships(self, board, ships):
        """
        computer will user random to generate ship places
        """
        for ship in list(ships.keys()):
            # genreate random coordinates and validate the postion
            valid = False
            while (not valid):
                # use randint from import random
                x = random.randint(1, 10) - 1
                y = random.randint(1, 10) - 1
                o = random.randint(0, 1)
                # vertical or horiz
                if o == 0:
                    ori = "v"
                else:
                    ori = "h"
                valid = self.validate(board, ships[ship], x, y, ori)
            # place the ship
            print("Computer placing a/an " + ship)
            board = self.place_ship(board, ships[ship], ship[0], ori, x, y)
        return board

    # let the user place a ship
    def place_ship(self, board, ship, s, ori, x, y):
        """
        accepts board, ship size, and position, places ship, it should already be verified by user_place_ships function
        """
        # orient ships
        if ori == "v":
            for i in range(ship):
                board[x + i][y] = s
        elif ori == "h":
            for i in range(ship):
                board[x][y + i] = s
        return board

    # check if the ship will actually fit, bool
    def validate(self, board, ship, x, y, ori):
        """
        check if ship will fit, based on ship size, board, orientation, and coordinates
        """
        if ori == "v" and x + ship > 10:
            return False
        elif ori == "h" and y + ship > 10:
            return False
        else:
            if ori == "v":
                for i in range(ship):
                    if board[x + i][y] != -1:
                        return False
            elif ori == "h":
                for i in range(ship):
                    if board[x][y + i] != -1:
                        return False
        return True

    # see if ship is horiz or vert
    def v_or_h(self):
        # get ship orientation from user
        while (True):
            user_input = input("vertical or horizontal (v,h) ? ")
            if user_input == "v" or user_input == "h":
                return user_input
            else:
                print("Incorrect input. Please only use the letters v or h.")

    def get_coor(self):
        """
        The user will input coordinates (column and row) for the ship to go.
        """
        while (True):
            user_input = input("Please input (row,col) coordinates?")
            try:
                # see that user entered 2 values seprated by comma
                coor = user_input.split(",")
                if len(coor) != 2:
                    raise Exception("Invalid input, insufficient/excessive coordinates");
                # check that 2 values are integers
                coor[0] = int(coor[0]) - 1
                coor[1] = int(coor[1]) - 1
                # check that values of integers are between 1 and 10 for both coordinates
                if coor[0] > 9 or coor[0] < 0 or coor[1] > 9 or coor[1] < 0:
                    raise Exception("Invalid input. Please only enter values ranging from 1 to 10.")
                # if everything is ok, return coordinates
                return coor
            # if the user enters something different
            except ValueError:
                print("The input is invalid. For coordinates, please only use numbers.")
            except Exception as e:
                print(e)

    # see what move does
    def make_move(self, board, x, y):
        """
        make the move on the board and return the board, modified
        """
        if board[x][y] == -1:
            return "Oh you miss? Unlucky"
        elif board[x][y] == '*' or board[x][y] == '$':
            return "You already hit this one, go shoot somewhere else"
        else:
            return "Bang!"

    def user_move(self, board):
        """
        Continue to obtain coordinates from the user and determine if it was a hit or a miss.
        """
        while (True):
            x, y = self.get_coor()
            res = self.make_move(board, x, y)
            if res == "hit":
                print("Hit at " + str(x + 1) + "," + str(y + 1))
                self.check_sink(board, x, y)
                board[x][y] = '$'
                if self.check_win(board):
                    return "WIN"
            elif res == "miss":
                print("Sorry, " + str(x + 1) + "," + str(y + 1) + " is a miss.")
                board[x][y] = "*"
            elif res == "try again":
                print("Sorry, but that coordinate has already been hit. Please try once more")
            if res != "try again":
                return board

    def computer_move(self, board):
        """
        Create random coorindates for the computer to use
        check for hit, sink, and miss in the same way as user_move function
        """
        while (True):
            x = random.randint(1, 10) - 1
            y = random.randint(1, 10) - 1
            res = self.make_move(board, x, y)
            if res == "hit":
                print("Hit at " + str(x + 1) + "," + str(y + 1))
                self.check_sink(board, x, y)
                board[x][y] = '$'
                if self.check_win(board):
                    return "WIN"
            elif res == "miss":
                print("Sorry, " + str(x + 1) + "," + str(y + 1) + " is a miss.")
                board[x][y] = "*"
            if res != "try again":
                return board

    def check_sink(self, board, x, y):
        """
        Determine which ship has been hit, then calculate how many points remain in the ship, and finally check
        whether it has sunk. If there are no more points, the ship sinks.
        """
        if board[x][y] == "A":
            ship = "Aircraft Carrier"
        elif board[x][y] == "B":
            ship = "Battleship"
        elif board[x][y] == "S":
            ship = "Submarine"
        elif board[x][y] == "C":
            ship = "Cruiser"
        elif board[x][y] == "D":
            ship = "Destroyer"
        # mark cell as hit and check if sunk
        board[-1][ship] -= 1
        if board[-1][ship] == 0:
            print(ship + " Sunk")

    def check_win(self, board):
        """
        When all of the ships are sunk, someone wins and the game is over.
        Return false if anything is not a hit.
        """
        for i in range(10):
            for j in range(10):
                if board[i][j] != -1 and board[i][j] != '*' and board[i][j] != '$':
                    return False
        return True

    # function called to start program
    def main(self):
        # types of ships
        ships = {"Aircraft Carrier": 5,
                 "Battleship": 4,
                 "Submarine": 3,
                 "Cruiser": 3,
                 "Destroyer": 2}
        # setup blank 10x10 board
        board = []
        for i in range(10):
            board_row = []
            for j in range(10):
                board_row.append(-1)
            board.append(board_row)
        # setup user and computer boards
        user_board = copy.deepcopy(board)
        comp_board = copy.deepcopy(board)
        # add ships in array
        user_board.append(copy.deepcopy(ships))
        comp_board.append(copy.deepcopy(ships))
        # ship placement
        user_board = self.user_place_ships(user_board, ships)
        comp_board = self.computer_place_ships(comp_board, ships)
        # game main loop
        while (1):
            # user move
            self.print_board("c", comp_board)
            comp_board = self.user_move(comp_board)
            # check if user won
            if comp_board == "VICTORY!":
                print("THE USER WON! :)")
                quit()
            # display current computer board
            self.print_board("c", comp_board)
            input("Press ENTER to continue")
            # computer move
            user_board = self.computer_move(user_board)
            # check if computer move
            if user_board == "VICTORY!":
                print("THE COMPUTER WON! :(")
                quit()
            # display user board
            input("Press ENTER to continue")


root = BattleshipGame()
root.main()