import numpy as np
import imgaug.augmenters as iaa # ImgAug Augmenters
import cv2
import matplotlib.pyplot as plt

image = cv2.imread("/Users/sang-yun/Desktop/Jupyter/Data_labeling/data/sample_data_01/train/snow/0830.jpg")

images = [image, image, image, image]





# rotate = iaa.Affine(rotate=(-25, 25))
# #-25에서 25사이에서 랜덤으로 회전 실행
# images_aug = rotate(images=images)

# plt.figure(figsize=(12,12))
# plt.imshow(np.hstack(images_aug))
# plt.show()




# crop = iaa.Crop(percent=(0, 0.2))
# #0.2로 설정되어 있다면 이미지의 가로 또는 세로 방향으로 20%까지 잘라내는 것을 의미합니다.
# images_aug01 = crop(images=images)

# plt.figure(figsize=(12,12))
# plt.imshow(np.hstack(images_aug01))
# plt.show()






# rotate_crop = iaa.Sequential([
#     #iaa.Sequential은 imgaug에서 제공하는 시퀀스 기반의 이미지 강화를 적용하기 위한 클래스입니다. 시퀀셜을 사용하면 여러 개의 이미지 변환을 순차적으로 적용할 수 있습니다.
#     iaa.Affine(rotate=(-25, 25)),
#     iaa.Crop(percent=(0, 0.2))
# ], random_order=True)
# images_aug02 = rotate_crop(images=images)
# plt.figure(figsize=(12,12))
# plt.imshow(np.hstack(images_aug02))
# plt.show()






# seq = iaa.OneOf([
#     #이중에 하나만 실행
#     iaa.Grayscale(alpha=(0.0, 1.0)),
#     iaa.AddToSaturation((-50, 50))
# ])
# images_aug04 = seq(images=images)

# plt.figure(figsize=(12,12))
# plt.imshow(np.hstack(images_aug04))
# plt.show()







seq = iaa.Sequential([
    iaa.Sometimes(
        0.6,
        iaa.AddToSaturation((-50, 50))
    ),
    iaa.Sometimes(
        0.2,
        iaa.Grayscale(alpha=(0.0, 1.0))
    )
])
images_aug05 = seq(images=images)

plt.figure(figsize=(12,12))
plt.imshow(np.hstack(images_aug05))
plt.show()