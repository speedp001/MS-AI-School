# pip install flask 

# 필요한 파일 : imagenet1000_labels_dict / vgg11.pt
import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms

from PIL import Image
from flask import Flask, jsonify, request

from imagenet1000_labels_temp import label_dicr
from vgg11 import VGG11

app = Flask(__name__)

# 모델 로드 함수 
def load_model(model_path) : 
    model = VGG11(num_classes=1000)  #num_classes는 최종 분류 라벨 개수
    model.load_state_dict(torch.load(model_path))
    #torch.load() 함수는 모델 파일로부터 저장된 상태 딕셔너리를 로드
    #model.load_state_dict() 함수는 모델의 상태 딕셔너리를 로드하여 모델의 가중치와 매개변수를 업데이트
    #이 명령어를 통해서 생성된 모델 객체에 이미 학습된 가중치와 매개변수를 넣어줄 수 있다.
    model.eval()

    return model

# 모델 로드 
# model_path = "/Users/sang-yun/Desktop/Jupyter/Model_training/data/vgg11-bbd30ac9.pth"
# model = load_model(model_path)
model = VGG11(num_classes=1000)
model.eval()

# 이미지 전처리 함수 
def preprocess_image(image) : 
    transform = transforms.Compose([
        transforms.Resize((224,224)),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5,0.5,0.5))
    ])
    image = transform(image).unsqueeze(0)
    #3차원인 이미지를 0번 위치 차원에 차원을 추가 -> 3차원 이미지가 4차원 이미지가 된다.(배치사이즈, 채널, 높이, 너비)

    return image

# API 엔드포인트 설정
@app.route('/predict', methods=['POST'])
#predict 경로에 대한 POST 메서드 요청을 처리하는 함수를 등록
#클라이언트가 /predict경로로 POST를 하면 이 함수가 실행
def predict() : 
    
    if 'image' not in request.files : 
        return jsonify({'error ': 'No image uploaded' }), 400
    
    image = request.files['image']
    #test.py에서 이미지를 딕셔너리 형태로 넘겨주었다.때문에 이미지 key값을 이용해 image 데이터를 로드한다.
    img = Image.open(image)
    img = preprocess_image(img)

    # 예측 
    with torch.no_grad() : 
        outputs = model(img)
        _, pred = torch.max(outputs.data, 1)

        label_number = int(pred.item())
        class_name = label_dicr[label_number]

        prediction = str(class_name)

    #json형태로 200코드와 prediction을 딕셔너리형태로 클라이언트한테 반환해준다.
    return jsonify({'predictions':prediction}), 200


if __name__ == '__main__' :
    app.run(host="0.0.0.0", port=80, debug=True)
    # app.run(debug=True)
