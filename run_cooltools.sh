#!/bin/bash
source ~/miniconda3/etc/profile.d/conda.sh
conda activate hic

for i in *_10kb.cool
do
echo $i
file=${i%_10kb.cool}  
coolfile=$file$'_50kb.cool'
cis_expected=$file$'_50kb_cis_expected.tsv'
trans_expected=$file$'_50kb_trans_expected.tsv'
cis_vec=$file$'_50kb_cis'
iinsulation=$file$'_50kb_insulation.tsv'
cis_vecs=$cis_vec$'.cis.vecs.tsv'
saddle=$file$'_50kb_saddle'


dots=$file$'_10kb_dots'
cis_expected_10kb=$file$'_10kb_cis_expected.tsv'
cooler balance $i 
cooltools expected-cis -o $cis_expected_10kb $i 
cooltools dots -o $dots $i $cis_expected_10kb 
cooler coarsen -k 5 -o $coolfile $i 
cooler balance $coolfile 

cooltools expected-cis -o $cis_expected $coolfile 
cooltools expected-trans -o $trans_expected $coolfile 
cooltools eigs-cis --reference-track /bianlab/zuowu/Index/PreL_std_50k.bedGraph -o $cis_vec $coolfile 
cooltools insulation -o $iinsulation $coolfile 
cooltools saddle $coolfile $cis_vecs::E1 $cis_expected -o $saddle --fig pdf --qrange 0.02 0.98 

coolfiles=$file$'_500kb.cool'
cooler coarsen -k 10 -o $coolfiles $coolfile 
cooler balance $coolfiles &

done
