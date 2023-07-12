import torch
import os
import glob
#파일 접근 및 관리
from PIL import Image
#Image 파일 관리 라이브러리
from torch.utils.data import Dataset, DataLoader
#데이터 셋과 데이터로더를 관리하는 라이브러리
from torchvision import transforms
#데이터 어그멘테이션 관련 라이브러리



def is_grayscale(img):
    #흑백이미지가 맞으면 True반환('L'로 지정 시)
    return img.mode =='L'


class CustomImageDataset(Dataset):
    
    def __init__(self, image_path, transform = None):
        #변형 인자값은 기본값으로 한다.(호출 시에 선언된 변형값 사용)
        self.image_path = glob.glob(os.path.join(image_path, "*", "*", "*.jpg"))
        
        #이미지 변형
        self.transform = transform
        
        #라벨링 할 항목을 딕셔너리로 선언
        self.label_dict = {"dew" : 0, "fogsmog" : 1, "frost" : 2, "glaze" : 3, "hail" : 4,
                           "lightning" : 5, "rain" : 6, "rainbow" : 7, "rime" : 8, "sandstorm" : 9,
                           "snow" : 10}


    def __getitem__(self, index):
        
        #str형태로 이미지 경로 읽어온 뒤 RGB형태로 변형
        image_path: str = self.image_path[index]
        image = Image.open(image_path).convert("RGB")
        
        #is_grayscale 함수로 흑백여부 판단
        if not is_grayscale(image):
            
            folder_name = image_path.split("/")
            folder_name = folder_name[-2]

            #라벨은 해당하는 폴더이름과 부합하여 딕셔너리의 value값으로 넣어준다.
            label = self.label_dict[folder_name]
            
            if self.transform:
                image = self.transform(image)
                
            return image, label
        
        else:
            print(f"{image_path}파일은 흑백 이미지입니다.")
        
        
    def __len__(self):
        return len(self.image_path)
    
    






if __name__ == "__main__":
    
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        #이미지 크기 변경
        transforms.ToTensor()
        #이미지를 텐서 형식으로 변환
    ])
     
    image_paths = "./data/sample_data_01"
    dataset = CustomImageDataset(image_paths, transform=transform)
    
    #Dataloader는 인자값으로 지정한 데이터셋을 배치사이즈와 셔플여부를 고려하여 데이터셋을 바꾸어주는 것
    data_loader = DataLoader(dataset, 32, shuffle=True)
    
    #Dataloader로 바뀐 dataset을 __getitem__을 for문을 통하여 호출
    for image, label in data_loader:
        print(f"Image : {image}")
        print(f"Label : {label}")