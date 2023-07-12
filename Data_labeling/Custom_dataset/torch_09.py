import torch
import os
import glob
import time
from PIL import Image
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms



#캐시 메모리 관리
def is_grayscale(img):
    return img.mode =='L'


class CustomImageDataset(Dataset):
    def __init__(self, image_path, transform = None):
        self.image_path = glob.glob(os.path.join(image_path, "*", "*", "*.jpg"))
        self.transform = transform
        self.label_dict = {"dew" : 0, "fogsmog" : 1, "frost" : 2, "glaze" : 3, "hail" : 4,
                           "lightning" : 5, "rain" : 6, "rainbow" : 7, "rime" : 8, "sandstorm" : 9,
                           "snow" : 10}
        
        self.cache = {}
        
    def __getitem__(self, index):
        
        if index in self.cache:
            image, label = self.cahe[index]
            
        
        else:
            image_path: str = self.image_path[index]
            image = Image.open(image_path).convert("RGB")
            
            if not is_grayscale(image):
                
                folder_name = image_path.split("/")
                folder_name = folder_name[-2]

                label = self.label_dict[folder_name]
                
                self.cache[index] = (image, label)
        
            else:
                print(f"{image_path}파일은 흑백 이미지입니다.")
                return None, None
                
        if self.transform:
            image = self.transform(image)
                    
        return image, label
            
    def __len__(self):
        return len(self.image_path)
    
    






if __name__ == "__main__":
    
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor()
    ])
     
    image_paths = "./data/sample_data_01"  #데이터 폴더 경로 지정
    # 캐시 처리
    dataset_with_cache = CustomImageDataset (image_paths, transform=transform)
    dataloader_with_cache = DataLoader (dataset_with_cache, batch_size=64, shuffle=True)
    
    # 캐시 미처리
    dataset_without_cache = CustomImageDataset (image_paths, transform=transform)
    dataloader_without_cache = DataLoader(dataset_without_cache, batch_size=64, shuffle=True)
    
    # 속도 비고
    start_time = time.time()
    for images, labels in dataloader_with_cache:
        # 캐시 처리된 데이터셋으로 연산 수행
        pass
    end_time = time.time()
    print("With Cache - Elapsed Time:", end_time - start_time)
    
    start_time - time.time()
    for images, labels in dataloader_without_cache:
        # 캐시 미처리된 데이터셋으로 연산 수행
        pass
    end_time = time.time()
    print("Without Cache - Elapsed Time:", end_time - start_time)