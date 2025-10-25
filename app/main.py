from fastapi import FastAPI, UploadFile, File, HTTPException, Header, Depends
from fastapi.responses import FileResponse, JSONResponse
import os
from pathlib import Path
from app.ingest import extract_text_from_file
from app.ner import NerWrapper
from app.postprocess import normalize_entities
from app.scoring import score_candidate
from app.db import init_db, save_candidate, get_candidate, save_score, list_candidates
from app.tasks import analyze_resume_task
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY', 'changeme')
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

app = FastAPI(title="Resume Analyzer MVP")

init_db()
ner = NerWrapper()

def api_key_auth(x_api_key: str | None = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail='Invalid API Key')
    return True

@app.post('/upload', dependencies=[Depends(api_key_auth)])
async def upload_file(file: UploadFile = File(...)):
    file_location = UPLOAD_DIR / file.filename
    with open(file_location, 'wb') as f:
        content = await file.read()
        f.write(content)
    return {"file_path": str(file_location)}


@app.post('/analyze', dependencies=[Depends(api_key_auth)])
async def analyze(file: UploadFile | None = File(None), file_path: str | None = None, background: bool = True):
    if file is not None:
        file_location = UPLOAD_DIR / file.filename
        with open(file_location, 'wb') as f:
            content = await file.read()
            f.write(content)
    elif file_path is not None:
        file_location = Path(file_path)
        if not file_location.exists():
            raise HTTPException(status_code=404, detail='file not found')
    else:
        raise HTTPException(status_code=400, detail='file or file_path required')

    candidate_id = save_candidate(str(file_location), {})

    if background:
        analyze_resume_task.delay(candidate_id, str(file_location))
        return {"candidate_id": candidate_id, "status": "processing"}
    else:
        text = extract_text_from_file(str(file_location))
        entities = ner.predict(text)
        normalized = normalize_entities(entities)
        vacancy_profile = {"skills": []}
        score, breakdown = score_candidate(normalized, vacancy_profile)
        save_score(candidate_id, score, breakdown)
        return {"candidate_id": candidate_id, "status": "done", "score": score, "breakdown": breakdown}

@app.get('/results/{candidate_id}', dependencies=[Depends(api_key_auth)])
def results(candidate_id: int):
    rec = get_candidate(candidate_id)
    if not rec:
        raise HTTPException(status_code=404, detail='candidate not found')
    return JSONResponse(content=rec)


@app.get('/download/{candidate_id}', dependencies=[Depends(api_key_auth)])
def download(candidate_id: int):
    rec = get_candidate(candidate_id)
    if not rec:
        raise HTTPException(status_code=404, detail='candidate not found')
    import pandas as pd
    df = pd.DataFrame([rec])
    out = Path('exports')
    out.mkdir(exist_ok=True)
    file_path = out / f'candidate_{candidate_id}.xlsx'
    df.to_excel(file_path, index=False)
    return FileResponse(str(file_path), filename=file_path.name)


@app.get('/candidates', dependencies=[Depends(api_key_auth)])
def list_all():
    return list_candidates()
