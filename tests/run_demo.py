from app.ingest import extract_text_from_file
from app.ner import NerWrapper
from app.postprocess import normalize_entities
from app.scoring import score_candidate

ner = NerWrapper()
SAMPLES = ['tests/samples/sample1.pdf']
for s in SAMPLES:
    try:
        txt = extract_text_from_file(s)
        ents = ner.predict(txt)
        norm = normalize_entities(ents)
        score, breakdown = score_candidate(norm, {'skills': []})
        print('\n', s, '\n', norm, '\nscore=', score, breakdown)
    except Exception as e:
        print('error', e)
