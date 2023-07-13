import torch.nn as nn
import torchvision.models as models
import torch

class VGG11(nn.Module) : 
    def __init__(self, num_classes=1000) :
        super(VGG11, self).__init__()
        #전이학습으로 VGG를 이용
        self.features = models.vgg11(pretrained=True).features
        #pretrained 옵션은 학습된 가중치가 저장된 모델 파일이 있기 때문에 False로 지정
        self.avgpool = nn.AdaptiveAvgPool2d((7,7))
        #끝의 형태를 7 * 7로 맞춘다.

        self.classifier = nn.Sequential(
            nn.Linear(512 * 7 * 7, 4096),
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(4096, 4096),
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(4096, num_classes)
        )

    def forward(self,x)  :
        x = self.features(x)
        #pretrained backbone vgg11 학습
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        #평탄화
        x = self.classifier(x)
        #커스텀 분류기에 평탄화한 데이터 입력
        
        return x
    
model = VGG11()
print(model)
    
