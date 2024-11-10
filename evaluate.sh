# Description: Evaluate the model on NTU60 dataset.
# Example: bash evaluate.sh on NTU60 dataset 

python main.py \
--config work_dir/ntu/csub/skmixf_241/config.yaml \
--work-dir work_dir/ntu/csub/skmixf_241 --phase test --save-score True \
--weights work_dir/ntu/csub/skmixf_241/runs-95-29735.pt 
--device 0
