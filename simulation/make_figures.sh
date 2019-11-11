rm -rf figure_intermediates figure_outputs

mkdir figure_intermediates
mkdir figure_intermediates/local_chains
mkdir figure_outputs
mkdir figure_outputs/local_chains

python3 figures.py

commandOutput="$(python3 figure_templates/get_dots_for_chains.py)"

for j in ${commandOutput[@]}; do
	dot -Kfdp -n -Tpdf figure_intermediates/local_chains/$j.dot -o figure_outputs/local_chains/$j.pdf
done
