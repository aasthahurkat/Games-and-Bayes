#!/usr/local/bin/python3

"""
This is where you should write your AI code!
Authors: [Rohit Rokde-rrokde, Bhumika Agrawal-bagrawal, Aastha Hurkat-aahurkat]
Based on skeleton code by Abhilash Kuhikar, October 2019
"""
import copy
from logic_IJK import Game_IJK, initialGame
import random
import math
# Suggests next move to be played by the current player given the current game
#
# inputs:
#     game : Current state of the game 
#
# This function should analyze the current state of the game and determine the 
# best move for the current player. It should then call "yield" on that move.


def heuristic(Game_IJK):

    grid = Game_IJK.getGame()
    #count=0
    player = Game_IJK.getCurrentPlayer()
    ascii_sum_capital = 0
    ascii_sum_small = 0
    for i in range(6):
        for j in range(6):
            #if grid[i][j] == ' ':
            #    count=count+1
            if player == '+' and checkIfCapital(grid[i][j]):
                ascii_sum_capital += ord(grid[i][j])
            elif player == '-' and checkIfSmall(grid[i][j]):
                ascii_sum_small += ord(grid[i][j])
    if player == '+':
        return ascii_sum_capital
    elif player == '-':
        return ascii_sum_small
    else:
        print("Serious error! Should never print this statement.")
        return ascii_sum_capital

def checkIfCapital(x):
    return x in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']

def checkIfSmall(x):
    return x in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k']

def terminal(Game_IJK):
#number of emptycells()
    return Game_IJK.isGameFull()
'''
    count=0
    for i in range(6):
        for j in range(6):
            if grid[i][j] == ' ':
                count=count+1
            if grid[i][j] == 'K'or grid[i][j] == 'k':
                return True
    return count == 0
'''

def Probability(child):
    Probability = 1 / heuristic(child)
    return Probability

def next_move(Game_IJK):

    '''board: list of list of strings -> current state of the game
       current_player: int -> player who will make the next move either ('+') or -'-')
       deterministic: bool -> either True or False, indicating whether the game is deterministic or not
    '''
    bestMove = 'L'
    maxV = float("-Inf")
    #game = Game_IJK

    for move in ['U', 'R', 'D', 'L']:
      #  if move=='U':
       #     (newGame, dummy) = Game_IJK.__up(Game_IJK)
        #elif move == 'D':
         #   (newGame, dummy) = Game_IJK.__down(Game_IJK)
        #elif move == 'R':
         #   (newGame, dummy) = Game_IJK.__right(Game_IJK)
        #elif move=='L':
         #   (newGame, dummy) = Game_IJK.__left(Game_IJK)

        v = ExpectiMiniMax(Game_IJK, move,-math.inf, math.inf, 3, 0)
        if(v > maxV):
            maxV = v
            bestMove = move
    #print(aastha)
    yield bestMove#random.choice('U', 'R', 'D', 'L')

def ExpectiMiniMax(Game_IJK, nextMove, alpha, beta, depth, player):
    #board = game.getGame()
    #player = game.getCurrentPlayer()
    #deterministic = game.getDeterministic()
    if depth == 0 or terminal(Game_IJK):
        return heuristic(Game_IJK)

    if player == 0: #max
        #children = placing a at every empty position.
        #children = [x for x in succ_a(Game_IJK)]
        #we played L
        for child in succ_a(Game_IJK):
            alpha = max(alpha, ExpectiMiniMax(Game_IJK=child, nextMove= nextMove, alpha = alpha, beta=beta, depth = depth-1, player=2))
            if beta <= alpha:
                break #(* β cut-off *)
        return alpha

    elif player == 1: #min
        
        #children = placing A at every possible empty position
        for child in succ_A(Game_IJK):
            beta = min(beta, ExpectiMiniMax(Game_IJK=child, nextMove= nextMove, alpha= alpha, beta= beta, depth= depth-1, player=3))
            if beta <= alpha:
                break #(* α cut-off *)
        return beta

    elif player == 2:  #chance node after max
        value = 0
        for move in ['U','L','D','R']:
            child = Game_IJK.makeMove( move)
            #for child in children:
            value = value + (Probability(child) * ExpectiMiniMax(Game_IJK = child, nextMove= nextMove, alpha=alpha, beta=beta, depth= depth-1, player=1))

    elif player == 3:  #chance node after min
        value = 0
        for move in ['U','L','D','R']:
            child = Game_IJK.makeMove(move)
            #for child in children:
            value = value + (Probability(child) * ExpectiMiniMax(Game_IJK = child, nextMove= nextMove, alpha= alpha, beta= beta, depth= depth-1, player=0))

    return value 

def succ_a(Game_IJK):
    retList = []
    grid = Game_IJK.getGame()
    player = Game_IJK.getCurrentPlayer()
    det = Game_IJK.getDeterministic()
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == ' ':
                grid[i][j] = 'a'
                Game_IJK.__init__(grid, player, det)
                #Game_IJK.setGame(copy.deepcopy(grid))
                retList.append(copy.deepcopy(Game_IJK))
                grid[i][j] = ' '
    return retList

def succ_A(Game_IJK):
    retList = []
    grid = Game_IJK.getGame()
    player = Game_IJK.getCurrentPlayer()
    det = Game_IJK.getDeterministic()
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == ' ':
                grid[i][j] = 'A'
                Game_IJK.__init__(grid, player, det)
                #Game_IJK.setGame(copy.deepcopy(grid))
                retList.append(copy.deepcopy(Game_IJK))
                grid[i][j] = ' '
    return retList
