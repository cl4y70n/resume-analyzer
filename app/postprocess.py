import re
from collections import defaultdict

PHONE_RE = re.compile(r"(\+?\d[\d\s().-]{6,}\d)")
EMAIL_RE = re.compile(r"[\w\.-]+@[\w\.-]+")

def normalize_entities(entities_raw):
    out = defaultdict(list)
    for e in entities_raw:
        t = e.get('type', '').upper()
        txt = e.get('text')
        if not txt:
            continue
        if t in ['PER', 'PERSON', 'NAME']:
            out['name'].append(txt)
        elif t in ['ORG', 'COMPANY']:
            out['companies'].append(txt)
        elif t in ['SKILL', 'MISC', 'OTHER']:
            out['skills'].append(txt)
        elif t in ['DATE']:
            out['dates'].append(txt)
        else:
            out['other'].append({'type': t, 'text': txt})
    for k in list(out.keys()):
        out[k] = list(dict.fromkeys(out[k]))
    return dict(out)
