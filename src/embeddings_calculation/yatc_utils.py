import os
import torch
from tqdm.auto import tqdm
from collections import defaultdict

def get_dataset(path, dataloader=True):
    os.chdir("../models/YaTC/src")    
    from finetune import build_dataset
    
    dataset = lambda: True
    dataset.data_path = path
    dataset = build_dataset(is_train=True, args=dataset)
    if not dataloader:
        return dataset
    else:
        return torch.utils.data.DataLoader(
            dataset, sampler=torch.utils.data.SequentialSampler(dataset),
            batch_size=256,
            num_workers=1,
            pin_memory=False,
            drop_last=True,
        )

def load_model(checkpoint_model, nb_classes=210, device="cuda"):
    os.chdir("../models/YaTC/src")
    from util.pos_embed import interpolate_pos_embed
    import models_YaTC
    
    checkpoint_model = torch.load(checkpoint_model)
    model = models_YaTC.__dict__['TraFormer_YaTC'](
        num_classes=nb_classes,
        drop_path_rate=0.1,
    )
    interpolate_pos_embed(model, checkpoint_model)
    msg = model.load_state_dict(checkpoint_model, strict=False)
    model.to(device)
    print(msg)
    return model  

def load_frozen_model(path="../models/YaTC/YaTC_pretrained_model.pth", nb_classes=210, device="cuda"):
    os.chdir("../models/YaTC/src")
    from util.pos_embed import interpolate_pos_embed
    import models_YaTC
    
    checkpoint_model = torch.load(path)['model']
    yatc_cross_frozen_model = models_YaTC.__dict__['TraFormer_YaTC'](
        num_classes=nb_classes,
        drop_path_rate=0.1,
    )
    interpolate_pos_embed(yatc_cross_frozen_model, checkpoint_model)

    #rename norm to fc_norm and delete extra keys
    checkpoint_model['fc_norm.bias'] = checkpoint_model['norm.bias']
    checkpoint_model['fc_norm.weight'] = checkpoint_model['norm.weight']

    keys_to_del = ['mask_token', 'norm.weight', 'norm.bias']
    for key in checkpoint_model.keys():
        if key.startswith('decoder'):
            keys_to_del.append(key)

    for key in keys_to_del:
        del checkpoint_model[key]

    yatc_cross_frozen_model.load_state_dict(checkpoint_model, strict=False)
    yatc_cross_frozen_model.to(device)
    return yatc_cross_frozen_model

def forward_features(model, imgs):
    with torch.no_grad():
        return model.forward_features(imgs).mean(dim=1).cpu()

# with torch.no_grad():
#     for i, (imgs, labels) in enumerate(crossmarket_w_short):
#         print('.', end='')
#         imgs = imgs.to(device)
#         crossmarket_w_short_emb['labels'].append(labels.cpu())
#         crossmarket_w_short_emb['yatc_cross_frozen_model'].append(yatc_cross_frozen_model.forward_features(imgs).mean(dim=1).cpu())
#         crossmarket_w_short_emb['yatc_cross_ft_short_model'].append(yatc_cross_ft_short_model.forward_features(imgs).mean(dim=1).cpu())
#         crossmarket_w_short_emb['yatc_cross_ft_wo_short_model'].append(yatc_cross_ft_wo_short_model.forward_features(imgs).mean(dim=1).cpu())
#         del imgs