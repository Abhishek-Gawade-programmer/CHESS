import numpy as np
class Coins_future_pos:
	def __init__(self,loc_to_coin,white_pos,black_pos,which_coin,
		postion_of_coin_row,postion_of_coin_col):
		self.coin=which_coin
		self.loc_to_coin=loc_to_coin
		self.white_pos=white_pos
		self.black_pos=black_pos
		self.postion_row=postion_of_coin_row
		self.postion_col=postion_of_coin_col
		self.box_ind=np.array([None,]*64).reshape(8,8)


		self.future_move=[]
		self.choices={
		'p':self.future_move_pawn,
		'h':self.future_move_knight,
		'k':self.future_move_king,
		'q':self.future_move_queen,
		'r':self.future_move_rook,
		'b':self.future_move_bishop}
		self.make_board_indexs()
		# self.is_king_in_check()


	def identify_coin(self):

		x=self.coin.lower()
		action = self.choices.get(x)
		return action()





	def future_move_pawn(self):
		self.future_move=[]
		if self.coin.isupper():
			if [self.postion_row-1,self.postion_col-1] in self.black_pos:
				self.future_move.append([self.postion_row-1,self.postion_col-1])

			if [self.postion_row-1,self.postion_col+1] in self.black_pos:
				self.future_move.append([self.postion_row-1,self.postion_col+1])

			if self.postion_row==6:
				for chances in range(-1,-3,-1):
					y=[self.postion_row+chances,self.postion_col]
					if y in self.black_pos or y in self.white_pos:
						break
					else:
						self.future_move.append(y)
			else:
				y=[self.postion_row-1,self.postion_col]
				if y in self.black_pos or y in self.white_pos:
					pass
				else:
					self.future_move.append(y)

			return self.not_hiting_ours(self.white_pos,self.future_move)

		else:

			if [self.postion_row+1,self.postion_col-1] in self.white_pos:
				self.future_move.append([self.postion_row+1,self.postion_col-1])
			if [self.postion_row+1,self.postion_col+1] in self.white_pos:
				self.future_move.append([self.postion_row+1,self.postion_col+1])
			if self.postion_row==1:
				for chances in range(1,3):
					y=[self.postion_row+chances,self.postion_col]
					if y in self.black_pos or y in self.white_pos:
						break
					else:
						self.future_move.append(y)
			else:
				y=[self.postion_row+1,self.postion_col]
				if y in self.black_pos or y in self.white_pos:
					pass
				else:
					self.future_move.append(y)


			return self.not_hiting_ours(self.black_pos,self.future_move)

	def future_move_knight(self):
		KNIGHT_POSITIONS=[[-2,-1],[-2,1],[-1,-2],[-1,2],[1,-2],[1,2],[2,-1],[2,1]]
		vaild_knight_move=[]
		for chance in KNIGHT_POSITIONS:
			y=[self.postion_row+chance[0],self.postion_col+chance[1]]
			if y in list(np.hstack(self.box_ind)):
				vaild_knight_move.append(y)
		if self.coin.isupper():
			return self.not_hiting_ours(self.white_pos,vaild_knight_move)
		else:
			return self.not_hiting_ours(self.black_pos,vaild_knight_move)

	def future_move_bishop(self):
		def f1(friend,foe,main_diagonal=None):	
			u=main_diagonal		
			main_diagonal= main_diagonal if main_diagonal else  self.box_ind.diagonal()		
			for re,cl in main_diagonal:
				if cl==self.postion_col:
					k=re-self.postion_row
					break
			if u==None:
				given_diagonal=list(self.box_ind.diagonal(k))

			else:
				given_diagonal=list(self.box_ind[::-1,:].diagonal(-k))

			return self.vaild_move_bishop_rook(given_diagonal,friend,foe)


		if self.coin.isupper():
			return f1(self.white_pos,self.black_pos,None)+f1(self.white_pos,self.black_pos,list(self.box_ind[::-1,:].diagonal()))
		else:
			return f1(self.black_pos,self.white_pos,None)+f1(self.black_pos,self.white_pos,list(self.box_ind[::-1,:].diagonal()))

		

	def future_move_king(self):
		
		def greented_vaild_king_move1(king_moves,friend,foe):
			g1=self.not_hiting_ours(friend,king_moves)
			return g1
			# print('VAILD OUTCOMES',g1)
			# print('*'*20)
			# total_list=[]
			# print('for',foe)
			# print('*'*20)
			# for ememy_loc in foe:
			# 	x=self.loc_to_coin[ememy_loc[0]][ememy_loc[1]][1][-5]
			# 	self.postion_row=ememy_loc[0]
			# 	self.postion_col=ememy_loc[1]
			# 	c=self.identify_coin(x).copy()
			# 	print(x,ememy_loc,c)
			# 	total_list.extend(c)


			# for posiable in g1:
			# 	if posiable in total_list:
			# 		print(posiable,'REMOVED')
			# 		g1.remove(posiable)
			# print('TOTAL OUTCOMES',total_list)
			# print('*'*20)
			# print('POSSSABLE OUTCOMES',g1)



							
				# else:
				# 	print('HSEJGYTB')
				# print(self.coin,self.identify_coin())
			
			# 	for ememy_loc1 in  self.identify_coin():
			# 		if ememy_loc1 in g1:
			# 			g1.remove(ememy_loc1)
			# return g1
			# return []







		KNIG_POSITIONS=[[-1,-1],[0,-1],[1,-1],[-1,0],[1,0],[-1,1],[0,1],[1,1]]
		vaild_king_move=[]

		for chance in KNIG_POSITIONS:
			y=[self.postion_row+chance[0],self.postion_col+chance[1]]
			if y in list(np.hstack(self.box_ind)):	
				vaild_king_move.append(y)
		






		if self.coin.isupper():
			return greented_vaild_king_move1(vaild_king_move,self.white_pos,self.black_pos)


		else:
			return greented_vaild_king_move1(vaild_king_move,self.black_pos,self.white_pos)


	def future_move_rook(self):
		row=self.box_ind[self.postion_row]
		col=self.box_ind.T[self.postion_col]

		if self.coin.isupper():
			return self.vaild_move_bishop_rook(list(row),self.white_pos,self.black_pos)+self.vaild_move_bishop_rook(list(col),self.white_pos,self.black_pos)
		else:
			return self.vaild_move_bishop_rook(list(row),self.black_pos,self.white_pos)+self.vaild_move_bishop_rook(list(col),self.black_pos,self.white_pos)

	def future_move_queen(self):
		return self.future_move_rook() +self.future_move_bishop()
		


	def not_hiting_ours(self,ous_list,hittng_list):
	 	m=[]
	 	for i in hittng_list:
	 		if i not in ous_list:
	 			m.append(i)
	
	 	return m

	def vaild_move_bishop_rook(self,row_or_col,friend,foe):
		left_move=[];right_move=[]
		rook_index=row_or_col.index([self.postion_row,self.postion_col])
		future_move_left=row_or_col[:rook_index]
		future_move_right=row_or_col[rook_index+1:]
		for left in future_move_left[::-1]:
			if left in foe:
				left_move.append(left)
				break
			elif left in friend:
				break
			else:
				left_move.append(left)
		for right in future_move_right:
			if right in foe:
				right_move.append(right)
				break
			elif right in friend:
				break
			else:
				right_move.append(right)



		return self.not_hiting_ours(friend,right_move+left_move)




	def make_board_indexs(self):
	 	self.box_ind=np.array([None,]*64).reshape(8,8)
	 	for row in range(8):
	 		for col in range(8):
	 			self.box_ind[row][col]=[row,col]
	# def is_king_in_check(self,king_r=None,king_c=None):
	# 	def greented_vaild_king_move(king_move,foe):
	# 		print('*'*20)
	# 		total_list=[]
	# 		print('*'*20)
	# 		for ememy_loc in foe:
	# 			x=self.loc_to_coin[ememy_loc[0]][ememy_loc[1]][1][-5]
	# 			# self.postion_row=ememy_loc[0]
	# 			# self.postion_col=ememy_loc[1]
	# 			print(x,ememy_loc[0],ememy_loc[1])
	# 			print('*'*20)
	# 			c=self.identify_coin(x,ememy_loc[0],ememy_loc[1]).copy()
	# 			print('POSSSABLE MOBVES',c)
	# 			total_list.extend(c)
	# 		if king_move in total_list :
	# 			print('THIS IS CHECK NOBODY MOVE')
	# 		else:
	# 			print('THIS not CHECK ANYONE CAN MOVE')
	# 		# return self.identify_coin()



		# if self.coin.islower():
		# 	#CALL WHITE
		# 	if not(king_r or king_c):
		# 		greented_vaild_king_move(self.king_b_w[1],self.black_pos)



		# else:
		# 	#CALL BLACK
		# 	if not(king_r or king_c):
		# 		greented_vaild_king_move(self.king_b_w[0],self.white_pos)

		

		



		
