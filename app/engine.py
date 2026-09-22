import os,json,sqlite3
from datetime import datetime
import requests
PHRASES={"hello":("नमस्ते","namaste","hello"),"water":("जलम्","jalam","water"),"book":("पुस्तकम्","pustakam","book"),"friend":("मित्रम्","mitram","friend"),"today":("अद्य","adya","today"),"I study Sanskrit":("अहं संस्कृतं पठामि।","ahaṃ saṃskṛtaṃ paṭhāmi.","I study Sanskrit"),"I speak Sanskrit":("अहं संस्कृतेन वदामि।","ahaṃ saṃskṛtena vadāmi.","I speak Sanskrit")}
def norm(s): return " ".join(s.lower().strip().replace("।","").split())
class SanskritBot:
 def __init__(self,db="sanskrit_bot.db"):
  self.db=db
  if db!=":memory:":
   with sqlite3.connect(db) as c:c.execute("create table if not exists events(ts text,lang text,kind text,payload text)")
 def log(self,lang,kind,payload):
  if self.db!=":memory:":
   with sqlite3.connect(self.db) as c:c.execute("insert into events values(?,?,?,?)",(datetime.utcnow().isoformat(),lang,kind,json.dumps(payload,ensure_ascii=False)))
 def local(self,text):
  for k,v in PHRASES.items():
   if norm(text) in (norm(k),norm(v[2])): return {"sanskrit":v[0],"iast":v[1],"english":v[2],"mode":"offline"}
 def ai(self,lang,text):
  key=os.getenv("OPENAI_API_KEY")
  if not key:return None
  base=os.getenv("OPENAI_BASE_URL","https://api.openai.com/v1"); model=os.getenv("OPENAI_MODEL","gpt-4o-mini")
  prompt=f'Return JSON keys sanskrit,iast,english,grammar,reply. Translate this {lang} learner input into natural Sanskrit, with Devanagari, IAST, English meaning, grammar note, and Sanskrit reply. Input: {text}'
  r=requests.post(base+"/chat/completions",headers={"Authorization":"Bearer "+key},json={"model":model,"messages":[{"role":"user","content":prompt}],"temperature":0.2},timeout=45)
  r.raise_for_status(); return json.loads(r.json()["choices"][0]["message"]["content"])
 def translate(self,lang,text):
  r=self.local(text)
  if r:return r
  try:
   r=self.ai(lang,text)
   if r:self.log(lang,"translation",r);return r
  except Exception as e:return {"error":str(e)}
  return {"sanskrit":"कृपया पुनः लिखतु।","iast":"kṛpayā punaḥ likhatu.","english":"Please try again with a short sentence.","mode":"offline"}