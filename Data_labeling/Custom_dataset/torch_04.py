import json
import os
from typing import Any
from PIL import Image
import torch
from torch.utils.data import Dataset, DataLoader



#실제 이미지 파일이 없기 때문에 이미지 처리는 주석처리
class JsonCustomDataset(Dataset):
    def __init__(self, json_path, transform=None):
        self.transform = transform
        with open(json_path, 'r', encoding='utf-8') as f:
            #파일 객체를 받아서 json을 읽어오는 함수
            self.data = json.load(f)
    
    def __getitem__(self, index):
        img_path = self.data[index]['filename']
        img_path = os.path.join("이미지 폴더", img_path)

        #image = Image.open(img_path)
        
        bboxes = self.data[index]['ann']['bboxes']
        labels = self.data[index]['ann']['labels']
        
        #if self.transform:
            #image = self.transform(image)       
            
            
        #이미지 경로는 str형태로 bbox와 label은 딕셔너리 형태로 반환
        return img_path, {'bboxes' : bboxes, "labels" : labels}   
    
        
    def __len__(self):
        return len(self.data)
    
    
    
    
    
if __name__ == "__main__":
    dataset = JsonCustomDataset("./data/test.json", transform=None)
    
    for item in dataset:
        print(f"Data of datset : {item}")