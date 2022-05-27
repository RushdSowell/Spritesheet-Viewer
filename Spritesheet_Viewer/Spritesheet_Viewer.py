#Creating pygame spritesheet reader
import pygame, sys
import tkinter
import tkinter.filedialog

#Defining some constant
FRAME_REFRESH_RATE = 30
#color
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
SOLARIZEDBASE3 = (253,246,227)
SOLARIZEDBASE2 = (238,232,213)
SOLARIZEDBASE0 = (131,148,150)
SOLARIZEDBASE03 = (0,43,54)
CYAN = (42,161,152)
RED = (220,50,47)
ORANGE = (203,75,22)
VIOLET = (108,113,196)


DISPLAY_WIDTH = 900
DISPLAY_HEIGHT = 600

class Spritesheet_Viewer:
	"""
	Represents the Viewer to view motion of spritesheet using 
	the sprite_sheet_loader and sprite_sheet_separator below
	"""
	
	def __init__(self):
		print("Initializing pygame")
		pygame.init()
		self.display_surface = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
		pygame.display.set_caption("Spritesheet Viewer")
		#Used for timing if neede down the line
		self.clock = pygame.time.Clock()
		
		################################
		#Storing images
		self.IMAGE = {"Add Button Normal": pygame.transform.rotozoom(pygame.image.load("Addition_button_unhover.png"),0,0.25),
				"Add Button Hovered":pygame.transform.rotozoom(pygame.image.load("Addition_button_hover.png"),0,0.25),
				"Add Button Clicked":pygame.transform.rotozoom(pygame.image.load("Addition_button_clicked.png"),0,0.25),
				"Browse Button Normal": pygame.transform.rotozoom(pygame.image.load("Browse_button_unhover.png"),0,0.25),
				"Browse Button Hovered": pygame.transform.rotozoom(pygame.image.load("Browse_button_hover.png"),0,0.25),
				"Browse Button Clicked": pygame.transform.rotozoom(pygame.image.load("Browse_button_clicked.png"),0,0.25),
				"OK Button Normal": pygame.transform.rotozoom(pygame.image.load("OK_button_unhover.png"),0,0.25),
				"OK Button Hovered": pygame.transform.rotozoom(pygame.image.load("OK_button_hover.png"),0,0.25),
				"OK Button Clicked": pygame.transform.rotozoom(pygame.image.load("OK_button_clicked.png"),0,0.25),
				"Cancel Button Normal": pygame.transform.rotozoom(pygame.image.load("Cancel_button_unhover.png"),0,0.25),
				"Cancel Button Hovered": pygame.transform.rotozoom(pygame.image.load("Cancel_button_hover.png"),0,0.25),
				"Cancel Button Clicked": pygame.transform.rotozoom(pygame.image.load("Cancel_button_clicked.png"),0,0.25)}
		
		#We'll have also new row and newcolumn buttons
		self.Buttons_list = [[First_buttons(self.IMAGE["Add Button Hovered"], self.IMAGE["Add Button Normal"], self.IMAGE["Add Button Clicked"], "First Button")]]
		
		#Setting the location for the first button
		self.Buttons_list[0][0].Set_Rect(20,20)
		####################################
		#Some fonts
		self.menu_fonts = pygame.font.Font('Comfortaa-Regular.ttf', 20)
		self.menu_fonts_addMinus = pygame.font.Font('Comfortaa-Regular.ttf', 40)
		self.menu_fonts_addMinus_clicked = pygame.font.Font('Comfortaa-Regular.ttf', 30)
		###################################
		#Backgound color
		self.BackgroundColor = WHITE
		
		######################################
		#List of Frames
		self.Frames = []
		
	def Adding_frame(self):
		"""
		Function for adding frame and adjusting variables
		"""
		#Setting up the menu's background
		Background = pygame.Surface((750,300))
		BackgroundRect = Background.get_rect()
		Background_Coord = pygame.math.Vector2(DISPLAY_WIDTH/2 - BackgroundRect.center[0], DISPLAY_HEIGHT/2 - BackgroundRect.center[1])
		BackgroundRect.topleft = Background_Coord #The code is here because of somem late adjustment (the clicked outside the backgroud frame) and I am too lazy to incorporate it with Background_Coord above, as a few line of codes need to be changed. 
		Background.fill(SOLARIZEDBASE3)
		###########
		#Some Constant
		row_num = 1
		col_num = 1
		slow_const = 1
		file = '...'
		Insert_Box_Clicked = "None"
		#alpha_color = [255,255,255] #[R, G, B]
		##############
		#The list of writing
		List_of_writings = {}
		#Title
		List_of_writings['Adding_frame_title'] = [self.menu_fonts.render('Adding Frame', True, SOLARIZEDBASE03), (0,0)] #[the text, (location on the menu)]
		#File name
		List_of_writings['File name'] = [self.menu_fonts.render('File name: ', True, SOLARIZEDBASE0), (0,30)]
		List_of_writings['File'] = [self.menu_fonts.render(file, True, CYAN), (List_of_writings['File name'][1][0]+List_of_writings['File name'][0].get_width(), List_of_writings['File name'][1][1])]
		#Row and column
		List_of_writings['Column number'] = [self.menu_fonts.render('Number of columns: ', True, SOLARIZEDBASE0), (0, BackgroundRect.height/2-30)]
		List_of_writings['Column'] = [self.menu_fonts.render(str(col_num), True, CYAN), (List_of_writings['Column number'][0].get_width()+30, BackgroundRect.height/2 - 30)]
		List_of_writings['Row number'] = [self.menu_fonts.render('Number of rows: ', True, SOLARIZEDBASE0), (0, List_of_writings['Column number'][1][1]+List_of_writings['Column number'][0].get_height()+10)]
		List_of_writings['Row'] = [self.menu_fonts.render(str(row_num), True, CYAN), (List_of_writings['Row number'][0].get_width()+30, List_of_writings['Column number'][1][1]+List_of_writings['Column number'][0].get_height()+10)]
		#Alpha channel
		List_of_writings['Alpha channel color'] = [self.menu_fonts.render('Alpha Channel Color:', True, SOLARIZEDBASE0), (0, List_of_writings['Row number'][1][1]+List_of_writings['Row number'][0].get_height()+20)]
		List_of_writings['R'] = [self.menu_fonts.render('R: ', True, SOLARIZEDBASE0), (0, List_of_writings['Alpha channel color'][1][1]+List_of_writings['Alpha channel color'][0].get_height()+10)]
		List_of_writings['G'] = [self.menu_fonts.render('G: ', True, SOLARIZEDBASE0), (List_of_writings['R'][1][0]+100, List_of_writings['Alpha channel color'][1][1]+List_of_writings['Alpha channel color'][0].get_height()+10)]
		List_of_writings['B'] = [self.menu_fonts.render('B: ', True, SOLARIZEDBASE0), (List_of_writings['G'][1][0]+100, List_of_writings['Alpha channel color'][1][1]+List_of_writings['Alpha channel color'][0].get_height()+10)]
		List_of_writings['Frame slow constant'] = [self.menu_fonts.render('Frame Slow Constant: ', True, SOLARIZEDBASE0), (0, List_of_writings['R'][1][1]+List_of_writings['R'][0].get_height()+10)]
		List_of_writings['slow constant'] = [self.menu_fonts.render(str(slow_const), True, CYAN), (List_of_writings['Frame slow constant'][0].get_width() + 30, List_of_writings['R'][1][1]+List_of_writings['R'][0].get_height()+10)]
		List_of_writings['Zooming scale'] = [self.menu_fonts.render("Zooming Scale: ", True, SOLARIZEDBASE0), (BackgroundRect.width/2 + 50, List_of_writings['Column number'][1][1])]
		List_of_writings['Rotation'] = [self.menu_fonts.render("Rotation Scale: ", True, SOLARIZEDBASE0), (BackgroundRect.width/2 + 50, List_of_writings['Row number'][1][1])]
		###########
		#buttons:
		Browse_button = buttons(self.IMAGE["Browse Button Hovered"], self.IMAGE["Browse Button Normal"], self.IMAGE["Browse Button Clicked"], "Browse Button")
		Browse_button.Set_Rect(BackgroundRect.width-Browse_button.get_width()-10+Background_Coord.x,30+Background_Coord.y) #Should be in the screen reference
		Cancel_button = buttons(self.IMAGE["Cancel Button Hovered"], self.IMAGE["Cancel Button Normal"], self.IMAGE["Cancel Button Clicked"], "Cancel Button")
		Cancel_button.Set_Rect(BackgroundRect.width-Cancel_button.get_width()-10+Background_Coord.x,BackgroundRect.height-Cancel_button.get_height() - 10+Background_Coord.y) #Should be in the screen reference
		OK_button = buttons(self.IMAGE["OK Button Hovered"], self.IMAGE["OK Button Normal"], self.IMAGE["OK Button Clicked"], "OK Button")
		OK_button.Set_Rect(BackgroundRect.width-Cancel_button.get_width()-OK_button.get_width()-30+Background_Coord.x,BackgroundRect.height-OK_button.get_height() - 10+Background_Coord.y) #Should be in the screen reference
		#Adding and minus button
		plus_sign = self.menu_fonts_addMinus.render("+", True, VIOLET)
		plus_sign_hover = self.menu_fonts_addMinus.render("+", True, ORANGE)
		plus_sign_clicked = self.menu_fonts_addMinus_clicked.render("+", True, ORANGE)
		minus_sign = self.menu_fonts_addMinus.render("-", True, VIOLET)
		minus_sign_hover = self.menu_fonts_addMinus.render("-", True, ORANGE)
		minus_sign_clicked = self.menu_fonts_addMinus_clicked.render("-", True, ORANGE)
		
		plus_col_button = buttons(plus_sign_hover, plus_sign, plus_sign_clicked, "Plus column button")
		plus_col_button.Set_Rect(List_of_writings['Column'][1][0] - 25 +Background_Coord.x, List_of_writings['Column'][1][1] - 10 +Background_Coord.y)
		minus_col_button = buttons(minus_sign_hover, minus_sign, minus_sign_clicked, "Minus column button")
		minus_col_button.Set_Rect(List_of_writings['Column'][1][0] + List_of_writings['Column'][0].get_width() + 10+Background_Coord.x, List_of_writings['Column'][1][1] - 15 +Background_Coord.y)
		plus_row_button = buttons(plus_sign_hover, plus_sign, plus_sign_clicked, "Plus row button")
		plus_row_button.Set_Rect(List_of_writings['Row'][1][0] - 25 +Background_Coord.x, List_of_writings['Row'][1][1] - 10 +Background_Coord.y)
		minus_row_button = buttons(minus_sign_hover, minus_sign, minus_sign_clicked, "Minus row button")
		minus_row_button.Set_Rect(List_of_writings['Row'][1][0] + List_of_writings['Row'][0].get_width() + 10+Background_Coord.x, List_of_writings['Row'][1][1] - 15 +Background_Coord.y)
		plus_slow_button = buttons(plus_sign_hover, plus_sign, plus_sign_clicked, "Plus slow button")
		plus_slow_button.Set_Rect(List_of_writings['slow constant'][1][0] - 25 + Background_Coord.x, List_of_writings['R'][1][1]+List_of_writings['R'][0].get_height()+0 +Background_Coord.y)
		minus_slow_button = buttons(minus_sign_hover, minus_sign, minus_sign_clicked, "Minus slow button")
		minus_slow_button.Set_Rect(List_of_writings['slow constant'][1][0] + List_of_writings['slow constant'][0].get_width() + 10+Background_Coord.x, List_of_writings['R'][1][1]+List_of_writings['R'][0].get_height()-5+Background_Coord.y)
		
		buttons_list = {"Browse Button":[Browse_button, (Browse_button.ButtonRect.x - Background_Coord.x, Browse_button.ButtonRect.y - Background_Coord.y)], 
				"OK Button":[OK_button, (OK_button.ButtonRect.x - Background_Coord.x, OK_button.ButtonRect.y - Background_Coord.y)],
				"Cancel Button":[Cancel_button, (Cancel_button.ButtonRect.x - Background_Coord.x, Cancel_button.ButtonRect.y - Background_Coord.y)],
				"Plus Column Button": [plus_col_button, (plus_col_button.ButtonRect.x - Background_Coord.x, plus_col_button.ButtonRect.y - Background_Coord.y)],
				"Minus Column Button": [minus_col_button, (minus_col_button.ButtonRect.x - Background_Coord.x, minus_col_button.ButtonRect.y - Background_Coord.y)],
				"Plus Row Button": [plus_row_button, (plus_row_button.ButtonRect.x - Background_Coord.x, plus_row_button.ButtonRect.y - Background_Coord.y)],
				"Minus Row Button": [minus_row_button, (minus_row_button.ButtonRect.x - Background_Coord.x, minus_row_button.ButtonRect.y - Background_Coord.y)],
				"Plus Slow Button": [plus_slow_button, (plus_slow_button.ButtonRect.x - Background_Coord.x, plus_slow_button.ButtonRect.y - Background_Coord.y)],
				"Minus Slow Button": [minus_slow_button, (minus_slow_button.ButtonRect.x - Background_Coord.x, minus_slow_button.ButtonRect.y - Background_Coord.y)]} #The coordinate should been in the button reference.
		
		#########################
		#Insert Box
		R_insert_box = Insert_Box_IntNumber("R insert box", self.menu_fonts)
		R_insert_box.Set_Rect(List_of_writings['R'][1][0] + 30 + Background_Coord.x, List_of_writings['R'][1][1] + Background_Coord.y)
		G_insert_box = Insert_Box_IntNumber("G insert box", self.menu_fonts)
		G_insert_box.Set_Rect(List_of_writings['G'][1][0] + 30 + Background_Coord.x, List_of_writings['G'][1][1] + Background_Coord.y)
		B_insert_box = Insert_Box_IntNumber("B insert box", self.menu_fonts)
		B_insert_box.Set_Rect(List_of_writings['B'][1][0] + 30 + Background_Coord.x, List_of_writings['B'][1][1] + Background_Coord.y)
		#Slow_Frame_box = Insert_Box_IntNumber("Frame slow constant", self.menu_fonts, "1")
		Zoom_insert_box = Insert_Box_FloatNumber("Zoom insert box", self.menu_fonts, "1")
		Zoom_insert_box.Set_Rect(List_of_writings["Zooming scale"][1][0]+List_of_writings["Zooming scale"][0].get_width()+10+Background_Coord.x, List_of_writings["Zooming scale"][1][1]+Background_Coord.y)
		Rotation_insert_box = Insert_Box_FloatNumber("Rotation insert box", self.menu_fonts, "0")
		Rotation_insert_box.Set_Rect(List_of_writings["Rotation"][1][0]+List_of_writings["Rotation"][0].get_width()+10+Background_Coord.x, List_of_writings["Rotation"][1][1]+Background_Coord.y)
		
		Insert_box_list = {"R insert box": [R_insert_box, (R_insert_box.Box_Rect.x - Background_Coord.x, R_insert_box.Box_Rect.y - Background_Coord.y)],
				"G insert box": [G_insert_box, (G_insert_box.Box_Rect.x - Background_Coord.x, G_insert_box.Box_Rect.y - Background_Coord.y)],
				"B insert box": [B_insert_box, (B_insert_box.Box_Rect.x - Background_Coord.x, B_insert_box.Box_Rect.y - Background_Coord.y)],
				"Zoom insert box":[Zoom_insert_box, (Zoom_insert_box.Box_Rect.x - Background_Coord.x, Zoom_insert_box.Box_Rect.y - Background_Coord.y)],
				"Rotation insert box":[Rotation_insert_box, (Rotation_insert_box.Box_Rect.x - Background_Coord.x, Rotation_insert_box.Box_Rect.y - Background_Coord.y)]}
		
		MOUSE_POSITION = (0,0)
		default_surface = self.display_surface.copy()
		clicked = False #To ackknowledge the execution of the fucntion after there is a mousebutton going down
		unclicked = False #Required to acknowledge the  execution of the function after mousebutton goes up
		Running = True
		while Running:
			unclicked = False
			keydown = False
			pygame.display.update()
			for event in pygame.event.get():
				#if event.type == pygame.KEYDOWN:
				#	if event.key == pygame.K_ESCAPE:
				#		print("escaping the Adding Frame")
				#		Running = False
				#		break
						
				if event.type == pygame.MOUSEMOTION:
					MOUSE_POSITION = pygame.mouse.get_pos()
					
				elif event.type == pygame.MOUSEBUTTONDOWN:
					MOUSE_POSITION = pygame.mouse.get_pos()
					clicked = True
					
				elif event.type == pygame.MOUSEBUTTONUP:
					MOUSE_POSITION = pygame.mouse.get_pos()
					clicked = False
					unclicked = True
					
				elif event.type == pygame.KEYDOWN:
					keydown = True 
					key_pressed = event.key
			#Update the background:
			Background.fill(SOLARIZEDBASE3)
			for writings in List_of_writings:
				Background.blit(List_of_writings[writings][0], List_of_writings[writings][1])
			
			for button in buttons_list:
				#print(button)
				if buttons_list[button][0].ButtonRect.collidepoint(MOUSE_POSITION): #Testing in the screen reference or coordinate
					if clicked == True:
						buttons_list[button][0].Mouse_Clicked()
					elif unclicked == True:
						if buttons_list[button][0].Name == "Cancel Button":
							print("Escaping the Adding Frame")
							Running = False
							break
						
						elif buttons_list[button][0].Name == "OK Button":
							if not file == "...":
								alpha_color = (Insert_box_list['R insert box'][0].Intnumber, Insert_box_list['G insert box'][0].Intnumber, Insert_box_list['B insert box'][0].Intnumber)
								ZoomScale = Insert_box_list['Zoom insert box'][0].Floatnumber
								RotationAngle = Insert_box_list['Rotation insert box'][0].Floatnumber
								return [file, row_num, col_num, alpha_color, slow_const, ZoomScale, RotationAngle]
						elif buttons_list[button][0].Name == "Browse Button":
							print("Browsing file")
							File_name = prompt_file()
							if not File_name:
								file = '...'
							else:
								file = File_name
								buttons_list[button][0].Set_Rect(buttons_list[button][1][0], List_of_writings['File'][1][1] + List_of_writings['File'][0].get_height()+Background_Coord.y) #Adjusting for background coordinate because the buttons are expressed initially in the screen coordintae (To interact with the mouse), while the writing sis expressed direcly in the menu background coordinate 9it didn't need to interact. 
								buttons_list[button][1] = (buttons_list[button][0].ButtonRect.x - Background_Coord.x, buttons_list[button][0].ButtonRect.y - Background_Coord.y)
								List_of_writings['File'] = [self.menu_fonts.render(File_name, True, CYAN), (List_of_writings['File name'][1][0]+List_of_writings['File name'][0].get_width(), List_of_writings['File name'][1][1])]
							
						elif buttons_list[button][0].Name == "Plus column button":
							col_num += 1
							List_of_writings['Column'] = [self.menu_fonts.render(str(col_num), True, CYAN), (List_of_writings['Column number'][0].get_width()+30, BackgroundRect.height/2 - 30)]
						
						elif buttons_list[button][0].Name == "Minus column button":
							if col_num >1:
								col_num -= 1
								List_of_writings['Column'] = [self.menu_fonts.render(str(col_num), True, CYAN), (List_of_writings['Column number'][0].get_width()+30, BackgroundRect.height/2 - 30)]
							
						elif buttons_list[button][0].Name == "Plus row button":
							row_num += 1
							List_of_writings['Row'] = [self.menu_fonts.render(str(row_num), True, CYAN), (List_of_writings['Row number'][0].get_width()+30, List_of_writings['Column number'][1][1]+List_of_writings['Column number'][0].get_height()+10)]
						
						elif buttons_list[button][0].Name == "Minus row button":
							if row_num >1:
								row_num -= 1
								List_of_writings['Row'] = [self.menu_fonts.render(str(row_num), True, CYAN), (List_of_writings['Row number'][0].get_width()+30, List_of_writings['Column number'][1][1]+List_of_writings['Column number'][0].get_height()+10)]
								
						elif buttons_list[button][0].Name == "Plus slow button":
							slow_const += 1
							List_of_writings['slow constant'] = [self.menu_fonts.render(str(slow_const), True, CYAN), (List_of_writings['Frame slow constant'][0].get_width() + 30, List_of_writings['R'][1][1]+List_of_writings['R'][0].get_height()+10)]
						
						elif buttons_list[button][0].Name == "Minus slow button":
							if slow_const >1:
								slow_const -= 1
								List_of_writings['slow constant'] = [self.menu_fonts.render(str(slow_const), True, CYAN), (List_of_writings['Frame slow constant'][0].get_width() + 30, List_of_writings['R'][1][1]+List_of_writings['R'][0].get_height()+10)]
							
							
							
							
							
					else:
						buttons_list[button][0].Mouse_Hover()
					
				else:
					if buttons_list[button][0].Is_hovered() or buttons_list[button][0].Is_clicked():
						buttons_list[button][0].Mouse_Unhover()
						
				
				Background.blit(buttons_list[button][0].Image, buttons_list[button][1]) #Blitting in the Background reference or coordinate
			
			for insert in Insert_box_list:
				if clicked:
					if Insert_box_list[insert][0].Box_Rect.collidepoint(MOUSE_POSITION):
						Insert_box_list[insert][0].Mouse_Clicked()
						
					elif Insert_box_list[insert][0].Is_Clicked:
						Insert_box_list[insert][0].Mouse_Unclicked()
				
				if Insert_box_list[insert][0].Is_Clicked():
					Insert_box_list[insert][0].blink()
					if keydown:
						if key_pressed in [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_BACKSPACE, pygame.K_PERIOD, pygame.K_KP_PERIOD, pygame.K_KP_0, pygame.K_KP_1, pygame.K_KP_2, pygame.K_KP_3, pygame.K_KP_4, pygame.K_KP_5, pygame.K_KP_6, pygame.K_KP_7, pygame.K_KP_8, pygame.K_KP_9]:
							Insert_box_list[insert][0].Word_type(key_pressed)

					
				Background.blit(Insert_box_list[insert][0].Surface_to_show, Insert_box_list[insert][1])
			#If there is a clicked outside of the background Menu, the code below enable us to escape the adding frame menu:
			if not BackgroundRect.collidepoint(MOUSE_POSITION) and unclicked == True:
				print("Escaping the Adding Frame")
				Running = False
				break
			#clear the screen:
			self.display_surface.blit(default_surface, (0,0))
			pygame.draw.rect(self.display_surface, (255,0,0), Browse_button.ButtonRect)
			self.display_surface.blit(Background, Background_Coord)
			pygame.display.update()
		
	def Editing_frame(self):
		pass
		
	def play(self):
		#Starting the condition for the while loop
		is_running = [True]
		MOUSE_POSITION = (0,0)
		
		clicked = False
		while is_running[0]:
			unclicked = False #Turned on when the mouse button is lift up
			#clicked_what = "Nothing"
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					print("Receiving Quit event:", event)
					is_running[0] = False
				
				elif event.type == pygame.MOUSEMOTION:
					MOUSE_POSITION = pygame.mouse.get_pos()
				elif event.type == pygame.MOUSEBUTTONDOWN:
					MOUSE_POSITION = pygame.mouse.get_pos()
					clicked = True
				elif event.type == pygame.MOUSEBUTTONUP:
					MOUSE_POSITION = pygame.mouse.get_pos()
					clicked = False
					unclicked = True
		
			#Clear the screen 
			self.display_surface.fill(self.BackgroundColor)
			for i in range(len(self.Buttons_list)): #i is the row of the matrix
				for j in range(len(self.Buttons_list[i])): #j is teh column of the matrix
					if self.Buttons_list[i][j].ButtonRect.collidepoint(MOUSE_POSITION) and self.Buttons_list[i][j].Appearance == "Show":
						if clicked == True:
							self.Buttons_list[i][j].Mouse_Clicked()
						elif unclicked == True:
							next_frame = self.Adding_frame()
							print(next_frame)
							if next_frame:
								Filename = next_frame[0]
								row_num = next_frame[1]
								col_num = next_frame[2]
								alpha_color = next_frame[3]
								slow_const = next_frame[4]
								ZoomScale = next_frame[5]
								RotationAngle = next_frame[6]
								spritesheet = pygame.transform.rotozoom(pygame.image.load(Filename), RotationAngle, ZoomScale)
								Frame, width, height = sprite_sheet_loader(spritesheet, row_num, col_num, alpha_color)
								Frame_num = len(Frame)
								Frame_list = {"Picture list": Frame, "Number of frames": Frame_num, 
									"Motion cycle":-1, "Slow constant": slow_const, 
									"Picture loc": Filename, "Row num": row_num, 
									"Col num": col_num, "Alpha color": alpha_color,
									"Frame Width": width, "Frame height": height,
									"Zoom scale": ZoomScale, "Rotation Angle": RotationAngle}
							
								Frame_Rect = Frame[0].get_rect()
								if self.Buttons_list[i][j].Name == "First Button":
									Frame_Rect.center = (10+width/2, 10+height/2)
									Frame_list["Rect"] = Frame_Rect
									self.Buttons_list[i][j].Appearance = "Not show"
									self.Frames.append([Frame_list])
									
								elif self.Buttons_list[i][j].Name == "Column Button":
									Latest_frame_in_row = len(self.Frames[i])
									Width_row_latest_frame = self.Frames[i][Latest_frame_in_row-1]["Frame Width"]
									Frame_list_Coord = pygame.math.Vector2(self.Frames[i][Latest_frame_in_row-1]["Rect"].topleft)
									Frame_Rect.topleft = (Frame_list_Coord.x + Width_row_latest_frame +10, Frame_list_Coord.y)
									Frame_list["Rect"] = Frame_Rect
									self.Frames[i].append(Frame_list)
								
								elif self.Buttons_list[i][j].Name == "Row Button":
									#First we need to get the maximum height of the frames above it.
									list_of_heights = []
									for Frame in range(len(self.Frames[i-1])):
										list_of_heights.append(self.Frames[i-1][Frame]["Frame height"])
									
									Height_of_the_frame_above =max(list_of_heights) 
									Frame_Rect.topleft = (self.Frames[i-1][0]["Rect"].x, self.Frames[i-1][0]["Rect"].y+Height_of_the_frame_above+10)
									Frame_list["Rect"] = Frame_Rect
									self.Buttons_list[i][j].Appearance = "Not show"
									self.Frames.append([Frame_list])
								
								#self.Frames.append([Frame_list])
								#self.Buttons_list[i][j].Appearance = "Not show"
								self.Buttons_list[i][j].run_function(Frame_list, self.Buttons_list, i, j)
						else:
							self.Buttons_list[i][j].Mouse_Hover()
					else:
						if self.Buttons_list[i][j].Is_hovered() or self.Buttons_list[i][j].Is_clicked():
							self.Buttons_list[i][j].Mouse_Unhover()
			
					#Blitting the buttons:
					if self.Buttons_list[i][j].Appearance == "Show":
						#blit_coord = pygame.math.Vector2(self.Buttons_list[i][j].CenterRect.x - self.Buttons_list[i][j].Image.get_width()/2, self.Buttons_list[i][j].CenterRect.y - self.Buttons_list[i][j].Image.get_height()/2)
						#self.display_surface.blit(self.Buttons_list[i][j].Image, blit_coord)
						self.display_surface.blit(self.Buttons_list[i][j].Image, self.Buttons_list[i][j].ButtonRect)
				
				#Blitting the frames:
				for i in range(len(self.Frames)):
					for j in range(len(self.Frames[i])):
						self.Frames[i][j]["Motion cycle"] +=1
						#if self.Frames[i][j]["Motion cycle"] >= self.Frames[i][j]["Number of frames"]*self.Frames[i][j]["Slow constant"]:
						if self.Frames[i][j]["Motion cycle"] >= self.Frames[i][j]["Number of frames"]*self.Frames[i][j]["Slow constant"]:
							self.Frames[i][j]["Motion cycle"] = 0
						self.display_surface.blit(self.Frames[i][j]["Picture list"][self.Frames[i][j]["Motion cycle"]//self.Frames[i][j]["Slow constant"]], self.Frames[i][j]["Rect"])
					
					
			
			
			#Updating the display:
			pygame.display.update()
			
			#Defines the frame rate
			self.clock.tick(FRAME_REFRESH_RATE)
		
		#Let pygame close:
		pygame.quit()
		sys.exit()
		
def main():
	print("Starting the program")
	program = Spritesheet_Viewer()
	program.play()
	print("Program close")
		
#Function that take the frames 
def sprite_sheet_loader(picture, row_num, column_num, color=(0,255,0)):
	"""
	This function will take a spritesheet with equal width and height of the
	frame and then return a list of the frame separated.
	Assumption: the spritesheet is travelling column wise. Meaning that it move
		through the first row first, passing all the columns, and then go
		to the next row and return to the first column. 
	picture: the spritesheet.
	row_num: the number of rows in the spritesheet.
	column_num: the number of column rows in the spritesheet. 
	"""
	Frame_width = picture.get_width() / column_num
	Frame_height = picture.get_height() / row_num
	Frames = []
	for row in range(row_num):
		for column in range(column_num):
			Frame = sprite_sheet_separator(picture, Frame_width, Frame_height, column*Frame_width, row*Frame_height, color)
			Frames.append(Frame)
	return Frames, Frame_width, Frame_height, 
	
	
	
	
def sprite_sheet_separator(picture, width, height, top_left_frame_width, top_left_frame_height, color):
	"""
	This function will take a spritesheet and return a specific frame 
	that is needed.
	picture: a spritesheet
	width: The width of the frame that we needed
	height: The height of the frame that we needed
	top_left_frame_width: the location of the top left frame that we need in 
				the overall picture, its x coordinate value
	top_left_frame_height: the location of the top left frame that we need in 
				the overall picture, its y coordinate value.
	"""
	Frame = pygame.Surface((width, height)).convert_alpha()
	#Setting up the mask
	Frame_mask = pygame.Surface(Frame.get_size()).convert_alpha() #Convert alpha to have an alpha channel
	Frame_mask.fill((255,255,255))
	Frame.fill(color)
	Frame.blit(picture, (0,0), area=(top_left_frame_width, top_left_frame_height, width, height))
    #Frame.blit(picture, (-top_left_frame_width, -top_left_frame_height))
	#Frame.blit(Frame_mask, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
	
	Frame.set_colorkey(color)
	return Frame
	
def prompt_file():
	"""
	Using Tkinter to create a file dialog and cleanup when finished
	this is taken from stackoverflow discussion forum by a user "import random", :
	stackoverflow.com/questions/63801960/how-to-prompt-user-to-open-a-file-with-python3-pygame
	"""
	top = tkinter.Tk()
	top.withdraw() #hide window
	file_name = tkinter.filedialog.askopenfilename(parent=top)
	top.destroy()
	
	return file_name

class buttons:
	"""
	This is for displaying and interacting with the butttons at the menu screen.
	But maybe I can use it for other places as well
	"""
	def __init__(self, ImageHover, ImageNormal, ImageClicked, name):
		self.Image_Hover = ImageHover
		self.Image_Normal = ImageNormal
		self.Image_Clicked = ImageClicked
		#self.Image_Click = []
		#The rect to interact with\
		self.Image = self.Image_Normal
		self.ButtonRect = self.Image.get_rect()
		self.CenterRect = pygame.math.Vector2(self.ButtonRect.center)
		self.Hovered = False
		self.Clicked = False
		self.Name = name
		self.Appearance = "Show" #or "Not show"
		
	def Mouse_Hover(self):
		self.Hovered = True
		self.Image = self.Image_Hover
		
	def Mouse_Unhover(self):
		self.Hovered = False
		self.Clicked = False
		self.Image = self.Image_Normal
		
	def Mouse_Clicked(self):
		self.Clicked = True
		self.Image = self.Image_Clicked
		
	def get_width(self):
		width = self.ButtonRect.width 
		
		return width
		
	def get_height(self):
		height = self.ButtonRect.height
		
		return height
		
	def Set_Rect(self, x, y):
		self.ButtonRect.x = x
		self.ButtonRect.y = y
		self.CenterRect.x = self.CenterRect.x + x
		self.CenterRect.y = self.CenterRect.y + y
		
	def Is_hovered(self):
		return self.Hovered
		
	def Is_clicked(self):
		return self.Clicked	


class First_buttons(buttons):
	"""
	For the first button to be used
	"""
	def __init__(self, ImageHover, ImageNormal, ImageClicked, name):
		super().__init__(ImageHover, ImageNormal, ImageClicked, name)
		
	def run_function(self, Frame, button_list, i, j):
		"""
		Frame consist of the follwing:
		Frame_list = {"Picture list": Frame, "Number of frames": Frame_num, "Motion cycle":-1, "Slow constant": slow_const, 
		"Picture loc": Filename, "Row num": row_num, "Col num": col_num, "Alpha color": alpha_color,
		"Frame Width": width, "Frame height": height, "Zoom scale": ZoomScale, "Rotation Angle": RotationAngle, "Rect":Frame_Rect}
		"""
		row_button = Row_Button(self.Image_Hover, self.Image_Normal, self.Image_Clicked, "Row Button", Frame)
		column_button = Column_Button(self.Image_Hover, self.Image_Normal, self.Image_Clicked, "Column Button", Frame)
		row_button.Set_Rect(self.ButtonRect.x, Frame["Rect"].y+Frame["Rect"].height+self.ButtonRect.y) 
		column_button.Set_Rect(Frame["Rect"].x+Frame["Rect"].width+self.ButtonRect.x, self.ButtonRect.y) 
		button_list.append([row_button])
		button_list[i].append(column_button)
		#button_list.remove(button_list[0])
		
class Addition_Button(buttons):
	"""
	The button that have frames attached to it. 
	"""		
	def __init__(self, ImageHover, ImageNormal, ImageClicked, name, Frame):
		super().__init__(ImageHover, ImageNormal, ImageClicked, name)
		
		self.Frame_Coord = pygame.math.Vector2(Frame["Rect"].x, Frame["Rect"].y)
		self.Frame_Size = pygame.math.Vector2(Frame["Rect"].width, Frame["Rect"].height)
	
	
	def upgrade_frame(self, Frame):
		self.Frame_Coord = pygame.math.Vector2(Frame["Rect"].x, Frame["Rect"].y)
		self.Frame_Size = pygame.math.Vector2(Frame["Rect"].width, Frame["Rect"].height)
		
class Row_Button(Addition_Button):
	"""
	The button that will add new row 
	"""
	def __init__(self, ImageHover, ImageNormal, ImageClicked, name, Frame):
		super().__init__(ImageHover, ImageNormal, ImageClicked, name, Frame)
		
	def upgrade_pos(self, Frame):
		newY = Frame["Rect"].y + Frame.height + self.ButtonRect.y
		newX = self.ButtonRect.x
		self.Set_Rect(newX, newY)
	
	def run_function(self, Frame, button_list, i, j): #Add new row
		"""
		Frame, button_list, i, and j are all a dummy input as Column function didn't use them. 
		It is put because the other type of buttons use it, so that the main code didn't differentiate between them. 
		"""
		new_column_button = Column_Button(self.Image_Hover, self.Image_Normal, self.Image_Clicked, "Column Button", Frame)
		centerY = Frame["Rect"].centery
		new_column_button.Set_Rect(Frame["Rect"].x+Frame["Rect"].width+10, max(self.ButtonRect.y, centerY)) 
		new_row_button = Row_Button(self.Image_Hover, self.Image_Normal, self.Image_Clicked, "Row Button", Frame)
		new_row_button.Set_Rect(self.ButtonRect.x, Frame["Rect"].y+Frame["Rect"].height+10)#+self.ButtonRect.y) 
		button_list.append([new_row_button])
		button_list[i].append(new_column_button)
		#self.upgrade_pos(Frame)
		#self.upgrade_frame(Frame)
		
		
		
class Column_Button(Addition_Button):
	"""
	The button that will add new column 
	"""
	def __init__(self, ImageHover, ImageNormal, ImageClicked, name, Frame):
		super().__init__(ImageHover, ImageNormal, ImageClicked, name, Frame)
		
	def upgrade_pos(self, Frame):
		newY = Frame["Rect"].y+Frame["Rect"].height/2-self.ButtonRect.width/2
		newX = Frame["Rect"].x + Frame["Rect"].width + 10# + self.ButtonRect.x
		self.Set_Rect(newX, newY)
	
	def run_function(self, Frame, button_list, i, j): #Add new column
		"""
		Frame, button_list, i, and j are all a dummy input as Column function didn't use them. 
		It is put because the other type of buttons use it, so that the main code didn't differentiate between them. 
		"""
		#new_row_button = Row_Button(self.Image_Hover, self.Image_Normal, self.Image_Clicked, "Row Button", Frame)
		#new_row_button.Set_Rect(self.ButtonRect.x, Frame["Rect"].y+Frame["Rect"].height+self.ButtonRect.y) 
		self.upgrade_pos(Frame)
		self.upgrade_frame(Frame)

class Insert_Box:
	"""
	To put in some input from the user
	"""
	def __init__(self, name, font, default_word = ""):
		self.name = name #The name to be identified the Insert_Box with
		self.Word = default_word #Saving the word to be written
		self.font = font #Saving the font for future writing and change
		self.Box = pygame.Surface((70,20)) #The box to be displayed
		self.Box.fill(SOLARIZEDBASE2) #Filling in the background color
		self.Box_Rect = self.Box.get_rect() #The rect of Box
		#self.Box_blinked = self.Box.copy() #FOr writing with marker
		self.Box_Empty = self.Box.copy() #FOr empty part of the blinking
		self.CenterRect = pygame.math.Vector2(self.Box_Rect.center) #Saving teh center coordinate for ease of logistic purposes if needed
		self.Word_in_Box = self.font.render(self.Word+' ', True, CYAN) #This is The one blitted to the original box
		self.Word_in_Box_Rect = self.Word_in_Box.get_rect() #The Rect of the written word
		self.Box.blit(self.Word_in_Box, (self.Box_Rect.width - self.Word_in_Box_Rect.width,0)) #Blitting the word to the box (withput marker)
		#self.Word_Marker = self.font.render(self.Word+'|', True, CYAN) #This is the one blitted to the Box_blinked
		#self.Marker_Rect = self.Word_Marker.get_rect() #The Rect of the word together withthe marker to be litted to the Box_blicked
		#self.Box_blinked.blit(self.Word_Marker, (self.Box_Rect.width - self.Marker_Rect.width,0)) #Putting the marked writing in the marked box
		self.Surface_counter = 1
		self.Surface_to_show = self.Box
		self.Clicked = False
		self.Blink_Counter = 1
	
	def change(self):
		if self.Surface_counter == 1:
			self.Surface_to_show = self.Box_Empty
			self.Surface_counter = 2
		elif self.Surface_counter == 2:
			self.Surface_to_show = self.Box
			self.Surface_counter = 1
		#elif self.Surface_counter == 3:
		#	self.Surface_to_show = self.Box
		#	self.Surface_counter = 1
			
	def blink(self):
		if self.Blink_Counter > 100:
			self.Blink_Counter = 1
		
		if self.Blink_Counter%100 == 0:
			self.change()

		self.Blink_Counter +=1
	
	def get_width(self):
		width = self.Box_Rect.width 
		
		return width
		
	def get_height(self):
		height = self.Box_Rect.height
		
		return height
		
	def Set_Rect(self, x, y):
		self.Box_Rect.x = x
		self.Box_Rect.y = y
		self.CenterRect.x = self.CenterRect.x + x
		self.CenterRect.y = self.CenterRect.y + y
		
	def Mouse_Clicked(self):
		self.Clicked = True
		self.Surface_to_show = self.Box_Empty
		self.Surface_counter = 2
		
	
	def Mouse_Unclicked(self):
		self.Clicked = False
		self.Surface_to_show = self.Box
		self.Surface_counter = 1
		
	def Is_Clicked(self):
		return self.Clicked	
		
class Insert_Box_IntNumber(Insert_Box):
	"""
	Same like insert box but for number only
	"""
	def __init__(self, name, font, default_word = "255"):
		super().__init__(name, font, default_word)
		self.Intnumber = int(default_word)
		
	def Change_Int(self,integer):
		"""
		Must enter a string integer
		"""
		self.Word = integer
		self.Intnumber = int(self.Word)
		self.Word_in_Box = self.font.render(self.Word+' ', True, CYAN) #This is The one blitted to the original box
		self.Word_in_Box_Rect = self.Word_in_Box.get_rect() #The Rect of the written word
		self.Box.fill(SOLARIZEDBASE2)
		self.Box.blit(self.Word_in_Box, (self.Box_Rect.width - self.Word_in_Box_Rect.width,0)) #Blitting the word to the box (withput marker)
		
		
	def Word_type(self, key_type):
		if key_type == pygame.K_BACKSPACE:
			if len(self.Word) > 1:
				self.Change_Int(self.Word[:-1])
			elif len(self.Word) == 1:
				self.Change_Int("0")
				
		else:
			number_as_word = number_typed(key_type)
			if not self.Word == "0":
				self.Change_Int(self.Word+number_as_word)
			elif self.Word == "0":
				self.Change_Int(number_as_word)
	
	def Mouse_Clicked(self):
		self.Clicked = True
		self.Surface_to_show = self.Box_Empty
		self.Surface_counter = 2
		self.Change_Int('0')

class Insert_Box_FloatNumber(Insert_Box):
	"""
	Same like insert box IntNumber but for having the ability to put in point '.'
	"""
	def __init__(self, name, font, default_word = "255"):
		super().__init__(name, font, default_word)
		self.Floatnumber = int(default_word)
		
	def Change_Float(self,float_number):
		"""
		Must enter a string float
		"""
		self.Word = float_number
		self.Floatnumber = float(self.Word)
		self.Word_in_Box = self.font.render(self.Word+' ', True, CYAN) #This is The one blitted to the original box
		self.Word_in_Box_Rect = self.Word_in_Box.get_rect() #The Rect of the written word
		self.Box.fill(SOLARIZEDBASE2)
		self.Box.blit(self.Word_in_Box, (self.Box_Rect.width - self.Word_in_Box_Rect.width,0)) #Blitting the word to the box (withput marker)
		
		
	def Word_type(self, key_type):
		if key_type == pygame.K_BACKSPACE:
			if len(self.Word) > 1:
				self.Change_Float(self.Word[:-1])
			elif len(self.Word) == 1:
				self.Change_Float("0")
		
		elif key_type in (pygame.K_PERIOD, pygame.K_KP_PERIOD):
			period = period_typed(self.Word, key_type)
			self.Change_Float(self.Word+period)
		else:
			number_as_word = number_typed(key_type)
			if not self.Word == "0":
				self.Change_Float(self.Word+number_as_word)
			elif self.Word == "0":
				self.Change_Float(number_as_word)
	
	def Mouse_Clicked(self):
		self.Clicked = True
		self.Surface_to_show = self.Box_Empty
		self.Surface_counter = 2
		self.Change_Float('0')
		
def letter_typed(player, key_typed):
	"""
	typing in the letter into the player.words_typed
	"""
	"""
	if key_typed == pygame.K_a:
		player.words_typed += 'a'
	elif key_typed == pygame.K_b:
		player.words_typed += 'b'
	elif key_typed == pygame.K_c:
		player.words_typed += 'c'
	elif key_typed == pygame.K_d:
		player.words_typed += 'd'
	elif key_typed == pygame.K_e:
		player.words_typed += 'e'
	elif key_typed == pygame.K_f:
		player.words_typed += 'f'	
	elif key_typed == pygame.K_g:
		player.words_typed += 'g'
	elif key_typed == pygame.K_h:
		player.words_typed += 'h'
	elif key_typed == pygame.K_i:
		player.words_typed += 'i'	
	elif key_typed == pygame.K_j:
		player.words_typed += 'j'
	elif key_typed == pygame.K_k:
		player.words_typed += 'k'
	elif key_typed == pygame.K_l:
		player.words_typed += 'l'
	elif key_typed == pygame.K_m:
		player.words_typed += 'm'
	elif key_typed == pygame.K_n:
		player.words_typed += 'n'
	elif key_typed == pygame.K_o:
		player.words_typed += 'o'
	elif key_typed == pygame.K_p:
		player.words_typed += 'p'
	elif key_typed == pygame.K_q:
		player.words_typed += 'q'
	elif key_typed == pygame.K_r:
		player.words_typed += 'r'
	elif key_typed == pygame.K_s:
		player.words_typed += 's'
	elif key_typed == pygame.K_t:
		player.words_typed += 't'
	elif key_typed == pygame.K_u:
		player.words_typed += 'u'
	elif key_typed == pygame.K_v:
		player.words_typed += 'v'
	elif key_typed == pygame.K_w:
		player.words_typed += 'w'
	elif key_typed == pygame.K_x:
		player.words_typed += 'x'
	elif key_typed == pygame.K_y:
		player.words_typed += 'y'
	elif key_typed == pygame.K_z:
		player.words_typed += 'z'
	"""
	if key_typed == pygame.K_a:
		player.words_typed += 'A'
	elif key_typed == pygame.K_b:
		player.words_typed += 'B'
	elif key_typed == pygame.K_c:
		player.words_typed += 'C'
	elif key_typed == pygame.K_d:
		player.words_typed += 'D'
	elif key_typed == pygame.K_e:
		player.words_typed += 'E'
	elif key_typed == pygame.K_f:
		player.words_typed += 'F'	
	elif key_typed == pygame.K_g:
		player.words_typed += 'G'
	elif key_typed == pygame.K_h:
		player.words_typed += 'H'
	elif key_typed == pygame.K_i:
		player.words_typed += 'I'	
	elif key_typed == pygame.K_j:
		player.words_typed += 'J'
	elif key_typed == pygame.K_k:
		player.words_typed += 'K'
	elif key_typed == pygame.K_l:
		player.words_typed += 'L'
	elif key_typed == pygame.K_m:
		player.words_typed += 'M'
	elif key_typed == pygame.K_n:
		player.words_typed += 'N'
	elif key_typed == pygame.K_o:
		player.words_typed += 'O'
	elif key_typed == pygame.K_p:
		player.words_typed += 'P'
	elif key_typed == pygame.K_q:
		player.words_typed += 'Q'
	elif key_typed == pygame.K_r:
		player.words_typed += 'R'
	elif key_typed == pygame.K_s:
		player.words_typed += 'S'
	elif key_typed == pygame.K_t:
		player.words_typed += 'T'
	elif key_typed == pygame.K_u:
		player.words_typed += 'U'
	elif key_typed == pygame.K_v:
		player.words_typed += 'V'
	elif key_typed == pygame.K_w:
		player.words_typed += 'W'
	elif key_typed == pygame.K_x:
		player.words_typed += 'X'
	elif key_typed == pygame.K_y:
		player.words_typed += 'Y'
	elif key_typed == pygame.K_z:
		player.words_typed += 'Z'
		
def number_typed(key_typed):
	"""
	typing in the number. Deletion is not managed here but elsewhere.
	"""
	words_typed = ""
	
	if key_typed in (pygame.K_0, pygame.K_KP_0):
		words_typed += '0'
	elif key_typed in (pygame.K_1, pygame.K_KP_1):
		words_typed += '1'
	elif key_typed == pygame.K_2:
		words_typed += '2'
	elif key_typed == pygame.K_3:
		words_typed += '3'
	elif key_typed == pygame.K_4:
		words_typed += '4'
	elif key_typed == pygame.K_5:
		words_typed += '5'	
	elif key_typed == pygame.K_6:
		words_typed += '6'
	elif key_typed == pygame.K_7:
		words_typed += '7'
	elif key_typed == pygame.K_8:
		words_typed += '8'	
	elif key_typed == pygame.K_9:
		words_typed += '9'
	
	return words_typed
	
def period_typed(existing_word, key_typed):
	"""
	typing in the flaoting number (period is allowed. Deletion is not managed here but elsewhere.
	"""
	words_typed = ""
	
	if existing_word.find(".") <0 and (key_typed in (pygame.K_PERIOD, pygame.K_KP_PERIOD)):
		words_typed += "."
	
	return words_typed
		
if __name__ == '__main__':
	main()
