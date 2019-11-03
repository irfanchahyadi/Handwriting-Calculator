import numpy as np

def find_image_center(img):
	"""Return tuple, coordinate center of img."""
	m = img / np.sum(np.sum(img))
	dx = np.sum(m, 0)
	dy = np.sum(m, 1)
	cx = int(round(np.sum(dx * np.arange(len(dx))), 0))
	cy = int(round(np.sum(dy * np.arange(len(dy))), 0))
	return cx, cy

def clean_equivalency_dict(d):
	"""Clean equivalency dict from connected component algorithm."""
	for key, val in d.items():
		d[key] = d[val]
	return d

def sort_by_other_list(this_list, by_this_list):
	"""Sort list based on another list."""
	result_list = []
	for cx, x in sorted(zip(by_this_list, this_list)):
		result_list.append(x)
	return result_list