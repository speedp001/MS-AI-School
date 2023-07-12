import torch
from torch.utils.data import Dataset, DataLoader




class HeightWeightDataset(Dataset):
    
    def __init__(self, csv_path):
        self.data = []
        
        #csv_path경로의 파일을 읽기모드로 열고 객체를 f에 담는다.
        with open(csv_path, 'r', encoding='utf-8') as f:
            next(f)
            #건너뛰기(다음 줄 이동)
            #첫 번째 라인은 헤더이므로 제외
            for line in f:
                #print(line)
                _, height, weight = line.strip().split(",")
                #strip() 앞뒤 공백 제거 후 split()문자열 구분
                height = float(height)
                weight = float(weight)
                #round()함수는 뒤에 소수점 몇재짜리까지 반올림하여 나타내는지 인자값을 주면 반환해주는 함수
                convert_to_kg_data = round(self.convert_to_kg(weight), 2)
                convert_to_cm_data = round(self.inch_to_cm(height), 1)
                
                #csv파일을 읽고 변형한 데이터들을 선언한 self.data 배열안에 추가
                self.data.append([convert_to_cm_data, convert_to_kg_data])
        
    def __getitem__(self, index):
        data = torch.tensor(self.data[index], dtype=torch.float)
        return data
    
    def __len__(self):
        return len(self.data)
        
    def convert_to_kg(self, weight_lb):
        return weight_lb * 0.453592
    
    def inch_to_cm(self, inch):
        return inch * 2.54
        
        
    
    
    
    
    
if __name__ == "__main__":
    dataset = HeightWeightDataset("./data/hw_200.csv")
    dataloader = DataLoader(dataset, batch_size=1, shuffle=True)
    
    for batch in dataloader:
        x = batch[:, 0].unsqueeze(1)
        y = batch[:, 1].unsqueeze(1)
        print(x, y)