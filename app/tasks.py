from .celery_app import celery_app
from .ingest import extract_text_from_file
from .ner import NerWrapper
from .postprocess import normalize_entities
from .scoring import score_candidate
from .db import save_score
import time

ner = NerWrapper()

@celery_app.task(bind=True)
def analyze_resume_task(self, candidate_id: int, file_path: str):
    try:
        text = extract_text_from_file(file_path)
        entities = ner.predict(text)
        normalized = normalize_entities(entities)
        vacancy_profile = {'skills': []}
        score, breakdown = score_candidate(normalized, vacancy_profile)
        save_score(candidate_id, score, breakdown)
        return {'status': 'done', 'candidate_id': candidate_id}
    except Exception as e:
        return {'status': 'error', 'error': str(e)}
