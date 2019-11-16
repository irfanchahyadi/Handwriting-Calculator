
"""
Add Dataset
Author: Irfan Chahyadi
Source: github.com/irfanchahyadi/Handwriting-Calculator
"""

import tkinter as tk
from PIL import ImageGrab
import model
import pickle


CANVAS_WIDTH = 200
CANVAS_HEIGHT = 200
LINE_WIDTH = 20
PICKLE_FILE = 'dataset/data.pickle'

class AddDataset(object):
	"""Add sample dataset manually."""

	def __init__(self):
		"""Init for creating gui structure."""
		self.root = tk.Tk()
		self.root.title('Add Dataset')
		self.saved_imgs = self.load_imgs()
		f1 = tk.Frame(self.root, width=CANVAS_WIDTH)
		f2 = tk.Frame(self.root, width=CANVAS_WIDTH)
		f1.grid(row=0, column=0, sticky='w')
		f2.grid(row=3, column=0, sticky='w')
		self.c = tk.Canvas(self.root, bg='white', width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
		self.c.grid(row=1, column=0)
		self.symbols = ['+', '-', 'x', '/', '(',  ')', ',']
		self.idx_v = tk.StringVar(self.root)
		self.idx_v.set(len(self.saved_imgs['label']))
		self.idx = int(self.idx_v.get()) % len(self.symbols)
		self.symbol = tk.StringVar(self.root)
		self.symbol.set(self.symbols[self.idx])
		label = tk.Label(f1, text=' Symbol: ', font=('Courier', 15))
		label2 = tk.Label(f1, textvariable=self.symbol, font=('Courier', 15, 'bold'))
		label3 = tk.Label(f1, text=' ', font=('Courier', 15))
		label4 = tk.Label(f2, text='Total: ', font=('Courier', 15))
		label5 = tk.Label(f2, textvariable=self.idx_v, font=('Courier', 15))
		self.button = tk.Button(f1, text='DONE', command=self.done)
		label.grid(row=0, column=0)
		label2.grid(row=0, column=1)
		label3.grid(row=0, column=2)
		label4.grid(row=0, column=0)
		label5.grid(row=0, column=1)
		self.button.grid(row=0, column=3)
		self.setup()

	def setup(self):
		"""Setup initial position and binding to mouse movement."""
		self.x_pos = None
		self.y_pos = None
		self.c.bind('<B1-Motion>', self.paint)
		self.c.bind('<ButtonRelease-1>', self.finish_draw)
		self.c.bind('<ButtonRelease-3>', self.reset)
		self.reset(None)
		self.translator = model.HandwritingTranslator(0)
		self.root.protocol("WM_DELETE_WINDOW", self.save_imgs)
		self.root.mainloop()
	
	def load_imgs(self):
		"""Load previous image data if exists."""
		try:
			with open(PICKLE_FILE, 'rb') as f:
				data = pickle.load(f)
		except FileNotFoundError:
			print(PICKLE_FILE, 'not found. Creating new file.')
			data = {'label': [], 'img': []}
		return data
	
	def save_imgs(self):
		"""Save image data after closing window."""
		with open(PICKLE_FILE, 'wb') as f:
				pickle.dump(self.saved_imgs, f)
		self.root.destroy()

	def done(self):
		"""Change symbol and save current image."""
		x1 = self.c.winfo_rootx()
		y1 = self.c.winfo_rooty()
		x2 = x1 + CANVAS_WIDTH
		y2 = y1 + CANVAS_HEIGHT
		image = ImageGrab.grab((x1,y1,x2,y2)).convert('L')
		img = self.translator.prep(image)
		self.saved_imgs['label'].append(self.symbol.get())
		self.saved_imgs['img'].append(img)
		count = len(self.saved_imgs['label'])
		print(count)
		self.idx_v.set(int(self.idx_v.get()) + 1)
		self.idx = int(self.idx_v.get()) % len(self.symbols)
		self.symbol.set(self.symbols[self.idx])
		self.x_pos, self.y_pos = None, None
		self.reset(None)

	def paint(self, event):
		"""Run when user writing in canvas."""
		if self.x_pos and self.y_pos:
			self.c.create_line(self.x_pos, self.y_pos, event.x, event.y, width=LINE_WIDTH, smooth=tk.TRUE, capstyle=tk.ROUND)
		self.x_pos = event.x
		self.y_pos = event.y

	def reset(self, event):
		"""Delete all."""
		self.c.delete('all')

	def finish_draw(self, event):
		"""Run when user release left click button.."""
		self.x_pos, self.y_pos = None, None


if __name__ == '__main__':
	AddDataset()