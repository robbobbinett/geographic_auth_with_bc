rm -rf figure_intermediates figure_outputs

mkdir figure_intermediates
mkdir figure_intermediates/local_chains
mkdir figure_intermediates/local_chains/horseshoe
mkdir figure_outputs
mkdir figure_outputs/local_chains
mkdir figure_outputs/local_chains/horseshoe

python3 horseshoe_partition.py

dot -Kfdp -n -Tpdf figure_intermediates/local_chains/horseshoe/union.dot -o figure_outputs/local_chains/horseshoe/union.pdf


declare -a arr
arr=( 0 1 2 3 )
for j in ${arr[@]}; do
	dot -Kfdp -n -Tpdf figure_intermediates/local_chains/horseshoe/$j.dot -o figure_outputs/local_chains/horseshoe/$j.pdf
	dot -Kfdp -n -Tpdf figure_intermediates/local_chains/horseshoe_$j.dot -o figure_outputs/local_chains/horseshoe_$j.pdf
done
