import numpy as np
from PIL import ImageTk,Image
class Board_perce:
	def __init__(self):
		self.dict_image_name={}

		self.imgs_box=np.array([None,]*64).reshape(8,8)
		self.dict_image_name_assg()
		self.changepics()
		

	def dict_image_name_assg(self):
		self.t1={
		'P':'IMGS/classic/white/P.png',
		'H':'IMGS/classic/white/H.png',
		'K':'IMGS/classic/white/K.png',
		'Q':'IMGS/classic/white/Q.png',
		'R':'IMGS/classic/white/R.png',
		'B':'IMGS/classic/white/B.png',
		'p':'IMGS/classic/black/p.png',
		'h':'IMGS/classic/black/h.png',
		'k':'IMGS/classic/black/k.png',
		'q':'IMGS/classic/black/q.png',
		'r':'IMGS/classic/black/r.png',
		'b':'IMGS/classic/black/b.png',
		}

		self.t2={
		'P':'IMGS/white/P.png',
		'H':'IMGS/white/H.png',
		'K':'IMGS/white/K.png',
		'Q':'IMGS/white/Q.png',
		'R':'IMGS/white/R.png',
		'B':'IMGS/white/B.png',
		'p':'IMGS/black/p.png',
		'h':'IMGS/black/h.png',
		'k':'IMGS/black/k.png',
		'q':'IMGS/black/q.png',
		'r':'IMGS/black/r.png',
		'b':'IMGS/black/b.png',
		}









		# self.dict_image_name['P'].save('IMGS/black/b.png','jpeg')


	def reset_board(self):
		for row in range(8):
			for col in range(8):
				if row==6:
					# pass
					self.imgs_box[row][col]=self.dict_image_name['P']
				elif row==1:
					self.imgs_box[row][col]=self.dict_image_name['p']
				elif row==7:
					if col==0 or col==7:
						self.imgs_box[row][col]=self.dict_image_name['R']
					elif col==1 or col==6:
						self.imgs_box[row][col]=self.dict_image_name['H']
					elif col==2 or col==5:
						self.imgs_box[row][col]=self.dict_image_name['B']
					elif col==4:
						self.imgs_box[row][col]=self.dict_image_name['K']
					else:
						self.imgs_box[row][col]=self.dict_image_name['Q']
				elif row==0:
					if col==0 or col==7:
						self.imgs_box[row][col]=self.dict_image_name['r']
					elif col==1 or col==6:
						self.imgs_box[row][col]=self.dict_image_name['h']
					elif col==2 or col==5:
						self.imgs_box[row][col]=self.dict_image_name['b']
					elif col==4:
						self.imgs_box[row][col]=self.dict_image_name['k']
					else:
						self.imgs_box[row][col]=self.dict_image_name['q']
		return self.imgs_box



		
	def changepics(self,which_theme=None):
		if not which_theme:
			self.dict_image_name=self.t1
		else:
			self.dict_image_name=self.t2


	def change_pics_runtime(self,imgs_loctions,all_pices):
		self.changepics('yt')
		for row,col in all_pices:
			self.imgs_box[row][col]=self.dict_image_name[imgs_loctions[row][col][1][-5]]

		return self.imgs_box



		
		
		
		
		
if __name__ == '__main__':
	x=Board_perce()
	print(x.reset_board())
	# x.move_piece(0,2,3,3)




	# def reset_board(self):
	# 	for row in range(8):
	# 		for col in range(8):
	# 			if row==6:
	# 				# pass
	# 				self.imgs_box[row][col]=self.dict_image_name['P']
	# 			elif row==1:
	# 				self.imgs_box[row][col]=self.dict_image_name['p']
	# 			elif row==7:
	# 				if col==0 or col==7:
	# 					self.imgs_box[row][col]=self.dict_image_name['R']
	# 				elif col==1 or col==6:
	# 					self.imgs_box[row][col]=self.dict_image_name['H']
	# 				elif col==2 or col==5:
	# 					self.imgs_box[row][col]=self.dict_image_name['B']
	# 				elif col==4:
	# 					self.imgs_box[row][col]=self.dict_image_name['K']
	# 				else:
	# 					self.imgs_box[row][col]=self.dict_image_name['Q']
	# 			elif row==0:
	# 				if col==0 or col==7:
	# 					self.imgs_box[row][col]=self.dict_image_name['r']
	# 				elif col==1 or col==6:
	# 					self.imgs_box[row][col]=self.dict_image_name['h']
	# 				elif col==2 or col==5:
	# 					self.imgs_box[row][col]=self.dict_image_name['b']
	# 				elif col==4:
	# 					self.imgs_box[row][col]=self.dict_image_name['k']
	# 				else:
	# 					self.imgs_box[row][col]=self.dict_image_name['q']
	# 	return self.imgs_box















# P=Image.open(r'IMGS\white\P.png').resize((78,78))
# H=Image.open(r'IMGS\white\H.png').resize((78,78))
# K=Image.open(r'IMGS\white\K.png').resize((78,78))
# Q=Image.open(r'IMGS\white\Q.png').resize((78,78))
# R=Image.open(r'IMGS\white\R.png').resize((78,78))
# B=Image.open(r'IMGS\white\B.png').resize((78,78))









