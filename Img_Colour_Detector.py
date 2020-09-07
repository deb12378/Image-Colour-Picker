#	Dependencies
#	pip install pandas,opencv-python

import pandas as pd
import cv2

#	UD Func 1: Records user mouse clicks

def click_record(event, x, y, flags, params):
	if event == cv2.EVENT_LBUTTONDOWN:
		global b, g, r, xp, yp, clicked
		clicked = True
		xp = x
		yp = y
		b,g,r = pic[y,x]
		b = int(b)
		g = int(g)
		r = int(r)


#	UD Func 2: Computes min colour deviation

def colour_identifier(R,G,B):
	min = 1000
	for i in range(len(df)):
		delta = abs(R - int(df.loc[i,'R'])) + abs(G - int(df.loc[i,'G'])) + abs(B - int(df.loc[i,'B']))
		if delta <= min:
			min = delta
			name = df.loc[i, 'cname']
	return name

#	main()
#	Declaration of Global Variables to call from UD Funcs

clicked = False
r = g = b = xp = yp = 0

#	Input picture name to check in current dir

picture = 'img/'+input("Enter name of image:")+'.jpg'

#	Read colour palette with hex and RGB values

col = 'colors.csv'
index = ['colour', 'cname', 'hex', 'R', 'G', 'B']
df = pd.read_csv(col, names=index, header=None)

#	Feeding picture data

pic = cv2.imread(picture)
pic = cv2.resize(pic, (1366,768))

#	Display Window

cv2.namedWindow('COLOUR DETECTION')
cv2.setMouseCallback('COLOUR DETECTION', click_record)
font=cv2.FONT_HERSHEY_SIMPLEX
while True:
	cv2.imshow('COLOUR DETECTION', pic)
	if clicked:
		#	cv2.rectangle(image, startpoint, endpoint, color, thickness)-1 fills entire rectangle 

		cv2.rectangle(pic, (20,20), (600,60), (b,g,r), -1)

		#	Creating text string to display( Color name and RGB values )
		
		display = colour_identifier(r,g,b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)

	#	Display Colour text in black colour for extreme light combinations

		if r+g+b >=600:
			cv2.putText(pic, display, (50,50), font,0.5, (0,0,0),1,4,False)
	#cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
		else:
			cv2.putText(pic, display, (50,50), font,0.5, (255,255,255),1,4,False)
	if cv2.waitKey(20) & 0xFF == 27:
		break

	if(cv2.getWindowProperty('COLOUR DETECTION',cv2.WND_PROP_VISIBLE)<1):
		break

cv2.destroyAllWindows()
