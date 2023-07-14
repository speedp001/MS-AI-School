import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as transform

from torch.utils.data import DataLoader
from torchvision.datasets import CIFAR10
from torchvision.models import resnet18

from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# GPU 설정 (사용 가능한 경우)
device = torch.device("mps")
# print("device >>" , device)

# 데이터셋 불러오기 .
train_transform = transform.Compose([
    transform.RandomHorizontalFlip(),
    transform.RandomVerticalFlip(),
    transform.RandAugment(),
    transform.ToTensor(),
    transform.Normalize((0.5,0.5,0.5),(0.5,0.5,0.5)) # 이미지를 -1 ~ 1로 정규화
])

test_transform = transform.Compose([
    transform.ToTensor(),
    transform.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))  # 이미지를 -1 ~ 1로 정규화
])

# 데이터셋, 데이터 로더
train_dataset = CIFAR10(root="../../data", train=True, download=False,
                        transform=train_transform)
test_dataset = CIFAR10(root="../../data", train=False, download=False,
                       transform=test_transform)

train_loader = DataLoader(train_dataset, batch_size=128, shuffle=True, num_workers=2)
test_loader = DataLoader(test_dataset, batch_size=128, shuffle=False, num_workers=2)

# ResNet-18 모델 정의
model = resnet18(pretrained=True)
#self.fc = nn.Linear(512 * block.expansion, num_classes)
#모델을 커서에 놓고 cmd키를 누르면 모델정보를 확인할 수 있다. -> fc층에서 파라미터의 수를 확인 후 적용

num_features = model.fc.in_features
#print("fc in features >> ", num_features)

model.fc = nn.Linear(num_features, 10) # 클래스 개수 10개 입니다.
# print("fc in features >> ", num_features)

# # 배깅 앙상블 모델 정의
# """
# BaggingClassifier() => 여러개 분류기를 앙상블 해서 더 좋은 결과를 얻기 위한 알고리즘
# DecisionTreeClassifier() => 결정나무 트리 알고리즘 (트리 깊이가 7로 제한)
# """
# bagging_model = BaggingClassifier(
#     base_estimator=DecisionTreeClassifier(max_depth=7),
#     n_estimators=5
# )
# """
# BaggingClassifier는 주어진 기본 분류기를 복제하여 n_estimators 개수만큼 앙상블 모델을 생성합니다. 
# 이렇게 생성된 모델들은 동일한 학습 데이터에 대해 별도로 학습을 수행하게 됩니다. 각 모델은 데이터의 복원추출(bootstrap sampling)을
# 통해 조금씩 다른 학습 데이터를 가지게 되어 다양성을 가지는 모델들이 만들어집니다.
# """

# 손실 함수와 옵티마이저 정의
criterion = nn.CrossEntropyLoss()
optimizer = optim.AdamW(model.parameters(), lr=0.001)

# 모델 학습 함수 정의
def train(model, device, train_loader, optimizer, criterion) :
    model.train()
    for batch_idx , (data, target) in enumerate(train_loader) :
        data, target = data.to(device), target.to(device)

        optimizer.zero_grad()
        outputs = model(data)

        loss = criterion(outputs, target)
        loss.backward()
        optimizer.step()

# 모델 평가 함수 정의
def evalute(model, device, test_loader) :
    model.eval()
    predictions = []
    targets = []
    with torch.no_grad() :
        for data, target in test_loader :
            data, target = data.to(device), target.to(device)
            output = model(data)
            _, pred = torch.max(output,1)
            predictions.extend(pred.cpu().numpy())
            targets.extend(target.cpu().numpy())
    acc = accuracy_score(targets, predictions)

    return acc

# 앙상블된 모델 예측 함수 정의
def ensemble_pred(models, device, test_loader ) :
    predictions = []
    with torch.no_grad() :
        for data,_ in test_loader :
            data = data.to(device)
            outputs = []
            for model in models :
                model = model.to(device)
                model.eval()
                output = model(data)
                outputs.append(output)

            #첫 번째 batch_size로 5개 모델을 돌린 결과(확률)를 평균낸 것을 저장 -> dim=0으로 10개의 요소로 바뀐다
            ensemble_output = torch.stack(outputs).mean(dim=0)
            
            #각 배치사이즈만큼에서 얻어낸 확률값에서 가장 높은 인덱스를 뽑아 pred에 저장
            _, pred = torch.max(ensemble_output, 1)
            #모델 5개를 거친 배치사이즈 만큼의 데이터를 통해 얻은 라벨 예측값
            predictions.extend(pred.cpu().numpy())

            #for data,_ in test_loader : -> for문을 통해 데이터 끝까지 학습해서 추가
    return predictions

if __name__ == '__main__':

    models = []
    for epoch in range(1, 20) :
        print(f"Train ... {epoch}")
        model = model.to(device)
        train(model, device, train_loader, optimizer, criterion)
        acc = evalute(model, device, test_loader)
        print(f"Model {epoch} ACC {acc:.2f}")
        models.append(model)

    ensemble_predictions = ensemble_pred(models, device, test_loader)
    
    #전체 test_data.target 순서와 ensemble_predictions은 비교가능하다!
    #이유는 batch_size만큼 나누었다고해도 for문을 통해 데이터 끝까지 순회하였기 때문에 순서가 같다.
    ensemble_acc = accuracy_score(test_dataset.targets, ensemble_predictions)
    print(f"\nEnsemble Acc : {ensemble_acc:.2f}")