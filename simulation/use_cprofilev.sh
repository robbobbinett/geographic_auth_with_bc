rm -f profile_output
python3 -m cProfile -o profile_output profile_simulation.py
cprofilev -f profile_output
