# sharepoint_connector.py
# Conexión y autenticación con SharePoint
import os
import pandas as pd
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File

class SharePointConnector:
    def __init__(self):
        self.site_url = os.environ.get("SHAREPOINT_SITE_URL")
        self.username = os.environ.get("SHAREPOINT_USERNAME")
        self.password = os.environ.get("SHAREPOINT_PASSWORD")
        self.file_path = os.environ.get("SHAREPOINT_FILE_PATH")
        
    def authenticate(self):
        auth_context = AuthenticationContext(self.site_url)
        auth_context.acquire_token_for_user(self.username, self.password)
        return ClientContext(self.site_url, auth_context)
    
    def get_pqrs_data(self):
        """Obtiene los datos de PQRS desde SharePoint"""
        ctx = self.authenticate()
        response = File.open_binary(ctx, self.file_path)
        
        # Guardar archivo temporalmente
        with open("temp_pqrs_data.xlsx", "wb") as local_file:
            local_file.write(response.content)
        
        # Leer con pandas
        df = pd.read_excel("temp_pqrs_data.xlsx")
        os.remove("temp_pqrs_data.xlsx")
        
        return df