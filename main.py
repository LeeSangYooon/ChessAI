import chess
import chess.svg
from gui import GUI
from AI import AI

from IPython.display import SVG, display

board = chess.Board()

ai_white = AI(board, chess.WHITE, [1000, 1000, 5, 5, 5])
ai_black = AI(board, chess.BLACK, [1000, 1000, 5, 5, 5])


def self_play():
    for n in range(1000):
        ai_move = ai_white.run()
        board.push(ai_move[1])
        #display(SVG(chess.svg.board(board=board, size=400)))
        print(board)
        print("white:", str(ai_move[1]), ai_move[0])

        ai_move = ai_black.run()
        board.push(ai_move[1])
        #display(SVG(chess.svg.board(board=board, size=400)))
        print(board)
        print("black:", str(ai_move[1]), ai_move[0])


def play_as_white():
    for n in range(1000):
        board.push_san(input("입력: "))
        print(board)

        ai_move = ai_black.run()
        board.push(ai_move[1])
        # display(SVG(chess.svg.board(board=board, size=400)))
        print(board)
        print("black:", str(ai_move[1]), ai_move[0])


def play_as_black():
    for n in range(1000):
        ai_move = ai_white.run()
        board.push(ai_move[1])
        #display(SVG(chess.svg.board(board=board, size=400)))
        print(board)
        print("white:", str(ai_move[1]), ai_move[0])

        board.push_san(input("입력: "))
        #display(SVG(chess.svg.board(board=board, size=400)))
        print(board)




gui = GUI(board)
done = False

ai_black.loading_func = gui.loading_bar
ai_white.loading_func = gui.loading_bar


ipt =input("#1 AI vs AI \n#2 Player vs AI \n#3 AI vs Player \n input: ")
if ipt == "1":
    while not done:
        move = ai_white.run()
        print("white:",str(move[1]), " 점수:",move[0])
        board.push(move[1])
        if board.is_checkmate() or board.is_stalemate():
            done = True
        move = ai_black.run()
        print("black:", str(move[1]), " 점수:", move[0])
        board.push(move[1])
        if board.is_checkmate() or board.is_stalemate():
            done = True
else:
    if ipt == "2":
        ai = ai_black
    else:
        ai = ai_white
        board.push(ai.run()[1])

    while not done:
        gui.loop()

        for event in gui.events:
            if event[0] == 'push':
                if event[1] in list(board.legal_moves):
                    board.push(event[1])
                    move = ai.run()
                    print("ai:", str(move[1]), " 점수:", move[0])
                    board.push(move[1])
                    print(ai.score_func(board))
            if event[0] == 'quit':
                done = True

    gui.pygame.quit()

