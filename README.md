# HistSumm
Code and data for [Summarising Historical Text in Modern Languages](https://arxiv.org/pdf/2101.10759.pdf) (EACL 2021)

## TL;DR
**Historical text summarisation** is a task where documents in historical forms of a language are summarised in the corresponding modern language. We are the first to explore this fascinating and useful direction (using cross-lingual transfer learning). Our repo contains
 - [x] **Testsets** for German and Chinese, annotated by experts
 - [x] Preprocessing code
 - [ ] Trained & aligned embeddings
 - [ ] Neural summariser
 
For more info, please read our paper or create an issue!

## Corpus
Some of the entries may be puzzling. We therefore explain them here
| entry             	| description                                                                    	|
|-------------------	|--------------------------------------------------------------------------------	|
| (de) germanc_file 	| the index of the story in the [GermanC dataset](http://hdl.handle.net/20.500.12024/2544)                               	|
| (de) region       	| historical German has dialects, so it's important to log the geometric sources 	|
| (zh) source       	| via which academic paper did we obtain the piece of Wanli Gazette news         	|
| human_eval_scores 	| annotation scores given by expert validator                                    	|


## Code and model
### Preprocessing
As suggesteded by anonymous reviewers, we release our preprocessings step for reproducibility check as well as to aid future studies on historical language processing. Our code is presented in documented Jupyter Notebooks.

### Embeddings and summariser code
To be released nearer the conference (late April) :eyes:

## About
If you like our project or find it uesful, please give us a :star: and cite us
```
@inproceedings{HistSumm-2021,
    title={Summarising Historical Text in Modern Languages}, 
    author={Xutan Peng and Yi Zheng and Chenghua Lin and Advaith Siddharthan},
    year={2021},
    booktitle = "Proceedings of the 16th Conference of the {E}uropean Chapter of the Association for Computational Linguistics: Volume 1, Long Papers",
    address = "Online",
    publisher = "Association for Computational Linguistics"
}
```
