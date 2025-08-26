import spacy
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class IntentClassifier:
    def __init__(self):
        self.nlp = spacy.load('es_core_news_md')  # Modelo en español
        self.vectorizer = TfidfVectorizer()
        self.pqrs_data = None
        self.vectorized_data = None
        
    def load_data(self, df):
        """Carga los datos de PQRS y los preprocesa"""
        self.pqrs_data = df
        questions = df['informacion_usuario'].tolist()
        self.vectorized_data = self.vectorizer.fit_transform(questions)
        
    def classify_query(self, user_query, threshold=0.6):
        """Clasifica la consulta del usuario y busca la mejor coincidencia"""
        query_vec = self.vectorizer.transform([user_query])
        similarities = cosine_similarity(query_vec, self.vectorized_data)[0]
        
        best_match_idx = np.argmax(similarities)
        max_similarity = similarities[best_match_idx]
        
        if max_similarity >= threshold:
            return self.pqrs_data.iloc[best_match_idx], max_similarity
        else:
            return None, max_similarity