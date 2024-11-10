# Example: Evaluate the model on NTU60 dataset.
# Change the commands depending on your evaluation

python main.py \
--config work_dir/ntu/csub/skmixf/config.yaml \
--work-dir work_dir/ntu/csub/skmixf --phase test --save-score True \
--weights work_dir/ntu/csub/skmixf/runs-95-29735.pt 
--device 0
