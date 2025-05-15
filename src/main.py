import pygame
from Engine import Board 
from Engine import Manager
from GUI import GuiManager
from GUI import UtilizationGui
from AI import AI
import time

gui = GuiManager.Gui()
# Game loop
running = True

mode_selected = UtilizationGui.Constants.INVALID_MODE
color_to_play = Board.Board.BLACK
board = Board.Board()
manager = Manager.Manager(board)
ai = AI.AI()
play_result = 0

while(running):   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:

            # Waiting on the mode selection menu
            if(mode_selected == UtilizationGui.Constants.INVALID_MODE):
                mode_selected = gui.select_mode(event.pos)

                if(mode_selected != UtilizationGui.Constants.INVALID_MODE):
                    gui.draw_board()

            elif(play_result == -1 or play_result == 0):    # If the play result was messy or it was valid (no draw/wins)
                if((mode_selected == 2 and color_to_play == Board.Board.BLACK) or mode_selected == 1):
                    col, row =gui.convert_pos_to_index(event.pos)
                    
                    if(col>=0 and col<15 and row >=0 and row < 15):
                        play_result = manager.play(row,col,color_to_play)
                        if(play_result == -1):
                            color_to_play = 3 - color_to_play   # will invert the play to make him try again

                # Solve this error plz @EbrahimMo50
                # First one: User must click on the board for the AI to play
                # Second one: Human vs AI is not working
                elif(mode_selected == 3):
                    # Ai vs Ai
                    if(color_to_play == Board.Board.BLACK):
                        print("Black AI to play")
                    else :
                        print("White AI to play")
                    start_time = time.time()
                    x,y = ai.ai_move(board)
                    end_time = time.time()
                    if (color_to_play == Board.Board.BLACK):
                        print("Black AI played at: ", x, y)
                        print("Time taken by Black AI: ", end_time - start_time)
                    else:
                        print("White AI played at: ", x, y)
                        print("Time taken by White AI: ", end_time - start_time)
                    play_result = manager.play(x,y,color_to_play)
                    if(play_result == -1):
                        color_to_play = 3 - color_to_play
                

                else:
                    print("AI to play")
                    start_time = time.time()
                    x,y = ai.ai_move(board)
                    end_time = time.time()
                    print("Time taken by AI: ", end_time - start_time)
                    color_to_play = Board.Board.WHITE
                    play_result = manager.play(x,y,color_to_play)
                    if(play_result == -1):
                        color_to_play = 3 - color_to_play

            gui.update_board(board.matrix)
            color_to_play = 3 - color_to_play

            if(play_result != -1 and play_result != 0):
                gui.show_game_over(play_result)

    pygame.display.flip()



# board = Board.Board()
# manager = Manager.Manager(board)
# color_to_play = Board.Board.BLACK

# mode = int(input("enter the mode you want to play\n1- human vs AI\n2- AI vs AI\n3- human vs human\n"))

# while(True):

#     board.display()

#     if(color_to_play == Board.Board.BLACK):
#         print("\nwhite to play\n")
#         color_to_play = Board.Board.WHITE
#     else:
#         print("\nblack to play\n")
#         color_to_play = Board.Board.BLACK

#     if((mode == 1 and color_to_play == Board.Board.WHITE) or mode == 3):
#         x = int(input("enter the x axis position: "))
#         y = int(input("enter the y axis position: "))

#     # else:
#     #     AI to play

#     play_result = manager.play(x,y,color_to_play)

#     if(play_result == -1):
#         print("invalid play try again")
#         color_to_play = 3 - color_to_play   # will invert the play to make him try again
    
#     elif(play_result == Manager.Manager.DRAW):
#         print("no more room to play")
#         break

#     elif(play_result == Manager.Manager.BLACK_WIN):
#         print("black player wins")
#         break

#     elif(play_result == Manager.Manager.WHITE_WIN):
#         print("white player wins")
#         break