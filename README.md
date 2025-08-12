# Frequency Guidance Matters: Skeletal Action Recognition by Frequency-Aware Mixed Transformer [ACM MM 2024]
[Wenhan Wu](https://sites.google.com/view/wenhanwu/%E9%A6%96%E9%A1%B5), [Ce Zheng](https://zczcwh.github.io/), [Zihao Yang](https://openreview.net/profile?id=~Zihao_Yang7), [Srijan Das](https://srijandas07.github.io/), [Chen Chen](https://www.crcv.ucf.edu/chenchen/), [Aidong Lu ](https://webpages.charlotte.edu/alu1/)

[![Website shields.io](https://img.shields.io/website?url=http%3A//poco.is.tue.mpg.de)](https://wenhanwu95.github.io/FreqMixFormer.github.io/)  [![arXiv](https://img.shields.io/badge/arXiv-2407.12322-00ff00.svg)](https://arxiv.org/abs/2407.12322)

## Abstract
Recently, transformers have demonstrated great potential for modeling long-term dependencies from skeleton sequences and thereby gained ever-increasing attention in skeleton action recognition. However, the existing transformer-based approaches heavily rely on the naive attention mechanism for capturing the spatiotemporal features, which falls short in learning discriminative representations that exhibit similar motion patterns. To address this challenge, we introduce the Frequency-aware Mixed Transformer (FreqMixFormer), specifically designed for recognizing similar skeletal actions with subtle discriminative motions. First, we introduce a frequency-aware attention module to unweave skeleton frequency representations by embedding joint features into frequency attention maps, aiming to distinguish the discriminative movements based on their frequency coefficients. Subsequently, we develop a mixed transformer architecture to incorporate spatial features with frequency features to model the comprehensive frequency-spatial patterns. Additionally, a temporal transformer is proposed to extract the global correlations across frames. Extensive experiments show that FreqMiXFormer outperforms SOTA on 3 popular skeleton action recognition datasets, including NTU RGB+D, NTU RGB+D 120, and NW-UCLA datasets. 

## Motivation
![motivation](imgs/fig1.png)
The overall design of our Frequency-aware Mixed Transformer. Our FreqMixFormer model overcomes the limitations of traditional transformer-based methods, which cannot effectively recognize confusing actions such as reading and writing due to the straightforward process of skeleton sequences. As highlighted with the colored boxes, the FreqMixFormer introduces the frequency domain and extracts high-frequency features, which often indicate subtle and dynamic movements (red), and low-frequency features, which are associated with slow and steady movements (blue). These features are then fused with spatial features. Our results demonstrate that the integrated frequency-spatial features significantly improve the model's capability to discern discriminative joint correlations.

## Our Approach
![Approach](imgs/fig2.png)
We propose a Frequency-aware Attention Block (FAB) to investigate frequency features within skeletal sequences. A frequency operator is specifically designed to improve the learning of frequency coefficients, thereby enhancing the ability to capture discriminative correlations among joints.
Consequently, we introduce the Frequency-aware Mixed Transformer (FreqMixFormer) to extract frequency-spatial joint correlations. The model incorporates a temporal transformer designed to enhance its ability to capture temporal features across frames.

## Results on popular datasets
![resuls](imgs/result.png)

## Latest Updates:
* We proposed a unified lightweight spatio-temporal transformer framework named UniSTFormer, which achieves a superior balance between accuracy and efficiency. The paper and codes are coming soon 2025/8/12
* FreqMixFormerV2 (A lightweight version of FreqMixFormer) is accepted by The 19th IEEE International Conference on Automatic Face and Gesture Recognition (FG 2025) 2024/12/13
* Codes updated 2024/11/10
* Create the GitHub repository and project website on 2024/7/18
* Preprint paper is available on arXiv 2024/7/18

## Download datasets
**NTU RGB+D 60 and 120**

1. Request dataset: https://rose1.ntu.edu.sg/dataset/actionRecognition
2. Download the skeleton-only datasets:  
    i. ```nturgbd_skeletons_s001_to_s017.zip``` (NTU RGB+D 60)  
    ii. ```nturgbd_skeletons_s018_to_s032.zip``` (NTU RGB+D 120)  
    iii. Extract above files to ```./data/nturgbd_raw```  

**NW-UCLA**

1. Download dataset from [here](https://drive.google.com/file/d/1wWhgqMEQlrCKcJHu6W72Zk_iloS7_JJw/view?usp=share_link)
2. Move ```all_sqe``` to ```./data/NW-UCLA```


## NTU Data Processing
### Directory Structure

Put downloaded data into the following directory structure:
~~~
  - NW-UCLA/
    - all_sqe
      ... # raw data of NW-UCLA
  - ntu/
  - ntu120/
  - nturgbd_raw/
    - nturgb+d_skeletons/     # from `nturgbd_skeletons_s001_to_s017.zip`
      ...
    - nturgb+d_skeletons120/  # from `nturgbd_skeletons_s018_to_s032.zip`
      ...
~~~

### Generating Data

+ Generate NTU RGB+D 60 or NTU RGB+D 120 dataset:
~~~
 cd ./data/ntu # or cd ./data/ntu120
 # Get skeleton of each performer
 python get_raw_skes_data.py
 # Remove the bad skeleton 
 python get_raw_denoised_data.py
 # Transform the skeleton to the center of the first frame
 python seq_transformation.py
~~~

## Training & Testing
### Training
+ Find the training commends in train.sh 
### Testing
+ Find the training commends in testing.sh  
### Ensemble
+ Find the training commends in ensemble.sh

## Citation
If you find this code useful for your research, please consider citing the following paper:

```bibtex

@inproceedings{wu2024frequencyguidancemattersskeletal,
  author = {Wenhan Wu and Ce Zheng and Zihao Yang and Chen Chen and Srijan Das and Aidong Lu},
  title = {Frequency Guidance Matters: Skeletal Action Recognition by Frequency-Aware Mixed Transformer},
  booktitle = {ACM Multimedia 2024},
  year = {2024}
}
```

## Acknowledgements
The code is mainly based on [Skeleton-MixFormer](https://github.com/ElricXin/Skeleton-MixFormer).
The data processing is borrowed from [CTR-GCN](https://github.com/Uason-Chen/CTR-GCN).
Thanks for their amazing work!  

## Contact
For any questions, feel free to create a new issue or contact:
```
Wenhan Wu: wwu25@uncc.edu
```
