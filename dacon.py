# -*- coding: utf-8 -*-
"""Dacon.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10ON2QcCUKm3u9al9MNC13e6w8CbkUdm5
"""

!pip install efficientnet-pytorch

import random
import pandas as pd
import numpy as np
import os
import cv2

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader

import albumentations as A
from albumentations.pytorch.transforms import ToTensorV2
import torchvision.models as models

from tqdm.auto import tqdm
from sklearn.metrics import accuracy_score
from efficientnet_pytorch import EfficientNet
import warnings
import torchvision.models as models
warnings.filterwarnings(action='ignore')

model0 = EfficientNet.from_pretrained('efficientnet-b0',num_classes = 10)
model1 = EfficientNet.from_pretrained('efficientnet-b1',num_classes = 10)
model2 = EfficientNet.from_pretrained('efficientnet-b2',num_classes = 10)
model3 = EfficientNet.from_pretrained('efficientnet-b3',num_classes = 10)
model4 = EfficientNet.from_pretrained('efficientnet-b4',num_classes = 10)
model5 = EfficientNet.from_pretrained('efficientnet-b5',num_classes = 10)
model6 = EfficientNet.from_pretrained('efficientnet-b6',num_classes = 10)
model7 = EfficientNet.from_pretrained('efficientnet-b7',num_classes = 10)

from google.colab import drive
drive.mount("/content/drive")

device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
print(device)

model_list = []
model_list.append(model0)
model_list.append(model1)
model_list.append(model2)
model_list.append(model3)
model_list.append(model4)
model_list.append(model5)
model_list.append(model6)
model_list.append(model7)

CFG = {
    'IMG_SIZE':400,
    'EPOCHS':2,
    'LEARNING_RATE':3e-4,
    'BATCH_SIZE':4,
    'SEED':41
}
#Efficientnet _B0: 224
#Efficientnet _B1: 240
#Efficientnet _B2: 260
#Efficientnet _B3: 380
#Efficientnet _B4: 456
#Efficientnet _B5: 528
#Efficientnet _B6: 600

def seed_everything(seed):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = True

seed_everything(CFG['SEED']) # Seed 고정

df = pd.read_csv('/content/drive/MyDrive/4d_multilabel/dacon_4d/train.csv')

df = df.sample(frac=1)
train_len = int(len(df) * 0.8)

train = df[:train_len]
val = df[train_len:]

def get_labels(df):
    return df.iloc[:,2:].values

train_labels = get_labels(train)
val_labels = get_labels(val)

df

import os

#/content/open.zip

for i in range(10):
    print(i)

import zipfile
original_data_path = '/content'
with zipfile.ZipFile(os.path.join(original_data_path, 'open.zip')) as train_zip:
    train_zip.extractall('/content/open')
    
# with zipfile.ZipFile(os.path.join(original_data_path, 'test.zip')) as test_zip:
#     test_zip.extractall('/content/test')

data_path = "/content/drive/MyDrive/4d_multilabel/dacon_4d/"

#/content/open/test/TEST_00000.jpg
dir = '/content/open/'

class CustomDataset(Dataset):
    def __init__(self, img_path_list, label_list, transforms=None):
        self.img_path_list = img_path_list
        self.label_list = label_list
        self.transforms = transforms
        
    def __getitem__(self, index):
        img_path = dir + self.img_path_list[index].replace("./",'')
        gc.collect()
        image = cv2.imread(img_path)
        #image = remove(image)
        #image = cv2.resize(image,(3,400,400))
        #image = fgbg.apply(image)
        #image = remove(image)
        
        if self.transforms is not None:
            image = self.transforms(image=image)['image']
        
        if self.label_list is not None:
            label = torch.FloatTensor(self.label_list[index])
            return image, label
        else:
            return image
        
    def __len__(self):
        return len(self.img_path_list)

# class CustomDataset_test(Dataset):
#     def __init__(self, img_path_list, label_list, transforms=None):
#         self.img_path_list = img_path_list
#         self.label_list = label_list
#         self.transforms = transforms
        
#     def __getitem__(self, index):
#         img_path = data_path + self.img_path_list[index].replace("./",'')
#         gc.collect()
#         image = cv2.imread(img_path)
#         #image = remove(image)
#         #image = cv2.resize(image,(3,400,400))
#         #image = fgbg.apply(image)
#         #image = remove(image)
        
#         if self.transforms is not None:
#             image = self.transforms(image=image)['image']
        
#         if self.label_list is not None:
#             label = torch.FloatTensor(self.label_list[index])
#             return image, label
#         else:
#             return image
        
#     def __len__(self):
#         return len(self.img_path_list)

# class CustomDataset_test(Dataset):
#     def __init__(self, img_path_list, label_list, transforms=None):
#         self.img_path_list = img_path_list
#         self.label_list = label_list
#         self.transforms = transforms
        
#     def __getitem__(self, index):
#         img_path = "/content/drive/MyDrive/4d_multilabel/dacon_4d/test_scaled/"+ self.img_path_list[index].replace("./test/",'')
#         gc.collect()
#         image = cv2.imread(img_path)
#         #image = remove(image)
#         #image = cv2.resize(image,(3,400,400))
#         #image = fgbg.apply(image)
#         #image = remove(image)
        
#         if self.transforms is not None:
#             image = self.transforms(image=image)['image']
        
#         if self.label_list is not None:
#             label = torch.FloatTensor(self.label_list[index])
#             return image, label
#         else:
#             return image
        
#     def __len__(self):
#         return len(self.img_path_list)

train_transform = A.Compose([
                            A.Resize(CFG['IMG_SIZE'],CFG['IMG_SIZE']),
                            A.RandomRotate90(p = 0.3),
                            A.VerticalFlip(p=0.3),
                            A.HorizontalFlip(p=0.3),
                            #A.RandomAdjustSharpness(p = 0.3),
                             
                            #A.GaussNoise(var_limit,mean,p= 0.2),
                            A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225), max_pixel_value=255.0, always_apply=False, p=1.0),
                            ToTensorV2()
                            ])

test_transform = A.Compose([
                            A.Resize(CFG['IMG_SIZE'],CFG['IMG_SIZE']),
                            A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225), max_pixel_value=255.0, always_apply=False, p=1.0),
                            ToTensorV2()
                            ])

train_dataset = CustomDataset(train['img_path'].values, train_labels, train_transform)
train_loader = DataLoader(train_dataset, batch_size = CFG['BATCH_SIZE'], shuffle=True, num_workers=0)

val_dataset = CustomDataset(val['img_path'].values, val_labels, test_transform)
val_loader = DataLoader(val_dataset, batch_size = CFG['BATCH_SIZE'], shuffle=False, num_workers=0)



class CNN(nn.Module):
    def __init__(self, n_classes=10):
        
        super().__init__()
        self.features = models.efficientnet_v2_s(weights="DEFAULT")
        self.n_classes = n_classes
        #self.gap = nn.AdaptiveAvgPool2d(1)
        self.fn1 = nn.Linear(1000, n_classes)
        #self.fn2 = nn.Linear(128, n_classes)
             
    def forward(self, x):
        x = self.features(x)
        #x = self.gap(x).squeeze(3).squeeze(2)
        #print(x.shape)
        x = self.fn1(x)
        x = F.relu(x)
       # x = self.fn2(x)
        x = F.sigmoid(x)

        return x

class BaseModel(nn.Module):
    def __init__(self, num_classes=10):
        super(BaseModel, self).__init__()
        self.backbone = model_list[6]
        #self.classifier = nn.Linear(1000, num_classes)
        
    def forward(self, x):
        x = self.backbone(x)
        x = F.sigmoid(x)
        return x

    # def __init__(self, num_labels=10, pretrained=False):
    #     super().__init__()
    #     self.num_labels = num_labels
    #     self.pretrained = pretrained
        
    #     self.model = ResNet_50(pretrained=self.pretrained)
    #     self.fc = nn.Sequential(nn.Linear(2048, 512),
    #                            nn.Linear(512, self.num_labels))
    #     self.model.fc = self.fc
        
    # def forward(self, x):
    #     return  F.sigmoid(self.model(x))

class ViTModelB16(nn.Module):
    def __init__(self,  num_classes=10):
        super().__init__()
        self.backbone = models.vit_b_16(weights=models.ViT_B_16_Weights.IMAGENET1K_SWAG_E2E_V1)
        self.num_classes = num_classes
        self.backbone.heads = nn.Linear(768, num_classes)

    def forward(self, x):
        x = self.backbone(x)
        x = F.sigmoid(x)
        return x

def train(model, optimizer, train_loader, val_loader, scheduler, device):
    model.to(device)
    criterion = nn.BCELoss().to(device)
    
    best_val_acc = 0
    best_model = None
    
    for epoch in range(1, CFG['EPOCHS']+1):
        model.train()
        train_loss = []
        for imgs, labels in tqdm(iter(train_loader)):
            imgs = imgs.float().to(device)
            labels = labels.to(device)
            
            optimizer.zero_grad()
            
            output = model(imgs)
            loss = criterion(output, labels)
            
            loss.backward()
            optimizer.step()
            
            train_loss.append(loss.item())
                    
        _val_loss, _val_acc = validation(model, criterion, val_loader, device)
        _train_loss = np.mean(train_loss)
        print(f'Epoch [{epoch}], Train Loss : [{_train_loss:.5f}] Val Loss : [{_val_loss:.5f}] Val ACC : [{_val_acc:.5f}]')
        
        if scheduler is not None:
            scheduler.step(_val_acc)
            
        if best_val_acc < _val_acc:
            best_val_acc = _val_acc
            best_model = model
            #joblib.dump(best_model,'/content/drive/MyDrive/4d_multilabel/dacon_4d/best_model_effi_3.pkl')
    
    return best_model



def validation(model, criterion, val_loader, device):
    model.eval()
    val_loss = []
    val_acc = []
    with torch.no_grad():
        for imgs, labels in tqdm(iter(val_loader)):
            imgs = imgs.float().to(device)
            labels = labels.to(device)
            
            probs = model(imgs)
            
            loss = criterion(probs, labels)
            
            probs  = probs.cpu().detach().numpy()
            labels = labels.cpu().detach().numpy()
            preds = probs > 0.5
            batch_acc = (labels == preds).mean()
            
            val_acc.append(batch_acc)
            val_loss.append(loss.item())
        
        _val_loss = np.mean(val_loss)
        _val_acc = np.mean(val_acc)
        
    
    return _val_loss, _val_acc





import torch, gc
gc.collect()
torch.cuda.empty_cache()

model = BaseModel()
model.eval()
optimizer = torch.optim.Adam(params = model.parameters(), lr = CFG["LEARNING_RATE"])
scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='max', factor=0.5, patience=1,threshold_mode='abs',min_lr=1e-6, verbose=True)

infer_model = train(model, optimizer, train_loader, val_loader, scheduler, device)

model = CNN()
model.eval()
optimizer = torch.optim.Adam(params = model.parameters(), lr = CFG["LEARNING_RATE"])
scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='max', factor=0.5, patience=1,threshold_mode='abs',min_lr=1e-6, verbose=True)

infer_model = train(model, optimizer, train_loader, val_loader, scheduler, device)

model = ViTModelB16()
model.eval()
optimizer = torch.optim.Adam(params = model.parameters(), lr = CFG["LEARNING_RATE"])
scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='max', factor=0.5, patience=1,threshold_mode='abs',min_lr=1e-6, verbose=True)

infer_model = train(model, optimizer, train_loader, val_loader, scheduler, device)

test = pd.read_csv('/content/drive/MyDrive/4d_multilabel/dacon_4d/test.csv')

test_dataset = CustomDataset(test['img_path'].values, None, test_transform)
test_loader = DataLoader(test_dataset, batch_size = CFG['BATCH_SIZE'], shuffle=False, num_workers=0)

def inference(model, test_loader, device):
    model.to(device)
    model.eval()
    predictions = []
    raw_predictions = []
    with torch.no_grad():
        for imgs in tqdm(iter(test_loader)):
            imgs = imgs.float().to(device)
            
            probs = model(imgs)

            probs  = probs.cpu().detach().numpy()
            primitive = probs
            preds = probs > 0.5
            preds = preds.astype(int)  #-> 후에 모델별로 더하고 모아서 나누고 결론 내기 
            predictions += preds.tolist()
            raw_predictions += primitive.tolist()
    return predictions,raw_predictions

preds,raw_predictions = inference(model, test_loader, device)

submit = pd.read_csv('/content/drive/MyDrive/4d_multilabel/dacon_4d/sample_submission.csv')
submit.iloc[:,1:] = preds
submit.head()
submit_raw = pd.read_csv('/content/drive/MyDrive/4d_multilabel/dacon_4d/sample_submission.csv')
submit_raw.iloc[:,1:] = raw_predictions
submit_raw.head()
submit.to_csv('/content/drive/MyDrive/4d_multilabel/dacon_4d/'+'effi_b6.csv',index = False)
submit_raw.to_csv('/content/drive/MyDrive/4d_multilabel/dacon_4d/'+'effi_b6_raw.csv',index = False)

# submit.iloc[:,1:] = preds
# submit.head()
# submit_raw = pd.read_csv('/content/drive/MyDrive/4d_multilabel/dacon_4d/sample_submission.csv')
# submit_raw.iloc[:,1:] = raw_predictions
# submit_raw.head()
# submit.to_csv('/content/drive/MyDrive/4d_multilabel/dacon_4d/'+'effi_b5.csv',index = False)
# submit_raw.to_csv('/content/drive/MyDrive/4d_multilabel/dacon_4d/'+'effi_b5_raw.csv',index = False)



# submit_raw = pd.read_csv('/content/drive/MyDrive/4d_multilabel/dacon_4d/sample_submission.csv')
# submit_raw.iloc[:,1:] = raw_predictions
# submit_raw.head()
# submit.to_csv('/content/drive/MyDrive/4d_multilabel/dacon_4d/'+'effi_b5.csv',index = False)
# submit_raw.to_csv('/content/drive/MyDrive/4d_multilabel/dacon_4d/'+'effi_b5_raw.csv',index = False)

# submit_raw.iloc[:,1:] = raw_predictions
# submit_raw.head()
# submit.to_csv('/content/drive/MyDrive/4d_multilabel/dacon_4d/'+'effi_b5.csv',index = False)
# submit_raw.to_csv('/content/drive/MyDrive/4d_multilabel/dacon_4d/'+'effi_b5_raw.csv',index = False)

# submit.to_csv('/content/drive/MyDrive/4d_multilabel/dacon_4d/'+'effi_b5.csv',index = False)

# submit_raw.to_csv('/content/drive/MyDrive/4d_multilabel/dacon_4d/'+'effi_b5_raw.csv',index = False)
# #/content/drive/MyDrive/4d_multilabel/dacon_4d/effi_b3_scaled.csv

# pd.read_csv("/content/drive/MyDrive/4d_multilabel/dacon_4d/b3_scaled.csv")

a = pd.read_csv("/content/drive/MyDrive/4d_multilabel/dacon_4d/effi_b4_raw.csv")
b = pd.read_csv("/content/drive/MyDrive/4d_multilabel/dacon_4d/effi_b5_raw.csv")
c=  pd.read_csv('/content/drive/MyDrive/4d_multilabel/dacon_4d/effi_b6_raw.csv')

a.loc[:,'A':'J']*0.7

b.loc[:,'A':'J']*0.3

pred1 = (a.loc[:,'A':'J']+b.loc[:,'A':'J']+c.loc[:,'A':'J'])/3
pred1 = (pred1 > 0.5).astype(int)

submit.iloc[:,1:] = pred1
submit.head()

submit.to_csv("/content/drive/MyDrive/4d_multilabel/dacon_4d/blended_b4+b5+b6.csv",index = False)