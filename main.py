import subprocess

def txt_to_fasta(txt_file, fasta_file):
    with open(txt_file, 'r') as txt, open(fasta_file, 'w') as fasta:
        next(txt)  # Skip header row
        for line in txt:
            columns = line.strip().split('\t')
            genename, protein_id, sequence = columns[0], columns[1], columns[2]
            fasta.write(f'>{genename}_{protein_id}\n{sequence}\n')

# Convert the file, local
biodata_txt = "biodata.txt"
txt_to_fasta(biodata_txt, 'biodata.fasta')

# FASTA 포맷의 단백질/펩티드 시퀀스 파일 경로
protein_file = "biodata.fasta"

# iFeature.py의 경로
ifeature_path = "iFeature/iFeature.py"

# 추출하려는 특징의 타입
feature_types = ["CTDC", "SSEB", "SSEC", "AAC"]

for feature_type in feature_types:
    # subprocess를 사용하여 iFeature.py를 실행
    output_file = f"{feature_type}_features.csv"
    result = subprocess.run(["python", ifeature_path, "--file", protein_file, "--type", feature_type, "--out", output_file], capture_output=True, text=True)

    # 결과 출력
    print(f"For feature type {feature_type}:")
    print(result.stderr)
    print(result.stdout)
