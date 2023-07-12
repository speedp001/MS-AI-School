import torch
import torchvision
from torchvision import transforms
from torch.utils.data import DataLoader
import numpy as np
import imgaug.augmenters as iaa 
import matplotlib.pyplot as plt




#Sequential 변형 시작
def imgaug_transform(image):
    seq = iaa.Sequential([
        #좌우 뒤집기(확률 50프로)
        iaa.Fliplr(0.5),
        #가우시안 블러(0부터 1사이 값 임의로 적용)
        iaa.GaussianBlur(sigma=(0, 1.0)),
        #밝기 조정(0.8부터 1.2까지 임의로 적용)
        iaa.Multiply((0.8, 1.2))
    ])
    image_np = image.permute(1, 2, 0).numpy()
    #(높이, 너비, 채널)로 배열 재배열해준다.
    #딥러닝이나 번형에서 채널, 높이, 너비로 설정하는 경우가 대부분
    image_aug = seq(image=image_np)
    image_aug_copy = image_aug.copy()
    image_aug_tensor = torch.from_numpy(image_aug_copy).permute(2, 0, 1)
    #(채널, 높이, 너비)로 permute함수를 통해 재배열
    return image_aug_tensor

#클래스 호출 시 transform설정으로 인해 실행
def transform_data(image):
    tensor = transforms.ToTensor()(image)
    #텐서로 변형한 이미지 데이터를 위 함수 호출로 변형 적용
    transformed_tensor = imgaug_transform(tensor)
    return transformed_tensor












#공개데이터 CIFAR-10
train_dataset = torchvision.datasets.CIFAR10(root='./data', train=True, download=True, transform=transform_data)
#transform=transform_data 함수 실행
batch_size = 4
#데이터로더 설정
train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

for images, labels in train_dataloader:
    fig, axes = plt.subplots(1, batch_size, figsize=(12, 4))
    #1행과 batch_size만큼의 열의 개수로 가로 12인치 세로 4인치 크기로 그래프 시각화

    for i in range(batch_size):
        image = images[i].permute(1, 2, 0).numpy()
        #imshow()는 높이, 너비, 채널 순으로 인자값을 받아서 형식 변경
        axes[i].imshow(image)
        axes[i].set_title(f"label : {labels[i]}")
        
    plt.show()
    break  #첫 번째 미니배치만 시각화