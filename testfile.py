# no label : for test

import subprocess
import os
import pandas as pd
from sklearn.model_selection import train_test_split

# 데이터 로드
LearningData = pd.read_csv('data.txt', sep='\t')
TestData = pd.read_csv('predict.txt', sep='\t')

# 저장할 디렉토리 지정
data_dir = "[4] predict"
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# txt 파일로 저장
LearningData.to_csv(os.path.join(data_dir, 'LearningData.txt'), sep='\t', index=False)
TestData.to_csv(os.path.join(data_dir, 'TestData.txt'), sep='\t', index=False)

# function
#------------------------------------------------------------------
def txt_to_fasta(txt_file, fasta_file):
    with open(txt_file, 'r') as txt, open(fasta_file, 'w') as fasta:
        next(txt)  # Skip header row
        for line in txt:
            columns = line.strip().split('\t')
            genename, protein_id, sequence = columns[0], columns[1], columns[2]
            fasta.write(f'>{genename}_{protein_id}\n{sequence}\n')

def test_fasta(txt_file, fasta_file):
    with open(txt_file, 'r') as txt, open(fasta_file, 'w') as fasta:
        i = 1
        for sequence in txt:
            fasta.write(f'>Protein_{i}\n{sequence}\n')
            i += 1

ifeature_path = "iFeature/iFeature.py"
feature_types = ["CTDC", "AAC"]

# "DPC", "DDE"

# LearningData
#------------------------------------------------------------------
modeldata_txt = data_dir + "/LearningData.txt"
txt_to_fasta(modeldata_txt, data_dir + '/LearningData.fasta') # convert file
model_file = data_dir + "/LearningData.fasta" # FASTA 포맷의 단백질/펩티드 시퀀스 파일 경로


for feature_type in feature_types:
    # subprocess를 사용하여 iFeature.py를 실행
    output_file = data_dir + f"/{feature_type}_features_model.csv"
    result = subprocess.run(
        ["python", ifeature_path, "--file", model_file, "--type", feature_type, "--out", output_file],
        capture_output=True, text=True)

    # 결과 출력
    print(f"For feature type {feature_type}:")
    print(result.stderr)
    print(result.stdout)

# TestData
#------------------------------------------------------------------
testdata_txt = data_dir + "/TestData.txt"
test_fasta(testdata_txt, data_dir + '/TestData.fasta') # convert file
test_file = data_dir + "/TestData.fasta" # FASTA 포맷의 단백질/펩티드 시퀀스 파일 경로


for feature_type in feature_types:
    # subprocess를 사용하여 iFeature.py를 실행
    output_file = data_dir + f"/{feature_type}_features_test.csv"
    result = subprocess.run(
        ["python", ifeature_path, "--file", test_file, "--type", feature_type, "--out", output_file],
        capture_output=True, text=True)

    # 결과 출력
    print(f"For feature type {feature_type}:")
    print(result.stderr)
    print(result.stdout)