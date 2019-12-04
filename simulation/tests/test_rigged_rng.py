from rigged_rng import make_rigged_rng

def test_rigged_rng():
	# Test basic functionality
	rigged_rng = make_rigged_rng([0, 1, 0, 3])
	assert rigged_rng() == 0
	assert rigged_rng() == 1
	assert rigged_rng() == 0
	assert rigged_rng() == 3
	try:
		rigged_rng()
		assert(False)
	except IndexError:
		pass
	except:
		assert(False)

	# Test interleaving rngs
	rigged_rng = make_rigged_rng([10, 11, 12])
	other_rng = make_rigged_rng([20, 21, 22])
	assert rigged_rng() == 10
	assert other_rng() == 20
	assert rigged_rng() == 11
	assert other_rng() == 21
	assert rigged_rng() == 12
	assert other_rng() == 22

	# Test appending terms to the given list
	l = [1]
	rigged_rng = make_rigged_rng(l)
	rigged_rng()
	l.append(5)
	assert rigged_rng() == 5
