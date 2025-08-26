# SIF-PQRS - Sistema Conversacional Inteligente

Este proyecto implementa un chatbot para consultas de PQRS (Peticiones, Quejas, Reclamos y Sugerencias) de la entidad pública SIF, utilizando una interfaz Gradio y sincronización con datos de SharePoint.

## Características

- Chat conversacional inteligente con procesamiento de lenguaje natural
- Interfaz web con Gradio para fácil acceso y uso
- Sincronización automática con hojas de cálculo en SharePoint
- Sistema de respuestas basado en estado actual de las PQRS
- Registro de interacciones para mejora continua

## Instalación

1. Clonar este repositorio:
```bash
git clone https://github.com/sif-entidad/pqrs-chatbot.git
cd pqrs-chatbot
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
python -m spacy download es_core_news_md
```

3. Configurar variables de entorno:
   - Copiar el archivo `.env.example` a `.env`
   - Completar las credenciales y configuraciones necesarias

## Uso

Para iniciar la aplicación:

```bash
python app.py
```

El servicio estará disponible en `http://localhost:7860`

## Estructura del Proyecto

- `/src`: Código fuente principal
  - `/api`: Conexiones a APIs externas (SharePoint)
  - `/models`: Modelos de IA para procesamiento de consultas
  - `/database`: Gestión de datos y cache
- `/data`: Almacenamiento de datos procesados
- `/assets`: Recursos visuales
- `/templates`: Plantillas de respuestas

## Contribución

Para contribuir a este proyecto:

1. Crear un fork del repositorio
2. Crear una rama para su característica (`git checkout -b feature/nueva-caracteristica`)
3. Hacer commit de sus cambios (`git commit -m 'Añadir nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Abrir un Pull Request

## Licencia

Este proyecto es propiedad de SIF y su uso está restringido según los términos establecidos por la entidad.