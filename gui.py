import chess
import pygame

pygame.init()



# Define the colors we will use in RGB format
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


# Set the height and width of the screen
size = [900, 600]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Game Title")
done = False
clock = pygame.time.Clock()

colorDict = {chess.WHITE:"W", chess.BLACK:"B"}
nameDict = {chess.PAWN:"P", chess.KNIGHT:"N", chess.BISHOP:"B",
             chess.ROOK:"R", chess.QUEEN:"Q", chess.KING:"K"}

font= pygame.font.SysFont("consolas",20)

x_pos_dict = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']


class GUI:
    def __init__(self, board:chess.Board):
        self.events = []
        self.board = board

        self.pygame = pygame
        self.size = 60
        self.images = dict()
        self.load_image()



        self.drag_from = None

    def printText(self, msg, color='BLACK', pos=(50, 50)):
        textSurface = font.render(msg, True, pygame.Color(color), None)
        textRect = textSurface.get_rect()
        textRect.topleft = pos

        screen.blit(textSurface, textRect)

    def load_image(self):
        for type in nameDict.values():
            self.images['W'+type] = pygame.image.load('Images/W' + type + '.png')
            self.images['W'+type] = pygame.transform.scale(self.images['W'+type], (self.size, self.size))
            self.images['B'+type] = pygame.image.load('Images/B' + type + '.png')
            self.images['B' + type] = pygame.transform.scale(self.images['B' + type], (self.size, self.size))

    def is_legal(self, f, t):
        p = self.board.piece_at(f)
        if p.piece_type == chess.PAWN and (t < 8 or t > 55):
            move = chess.Move(f,t,chess.QUEEN)
        else:
            move = chess.Move(f, t)
        return self.board.is_legal(move)

    def draw_board(self,x, y):
        # Size of squares
        size = self.size

        # board length, must be even
        boardLength = 8
        screen.fill((18, 89, 71))

        board_x = 7- round(x / self.size - 1.5)
        board_y = round(y / self.size - 1.5)
        board_n = 63 - (board_x + board_y * 8)
        draw_to = self.drag_from is not None and self.is_legal(self.drag_from, board_n)

        n = 63
        cnt = 0
        for i in range(1, boardLength + 1):
            for z in range(1, boardLength + 1):
                if cnt % 2 == 1:
                    pygame.draw.rect(screen, (145, 80, 0), [size * (9 - z), size * i, size, size])
                else:
                    pygame.draw.rect(screen, (196, 142, 49), [size * (9 - z), size * i, size, size])
                cnt += 1

                piece = self.board.piece_at(n)

                if self.drag_from is not None:
                    if n == self.drag_from:
                        pygame.draw.rect(screen, (200, 255, 200), [size * (9 - z), size * i, size, size])
                    if draw_to and n == board_n:
                        pygame.draw.rect(screen, (200, 255, 200), [size * (9 - z), size * i, size, size])

                if piece is not None and n != self.drag_from:
                    name = colorDict[piece.color] + nameDict[piece.piece_type]
                    screen.blit(self.images[name], [size * ( 9-z), size * i])
                n -= 1


            cnt -= 1
        pygame.draw.rect(screen, BLACK, [size, size, boardLength * size, boardLength * size], 3)

        if self.drag_from is not None:
            piece = self.board.piece_at(self.drag_from)
            name = colorDict[piece.color] + nameDict[piece.piece_type]
            p = pygame.mouse.get_pos()
            screen.blit(self.images[name], [p[0] - self.size // 2, p[1] - self.size // 2])



    def mouse_down(self, x, y):
        self.drag_from = None
        board_x = 7 - round(x  / self.size - 1.5)
        board_y = round(y / self.size - 1.5)
        board_n = 63 - (board_x + board_y * 8)

        piece = self.board.piece_at(board_n)
        if piece is not None and piece.color == self.board.turn:
            self.drag_from = board_n


    def mouse_up(self, x, y):
        if self.drag_from == None:
            return
        board_x = 7 - round(x / self.size - 1.5)
        board_y = round(y / self.size - 1.5)
        board_n = 63 - (board_x + board_y * 8)
        piece = self.board.piece_at(self.drag_from)
        if piece.piece_type == chess.PAWN and (board_n < 8 or board_n > 55):
            move = chess.Move(self.drag_from,board_n,chess.QUEEN)
        else:
            move = chess.Move(self.drag_from,board_n)

        if self.is_legal(self.drag_from, board_n):
            self.events.append(['push', move])

        self.drag_from = None


    def loop(self):
        self.events = []

        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.events.append(["quit"])
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_down(mouse_x, mouse_y)
            if event.type == pygame.MOUSEBUTTONUP:
                self.mouse_up(mouse_x, mouse_y)


        self.draw_board(mouse_x, mouse_y)



        pygame.display.flip()

    def loading_bar(self, percent):
        pygame.event.get()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.draw_board(mouse_x, mouse_y)
        self.printText("AI is thinking..." + str(round(percent * 100)) + "%", pos=(600, 70))
        pygame.draw.rect(screen, BLUE, [600, 100, 220, 20], 2)
        pygame.draw.rect(screen, BLUE, [600, 100, round(percent * 220), 20])
        pygame.display.flip()
