import subprocess
import os
import pandas as pd
from sklearn.model_selection import train_test_split

# 데이터 로드
data = pd.read_csv('data.txt', sep='\t')

#------------------------------------------------------------------

# 데이터 분할 (90% for biodata, 10% for testdata)
biodata, testdata = train_test_split(data, test_size=0.1, random_state=23)

# 인덱스 재설정
biodata.reset_index(drop=True, inplace=True)
testdata.reset_index(drop=True, inplace=True)

# 저장할 디렉토리 지정
data_dir = "[0] data"
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# 데이터 분할 개수
num_splits = 5

# 데이터 분할 크기
split_size = len(biodata) // num_splits

# 데이터 분할 및 저장
for i in range(num_splits):
    start_idx = i * split_size
    end_idx = (i + 1) * split_size if i < num_splits - 1 else len(biodata)

    split_data = biodata[start_idx:end_idx]
    split_data.to_csv(os.path.join(data_dir, f'biodata_split{i + 1}.txt'), sep='\t', index=False)

# 테스트 데이터 저장
testdata.to_csv(os.path.join(data_dir, 'testdata.txt'), sep='\t', index=False)

# dir
#------------------------------------------------------------------

model_dir = "[1] modeldata_iFeature"
os.makedirs(model_dir, exist_ok=True)

test_dir = "[2] testdata_iFeature"
os.makedirs(test_dir, exist_ok=True)

# function
#------------------------------------------------------------------
def txt_to_fasta(txt_file, fasta_file):
    with open(txt_file, 'r') as txt, open(fasta_file, 'w') as fasta:
        next(txt)  # Skip header row
        for line in txt:
            columns = line.strip().split('\t')
            genename, protein_id, sequence = columns[0], columns[1], columns[2]
            fasta.write(f'>{genename}_{protein_id}\n{sequence}\n')


ifeature_path = "iFeature/iFeature.py"
feature_types = ["CTDC", "AAC"]
# "DPC", "DDE"

# model data
#------------------------------------------------------------------
for i in range(num_splits):
    split_txt_file = os.path.join(data_dir, f'biodata_split{i+1}.txt')
    split_fasta_file = os.path.join(model_dir, f'biodata_split{i+1}.fasta')

    # txt 파일을 fasta 파일로 변환
    txt_to_fasta(split_txt_file, split_fasta_file)

    for feature_type in feature_types:
        # iFeature를 실행하여 특징 추출
        output_file = os.path.join(model_dir, f"{feature_type}_features_model_split{i+1}.csv")
        result = subprocess.run(
            ["python", ifeature_path, "--file", split_fasta_file, "--type", feature_type, "--out", output_file],
            capture_output=True, text=True)

        # 결과 출력
        print(f"For feature type {feature_type}, split {i+1}:")
        print(result.stderr)
        print(result.stdout)


# test data
#------------------------------------------------------------------
testdata_txt = data_dir + "/testdata.txt"
txt_to_fasta(testdata_txt, test_dir + '/testdata.fasta') # convert file
test_file = test_dir + "/testdata.fasta" # FASTA 포맷의 단백질/펩티드 시퀀스 파일 경로

for feature_type in feature_types:
    # subprocess를 사용하여 iFeature.py를 실행
    output_file = test_dir + f"/{feature_type}_features_test.csv"
    result = subprocess.run(
        ["python", ifeature_path, "--file", test_file, "--type", feature_type, "--out", output_file],
        capture_output=True, text=True)
