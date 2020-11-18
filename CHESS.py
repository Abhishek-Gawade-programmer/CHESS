from tkinter import *
from tkinter import messagebox
from PIL import ImageTk,Image
import numpy as np
import pygame
from pecies_postion import Board_perce
import coins_move
pygame.mixer.init()


window=Tk()
window.title('CHESS MUTIPLAYER')
window.iconbitmap('Icon.ico')


class Board:
	def __init__(self,master):
		self.master=master
		self.board_frame=Frame(self.master)
		self.board_frame.pack()
		self.board_box=np.array([None,]*64).reshape(8,8)
		self.image_locs=Board_perce().reset_board()
		self.coins_loc_b=[] 
		self.coins_loc_w=[]
		self.king_positions=[]
		self.chance_of=StringVar();self.chance_of.set('white')
		self.king_in_checked=BooleanVar();self.king_in_checked.set(False)
		self.castle_of_white=BooleanVar();self.castle_of_white.set(False)
		self.castle_of_black=BooleanVar();self.castle_of_black.set(False)


	def create_boxes(self):
		for row in range(8):
			for col in range(8):
				if (row+col)%2==0:
					box_colour="#DDB88C"
				else:
					box_colour="#A66D4F"

				self.board_box[row][col]=Button(self.board_frame,relief='sunken',padx=35,
				pady=30,background=box_colour)

				self.board_box[row][col].grid(row=row,column=col)
				self.loc_to_imag(self.image_locs[row][col],row,col)
			
				self.board_box[row][col].config(image=self.image_locs[row][col][0],
					command=lambda r=row,c=col,l=self.image_locs[row][col][1]: self.on_peice_click(r,c,l))
				# self.alternate_chance()



 
	def loc_to_imag(self,loc,row,col):
		if loc:
			if loc[-5].isupper():
				if loc[-5]=='K':
					self.king_positions.append([row,col])

				self.coins_loc_w.append([row,col])
			else:
				if loc[-5]=='k':
					self.king_positions.append([row,col])
				self.coins_loc_b.append([row,col])


			self.image_locs[row][col]=[ImageTk.PhotoImage(Image.open(loc).resize((71,75))),loc]
		else:
			self.image_locs[row][col]=['',loc]

	def on_peice_click(self,row,col,loc_img):
		global coins_move_display
		try:
			self.remove_highlighting('1')
		except NameError:
			pass

		if loc_img!=None:

			coins_move_display=[]
			coins_move_display=coins_move.Coins_future_pos(self.image_locs,self.coins_loc_w,self.coins_loc_b,loc_img[-5],row,col).identify_coin()
			# print(coins_move_display)
			

			if  loc_img[-5]=='k':
				self.black_king_moves(row,col)



			elif  self.chance_of.get()!='black' and loc_img[-5].islower():
				self.for_black_check(row,col)

			# if coins_move_display==[] and self.king_in_checked.get()==True:
			# 	print('I KING HAVE NO CHACE TO MOVE')






			if  loc_img[-5]=='K':
				self.white_king_moves(row,col)
				
				




			elif  self.chance_of.get()!='white' and loc_img[-5].isupper():
				self.for_white_check(row,col)
				


				
			if coins_move_display!=[]:					

				for i ,j  in coins_move_display:
					if loc_img[-5].islower():


						if [i,j] in self.coins_loc_w:
							self.board_box[i][j].config(background='#FF6666',command=lambda i=i,j=j: self.move_coins_another_pos(loc_img,row,col,i,j,coins_move_display))

						else:

							if  (i==7 and loc_img[-5]=='p') or ((row==0 and col==4 and not self.castle_of_black.get()) and  loc_img[-5]=='k' and  i==0 and j==6) or ((row==0 and col==4 and not self.castle_of_white.get()) and loc_img[-5]=='k' and  i==0 and j==2):	
								self.board_box[i][j].config(background='#CC33CC',command=lambda i=i,j=j: self.move_coins_another_pos(loc_img,row,col,i,j,coins_move_display))
							else:
								self.board_box[i][j].config(background='#33CCFF',command=lambda i=i,j=j: self.move_coins_another_pos(loc_img,row,col,i,j,coins_move_display))
					else:
						if [i,j] in self.coins_loc_b:
							self.board_box[i][j].config(background='#FF6666',command=lambda i=i,j=j: self.move_coins_another_pos(loc_img,row,col,i,j,coins_move_display))

						else:
							if  (i==0 and loc_img[-5]=='P') or  ((row==7 and col==4 and  not self.castle_of_white.get()) and  loc_img[-5]=='K' and  i==7 and j==6) or ((row==7 and col==4 and not self.castle_of_white.get()) and loc_img[-5]=='K' and  i==7 and j==2):									
								self.board_box[i][j].config(background='#CC33CC',command=lambda i=i,j=j: self.move_coins_another_pos(loc_img,row,col,i,j,coins_move_display))
							else:
							
								self.board_box[i][j].config(background='#33CCFF',command=lambda i=i,j=j: self.move_coins_another_pos(loc_img,row,col,i,j,coins_move_display))
			else:
				pygame.mixer.music.load('chess_audio/ERROR.mp3')	
				pygame.mixer.music.play()					






		
	def remove_highlighting(self,x=None):
		print('I HAVE CLEAN remove_highlighting',x)
		for row in range(8):

			for col in range(8):
				if (row+col)%2==0:
					box_colour="#DDB88C"
				else:
					box_colour="#A66D4F"

				if  x==None:
					self.board_box[row][col].config(background=box_colour)
				else:
					if self.board_box[row][col]['background']!='red':
						self.board_box[row][col].config(background=box_colour)








	def move_coins_another_pos(self,which_coin_loc,whichr,whichc,from_r,from_c,coridates):
		self.remove_highlighting()
		if [from_r,from_c] in coridates:
			pygame.mixer.music.load('chess_audio/PUTING_THE_PICE.mp3')	
			pygame.mixer.music.play(start=0.5)
			if which_coin_loc[-5]=='K':
				self.castle_of_white.set(False)

				self.king_positions[1]=[from_r,from_c]
			elif which_coin_loc[-5]=='k':
				self.castle_of_black.set(False)
				self.king_positions[0]=[from_r,from_c]

			self.image_locs[from_r][from_c][0],self.image_locs[from_r][from_c][1]=self.image_locs[whichr][whichc][0],self.image_locs[whichr][whichc][1]


			self.board_box[from_r][from_c].config(image=self.image_locs[from_r][from_c][0],
					command=lambda r=from_r,c=from_c,l=self.image_locs[from_r][from_c][1]: self.on_peice_click(r,c,l))
			
			self.image_locs[whichr][whichc][0],self.image_locs[whichr][whichc][1]='',None

			self.board_box[whichr][whichc].config(image=self.image_locs[whichr][whichc][0],
					command=lambda r=whichr,c=whichc,l=self.image_locs[whichr][whichc][1]: self.on_peice_click(r,c,l))
				

			if which_coin_loc[-5].isupper():
				if [whichr,whichc] in self.coins_loc_w:
					self.coins_loc_w.remove([whichr,whichc])
				if [from_r,from_c] in self.coins_loc_b:
					self.coins_loc_b.remove([from_r,from_c])
				self.coins_loc_w.append([from_r,from_c])
			else:
				if [whichr,whichc] in self.coins_loc_b:
					self.coins_loc_b.remove([whichr,whichc])
				if [from_r,from_c] in self.coins_loc_w:
					self.coins_loc_w.remove([from_r,from_c])
				self.coins_loc_b.append([from_r,from_c])

			if which_coin_loc[-5]=='K' and  whichr== 7 and whichc==4 and from_r==7 and from_c==6:
				self.castle_of_white.set(True)
				return self.move_coins_another_pos('R.PNG',7,7,7,5,[[7,5]])

			if which_coin_loc[-5]=='K' and  whichr== 7 and whichc==4 and from_r==7 and from_c==2: 
				self.castle_of_white.set(True)
				return self.move_coins_another_pos('R.PNG',7,0,7,3,[[7,3]])	
	
			if which_coin_loc[-5]=='k' and  whichr== 0 and whichc==4 and from_r==0 and from_c==6: 
				self.castle_of_black.set(True)
				return self.move_coins_another_pos('r.PNG',0,7,0,5,[[0,5]])

			if which_coin_loc[-5]=='k' and  whichr== 0 and whichc==4 and from_r==0 and from_c==2: 
				self.castle_of_black.set(True)
				return self.move_coins_another_pos('r.PNG',0,0,0,3,[[0,3]])		

			
			if  (from_r==7 and which_coin_loc[-5]=='p') or ( from_r==0 and which_coin_loc[-5]=='P'):
				self.pawn_get_promoted(which_coin_loc[-5],from_r,from_c)

			self.alternate_chance()

		

	def alternate_chance(self):
		global coins_move_display
		for row in range(8):
			for col in range(8):
				self.board_box[row][col].config(command=lambda r=row,c=col,
					l=self.image_locs[row][col][1]: self.on_peice_click(r,c,l))

		def i():
			print(self.chance_of.get().upper()+' HAS NO CHANCE')

		if self.chance_of.get()=='white':	
			for r,c in self.coins_loc_b:
				self.board_box[r][c].config(command=lambda:i())
			self.chance_of.set('black')

			x=self.is_king_in_checked(self.king_positions[1][0],
				self.king_positions[1][1],'K',self.coins_loc_b,self.coins_loc_w)

			if x:
				self.king_in_checked.set(True)								
				pygame.mixer.music.load('chess_audio/CHECK-2.mp3')	
				pygame.mixer.music.play()
				self.board_box[self.king_positions[1][0]][self.king_positions[1][1]].config(background='red')
				if self.king_in_checked.get():
					coins_move_display=coins_move.Coins_future_pos(self.image_locs,self.coins_loc_w,self.coins_loc_b,'K',self.king_positions[1][0],self.king_positions[1][1]).identify_coin()
					chk_data=self.white_king_moves(self.king_positions[1][0],self.king_positions[1][1])

					if not coins_move_display:
						wb=self.coins_loc_w.copy()
						for friend in wb:
							our_friend=self.image_locs[friend[0]][friend[1]][1][-5]
							if our_friend!='K':
								coins_move_display=coins_move.Coins_future_pos(self.image_locs,self.coins_loc_w,self.coins_loc_b,our_friend,friend[0],friend[1]).identify_coin().copy()
								self.for_white_check(friend[0],friend[1])
								if coins_move_display!=[]:
									break
						else:
							pygame.mixer.music.load('chess_audio/CHAEK.mp3')	
							pygame.mixer.music.play()					
							self.messageox_when_check(self.king_positions[1][0],self.king_positions[1][1],'Black')
			
			else:
				coins_move_display=coins_move.Coins_future_pos(self.image_locs,self.coins_loc_w,self.coins_loc_b,'K',self.king_positions[1][0],self.king_positions[1][1]).identify_coin()
				chk_data=self.white_king_moves(self.king_positions[1][0],self.king_positions[1][1])

				if not coins_move_display:
					wb=self.coins_loc_w.copy()
					for friend in wb:
						our_friend=self.image_locs[friend[0]][friend[1]][1][-5]
						if our_friend!='K':
							coins_move_display=coins_move.Coins_future_pos(self.image_locs,self.coins_loc_w,self.coins_loc_b,our_friend,friend[0],friend[1]).identify_coin().copy()
							self.for_white_check(friend[0],friend[1])
							if coins_move_display!=[]:
								break
					else:
						x=messagebox.askyesno('GAME OVER MATCH IS DRAW','NOBODY IS WINNER\n\nDo You Want To Play Again')
						if x:
							self.board_frame.destroy()
							f=Board(window)
							f.create_boxes()
							f.alternate_chance()
						else:
							window.destroy()

					self.king_in_checked.set(False)


		else:
			for r,c in self.coins_loc_w:
				self.board_box[r][c].config(command= lambda:i())
				self.chance_of.set('white')

			x=self.is_king_in_checked(self.king_positions[0][0],
				self.king_positions[0][1],'k',self.coins_loc_w,self.coins_loc_b)
			if x:
				self.king_in_checked.set(True)
				pygame.mixer.music.load('chess_audio/CHECK-2.mp3')	
				pygame.mixer.music.play()
				self.board_box[self.king_positions[0][0]][self.king_positions[0][1]].config(background='red')
				if self.king_in_checked.get():
					coins_move_display=coins_move.Coins_future_pos(self.image_locs,self.coins_loc_w,self.coins_loc_b,'k',self.king_positions[0][0],self.king_positions[0][1]).identify_coin()
					chk_data=self.black_king_moves(self.king_positions[0][0],self.king_positions[0][1])
					if not coins_move_display:

						bb=self.coins_loc_b.copy()
						for friend in bb:
							our_friend=self.image_locs[friend[0]][friend[1]][1][-5]
							if our_friend!='k':
								coins_move_display=coins_move.Coins_future_pos(self.image_locs,self.coins_loc_w,self.coins_loc_b,our_friend,friend[0],friend[1]).identify_coin().copy()
								self.for_black_check(friend[0],friend[1])
								if coins_move_display!=[]:
									break
						else:
							pygame.mixer.music.load('chess_audio/CHAEK.mp3')	
							pygame.mixer.music.play()
							self.messageox_when_check(self.king_positions[0][0],self.king_positions[0][1],'White')



			else:
				coins_move_display=coins_move.Coins_future_pos(self.image_locs,self.coins_loc_w,self.coins_loc_b,'k',self.king_positions[0][0],self.king_positions[0][1]).identify_coin()
				chk_data=self.black_king_moves(self.king_positions[0][0],self.king_positions[0][1])
				if coins_move_display==[]:
					bb=self.coins_loc_b.copy()
					for friend in bb:
						our_friend=self.image_locs[friend[0]][friend[1]][1][-5]
						if our_friend!='k':
							coins_move_display=coins_move.Coins_future_pos(self.image_locs,self.coins_loc_w,self.coins_loc_b,our_friend,friend[0],friend[1]).identify_coin().copy()
							self.for_black_check(friend[0],friend[1])
							if coins_move_display!=[]:
								break
					else:
						x=messagebox.askyesno('GAME OVER MATCH IS DRAW','NOBODY IS WINNER\n\nDo You Want To Play Again')
						if x:
							self.board_frame.destroy()
							f=Board(window)
							f.create_boxes()
							f.alternate_chance()
						else:
							window.destroy()

					self.king_in_checked.set(False)






	def pawn_get_promoted(self,which_pawn,loc_r,loc_c):
		global p,h
		x=Board_perce()
		f=x.dict_image_name
		window=Toplevel(self.master)
		window.title('Your Pawn Get Promated !!')
		window.transient(self.master)
		window.grab_set()
		frame_title=Frame(window)
		Label(frame_title,text='What You Want...',font=('Arial Bold',40)).pack()
		frame_title.pack(side=TOP,fill=X)
		frame_chose=Frame(window)

		def x(s):
			window.destroy()

			if which_pawn.islower():
				q=ImageTk.PhotoImage(Image.open(f[s]).resize((71,75)))
				self.image_locs[loc_r][loc_c][0],self.image_locs[loc_r][loc_c][1]=q,f[s]

			else:
				q=ImageTk.PhotoImage(Image.open(f[s.upper()]).resize((71,75)))
				self.image_locs[loc_r][loc_c][0],self.image_locs[loc_r][loc_c][1]=q,f[s.upper()]
			self.board_box[loc_r][loc_c].config(image=self.image_locs[loc_r][loc_c][0])
		h=[]
		vp={'h':'Hourse','q':'Queen','r':'Rook','b':'Bishop'}
		for i in vp:
			if which_pawn.isupper():
				loc=f[i.upper()]
			else:
				loc=f[i]
			framex=Frame(frame_chose)
			q=ImageTk.PhotoImage(Image.open(loc).resize((75,95)))
			h.append(q)
			l1=Label(framex,image=q,bg='white',relief='raised',bd=0)
			l1.pack(side=LEFT,fill=X)
			Radiobutton(framex, text=vp[i],font=('Bold',50), value=i,bd=0,
				indicatoron=0,background='white',activeforeground='black',
				activebackground='yellow',fg='Green',command=lambda s=i:x(s) ).pack(side=LEFT,fill=X,expand=1)
			framex.pack(fill=X,pady=10)


		frame_chose.pack(side=TOP,fill=X)

	def is_king_in_checked(self,king_pos_r,king_pos_c,which_king,foe,frien):

		# WE HAVE TO CHECK append THE POS IN FRIEND AND 
		#CHECK THAT OUR KING POS IS IN FOES MOVES IS YESH WHAT IS NAME 
		#OF THE FOE'S AND WANHT IS LOCTION OF IT'
		friend=frien.copy()
		king_pos=[king_pos_r,king_pos_c]
		d={}
		for ememy_loc in foe:
			our_foe=self.image_locs[ememy_loc[0]][ememy_loc[1]][1][-5]

			our_foe_move=coins_move.Coins_future_pos(self.image_locs,self.coins_loc_w,
				self.coins_loc_b,our_foe,ememy_loc[0],ememy_loc[1]).identify_coin().copy()
			if king_pos in our_foe_move:
				d[tuple(ememy_loc)]=our_foe

		return d



	def for_black_check(self,row,col):
		global coins_move_display
		if  self.king_in_checked.get()!=True:
			self.coins_loc_b.remove([row,col])
			vm1=coins_move_display.copy()
			for i in vm1 :
				self.coins_loc_b.append(i)
				chk_data=self.is_king_in_checked(self.king_positions[0][0],self.king_positions[0][1],'k',self.coins_loc_w,self.coins_loc_b)
				self.coins_loc_b.remove(i)
				if chk_data:
					if i in self.coins_loc_w:
						self.coins_loc_w.remove(i)
						self.coins_loc_b.append(i)
						cd=self.is_king_in_checked(self.king_positions[0][0],self.king_positions[0][1],'k',self.coins_loc_w,self.coins_loc_b)
						self.coins_loc_b.remove(i)
						self.coins_loc_w.append(i)
						if cd:
							coins_move_display.remove(i)

					else:
						coins_move_display.remove(i)

			self.coins_loc_b.append([row,col])



		else:
			self.coins_loc_b.remove([row,col])
			chk_data=self.is_king_in_checked(self.king_positions[0][0],self.king_positions[0][1],'k',self.coins_loc_w,self.coins_loc_b)
			self.coins_loc_b.append([row,col])
			if len(chk_data)>1:
				coins_move_display=[].copy()

			vm1=coins_move_display.copy()
			for item in vm1:
				self.coins_loc_b.append(item)
				
				chk_data=self.is_king_in_checked(self.king_positions[0][0],self.king_positions[0][1],'k',self.coins_loc_w,self.coins_loc_b)
				self.coins_loc_b.remove(item)
				if chk_data:

					if item in self.coins_loc_w:
						self.coins_loc_w.remove(item)
						self.coins_loc_b.append(item)
						cd=self.is_king_in_checked(self.king_positions[0][0],self.king_positions[0][1],'k',self.coins_loc_w,self.coins_loc_b)
						self.coins_loc_b.remove(item)
						self.coins_loc_w.append(item)
						if cd:
							coins_move_display.remove(item)

					else:
						coins_move_display.remove(item)



	def for_white_check(self,row,col):
		global coins_move_display
		if  self.king_in_checked.get()!=True:
			self.coins_loc_w.remove([row,col])
			vm1=coins_move_display.copy()
			for i in vm1 :
				self.coins_loc_w.append(i)
				chk_data=self.is_king_in_checked(self.king_positions[1][0],self.king_positions[1][1],'K',self.coins_loc_b,self.coins_loc_w)
				self.coins_loc_w.remove(i)
				if chk_data:
					if i in self.coins_loc_b:
						self.coins_loc_b.remove(i)
						self.coins_loc_w.append(i)
						cd=self.is_king_in_checked(self.king_positions[1][0],self.king_positions[1][1],'K',self.coins_loc_b,self.coins_loc_w)
						self.coins_loc_w.remove(i)
						self.coins_loc_b.append(i)
						if cd:
							coins_move_display.remove(i)

					else:
						coins_move_display.remove(i)



			self.coins_loc_w.append([row,col])




		else:
			self.coins_loc_w.remove([row,col])
			chk_data=self.is_king_in_checked(self.king_positions[1][0],self.king_positions[1][1],'K',self.coins_loc_b,self.coins_loc_w)
			self.coins_loc_w.append([row,col])
			if len(chk_data)>1:
				coins_move_display=[].copy()


			vm=coins_move_display.copy()
			for item in vm:
				self.coins_loc_w.append(item)
				
				chk_data=self.is_king_in_checked(self.king_positions[1][0],self.king_positions[1][1],'K',self.coins_loc_b,self.coins_loc_w)
				self.coins_loc_w.remove(item)
				if chk_data:

					if item in self.coins_loc_b:
						self.coins_loc_b.remove(item)
						self.coins_loc_w.append(item)
						cd=self.is_king_in_checked(self.king_positions[1][0],self.king_positions[1][1],'K',self.coins_loc_b,self.coins_loc_w)
						self.coins_loc_w.remove(item)
						self.coins_loc_b.append(item)
						if cd:
							coins_move_display.remove(item)

					else:
						coins_move_display.remove(item)	


	def black_king_moves(self,row,col):
		global coins_move_display		
		if ( not self.castle_of_black.get()) and row==0 and col==4 and (not self.king_in_checked.get()) and self.image_locs[0][5][0]=='' and self.image_locs[0][6][0]=='':
			try:
				if self.image_locs[0][7][1][-5]=='r':
					self.coins_loc_b.remove([0,4])
					self.coins_loc_b.append([0,6])

					chk_data=self.is_king_in_checked(0,6,'k',self.coins_loc_w,self.coins_loc_b)
					self.coins_loc_b.remove([0,6])
					self.coins_loc_b.append([0,4])
					if not chk_data:
						coins_move_display.append([0,6])
					else:
						raise Exception
			except:
				pass
		if ( not self.castle_of_black.get()) and row==0 and col==4 and(not self.king_in_checked.get()  and  self.image_locs[0][3][0]==''  and     self.image_locs[0][2][0]=='' and  self.image_locs[0][1][0]=='' ):
			try:
				if self.image_locs[0][0][1][-5]=='r':
					self.coins_loc_b.remove([0,4])
					self.coins_loc_b.append([0,2])


					chk_data=self.is_king_in_checked(0,2,'k',self.coins_loc_w,self.coins_loc_b)
					self.coins_loc_b.remove([0,2])
					self.coins_loc_b.append([0,4])
					if not chk_data:
						coins_move_display.append([0,2])
					else:
						raise Exception				
			except:
				pass						




		vaild_input=coins_move_display.copy()
		for  i in vaild_input:
			self.coins_loc_b.remove([row,col])
			chk_grent=[i[0],i[1]]
			self.coins_loc_b.append(i)
			chk_data=self.is_king_in_checked(chk_grent[0],chk_grent[1],'k',self.coins_loc_w,self.coins_loc_b)
			self.coins_loc_b.remove(i)
			if chk_data:
				coins_move_display.remove(chk_grent)

			if i in self.coins_loc_w:
				self.coins_loc_w.remove(i)
				self.coins_loc_b.append(i)
				chk=self.is_king_in_checked(i[0],i[1],'k',self.coins_loc_w,self.coins_loc_b)
				self.coins_loc_w.append(i)
				self.coins_loc_b.remove(i)
				if chk:
					coins_move_display.remove(i)
			self.coins_loc_b.append([row,col])						


	def white_king_moves(self,row,col):
		global coins_move_display		
		vaild_input=coins_move_display.copy()
		if ( not self.castle_of_white.get()) and row==7 and col==4 and (not self.king_in_checked.get()) and self.image_locs[7][5][0]=='' and self.image_locs[7][6][0]=='':
			try:
				if self.image_locs[7][7][1][-5]=='R':
					self.coins_loc_w.remove([7,4])
					self.coins_loc_w.append([7,6])

					chk_data=self.is_king_in_checked(7,6,'K',self.coins_loc_b,self.coins_loc_w)
					self.coins_loc_w.remove([7,6])
					self.coins_loc_w.append([7,4])
					if not chk_data:
						coins_move_display.append([7,6])						
				else:
					raise Exception
									
			except:
				pass
			
		if ( not self.castle_of_white.get()) and row==7 and col==4 and(not self.king_in_checked.get()  and  self.image_locs[7][3][0]==''  and     self.image_locs[7][2][0]=='' and  self.image_locs[7][1][0]=='' ):
			try:
				if self.image_locs[7][0][1][-5]=='R':
					self.coins_loc_w.remove([7,4])
					self.coins_loc_w.append([7,2])


					chk_data=self.is_king_in_checked(7,2,'K',self.coins_loc_b,self.coins_loc_w)
					self.coins_loc_w.remove([7,2])
					self.coins_loc_w.append([7,4])
					if not chk_data:
						coins_move_display.append([7,2])						
				else:
					raise Exception
									
			except:
				pass




		for  i in vaild_input:
			self.coins_loc_w.remove([row,col])
			self.coins_loc_w.append(i)
			chk_data=self.is_king_in_checked(i[0],i[1],'K',self.coins_loc_b,self.coins_loc_w)
			self.coins_loc_w.remove(i)
			if chk_data!={}:
				coins_move_display.remove(i)

			if i in self.coins_loc_b:

				self.coins_loc_b.remove(i)
				self.coins_loc_w.append(i)
				chk=self.is_king_in_checked(i[0],i[1],'K',self.coins_loc_b,self.coins_loc_w)
				self.coins_loc_b.append(i)
				self.coins_loc_w.remove(i)
				if chk:
					coins_move_display.remove(i)
			self.coins_loc_w.append([row,col])


	def messageox_when_check(self,which_king_r,which_king_c,which_win):
		if which_win=='Black':
			chk_data1=self.is_king_in_checked(which_king_r,which_king_c,'K',self.coins_loc_b,self.coins_loc_w)
		else:
			chk_data1=self.is_king_in_checked(self.king_positions[0][0],self.king_positions[0][1],'k',self.coins_loc_w,self.coins_loc_b)
		for check in chk_data1:
			self.board_box[check[0]][check[1]].config(background='#FF6666')
		x=messagebox.askyesno('GAME OVER CHECKMATE','{} wins\nDo You Want To Play Again'.format(which_win))
		if x:
			self.board_frame.destroy()
			f=Board(window)
			f.create_boxes()
			f.alternate_chance()
		else:
			window.destroy()


	

	



if __name__ == '__main__':
	x=Board(window)
	
	x.create_boxes()
	x.alternate_chance()



window.mainloop()
