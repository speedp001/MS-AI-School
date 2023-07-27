import cv2
import os
import glob

from tqdm import tqdm

#수집한 데이터를 Augmentation

def image_aug_angle(img, file_name, folder_name) : 
    
    # image BGR -> RGB
    image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # 회전할 각도 설정 
    angle = 20
    
    # 이미지 중심 기준으로 회전 행렬 생성
    (h, w) = image.shape[:2]
    center = (w // 2 , h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    
    # 회전 적용 
    rotated = cv2.warpAffine(image, M, (w, h))
    
    file_name = f"rotate_{file_name}"
    file_path = f"./data/fruit_aug_img/{folder_name}/{file_name}"
        
    image = cv2.cvtColor(rotated, cv2.COLOR_BGR2RGB)

    cv2.imwrite(file_path, image)

    
def image_aug_flip(img, file_name, folder_name) : 
    
     # image BGR -> RGB
    image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    flipped_right_and_left = cv2.flip(image, 1)
    flipped_up_and_down = cv2.flip(image, 0)
    
    file_name_right = f"flipped_right_and_left_{file_name}"
    file_name_up = f"flipped_up_and_down_{file_name}"
    
    file_path = f"./data/fruit_aug_img/{folder_name}/{file_name_right}"
    file_path_temp = f"./data/fruit_aug_img/{folder_name}/{file_name_up}"
        
    image01 = cv2.cvtColor(flipped_right_and_left, cv2.COLOR_BGR2RGB)
    image02 = cv2.cvtColor(flipped_up_and_down, cv2.COLOR_BGR2RGB)
    
    cv2.imwrite(file_path, image01)
    cv2.imwrite(file_path_temp, image02)

def image_aug_hsv(img, file_name, folder_name) : 
    
     # image BGR -> RGB
    image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
     ###### 채도값 변경하기 -> HSV 이미지 변환 
    img_hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV) 
    
    # 채도 값을 0.8 배로 증가 
    saturation_factor = 0.8
    img_hsv[:,:,1] = img_hsv[:,:,1] * saturation_factor
    
    img_saturated = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2RGB) 
    
    
    file_name = f"hsv_{file_name}"
    file_path = f"./data/fruit_aug_img/{folder_name}/{file_name}"
        
    image = cv2.cvtColor(img_saturated, cv2.COLOR_BGR2RGB)

    cv2.imwrite(file_path, image)









image_dir = "./data/fruit_data/"

# ./datasest/폴더/image.png
image_path_list = glob.glob(os.path.join(image_dir, "*", "*.png"))
# print(image_path_list)


for path in image_path_list : 
    # ./datasest/apple/apples3.jpg
    image_name = path.split("/")[4]
    print(image_name)
    folder_name = path.split("/")[3]
    print(folder_name)
    os.makedirs(f"./data//fruit_aug_img/{folder_name}", exist_ok=True)

    # image raed 
    img = cv2.imread(path)
    
    image_aug_angle(img, image_name ,folder_name)