import cv2
import os





# ######비디오 정보 읽기
# cap = cv2.VideoCapture("./Dataset_construction/data/blooms-113004.mp4")

# # 비디오 정보 가져오기
# width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
# height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
# fps = cap.get(cv2.CAP_PROP_FPS)
# frmae_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)

# # 비디오 정보 보기
# print(f"Oringinal width and height : {width}x{height}")
# print(f"fps : {fps}")
# print(f"fram count : {frmae_count}")

# """
# 결과
# Oringinal width and height : 1920x1080
# fps : 29.97002997002997
# fram count : 751.0
# """



















# ######비디오 파일 읽기 및 비디오 리사이즈
# cap = cv2.VideoCapture("./Dataset_construction/data/blooms-113004.mp4")

# # 비디오 정보 가져오기
# width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
# height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
# fps = cap.get(cv2.CAP_PROP_FPS)
# frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)

# # 비디오 정보 출력
# print(width, height, fps, frame_count)

# # 동영상 파일 읽기 예시
# if cap.isOpened():  # 캡처 객체 초기화 확인
#     print("캡처 객체 초기화 확인")
#     while True:
#         ret, frame = cap.read()  # 다음 프레임 읽기
#         # ret -> 프레임 읽기가 성공했는지를 나타내는 부울 값
#         # frame -> 이미지 numpy 배열 형태 -> 픽셀 정보
#         if not ret:  # 프레임 읽기 실패 시 루프 종료
#             break
#         else:  # 프레임 읽기 성공 시 루프 실행
#             # 프레임 크기 조정 -> 영상 크기 수정
#             frame = cv2.resize(frame, (640, 480))
#             # print(frame.shape) # (480, 640, 3)
#             cv2.imshow("video test", frame)  # 화면 표시
#             # q 버튼을 누르면 종료
#             if cv2.waitKey(25) & 0xFF == ord("q"):
#                 exit()
# else:
#     print("캡처 객체 초기화 실패 !!")

# # 카메라 자원 반납
# cap.release()
# cv2.destroyAllWindows()















# ###### Webcam을 이용해서 비디오 재생
# cap = cv2.VideoCapture(0)

# width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
# height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
# print(width, height)
# # 1280 x 720 -> 종횡비에 맞게 이미지 크기 수정 16:9 -> 854×480

# while True:
#     ret, frame = cap.read()
#     if ret:
#         # 화면 사이즈 조절
#         frame = cv2.resize(frame, (854, 480))

#         cv2.imshow("Webcam", frame)

#         if cv2.waitKey(1) == ord("q"):
#             break

# cap.release()
# cv2.destroyAllWindows()














# ###### 25FPS 기준으로 프레임 나눠서 저장
# # 비디오 파일 읽기
# cap = cv2.VideoCapture("../data/blooms-113004.mp4")

# # FPS 지정
# fps = 25

# count = 0
# if cap.isOpened():
#     while True:
#         ret, frame = cap.read()

#         if ret:
#             if int(cap.get(1)) % fps == 0:
#                 # fps 25
#                 cv2.imwrite(
#                     f"../data/image_{str(count).zfill(4)}.png", frame
#                 )

#                 count = count + 1

#         else:
#             break

# cap.release()
# cv2.destroyAllWindows()
