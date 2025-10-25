from transformers import pipeline

class NerWrapper:
    def __init__(self, model_name: str | None = 'neuralmind/bert-base-portuguese-cased'):
        # default suggested model for PT-BR; change if you have a fine-tuned resume NER
        try:
            self.pipe = pipeline('ner', model=model_name, grouped_entities=True)
        except Exception:
            # fallback to a generic pipeline (will download default HF model)
            self.pipe = pipeline('ner', grouped_entities=True)

    def predict(self, text: str):
        ner = self.pipe(text)
        results = []
        for ent in ner:
            results.append({
                'type': ent.get('entity_group') or ent.get('entity'),
                'text': ent.get('word') or ent.get('entity'),
                'score': float(ent.get('score', 0)),
                'start': ent.get('start'),
                'end': ent.get('end')
            })
        return results
