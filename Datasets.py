from torchvision import datasets
import torch
from torch.utils.data import DataLoader, Dataset, random_split, Subset
import numpy as np

class AngleActionDatasets(Dataset):
    def __init__(self, csv_path, transform=None, target_transform=None, pick_path = "data.pkl"):
        super(AngleActionDatasets, self).__init__()
        self.transform = transform
        self.target_transform = target_transform
        import pandas as pd
        from glob import glob
        import os
        csvs = glob(os.path.join(csv_path, "*.csv"))

        if len(csvs) == 0:
            raise ValueError("路径下不存在csv文件")
            return
        df = []

        if os.path.exists(pick_path):
            df = pd.read_pickle(pick_path)
        else:
            for label, csv in enumerate(csvs):
                if type(df) == list:
                    df = pd.read_csv(csv)
                    df['label'] = label
                else:
                    df_tmp = pd.read_csv(csv)
                    df_tmp['label'] = label
                    df = pd.concat([df, df_tmp])
            df.to_pickle(pick_path)
        
        self.labels_values = df[['label']].values
        self.values = df.values[:, 1:-1]
        
        # mean = np.mean(self.values, axis=0)
        # std = np.std(self.values, axis=0)
        
        # self.values = (self.values - mean) / std
        
    def __getitem__(self, idx):
        train_data = torch.tensor(self.values[idx*40:(idx+1)*40, :],dtype=torch.float32)
        label_data = torch.tensor(self.labels_values[idx*40:(idx+1)*40, -1][0], dtype=torch.long)

        if self.transform:
            train_data = self.transform(train_data)
        if self.target_transform:
            label_data = self.target_transform(label_data)

        return train_data ,label_data

    def __len__(self):
        return self.values.shape[0]//40



class ActionDatasets3Layer(Dataset):
    def __init__(self, csv_path, transform=None, target_transform=None, pick_path = "data.pkl"):
        super(ActionDatasets3Layer, self).__init__()
        self.transform = transform
        self.target_transform = target_transform
        import pandas as pd
        from glob import glob
        import os
        csvs = glob(os.path.join(csv_path, "*.csv"))

        if len(csvs) == 0:
            raise ValueError("路径下不存在csv文件")
            return
        df = []

        if os.path.exists(pick_path):
            df = pd.read_pickle(pick_path)
        else:
            for label, csv in enumerate(csvs):
                if type(df) == list:
                    df = pd.read_csv(csv)
                    df['label'] = label
                else:
                    df_tmp = pd.read_csv(csv)
                    df_tmp['label'] = label
                    df = pd.concat([df, df_tmp])
            df.to_pickle(pick_path)
            
        self.A_values = df[['aAX', 'aAY', 'aAZ','bAX', 'bAY', 'bAZ', 'cAX', 'cAY', 'cAZ', 'dAX', 'dAY', 'dAZ', 'eAX', 'eAY', 'eAZ', 'fAX', 'fAY', 'fAZ', 'gAX', 'gAY', 'gAZ']].values

        self.B_values = df[['aWX', 'aWY', 'aWZ','bWX', 'bWY', 'bWZ', 'cWX', 'cWY', 'cWZ', 'dWX', 'dWY', 'dWZ', 'eWX', 'eWY', 'eWZ', 'fWX', 'fWY', 'fWZ', 'gWX', 'gWY', 'gWZ']].values
        self.labels_values = df[['label']].values
        a_mean = np.mean(self.A_values, axis=0)
        a_std = np.std(self.A_values, axis=0)
        b_mean = np.mean(self.B_values, axis=0)
        b_std = np.std(self.B_values, axis=0)
        
        self.A_values = (self.A_values - a_mean) / a_std
        self.B_values = (self.B_values - b_mean) / b_std
        
    def __getitem__(self, idx):
            
        A_data = torch.tensor(self.A_values[idx*40:(idx+1)*40, :],dtype=torch.float32)
        B_data = torch.tensor(self.B_values[idx*40:(idx+1)*40, :],dtype=torch.float32)
        label_data = torch.tensor(self.labels_values[idx*40:(idx+1)*40, -1][0], dtype=torch.long)

        if self.transform:
            A_data = self.transform(A_data)
            B_data = self.transform(B_data)
        if self.target_transform:
            label_data = self.target_transform(label_data)

        return (A_data, B_data), label_data

    def __len__(self):
        return self.labels_values.shape[0]//40


class ActionDatasets(Dataset):
    def __init__(self, csv_path, transform=None, target_transform=None, pick_path = "data.pkl"):
        super(ActionDatasets, self).__init__()
        self.transform = transform
        self.target_transform = target_transform
        import pandas as pd
        from glob import glob
        import os
        csvs = glob(os.path.join(csv_path, "*.csv"))

        if len(csvs) == 0:
            raise ValueError("路径下不存在csv文件")
            return
        df = []

        if os.path.exists(pick_path):
            df = pd.read_pickle(pick_path)
        else:
            for label, csv in enumerate(csvs):
                if type(df) == list:
                    df = pd.read_csv(csv)
                    df['label'] = label
                else:
                    df_tmp = pd.read_csv(csv)
                    df_tmp['label'] = label
                    df = pd.concat([df, df_tmp])
            df.to_pickle(pick_path)
        
        self.values = df.values[:, 1:-2]
        
        mean = np.mean(self.values, axis=0)
        std = np.std(self.values, axis=0)
        
        self.values = (self.values - mean) / std
        self.labels_values = df[['label']].values
        
    def __getitem__(self, idx):
        train_data = torch.tensor(self.values[idx*40:(idx+1)*40, :],dtype=torch.float32)
        label_data = torch.tensor(self.labels_values[idx*40:(idx+1)*40, -1][0], dtype=torch.long)

        if self.transform:
            train_data = self.transform(train_data)
        if self.target_transform:
            label_data = self.target_transform(label_data)

        return train_data ,label_data

    def __len__(self):
        return self.values.shape[0]//40