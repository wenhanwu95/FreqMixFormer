
##################################  60CS ################################# 
python main.py \
--config config/nturgbd-cross-subject/joint.yaml \
--work-dir work_dir/ntu/csub/skmixf_joint\
--device 0 1

##################################  60CV  ################################# 

python main.py \
--config config/nturgbd-cross-view/joint.yaml \
--work-dir work_dir/ntu/cview/skmixf_joint \
--device 2 3


##################################  120CSUB  ################################# 
python main.py \
--config config/nturgbd120-cross-subject/joint.yaml \
--work-dir work_dir/ntu120/csub/skmixf_joint  \
--device 4 5


##################################  120CSET  ################################# 
python main.py \
--config config/nturgbd120-cross-set/joint.yaml \
--work-dir work_dir/ntu120/cset/skmixf_joint  \
--device 6 7

##################################  UCLA  #################################     
python main.py \
--config config/ucla/default.yaml \
--work-dir work_dir/ucla/skmixf_joint  \
--device 0 1 
