from rigged_rng import make_rigged_rng

def test_rigged_rng():
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

	rigged_rng = make_rigged_rng([10, 11, 12])
	other_rng = make_rigged_rng([20, 21, 22])
	assert rigged_rng() == 10
	assert other_rng() == 20
	assert rigged_rng() == 11
	assert other_rng() == 21
	assert rigged_rng() == 12
	assert other_rng() == 22

test_rigged_rng()
