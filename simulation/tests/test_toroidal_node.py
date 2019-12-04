import math
from toroidal_node import *

def test_toroidal_distances():
	sqrt2 = math.sqrt(2)

	assert math.isclose( toroidal_distance(0.1, 0.1, 0.1, 0.1), 0 )
	assert math.isclose( toroidal_distance(0.1, 0.1, 0.1, 0.9), 0.2 )
	assert math.isclose( toroidal_distance(0.1, 0.1, 0.9, 0.9), 0.2*sqrt2 )
	assert math.isclose( toroidal_distance(0.1, 0.1, 0.9, 0.1), 0.2 )

	assert math.isclose( toroidal_distance(0.1, 0.9, 0.1, 0.1), 0.2 )
	assert math.isclose( toroidal_distance(0.1, 0.9, 0.1, 0.9), 0 )
	assert math.isclose( toroidal_distance(0.1, 0.9, 0.9, 0.9), 0.2 )
	assert math.isclose( toroidal_distance(0.1, 0.9, 0.9, 0.1), 0.2*sqrt2 )

	assert math.isclose( toroidal_distance(0.9, 0.9, 0.1, 0.1), 0.2*sqrt2 )
	assert math.isclose( toroidal_distance(0.9, 0.9, 0.1, 0.9), 0.2 )
	assert math.isclose( toroidal_distance(0.9, 0.9, 0.9, 0.9), 0 )
	assert math.isclose( toroidal_distance(0.9, 0.9, 0.9, 0.1), 0.2 )

	assert math.isclose( toroidal_distance(0.9, 0.1, 0.1, 0.1), 0.2 )
	assert math.isclose( toroidal_distance(0.9, 0.1, 0.1, 0.9), 0.2*sqrt2 )
	assert math.isclose( toroidal_distance(0.9, 0.1, 0.9, 0.9), 0.2 )
	assert math.isclose( toroidal_distance(0.9, 0.1, 0.9, 0.1), 0 )

	assert math.isclose( toroidal_distance(0.0, 0.0, 0.0, 0.0), 0 )
	assert math.isclose( toroidal_distance(0.0, 0.0, 0.0, 0.1), 0.1 )
	assert math.isclose( toroidal_distance(0.0, 0.0, 0.1, 0.1), 0.1*sqrt2 )
	assert math.isclose( toroidal_distance(0.0, 0.0, 0.1, 0.0), 0.1 )

test_toroidal_distances()
