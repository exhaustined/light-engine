import pygame,random
from math import atan2, degrees, pi, floor, ceil
pygame.init()
display=pygame.display.set_mode((1280,720))
width,height=display.get_rect()[2],display.get_rect()[3]
# print(pygame.font.get_fonts())

vec=pygame.math.Vector2
distance=vec(0,-2000)

reflections=500		#max number of reflections
rotation_speed= 0.3 	#speed of ray rotation

reflect=False
objects=[]	#list of rects
objects.append(pygame.Rect(0,0,120,110))
rays=10 	#number of rays from source
draw=False	#flag for drawing objects
rotation=False	#flag for rotation
dim= False	#flag for dimming
rot=0
dimrate= 10 #rate at which the brightness reduces, if dimrate is 1, it reduces after 1 bounce, if its 10, reduces after 10 bounces

font=pygame.font.Font('font.otf',45)
font2=pygame.font.SysFont('square721cn',24)
clock=pygame.time.Clock()

colour_counter = 0
colours = [((50,50,50),(50,50,50),(100,100,100),(150,150,150),(200,200,200),(255,255,255)),
		((10, 5, 2), (50, 25, 15), (100, 50, 30), (150, 80, 50), (200, 120, 70), (255, 180, 100)),
		((14, 22, 26), (26, 52, 65), (32, 84, 108), (33, 119, 154), (28, 156, 203), (0, 195, 255)),
		((40, 40, 40), (70, 70, 50), (100, 100, 40), (160, 160, 30), (210, 210, 20), (255, 255, 0)),
		((43, 0, 0), (79, 0, 0), (116, 0, 0), (152, 0, 0), (211, 0, 0), (245, 15, 15)),
		((23, 10, 26), (50, 20, 65), (80, 24, 108), (112, 25, 154), (145, 19, 204), (179, 0, 255)),
		((31, 11, 17), (50, 17, 28), (69, 24, 38), (108+20, 36+20, 58+20), (147+20, 48+20, 78+20), (187+20, 59+20, 98+20))]
def Light(origin,direction,bounces,objects,colours,reflections=0,colour_range=-1,width=5,new=False):
	origin=origin	#line start coordinates
	direction=vec(direction)	#vector specifiying the direction of ray
	end=origin	#line end coordinates(origin+direction, line 33)
	bounces=bounces
	reflections= reflections
	new=new
	colour_range= colour_range
	colour = colours[colour_counter]
	width=width
	hit=False	#hit flag

	while True:
		end+=direction.normalize()*50 	#increment the ray little by little to detect collisions,
										#normalize the vector to length 1 and multiply it by the length needed
		for ob in objects:		
			clipped_line = ob.clipline(origin,end)	#check for collision
			if clipped_line:		#limit for reflections
				start1= clipped_line[0]
				hitstart= list(start1)	#coordinates of where the ray hits
				end=hitstart	#the end of the ray is where it hits
				if hitstart[0]>=ob.right-1:		#reflection based on where the ray hit
					direction[0]*=-1
					end[0]+=1
				elif hitstart[0]<=ob.left:
					direction[0]*=-1
					end[0]-=1
				elif hitstart[1]<=ob.top:
					direction[1]*=-1
					end[1]-=1
				elif hitstart[1]>=ob.bottom-1:
					direction[1]*=-1
					end[1]+=1
				hit=True	
				break
		if hit or (end).length()>2000:	#max length for ray, could optimize further but good enough
			break
	if dim:
		if new: #checks if ray hasn't been reflected yet
			pygame.draw.line(display, colour[-1], origin, end, 5) #ensure first ray is always brightest
			new= False
		else:
			if reflections>=dimrate:	#adjusting brightness and width of ray after bouncing
				if colour_range>-6:
					colour_range-=1
				reflections=0
				width-=1
			colour = colour[colour_range]
			pygame.draw.line(display, colour, origin, end, width)	#draw the ray
	else:
		pygame.draw.line(display, colour[-1], origin, end, 5)
		pygame.draw.circle(display, colour[-1], (end[0]+1,end[1]+1), 5, width=0) #draw the ray


	if hit and reflect:
		bounces-=1
		reflections+=1
		if bounces>=0:
			Light(hitstart,direction,bounces,objects,colours,reflections,colour_range,width)	#create a new ray starting from where parent ray hit
	else:
		return

while True:
	clock.tick(60)
	display.fill((0,0,0))
	fps=clock.get_fps()
	fpstext=font.render(str(int(fps)),False,(190,190,190))
	raystext=font2.render("RAYS= "+str(rays),False,(190,190,190))
	rotatetext=font2.render("ROTATE",False,(190,190,190))
	reflecttext=font2.render("REFLECT",False,(190,190,190))
	dimtext=font2.render("DIM",False,(190,190,190))
	dimratetext=font2.render("DIMRATE= ",False,(190,190,190))
	
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			pygame.quit()
			exit()
		elif event.type==pygame.MOUSEBUTTONDOWN:
			if event.button==1: 
				reflect=not reflect
			elif event.button==3: 
				draw=True
				startpos=list(pygame.mouse.get_pos())	#mouse position for drawing objects
			elif event.button==4:
				if rays>1:
					rays-=1
			elif event.button==5:
				if rays<360:
					rays+=1
		elif event.type==pygame.MOUSEBUTTONUP:
			if draw:
				draw=False	#stop drawing
				objects.append(pygame.Rect(topleft[0],topleft[1],xdist,ydist))	
		elif event.type==pygame.KEYDOWN:  #looking for key presses
			if event.key==pygame.K_ESCAPE:
				objects=[pygame.Rect(0,0,120,110)]
			elif event.key==pygame.K_SPACE:
				rotation=not rotation
			elif event.key==pygame.K_c:
				colour_counter+=1
				colour_counter%=7
			elif event.key==pygame.K_d:
				dim= not dim
			elif event.key==pygame.K_UP:
				rotation_speed+=0.2
			elif event.key==pygame.K_DOWN:
				rotation_speed-=0.5
				if rotation_speed<=0.2:
					rotation_speed=0.2
			elif event.key==pygame.K_RIGHT:
				dimrate+=1
			elif event.key==pygame.K_LEFT:
				dimrate-=1
				if dimrate<=1:
					dimrate=1
	keys = pygame.key.get_pressed()  # Checking pressed keys
	if keys[pygame.K_RIGHT]:
		dimrate+=0.1
	elif keys[pygame.K_LEFT]:
		dimrate-=0.1
		if dimrate<1:
			dimrate=1
	if draw:
		topleft=list(startpos)		#creating and drawing objects
		curpos=list(pygame.mouse.get_pos())
		xdist=abs(curpos[0]-topleft[0])
		ydist=abs(curpos[1]-topleft[1])
		if curpos[0]<topleft[0]:
			if curpos[1]<topleft[1]:
				topleft=curpos
			else:
				topleft[0]-=xdist
		elif curpos[1]<topleft[1]:
			topleft[1]-=ydist
		pygame.draw.rect(display,(100,30,30),(topleft[0],topleft[1],xdist,ydist),4)

	if objects:
		for ob in objects[1:]:
			pygame.draw.rect(display,(100,100,30),ob,4)		#displaying objects

	origin=pygame.mouse.get_pos()	#light source coordinates

	angle=0
	for k in range(rays):	
		angle+=360/rays
		nline=distance.rotate(angle+rot)	#source ray rotation
		Light(origin,nline,reflections,objects,colours,new=True)	#creating source rays

	x_offset=-5
	y_offset=-3

	display.blit(fpstext, (7,2))
	display.blit(font2.render("FPS",False,(190,190,190)), (63,15))
	display.blit(raystext, (13+x_offset,40+y_offset))
	display.blit(reflecttext, (13+x_offset,60+y_offset))
	display.blit(rotatetext, (13+x_offset,80+y_offset))
	display.blit(dimtext, (13+x_offset,100+y_offset))

	if rotation:
		rot+=rotation_speed
	else:
		pygame.draw.line(display, (190,190,190), (5,95+y_offset), (80,95+y_offset),3)		#rotation ui strikethrough

	if not reflect:
		pygame.draw.line(display, (190,190,190), (5,75+y_offset), (80,75+y_offset),3)		#reflection ui strikethrough
	if dim:
		display.blit(dimratetext, (13+x_offset,120+y_offset))
		display.blit(font2.render(str(int(dimrate)),False,(190,190,190)), (120+x_offset,120+y_offset))
	else:
		pygame.draw.line(display, (190,190,190), (5,115+y_offset), (50,115+y_offset),3)		#dim ui strikethrough

	pygame.display.update()
