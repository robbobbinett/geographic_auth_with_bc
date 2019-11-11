rm -rf figure_intermediates

mkdir figure_intermediates
mkdir figure_intermediates/local_chains

python3 figures.py

dot -Kfdp -n -Tpdf dec$j.dot -o dec$j.pdf
