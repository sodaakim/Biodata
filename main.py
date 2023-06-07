import subprocess
import os
import pandas as pd
from sklearn.model_selection import train_test_split

# 데이터 로드
data = pd.read_csv('data.txt', sep='\t')

# 데이터 분할 (90% for biodata, 10% for testdata)
biodata, testdata = train_test_split(data, test_size=0.35, random_state=30)

# 인덱스 재설정
biodata.reset_index(drop=True, inplace=True)
testdata.reset_index(drop=True, inplace=True)

# 저장할 디렉토리 지정
data_dir = "[0] data"
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# txt 파일로 저장
biodata.to_csv(os.path.join(data_dir, 'biodata.txt'), sep='\t', index=False)
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
modeldata_txt = data_dir + "/biodata.txt"
txt_to_fasta(modeldata_txt, model_dir + '/biodata.fasta') # convert file
model_file = model_dir + "/biodata.fasta" # FASTA 포맷의 단백질/펩티드 시퀀스 파일 경로


for feature_type in feature_types:
    # subprocess를 사용하여 iFeature.py를 실행
    output_file = model_dir + f"/{feature_type}_features_model.csv"
    result = subprocess.run(
        ["python", ifeature_path, "--file", model_file, "--type", feature_type, "--out", output_file],
        capture_output=True, text=True)

    # 결과 출력
    print(f"For feature type {feature_type}:")
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
