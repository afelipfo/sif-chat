import os
import pandas as pd
import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account

class GoogleDriveConnector:
    def __init__(self):
        self.credentials_path = os.environ.get("GOOGLE_CREDENTIALS_PATH")
        self.file_id = os.environ.get("GOOGLE_DRIVE_FILE_ID")
        
    def authenticate(self):
        """Autentica con la API de Google Drive"""
        credentials = service_account.Credentials.from_service_account_file(
            self.credentials_path, 
            scopes=['https://www.googleapis.com/auth/drive.readonly']
        )
        service = build('drive', 'v3', credentials=credentials)
        return service
    
    def get_pqrs_data(self):
        """Obtiene los datos de PQRS desde Google Drive"""
        service = self.authenticate()
        
        # Descargar archivo
        request = service.files().get_media(fileId=self.file_id)
        file_handle = io.BytesIO()
        downloader = MediaIoBaseDownload(file_handle, request)
        
        done = False
        while not done:
            status, done = downloader.next_chunk()
        
        file_handle.seek(0)
        
        # Detectar formato del archivo
        if self.file_id.endswith('.xlsx') or self.file_id.endswith('.xls'):
            df = pd.read_excel(file_handle)
        else:  # Asumimos que es CSV si no es Excel
            df = pd.read_csv(file_handle)
        
        return df
    
    def get_last_modified_time(self):
        """Obtiene la última fecha de modificación del archivo"""
        service = self.authenticate()
        file_metadata = service.files().get(fileId=self.file_id, fields='modifiedTime').execute()
        return file_metadata.get('modifiedTime')