#pip install albumentations

import random
import cv2
import albumentations as A
import matplotlib.pyplot as plt





def visualize(tf_img):
    cv2.imshow("org", image)
    cv2.imshow("tf_img", tf_img)
    cv2.waitKey()





# image = cv2.imread('./data/01.jpg')
# #visualize(image)

# # 좌우반전
# transform = A.HorizontalFlip(p=0.5)
# #50프로 확률로 실행
# horizontalflip_img = transform(image=image)['image']
# visualize(horizontalflip_img)

# #ShiftScaleRotate
# transform = A.ShiftScaleRotate(p=0.5)
# #50프로 확률로 실행
# random.seed(7)
# shiftscalerotate = transform(image=image)['image']
# visualize(shiftscalerotate)






#복잡한 파이프라인 구축하여 image aug 실행
# transform = A.Compose([
#     A.CLAHE(),
#     A.RandomRotate90(),
#     A.Transpose(),
#     A.ShiftScaleRotate(shift_limit=0.0625, scale_limit=0.50, rotate_limit=45, p=0.75),
#     A.Blur(blur_limit=3),
#     A.OpticalDistortion(),
#     A.GridDistortion(),
#     A.HueSaturationValue(),
# ])

# while True :

#     augmented_image = transform(image=image)['image']
#     cv2.imshow("org", image)
#     cv2.imshow("tf", augmented_image)
#     key = cv2.waitKey()
#     if key == ord('q') :
#         cv2.destroyAllWindows()
#         break



#Albumentations 날씨 실습

# #rain
# image = cv2.imread('../data/01.jpg')

# transform = A.Compose(
#     [A.RandomRain(brightness_coefficient=0.9, drop_width=1, blur_value=5, p=1)]

#     # brightness_coefficient: 비 노이즈의 밝기 조절 계수입니다. 기본값은 0.9입니다. 이 값이 높을수록 비 노이즈가 더 밝아지고, 낮을수록 어두워집니다.
#     # drop_width: 비 노이즈의 너비입니다. 기본값은 1입니다. 비 노이즈의 너비가 클수록 더 굵은 비가 생성됩니다.
#     # blur_value: 비 노이즈의 블러(blur) 값입니다. 기본값은 5입니다. 이 값이 크면 비 노이즈가 더 흐려지고, 작으면 더 선명해집니다.
#     # p: 변환을 적용할 확률입니다. 기본값은 1입니다. 0과 1 사이의 값을 가지며, 이 값이 높을수록 변환을 적용하는 빈도가 높아집니다.

# )

# rain_img = transform(image=image)['image']

# cv2.imshow("rain", rain_img)
# cv2.waitKey()







# #snow
# image = cv2.imread('../data/image02.jpeg')

# transform = A.Compose(
#     [A.RandomSnow(brightness_coeff=2.5, snow_point_lower=0.3, snow_point_upper=0.5, p=1)]

#     #brightness_coeff: 눈 노이즈의 밝기 조절 계수입니다. 기본값은 2.5입니다. 이 값이 높을수록 눈 노이즈가 더 밝아지고, 낮을수록 어두워집니다.
#     #snow_point_lower: 눈 노이즈가 생성될 픽셀의 최소 값 비율입니다. 기본값은 0.3입니다. 0과 1 사이의 값을 가지며, 이 값이 높을수록 더 많은 픽셀에 눈 노이즈가 생성됩니다.
#     #snow_point_upper: 눈 노이즈가 생성될 픽셀의 최대 값 비율입니다. 기본값은 0.5입니다. 0과 1 사이의 값을 가지며, 이 값이 높을수록 더 많은 픽셀에 눈 노이즈가 생성됩니다.
#     #p: 변환을 적용할 확률입니다. 기본값은 1입니다. 0과 1 사이의 값을 가지며, 이 값이 높을수록 변환을 적용하는 빈도가 높아집니다.
# )

# snow_img = transform(image=image)['image']

# cv2.imshow("rain", snow_img)
# cv2.waitKey()







# #RandomSunFlare
# image = cv2.imread('../data/image02.jpeg')

# transform = A.Compose([
#     A.RandomSunFlare(flare_roi=(0,0,1,0.5), angle_lower=0.5, p=1)

#     # flare_roi: 플레어 효과가 적용될 이미지 내의 ROI(Region of Interest)입니다. 기본값은 (0, 0, 1, 0.5)입니다. (x, y, w, h) 형식으로 ROI를 지정합니다. (x, y)는 ROI의 좌측 상단 모서리 좌표이며, (w, h)는 ROI의 너비와 높이입니다. 이를 통해 플레어 효과가 이미지의 일부 영역에만 적용되도록 할 수 있습니다.
#     # angle_lower: 플레어 효과의 각도 범위의 하한값입니다. 기본값은 0.5입니다. 이 값보다 큰 각도 범위에서 플레어가 생성됩니다.
#     # p: 변환을 적용할 확률입니다. 기본값은 1입니다. 0과 1 사이의 값을 가지며, 이 값이 높을수록 변환을 적용하는 빈도가 높아집니다.
# ])

# flare_img = transform(image=image)['image']

# visualize(flare_img)








# #RandomShadow
# image = cv2.imread('../data/image02.jpeg')

# transform = A.Compose([
#     A.RandomShadow(num_shadows_lower=1, num_shadows_upper=1, shadow_dimension=5, shadow_roi=(0,0.5,1,1), p=1)

#     # num_shadows_lower: 그림자의 최소 수입니다. 기본값은 1입니다. 생성될 그림자의 최소 개수를 지정합니다.
#     # num_shadows_upper: 그림자의 최대 수입니다. 기본값은 1입니다. 생성될 그림자의 최대 개수를 지정합니다.
#     # shadow_dimension: 그림자의 크기입니다. 기본값은 5입니다. 그림자의 크기를 조절하여 그림자의 강도를 변경할 수 있습니다.
#     # shadow_roi: 그림자 효과가 적용될 이미지 내의 ROI(Region of Interest)입니다. 기본값은 (0, 0.5, 1, 1)입니다. (x, y, w, h) 형식으로 ROI를 지정합니다. (x, y)는 ROI의 좌측 상단 모서리 좌표이며, (w, h)는 ROI의 너비와 높이입니다. 이를 통해 그림자 효과가 이미지의 일부 영역에만 적용되도록 할 수 있습니다.
#     # p: 변환을 적용할 확률입니다. 기본값은 1입니다. 0과 1 사이의 값을 가지며, 이 값이 높을수록 변환을 적용하는 빈도가 높아집니다.
# ])

# shadow_img = transform(image=image)['image']

# visualize(shadow_img)







# #RandomFog
# image = cv2.imread('../data/image02.jpeg')

# transform = A.Compose([
#     A.RandomFog(fog_coef_lower=0.4, fog_coef_upper=0.6, alpha_coef=0.1, p=1)

#     # fog_coef_lower: 안개의 강도(농도)의 최소값입니다. 기본값은 0.4입니다. 안개의 강도는 0과 1 사이의 값을 가지며, 최소값을 지정하여 안개의 약한 효과를 만들 수 있습니다.
#     # fog_coef_upper: 안개의 강도(농도)의 최대값입니다. 기본값은 0.6입니다. 안개의 강도는 0과 1 사이의 값을 가지며, 최대값을 지정하여 안개의 강한 효과를 만들 수 있습니다.
#     # alpha_coef: 안개의 투명도(불투명도)입니다. 기본값은 0.1입니다. 안개의 투명도는 0과 1 사이의 값을 가지며, 작은 값으로 지정할수록 안개의 효과가 뚜렷해집니다.
#     # p: 변환을 적용할 확률입니다. 기본값은 1입니다. 0과 1 사이의 값을 가지며, 이 값이 높을수록 변환을 적용하는 빈도가 높아집니다.

# ])

# fog_img = transform(image=image)['image']

# visualize(fog_img)