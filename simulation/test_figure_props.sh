rm -rf figure_intermediates test_outputs

mkdir figure_intermediates
mkdir figure_intermediates/local_chains
mkdir figure_intermediates/local_chains/small_world
mkdir test_outputs
mkdir test_outputs/local_chains
mkdir test_outputs/local_chains/small_world
mkdir test_outputs/global_chains

python3 validate_figure_props.py

commandOutput="$(python3 figure_templates/get_dots_for_chains.py)"

for j in ${commandOutput[@]}; do
	dot -Kfdp -n -Tpdf figure_intermediates/local_chains/$j.dot -o test_outputs/local_chains/$j.pdf
done
