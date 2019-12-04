def make_rigged_rng(number_list):
	"""
	Returns a function which walks through the elements of the given number list.
	Throws an IndexError if it runs out of elements.
	"""
	i = 0
	def get_next_number():
		nonlocal i
		i += 1
		return number_list[i-1]
	return get_next_number
