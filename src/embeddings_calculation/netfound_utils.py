import os
from datasets import load_dataset
import torch
from torch.utils.data import DataLoader
from transformers import Trainer, TrainingArguments
import torch
import torch.nn
import threading
from collections import defaultdict

def load_model(path: str, tcpoptions: bool = False, device="cuda"):
    os.chdir("../models/netFound/src/train")
    from NetfoundConfig import NetFoundLarge, NetFoundTCPOptionsConfig
    from NetFoundModels import NetfoundFinetuningModel

    config = NetFoundTCPOptionsConfig() if tcpoptions else NetFoundLarge()
    return NetfoundFinetuningModel.from_pretrained(path, config=config, ignore_mismatched_sizes=True).to(torch.device(device))



def load_data(path, model, tcpoptions: bool = False, batch_size = 32, map_labels_c=None):
    os.chdir("../models/netFound/src/train")
    from NetFoundModels import NetFoundLanguageModelling, NetfoundFinetuningModel, NetFoundBase
    from NetfoundConfig import NetFoundLarge, NetFoundTCPOptionsConfig
    from NetfoundTokenizer import NetFoundTokenizer
    from NetFoundDataCollator import DataCollatorForFlowClassification
    from NetFoundTrainer import NetfoundTrainer



    tdataset = load_dataset("arrow", data_dir=path, split="train", cache_dir=None, streaming=True)
    total_bursts_train = defaultdict(lambda: 0)
    tdataset = tdataset.add_column("total_bursts", total_bursts_train)
    
    def map_labels(example):
        example["labels"] = [int(x) for x in example["labels"]]
        return example
    
    if map_labels_c is not None:
        map_labels = map_labels_c 
    tdataset = tdataset.map(map_labels, batched=True) 
    
    config = NetFoundTCPOptionsConfig() if tcpoptions else NetFoundLarge()
    config.pretraining = False
    tokenizer = NetFoundTokenizer(config=config)
    
    def preprocess_function(examples):
        return tokenizer(examples)

    tdataset = tdataset.map(preprocess_function, batched=True)
    
    training_args = TrainingArguments(
        output_dir="./results",
        per_device_train_batch_size=64,
        per_device_eval_batch_size=64,
        max_steps=1e6,
        dataloader_num_workers=32,
        dataloader_prefetch_factor=4,
    )
    
    trainer = NetfoundTrainer(
        model=model,
        args=training_args,
        train_dataset=tdataset,
        eval_dataset=tdataset,
        tokenizer=tokenizer,
        data_collator=DataCollatorForFlowClassification(config.max_burst_length),
    )
    
    return trainer.get_train_dataloader()

def forward_features(model, batch):
    with torch.no_grad():
        batch['position_ids'] = torch.arange(
                batch['input_ids'].size(1),
                device=batch['input_ids'].device
            ).unsqueeze(0).expand(batch['input_ids'].size(0), -1)

        output = model.base_transformer(
            input_ids=batch['input_ids'].to(model.device),
            attention_mask=batch['attention_mask'].to(model.device),
            position_ids=batch['position_ids'].to(model.device),
            direction=batch['direction'].to(model.device),
            iats=batch['iats'].to(model.device),
            bytes=batch['bytes'].to(model.device),
            return_dict=True,
            pkt_count=batch['pkt_count'].to(model.device),
            protocol=batch['protocol'].to(model.device),
        ).last_hidden_state
        return torch.mean(output, 1).cpu()

def forward_features_first_token(model, batch):
    with torch.no_grad():
        batch['position_ids'] = torch.arange(
                batch['input_ids'].size(1),
                device=batch['input_ids'].device
            ).unsqueeze(0).expand(batch['input_ids'].size(0), -1)

        output = model.base_transformer(
            input_ids=batch['input_ids'].to(model.device),
            attention_mask=batch['attention_mask'].to(model.device),
            position_ids=batch['position_ids'].to(model.device),
            direction=batch['direction'].to(model.device),
            iats=batch['iats'].to(model.device),
            bytes=batch['bytes'].to(model.device),
            return_dict=True,
            pkt_count=batch['pkt_count'].to(model.device),
            protocol=batch['protocol'].to(model.device),
        ).last_hidden_state
        return output.data[:, 0].cpu()