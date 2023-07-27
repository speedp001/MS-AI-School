import cv2
import os
import json
import glob
from tqdm import tqdm



# JSON 파일들을 순회하면서 동영상 파일을 읽어와 원하는 프레임들을 이미지로 저장하는 작업을 수행합니다.

#JSON 동영상 파일 읽기
json_dir = "./data/raw_data/json/Stealing_Courier/"
json_path_list = glob.glob(os.path.join(json_dir, "*.json"))
#print(json_path_list)


video_dir = "./data/raw_data/video/Stealing_Courier/"

for json_path in json_path_list :
    
    #json read
    with open(json_path, 'r', encoding='utf-8') as f:
        
        json_data = json.load(f)
        
        #json metadata
        metadata_info = json_data['metadata']
        #print(metadata_info)
        
        file_name = metadata_info['filename']
        #print(file_name)
        
        #video pull path
        video_path = os.path.join(video_dir, file_name)
        #print(video_path)
        
        #json Categories data info
        categories_info = json_data['categories']
        #print(categories_info)
        
        #crime, action, symptom 확인
        crime_info = categories_info['crime']
        action_info = categories_info['action']
        symptom_info = categories_info['symptom']
        #print(crime_info, action_info, symptom_info)
        
        #video read
        cap = cv2.VideoCapture(video_path)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        
        file_info = json_data['file']
        folder_name = video_path.split("/")[4]
        #print(folder_name)
        image_name = file_name.replace(".mp4", "")
        #print(image_name)
        
        for i in file_info :
            videos_info = i['videos']
            block_info = videos_info['block_information']
            
            count = 0
            for j in block_info :
                
                # A30인 경우만 해당 프레임과 시간확인
                if j['block_detail'] == 'A30':
                    start_time = j['start_time']
                    end_time = j['end_time']
                    start_frame_index = j['start_frame_index']
                    end_frame_index = j['end_frame_index']

                    print(start_time, end_time)
                    print(start_frame_index, end_frame_index)
                    
                    ######################################################
                    
                    for frame_idx in range(int(start_frame_index), int(end_frame_index), 30) : 
                        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
                        
                        ret, frame = cap.read()
                        
                        if ret : 
                            os.makedirs(f"./data/AI_hub_dataset/{folder_name}/{image_name}/", exist_ok=True )
                            image_name_temp = f"./data/AI_hub_dataset/{folder_name}/{image_name}/{image_name}_frame_{str(count).zfill(4)}.png"

                            cv2.imwrite(image_name_temp, frame)
                            count = count + 1
                            
                    print("다운로드 완료", image_name)
    
    