import os
import gradio as gr
import pandas as pd
import schedule
import time
import threading
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Importar módulos del proyecto
from src.api.drive_connector import GoogleDriveConnector
from src.models.intent_classifier import IntentClassifier
from src.database.db_manager import DBManager
from src.utils.logger import setup_logger

# Configurar logger
logger = setup_logger()

# Inicializar componentes
drive_connector = GoogleDriveConnector()
intent_classifier = IntentClassifier()
db_manager = DBManager()

# Variable para almacenar la última fecha de modificación
last_modified_time = None

# Función para actualizar datos desde Google Drive
def update_data():
    global last_modified_time
    try:
        # Verificar si el archivo ha sido modificado
        current_modified_time = drive_connector.get_last_modified_time()
        
        if last_modified_time != current_modified_time:
            logger.info("Actualizando datos desde Google Drive...")
            df = drive_connector.get_pqrs_data()
            intent_classifier.load_data(df)
            db_manager.update_cache(df)
            last_modified_time = current_modified_time
            logger.info(f"Datos actualizados correctamente. {len(df)} registros obtenidos.")
        else:
            logger.info("No hay actualizaciones disponibles.")
        return True
    except Exception as e:
        logger.error(f"Error al actualizar datos: {str(e)}")
        return False

# Programar actualización periódica de datos
def schedule_data_updates():
    schedule.every(1).hour.do(update_data)  # Verificar actualizaciones cada hora
    while True:
        schedule.run_pending()
        time.sleep(60)

# Iniciar hilo para actualización de datos
update_thread = threading.Thread(target=schedule_data_updates)
update_thread.daemon = True
update_thread.start()

# Cargar datos iniciales
update_data()

# Función para manejar las consultas de usuario
def process_query(message, history):
    try:
        # Buscar coincidencia en los datos de PQRS
        match, confidence = intent_classifier.classify_query(message)
        
        if match is not None:
            estado = match['estado_respuesta']
            id_consulta = match['ID']
            nombre = match['nombre_usuario']
            
            if estado == 'Respondido':
                response = f"ID consulta #{id_consulta}: Su PQRS ha sido respondida. Por favor revise su correo electrónico para más detalles."
            elif estado == 'En proceso':
                response = f"ID consulta #{id_consulta}: Su PQRS está siendo procesada actualmente por nuestro equipo."
            elif estado == 'Pendiente':
                response = f"ID consulta #{id_consulta}: Su PQRS está en la lista de espera y será atendida pronto."
            else:
                response = "No se encontró información sobre su consulta."
                
            # Registrar interacción
            db_manager.log_interaction(message, response, confidence)
            return response
        else:
            general_response = "No he podido encontrar información específica sobre su consulta. Por favor proporcione más detalles o su número de ID de consulta."
            db_manager.log_interaction(message, general_response, confidence)
            return general_response
            
    except Exception as e:
        logger.error(f"Error al procesar consulta: {str(e)}")
        return "Lo siento, ha ocurrido un error al procesar su consulta. Por favor, inténtelo de nuevo más tarde."

# Interfaz de Gradio
with gr.Blocks(title="SIF - Sistema de Consulta PQRS", theme="soft") as demo:
    gr.Markdown("# SIF - Consulta de PQRS")
    gr.Markdown("### Bienvenido al asistente de consultas PQRS de SIF")
    
    chatbot = gr.Chatbot(height=400)
    msg = gr.Textbox(placeholder="Escriba su consulta aquí...", label="Consulta")
    clear = gr.Button("Limpiar")
    
    msg.submit(process_query, inputs=[msg, chatbot], outputs=[chatbot])
    clear.click(lambda: None, None, chatbot, queue=False)

# Iniciar la aplicación
if __name__ == "__main__":
    demo.launch()