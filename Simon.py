#import necessary modules
import pygame
import math
import random

#set size of window, central highscore button
WS = 800
HSQ = 100

#Points defining buttons(to be calculated later)
BUTTONS = [[] for n in range(4)]

#Miscellaneous helper variables
lightarray = []
rf = 1
crs = 0
lighton = 0

# initiate pygame and give permission to use pygame's functionality.
pygame.init()

# create the display surface object of specific dimension.
window = pygame.display.set_mode((WS, WS))
#Fill the scree with white color
window.fill((255, 255, 255))

# Draws the surface object to the screen.
#pygame.display.update()

#This is in practice the black piece of plastic in real life
def BackGround(marg, hsq = HSQ, ws = WS):
	# Using draw.circle module of pygame to draw the solid circle and the highscore query button at the middle
	pygame.draw.circle(window, (0, 0, 0), [ws/2, ws/2], (ws/2 - marg), 0)
	pygame.draw.circle(window, (127, 127, 127), [ws/2, ws/2], (hsq), 0)


#returns colors of the buttons, depending on color and light state(off/on))
def ColorSelect(col,lghtd):
	#print(col)
	# 0 - red
	if col == 0:
		if lghtd == 0:
			ca = (180,0,0)
		if lghtd == 1:
			ca = (255,75,75)
	# 1 - blue
	elif col == 1:
		if lghtd == 0:
			ca = (0,0,180)
		if lghtd == 1:
			ca = (75,75,255)
	# 2 - yellow
	elif col == 2:
		if lghtd == 0:
			ca = (180,180,0)
		if lghtd == 1:
			ca = (255,255,75)
	# 3 - green
	elif col == 3:
		if lghtd == 0:
			ca = (0,180,0)
		if lghtd == 1:
			ca = (75,255,75)
	else:
		ca = (127,127,127)
	return ca


#Mathematical description of shapes to be drawn
def PointCalc(pos, cb, mrg, ws = WS):
	#print("points were recalculated")
	mcp = []
	pl = []
	for ang in range(pos * 90, (pos + 1) * 90, 3):
		mcp.append([round((ws/2) * (1 + math.sin(math.radians(ang)))), round(ws/2  * (1 - math.cos(math.radians(ang))))])
	if pos == 0:
		pl.append([round(ws/2 + mrg), round(ws/2 - mrg - cb)])
		pl.append([round(ws/2 + mrg), mrg + 10])
		for i in range(len(mcp)):
			if mcp[i][0] - mrg > ws/2 + mrg and mcp[i][1] + mrg > mrg and mcp[i][1] + mrg < ws/2 - mrg:
				pl.append([mcp[i][0] - mrg, mcp[i][1] + mrg])
		pl.append([ws - mrg - 10, round(ws/2 - mrg)])
		pl.append([ws - cb - mrg, round(ws/2 - mrg)])
		for i in range(len(mcp)-1,-1,-1):
			if mcp[i][0] - cb > ws/2 + mrg and mcp[i][1] + cb > mrg and mcp[i][1] + cb < ws/2 - mrg:
				pl.append([mcp[i][0] - cb, mcp[i][1] + cb])
		return pl
	elif pos == 1:
		pl.append([round(ws/2 + cb + mrg), round(ws/2 + mrg)])
		pl.append([round(ws - mrg - 10), round(ws/2 + mrg)])
		for i in range(len(mcp)):
			if mcp[i][0] - mrg > ws/2 + mrg and mcp[i][1] - mrg > mrg and mcp[i][1] - mrg > ws/2 + mrg:
				pl.append([mcp[i][0] - mrg, mcp[i][1] - mrg])
		pl.append([round(ws/2 + mrg), round(ws - mrg - 10)])
		pl.append([round(ws/2 + mrg), round(ws/2 + cb + mrg)])
		for i in range(len(mcp)-1,-1,-1):
			if mcp[i][0] - cb > ws/2 + mrg and mcp[i][1] - cb < ws - mrg and mcp[i][1] - cb > ws/2 + mrg:
				pl.append([mcp[i][0] - cb, mcp[i][1] - cb])
		return pl
	elif pos == 2:
		pl.append([round(ws/2 - mrg), round(ws/2 + mrg + cb)])
		pl.append([round(ws/2 - mrg), round(ws - mrg - 10)])
		for i in range(len(mcp)):
			if mcp[i][0] + mrg < ws/2 - mrg and mcp[i][1] - mrg > mrg and mcp[i][1] - mrg > ws/2 + mrg:
				pl.append([mcp[i][0] + mrg, mcp[i][1] - mrg])
		pl.append([mrg + 10, round(ws/2 + mrg)])
		pl.append([ws/2 - cb - mrg, round(ws/2 + mrg)])
		for i in range(len(mcp)-1,-1,-1):
			if mcp[i][0] + cb < ws/2 - mrg and mcp[i][1] - cb < ws - mrg and mcp[i][1] - cb > ws/2 + mrg:
				pl.append([mcp[i][0] + cb, mcp[i][1] - cb])
		return pl
	else:
		pl.append([ws/2 - cb - mrg, round(ws/2 - mrg)])
		pl.append([mrg + 10, round(ws/2 - mrg)])
		for i in range(len(mcp)):
			if mcp[i][0] + mrg < ws/2 - mrg and mcp[i][1] + mrg > mrg and mcp[i][1] + mrg < ws/2 - mrg:
				pl.append([mcp[i][0] + mrg, mcp[i][1] + mrg])
		pl.append([round(ws/2 - mrg), round(mrg + 10)])
		pl.append([round(ws/2 - mrg), round(ws/2 - mrg - cb)])
		for i in range(len(mcp)-1,-1,-1):
			if mcp[i][0] + cb < ws/2 - mrg and mcp[i][1] + cb > mrg and mcp[i][1] + cb < ws/2 - mrg:
				pl.append([mcp[i][0] + cb, mcp[i][1] + cb])
		return pl


def ButtonDraw(col,lghtd,pos,ws = WS):
	global BUTTONS
	ca = ColorSelect(col, lghtd)
	if len(BUTTONS[pos]) == 0:
		BUTTONS[pos] = PointCalc(pos, 170, 30,)
	pygame.draw.polygon(window,ca,BUTTONS[pos])


#Draw the game itself, with 0/1 bit if light off/on
def GameDraw(rl,bl,yl,gl):
	#print("Request received" + " " + str(rl) + " " + str(bl) + " " + str(yl)  + " " + str(gl))
	#Draw background only the first time
	global BUTTONS
	if BUTTONS[0] == []:
		BackGround(20,HSQ,)
	ButtonDraw(0,rl,0,)
	ButtonDraw(1,bl,1,)
	ButtonDraw(2,yl,2,)
	ButtonDraw(3,gl,3,)
	pygame.display.update()


def LightRequest(cv):
	#Decode control value to each single color
	rl = cv % 2
	bl = (cv % 4 - rl) / 2
	yl = (cv % 8 - 2 * bl - rl) / 4
	gl = (cv % 16 - 4 * yl - 2 * bl - rl) / 8
	GameDraw(rl,bl,yl,gl)


class LightProcess():
	def __init__(self, ontime, colorcode, offtime):
		self.ontime = ontime
		self.colorcode = colorcode
		self.offtime = offtime


def GameEngine(lo,cl,io,ci):
	if io == 0:
	#Output mode
		if cl < len(lo):
			return lo, 2**lo[cl], 0
			#Request light already in list
		else:
			new = random.randint(0,100000) % 4
			lo.append(new)
			return lo, 2**new, 1
			#Chose a new light, request it, set finished flag.
	if io == 1:
	#Input processing
		if cl < len(lo):
			if ci == lo[cl]:
				if cl != len(lo) - 1:
					#expected button pressed and it is not the last one
					return lo, 0, 0
				if cl == len(lo) - 1:
					#expected button pressed and it is the last one
					return lo, 0, 1
			else:
				#unexpected button pressed, player loses
				return lo, 0, 2
		else:
			#out of buttons to press
			return lo, 0, 1


#decide what user click was
# 0 - red
# 1 - blue
# 2 - yellow
# 3 - green
# 4 - highscore
# 9 - nothing
def EvaluateClick(x,y,hsq,ws,bs):
	len = math.sqrt((x-ws/2)**2 + (y-ws/2)**2)
	#center
	if len < hsq:
		return 4
	# top right of the screen
	elif len > (hsq + 2 * bs) and len < ws/2 - bs and x > ws/2 + bs and y < ws/2 - bs:
		return 0
	# bottom right of the screen
	elif len > (hsq + 2 * bs) and len < ws/2 - bs and x > ws/2 + bs and y > ws/2 + bs:
		return 1
	# bottom left of the screen
	elif len > (hsq + 2 * bs) and len < ws/2 - bs and x < ws/2 - bs and y > ws/2 + bs:
		return 2
	# top left of the screen
	elif len > (hsq + 2 * bs) and len < ws/2 - bs and x < ws/2 - bs and y < ws/2 + bs:
		return 3
	#areas without any specific functionality
	else:
		return 9

def RequestHandler(on, col, off, prio):
	global lightarray
	global lighton
	global rf
	if prio == 0:
		#Generic case, just next one in the list
		lightarray.append(LightProcess(on, col, off))
	if prio == 1:
		#Do immediately
		lighton, rf = 0, 1
		lightarray = []
		lightarray.append(LightProcess(on, col, off))
	if prio == 2:
		#Blinking request at the beginning
		if lightarray == []:
			lightarray.append(LightProcess(on, col, off))


def PerformRequests():
	global lightarray
	global rf
	global crs
	global lighton
	global cr
	if rf == 1 and len(lightarray) != 0:
		#if no request is being processed, start processing the next request, turn on the requested light, save the moment the light was turned on
		rf = 0
		cr = lightarray.pop(0)
		crs = pygame.time.get_ticks()
		LightRequest(cr.colorcode)
		lighton = 1
	if rf == 0:
		if pygame.time.get_ticks() > crs + cr.ontime and lighton == 1:
			#If the light was turned on for more than it was supposed to, turn it off
			LightRequest(0)
			lighton = 0
		if pygame.time.get_ticks() > crs + cr.ontime + cr.offtime:
			#If the minimum offtime has passed, a new request can be processed
			rf = 1


def GameEndSeq(t):
	for _ in range(2):
		for cnt in [3,6,12,9]:
			RequestHandler(t,cnt,1,0)


def ScoreOutput(score,t):
	us = int(score % 10)
	ts = int((score - us)/10)
	RequestHandler(t,0,t*5,0)
	for _ in range (ts):
		RequestHandler(t,15,t,0)
	for _ in range (us):
		RequestHandler(t,8,t,0)
	RequestHandler(t,0,t*5,0)


def main():
	global lightarray
	nst = 1
	sl = 250
	ll = 750
	lo = []
	cl = 0
	highscore = 0
	while True:
		if nst == 1:
			RequestHandler(ll,8,ll,2)
		ev = pygame.event.get()
		for event in ev:
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()
			if event.type == pygame.MOUSEBUTTONUP:
				x,y = pygame.mouse.get_pos()
				ret = EvaluateClick(x,y,HSQ,WS,30)
				if ret == 4 and len(lo) == 0:
					#Handle case highscore request came in
					ScoreOutput(highscore,sl)
				if nst == 1 and ret == 3:
					#Handle case game start request was received
					#Turn off blinking light, request a new one, randomly, first of the list
					nst = 0
					RequestHandler(ll,0,ll,1)
					tmp = GameEngine(lo,0,0,0)
					lo = tmp[0]
					RequestHandler(ll,2**lo[0],ll,0)
				elif nst == 0 and len(lightarray) < 3:
					RequestHandler(ll,2**ret,ll,0)
					tmp = GameEngine(lo,cl,1,ret)
					lo = tmp[0]
					if tmp[2] == 0:
						#Correct button pressed and not the last one
						cl += 1
					elif tmp[2] == 1:
						#Correct button pressed and the last one
						cl = 0
						ended = 0
						RequestHandler(sl,0,sl,0)
						#Blink sequence, add one button and blink that too
						while ended == 0:
							tmp = GameEngine(lo,cl,0,0)
							lo = tmp[0]
							lr = tmp[1]
							RequestHandler(ll,lr,ll,0)
							ended = tmp[2]
							cl += 1
						cl = 0
					elif tmp[2] == 2:
						#Player lost
						RequestHandler(1,0,1,1)
						GameEndSeq(sl)
						ScoreOutput(len(lo) - 1, sl)
						highscore = max(highscore, len(lo) - 1)
						nst = 1
						lo = []
						cl = 0
						#print("You lose")
		PerformRequests()


main()