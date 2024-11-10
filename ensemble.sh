# Ensemble the predictions of different models.
# Example of NTU60 CS setting

###################  60cs   ################### 
python ensemble.py --dataset ntu/xsub  \
--joint-dir  work_dir/ntu/csub/skfreq_8joint \
--bone-dir  work_dir/ntu/csub/skfreq_8motion \
--joint-motion-dir work_dir/ntu/csub/skfreq_1joint \
--bone-motion-dir work_dir/ntu/csub/skfreq_1motion \
--joint-k2-dir work_dir/ntu/csub/skfreq_2joint \
--joint-motion-k2-dir  work_dir/ntu/csub/skfreq_2motion






