# Models

To completely reproduce the results including embeddings recalculation, you will need to download four public models checkpoints used in the paper, set up their corresponding environment, and download the datasets.

### Downloading the models and their source code
If you want to recalculate the embeddings or conduct experiments that require the original models, please download the following models and their source code and put in the `models` folder:
- YaTC: use https://github.com/NSSL-SJTU/YaTC to obtain the source code and [this link](https://drive.google.com/file/d/1wWmZN87NgwujSd2-o5nm3HaQUIzWlv16/view?usp=drive_link) to download the checkpoint (the same link is provided in the YaTC repository). 
  - To create the virtual environment for YaTC, please refer to the [instructions](https://github.com/NSSL-SJTU/YaTC?tab=readme-ov-file#dependency) in the YaTC repository.
- ET-BERT: use https://github.com/linwhitehat/ET-BERT to obtain the source code, checkpoint, and the requirements for the environment.
- netFound: use https://github.com/SNL-UCSB/netfound to obtain the source code for the netFound model. The public checkpoint is available at https://huggingface.co/snlucsb/netFound-640M-base.
- NetMamba: use https://github.com/wangtz19/NetMamba to obtain the source code, checkpoint, and the requirements for the environment.

### Embeddings calculation
After the preparation of the models and environments, use ```src\embeddings_calculation``` to recalculate the embeddings. 