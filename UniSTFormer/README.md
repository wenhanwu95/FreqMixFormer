# [UniSTFormer: Unified Lightweight Spatio-Temporal Transformer for Skeleton-based Action Recognition](https://www.arxiv.org/abs/2508.08944)
[Wenhan Wu](https://sites.google.com/view/wenhanwu/%E9%A6%96%E9%A1%B5), [Zhishuai Guo](https://zhishuaiguo.github.io/), [Chen Chen](https://www.crcv.ucf.edu/chenchen/), [Aidong Lu](https://webpages.charlotte.edu/alu1/)

## Abstract
Skeleton-based action recognition (SAR) has achieved impressive progress with transformer architectures. However, existing methods often rely on complex module compositions and heavy designs, leading to increased parameter counts, high computational costs, and limited scalability. In this paper, we propose a unified spatio-temporal lightweight transformer framework that integrates spatial and temporal modeling within a single attention module, eliminating the need for separate temporal modeling blocks. This approach reduces redundant computations while preserving temporal awareness within the spatial modeling process. Furthermore, we introduce a simplified multi-scale pooling fusion module that combines local and global pooling pathways to enhance the model’s ability to capture fine-grained local movements and overarching global motion patterns. Extensive experiments on benchmark datasets demonstrate that our lightweight model achieves a superior balance between accuracy and efficiency, reducing parameter complexity by over 58% and lowering computational cost by over 60% compared to state-of-the-art transformer-based baselines, while maintaining competitive recognition performance.

## Overall Performance
<img src="imgs/fig1-1.png" width="500">

## Baseline
UniSTFormer is developed on top of [Skeleton-MixFormer](https://github.com/ElricXin/Skeleton-MixFormer) and can be run under the same settings as [FreqMixFormer](https://github.com/wenhanwu95/FreqMixFormer.github.io).

