from Engine import Board 
from Engine import Manager 


board = Board.Board()
manager = Manager.Manager(board)
color_to_play = Board.Board.BLACK

mode = int(input("enter the mode you want to play\n1- human vs AI\n2- AI vs AI\n3- human vs human\n"))

while(True):

    board.display()

    if(color_to_play == Board.Board.BLACK):
        print("\nwhite to play\n")
        color_to_play = Board.Board.WHITE
    else:
        print("\nblack to play\n")
        color_to_play = Board.Board.BLACK

    if((mode == 1 and color_to_play == Board.Board.WHITE) or mode != 2):
        x = int(input("enter the x axis position: "))
        y = int(input("enter the y axis position: "))

    # else:
    #     AI to play

    play_result = manager.play(x,y,color_to_play)

    if(play_result == -1):
        print("invalid play try again")
        color_to_play = 1 - color_to_play   # will invert the play to make him try again
    
    elif(play_result == Manager.Manager.DRAW):
        print("no more room to play")
        break

    elif(play_result == Manager.Manager.BLACK_WIN):
        print("black player wins")
        break

    elif(play_result == Manager.Manager.WHITE_WIN):
        print("white player wins")
        break