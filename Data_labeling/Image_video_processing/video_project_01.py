import cv2
import os

from pytube import YouTube
from IPython.display import HTML

url = "https://www.youtube.com/watch?v=0TNFb5zgpbg&list=PL3NgX4uqPt40T1iNoiN9z8CErtWHm06El"

yt = YouTube(url)

stream = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().first()

stream.download("./data/")

HTML("""
     <video width="640 height="480 controls>
        <source src="download_video_by_python.mp4", type="video/mp4>
     </video>
     """
    )

#위에서 다운받은 동영상을 불러온다.
cap = cv2.VideoCapture("./data/저작권 없는 무료 영상 소스 여의도 벚꽃  free video (cherry blossoms).mp4")

# print(cap.get(cv2.CAP_PROP_FRAME_COUNT))
# print(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# print(cap.get(cv2.CAP_PROP_FPS))

#비디오 데이터 프레임 단위로 나눠서 캡쳐하기 실습 -> 동영상 Object Detection에 사용
os.makedirs("./data/video_frame_dataset", exist_ok=True)

img_count = 0
while True:
    ret, frame = cap.read()
    
    if not ret:
        break
    
    if img_count % 15 == 0:
        img_filename = f"./data/video_frame_dataset/frame_{img_count:04}.png"
        #img_count:04 : 뒤에 숫자는 4자리로 맞추는 설정
        cv2.imwrite(img_filename, frame)
        
    img_count += 1
        
cap.release()