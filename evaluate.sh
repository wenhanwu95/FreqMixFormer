# Example: Evaluate the model on NTU60 dataset.
# Change the commands depending on your evaluation

python main.py \
--config work_dir/ntu/csub/skfreq/config.yaml \
--work-dir work_dir/ntu/csub/skfreq --phase test --save-score True \
--weights work_dir/ntu/csub/skfreq/runs-95-29735.pt 
--device 0
