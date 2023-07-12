import cv2
import os
import glob
import numpy as np
from torch.utils.data import Dataset
from torchvision import transforms

import albumentations as A
from albumentations.pytorch import ToTensorV2





class AlbumentationsDataset(Dataset):
    
    def __init__(self, file_paths, transform=None):
        
        self.file_paths = glob.glob(os.path.join(file_paths, "*", "*", "*.jpg"))
        #print(self.file_paths)
        #변형 객체 class 내에서 선언
        self.transform = transform
        
        #폴더의 라벨 정보를 딕셔너리 형태로 저장
        self.labels = {"dew" : 0, "fogsmog" : 1, "frost" : 2, "glaze" : 3, "hail" : 4,
                       "lightning" : 5, "rain" : 6, "rainbow" : 7, "rime" : 8, "sandstorm" : 9,
                       "snow" : 10}
        
        
    def __getitem__(self, index):
        
        #str형태로 이미지 경로 읽어온 뒤 RGB형태로 변형
        file_path: str = self.file_paths[index]
        image = cv2.imread(file_path)
        
        if image is None:
            # 이미지 파일을 읽을 수 없는 경우, 예외 처리 또는 다른 대체 동작 수행
            # 예: 이미지 파일 경로 출력 또는 빈 이미지 반환
            print(f"Failed to read image: {file_path}")
            return None, None

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        folder_name = file_path.split("/")
        folder_name = folder_name[-2]

        #라벨은 해당하는 폴더이름과 부합하여 딕셔너리의 value값으로 넣어준다.
        label = self.labels[folder_name]
        
        if self.transform:
            augmented = self.transform(image=image)
            image = augmented['image']

        return image, label
            
    
    def __len__(self):
        return len(self.file_paths)
    




    
    
if __name__ == "__main__":

    albumentations_transform = A.Compose([
        #이미지 크기조정
        A.Resize(256, 256),
        #랜덤으로 224x224형태로 자르기
        A.RandomCrop(224, 224),
        #수평 뒤집기
        A.HorizontalFlip(),
        #정규화
        A.Normalize(

            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]

        ),

        #ToTensorV2는 Albumentations 라이브러리의 특성에 맞게 이미지를 텐서로 변환합니다.
        ToTensorV2()
    ])
    
    image_path = "./data/sample_data_01"
    dataset = AlbumentationsDataset(image_path, transform=albumentations_transform)

    for image, label in dataset:

        print(f"Augmentation image : {image}, Label : {label}")