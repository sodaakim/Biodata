import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account

# 구글 드라이브 API 인증 정보를 포함한 서비스 계정 키 파일 경로
SERVICE_ACCOUNT_FILE = '/path/to/service-account-file.json'

# 파일을 업로드할 구글 드라이브 폴더 ID
DRIVE_FOLDER_ID = 'your-folder-id'

# 업로드할 로컬 파일 경로
LOCAL_FILE_PATH = '/home/user/Documents/example.txt'

# 구글 드라이브 API 서비스 객체 생성
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/drive'])
drive_service = build('drive', 'v3', credentials=credentials)

# 업로드할 파일의 메타데이터 생성
file_metadata = {
    'name': os.path.basename(LOCAL_FILE_PATH),
    'parents': [DRIVE_FOLDER_ID]
}

# 파일 업로드를 위한 MediaFileUpload 객체 생성
media = MediaFileUpload(LOCAL_FILE_PATH)

# 파일 업로드 요청
uploaded_file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

# 업로드된 파일의 ID 출력
print('File ID:', uploaded_file['id'])
