import os
import sys
import random
import threading
import queue
import time
from getkey import getkey

def read_kbd_input(inputQueue):
	print('Ready for keyboard input:')
	while (True):
		input_str = getkey()
		inputQueue.put(input_str)



def check_for_game_end(snake, ymax, xmax):
	if len(snake)==ymax*xmax:
		print("YOU WIN!")
		return 1

	for i in range(len(snake)-1):
		for pos in snake[i+1:]:
			if snake[i]==pos:
				print("GAME OVER!")
				return 1
	x,y=snake[-1]
	if not (0<=x<xmax and 0<=y<ymax):
		print("GAME OVER!")
		return 1

def draw_map(snake,food,ymax,xmax):
	
	if(os.name == 'posix'):
	   os.system('clear')
	else:
	   os.system('cls')

	matrix=[[EMPTY_CHAR for j in range(xmax)] for i in range(ymax)]
	board=""
	food_possibility=[]
	#win or loose before here

	for elem in snake[:-1]:
		x,y=elem
		matrix[y][x]=SNAKE_CHAR
	
	x,y=snake[-1]
	if 0<=y<ymax and 0<=x<xmax:	
		matrix[y][x]=SNAKE_HEAD_CHAR

	food_possibility = [(x,y) for y in range(ymax) for x in range(xmax) if (x,y) not in snake ]

	
	if len(food_possibility)>0:
		if snake[-1] == food:
			x,y=random.choice(food_possibility)
			food=(x,y)
		else:
			x,y=food
		matrix[y][x]=FOOD_CHAR

	board="".join([matrix[y][x] if x !=xmax-1 else f"{matrix[y][x]}\n" for y in range(ymax) for x in range(xmax)])

	print(board)
	
	return food



if (__name__ == '__main__'): 
	#Init Global static Vars
	SNAKE_CHAR="🐍"
	SNAKE_HEAD_CHAR="👀"
	FOOD_CHAR="🍎"
	EMPTY_CHAR="🌳"
	ymax=10
	xmax=10
	
	#Init scope mutable Vars
	snake=[(xmax//2, ymax//2)]
	food=(random.randrange(xmax), random.randrange(ymax))
	already_shown=False
	newPos=()

	#Init Threading for Keyboard Input
	direction=""
	inputQueue = queue.Queue()
	inputThread = threading.Thread(target=read_kbd_input, args=(inputQueue,), daemon=True)
	inputThread.start()
 
	while True:
		
		if (inputQueue.qsize() > 0):
			direction = inputQueue.get()
		#Print field only once before Input is given
		if direction=="":
			if not already_shown:
				food=draw_map(snake,food,ymax,xmax)
				print("Moveset: W, A, S, D! Grow in size and dont stay Smol to win the game")
				already_shown=True
			continue


		food=draw_map(snake,food,ymax,xmax) #First draw map, with a hack. 
											#Food is stored here, because it is needed to track growth of the snake
											#also we multipurpose it. Because we expect it to be a tuple, 
											#it cannot reach states 1 or 0.

		if check_for_game_end(snake,ymax,xmax)==1: #end
			sys.exit()
		
		
		x,y=snake[-1]
		match direction:
			case "w":
				newPos=(x,y-1)
			case "a":
				newPos=(x-1,y)
			case "s":
				newPos=(x,y+1)
			case "d":
				newPos=(x+1,y)

		snake.append(newPos)

		#I love the next line. Only shift the snake if not at food.
		#Two lines in python, in lolcode its 60 (because why compare to actual languages amirite)
		if newPos!=food:
			snake=snake[1:]
		time.sleep(0.2)