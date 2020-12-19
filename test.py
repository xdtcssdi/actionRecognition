# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
# 原始模型

import torch
from torch import nn
from torchvision import datasets, transforms
from torch import optim
from torch.utils.data import DataLoader, Dataset, random_split, Subset
from tqdm import tqdm,trange
import torch.nn.functional as F

    
# %%
class ActionDatasets(Dataset):
    def __init__(self, csv_path, transform=None, target_transform=None):
        super(ActionDatasets, self).__init__()
        self.transform = transform
        self.target_transform = target_transform
        import pandas as pd
        from glob import glob
        import os
        csvs = glob(os.path.join(csv_path, "*.csv"))
        
        if len(csvs) == 0:
            raise ValueError("路径下不存在csv文件")

        df = []
        for label, csv in enumerate(csvs):
            if type(df) == list:
                df = pd.read_csv(csv)
                df['label'] = label
            else:
                df_tmp = pd.read_csv(csv)
                df_tmp['label'] = label
                df = pd.concat([df, df_tmp])
        
        self.data = df
        
    def __getitem__(self, idx):
        
        # train_data, label_data = self.data.values[idx*40:(idx+1)*40, 1:-2] ,self.data.values[idx*40:(idx+1)*40, -1][0]
        train_data, label_data = self.data.values[idx*40:(idx+1)*40, -2] ,self.data.values[idx*40:(idx+1)*40, -1][0]
        if self.transform:
            train_data = self.transform(train_data,dtype=torch.float32)

        if self.target_transform:
            label_data = self.target_transform(label_data)
        
        return train_data ,label_data.long()

    def __len__(self):
        return len(self.data)//40


# %%
classes = 5  #分类
hidden_dim = 64 # rnn隐藏单元数
lr = 0.001 # 学习率
epoches = 100 #训练次数
batch_size = 32 # 每一个训练批次数量
print_epoch = 500 # 每训练500批打印中间结果
input_dim=1
device = "cuda" if torch.cuda.is_available() else "cpu"
print(device)


# %%
train_data_path = r"/media/oswin/1F8E031F348BA466/temp/action_windows-test/"
# train_data_path = "D:\\temp\\augment_action_windows"
datasets = ActionDatasets(train_data_path, transform=torch.tensor, target_transform=torch.tensor)
test_datasets = ActionDatasets(r"/media/oswin/1F8E031F348BA466/temp/yan1_action_windows/action_windows/", transform=torch.tensor, target_transform=torch.tensor)
split_rate = 0.8  # 训练集占整个数据集的比例
train_len = int(split_rate * len(datasets))
valid_len = len(datasets) - train_len

train_sets, valid_sets = random_split(datasets, [train_len, valid_len], generator=torch.Generator().manual_seed(42))

train_loader = DataLoader(train_sets, batch_size=batch_size, shuffle=True,drop_last=True, num_workers=32,pin_memory=True)
test_loader = DataLoader(test_datasets, batch_size=batch_size, shuffle=True,drop_last=True, num_workers=32,pin_memory=True)
valid_loader = DataLoader(valid_sets, batch_size=batch_size, shuffle=True,drop_last=True, num_workers=32,pin_memory=True)

print(f"训练集大小{len(train_sets)}， 验证集大小{len(valid_sets)}")


# %%
import time
s = time.time()
for data, label in train_loader:
    pass
print(time.time()-s)


# %%
class RNN(nn.Module):
    def __init__(self, input_dim, hidden_dim, out_dim):
        super(RNN, self).__init__()
        self.rnn = nn.LSTM(input_dim, hidden_dim, 2, batch_first=True)
        self.linear1 = nn.Linear(hidden_dim, 64)
        self.linear2 = nn.Linear(64, out_dim)
    def forward(self, X):
        out, status = self.rnn(X)
        return self.linear2(F.relu(self.linear1(F.relu(out[:,-1,:]))))


# %%
rnn = RNN(input_dim, hidden_dim, classes).to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(rnn.parameters(), lr=lr)


# %%
def GETACC(loader=valid_loader):
    rnn.eval()
    cnt = 0
    sum_valid_acc = 0
    sum_valid_loss = 0
    for data, label in loader:
        data = data.view(batch_size, 40, 1).to(device)
        label = label.to(device)
        out = rnn(data)
        
        _, predict = torch.max(out, 1)
        
        loss = criterion(out, label)
        sum_valid_loss += loss.item()
        acc = torch.sum((predict == label).int()) / batch_size
        sum_valid_acc += acc
        cnt+=1
    
    return sum_valid_loss/cnt, sum_valid_acc/cnt


# %%
for epoch in range(epoches):
    i = 0
    loss_sum = 0
    bar = tqdm(train_loader)
    for ii, (data , label) in enumerate(bar):
        rnn.train()
        data = data.view(batch_size, 40, 1).to(device)
        label = label.to(device)
        out = rnn(data)
        
        loss = criterion(out, label)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        i+=1
        loss_sum += loss.item()

        if ii == 0:
            valid_loss,valid_acc = GETACC(valid_loader)
            
            bar.set_description(f"epoch = {epoch} train_loss = {loss_sum/i} valid_loss = {valid_loss} valid_acc= {valid_acc}")


# %%
# test_loss,test_acc = GETACC(test_loader)
# print(f"test_loss = {test_loss}, test_acc = {test_acc}")


# %%



