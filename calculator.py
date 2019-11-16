
"""
Calculator
Author: Irfan Chahyadi
Source: github.com/irfanchahyadi/Handwriting-Calculator
"""

import tkinter as tk
from PIL import ImageGrab
import sys
sys.path.insert(0, sys.path[0]+'\\src')
import model


CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 200
LINE_WIDTH = 20

class HandwritingCalculator(object):
	"""Create gui apps for handwriting calculator using tkinter."""

	def __init__(self):
		"""Init for creating gui structure."""
		self.translator = model.HandwritingTranslator()
		self.root = tk.Tk()
		self.root.title('Handwritten Calculator')
		self.c = tk.Canvas(self.root, bg='white', width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
		self.c.grid(row=0, column=0)
		self.v_calculation = tk.StringVar()
		f1 = tk.Frame(self.root, width=CANVAS_WIDTH)
		f1.grid(row=1, column=0, sticky='w')
		self.label = tk.Label(f1, textvariable=self.v_calculation, font=('Courier', 30))
		self.label.grid(row=0, column=0)
		self.v_calculation.set('Right-click for clear')
		self.setup()

	def setup(self):
		"""Setup initial position and binding to mouse movement."""
		self.x_pos = None
		self.y_pos = None
		self.c.bind('<B1-Motion>', self.paint)
		self.c.bind('<ButtonRelease-1>', self.finish_draw)
		self.c.bind('<ButtonRelease-3>', self.reset)
		self.reset(None)
		self.root.mainloop()

	def paint(self, event):
		"""Run when user writing in canvas."""
		if self.x_pos and self.y_pos:
			self.c.create_line(self.x_pos, self.y_pos, event.x, event.y, width=LINE_WIDTH, smooth=tk.TRUE, capstyle=tk.ROUND)
		self.x_pos = event.x
		self.y_pos = event.y

	def reset(self, event):
		"""Delete all."""
		self.c.delete('all')
		self.v_calculation.set('Right-click for clear')

	def finish_draw(self, event):
		"""Run when user done writing single number/symbol."""
		self.x_pos, self.y_pos = None, None
		x1 = self.c.winfo_rootx() + self.c.winfo_x()
		y1 = self.c.winfo_rooty() + self.c.winfo_y()
		x2 = x1 + CANVAS_WIDTH
		y2 = y1 + CANVAS_HEIGHT
		image = ImageGrab.grab((x1,y1,x2,y2)).convert('L')
		# image.save('tes.jpg')
		calculation = self.translator.translate(image)
		self.v_calculation.set(calculation)



if __name__ == '__main__':
	HandwritingCalculator()