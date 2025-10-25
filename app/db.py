from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text
from sqlalchemy.sql import select, insert
import json
import os

DB_URL = os.getenv('DATABASE_URL', 'sqlite:///resume_analyzer.db')
engine = create_engine(DB_URL, echo=False)
metadata = MetaData()

candidates = Table(
    'candidates', metadata,
    Column('id', Integer, primary_key=True),
    Column('file_path', String, nullable=False),
    Column('data', Text),
)

scores = Table(
    'scores', metadata,
    Column('id', Integer, primary_key=True),
    Column('candidate_id', Integer),
    Column('score', String),
    Column('breakdown', Text),
)

def init_db():
    metadata.create_all(engine)

def save_candidate(file_path: str, data: dict) -> int:
    j = json.dumps(data, ensure_ascii=False)
    with engine.connect() as conn:
        res = conn.execute(insert(candidates).values(file_path=file_path, data=j))
        conn.commit()
        return res.inserted_primary_key[0]

def save_score(candidate_id: int, score: float, breakdown: dict):
    with engine.connect() as conn:
        conn.execute(insert(scores).values(candidate_id=candidate_id, score=str(score), breakdown=json.dumps(breakdown, ensure_ascii=False)))
        conn.commit()

def get_candidate(candidate_id: int):
    with engine.connect() as conn:
        q = select(candidates).where(candidates.c.id == candidate_id)
        r = conn.execute(q).mappings().first()
        if not r:
            return None
        data = json.loads(r['data'])
        data_out = {'id': r['id'], 'file_path': r['file_path'], **data}
        q2 = select(scores).where(scores.c.candidate_id == candidate_id)
        s = conn.execute(q2).mappings().first()
        if s:
            data_out['score'] = float(s['score'])
            data_out['breakdown'] = json.loads(s['breakdown'])
        return data_out

def list_candidates():
    with engine.connect() as conn:
        q = select(candidates)
        rows = conn.execute(q).mappings().all()
        out = []
        import json
        for r in rows:
            try:
                data = json.loads(r['data'])
            except:
                data = {}
            out.append({'id': r['id'], 'file_path': r['file_path'], **data})
        return out
