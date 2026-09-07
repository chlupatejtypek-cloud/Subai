#!/usr/bin/env python3
"""One-session YouTube OAuth connector. Never logs codes, tokens or client secrets.
Desktop loopback redirect is copied manually from the owner's browser, not OOB OAuth.
Token is local in .git/credentials (excluded from workspace snapshots); no durable
session persistence is promised. Run again after environment loss.
"""
import base64,hashlib,json,os,secrets,urllib.parse
from pathlib import Path
from http.server import BaseHTTPRequestHandler,HTTPServer
import requests
ROOT=Path(__file__).resolve().parents[1]
CLIENT=json.loads((ROOT/'credentials/youtube-client.json').read_text())['installed']
TOKEN=ROOT/'.git/credentials'
STATE=secrets.token_urlsafe(32); VERIFIER=secrets.token_urlsafe(64)
ACCESS=secrets.token_urlsafe(24)
REDIRECT='http://localhost:8765/'
SCOPES='https://www.googleapis.com/auth/youtube.upload https://www.googleapis.com/auth/youtube.readonly'
AUTH='https://accounts.google.com/o/oauth2/v2/auth?'+urllib.parse.urlencode({'client_id':CLIENT['client_id'],'redirect_uri':REDIRECT,'response_type':'code','scope':SCOPES,'state':STATE,'access_type':'offline','prompt':'consent','code_challenge':base64.urlsafe_b64encode(hashlib.sha256(VERIFIER.encode()).digest()).decode().rstrip('='),'code_challenge_method':'S256'})
DONE=False
PAGE='''<!doctype html><html lang="cs"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Připojit YouTube · Subai</title><style>body{background:#101b24;color:#edf1ef;font:17px system-ui;max-width:740px;margin:60px auto;padding:24px}h1{font-size:38px}p{line-height:1.7;color:#c0ccd1}a,button{background:#f7c369;border:0;border-radius:10px;color:#17222a;padding:15px 22px;font-weight:700;text-decoration:none;display:inline-block;cursor:pointer}textarea{box-sizing:border-box;width:100%;min-height:120px;background:#1d303d;border:1px solid #587080;color:white;padding:15px;border-radius:10px;font:14px monospace}section{background:#172733;padding:24px;border-radius:18px;margin:20px 0}.note{font-size:14px}#result{white-space:pre-wrap}</style><h1>Připojit YouTube</h1><p>Stiles Psychology / Subai — propojení účtu, nikoli zveřejnění videa.</p><section><h2>1. Přihlas se u Googlu</h2><p>Vyber účet a případně správný značkový kanál. Povol nahrávání videí a čtení kanálu. Oprávnění čtení používáme k ověření, kam se bude nahrávat.</p><a href="AUTH_URL" target="_blank" rel="noreferrer">Otevřít Google přihlášení ↗</a></section><section><h2>2. Vlož návratovou adresu</h2><p>Po souhlasu se otevře <b>localhost:8765</b> a může ukázat chybu připojení. Zkopíruj <b>celou adresu z adresního řádku</b> a vlož ji sem. Neodesílej ji do chatu.</p><textarea id="callback" spellcheck="false" placeholder="http://localhost:8765/?state=…&code=…"></textarea><p><button id="connect">Dokončit připojení</button></p><div id="result" role="status"></div></section><p class="note">Tato jednorázová stránka ukládá token pouze do chráněného souboru prostředí agenta, mimo Git a veřejné výstupy. Po zániku prostředí může být nutné přihlášení opakovat. Přístup lze kdykoliv odvolat v nastavení Google účtu. Pokud Google hlásí access_denied, přidej svůj účet mezi testovací uživatele projektu. Nepřecházej přes varování, pokud nesouhlasí tvůj vlastní OAuth projekt.</p><script>document.getElementById('connect').onclick=async()=>{let b=document.getElementById('connect'),r=document.getElementById('result');b.disabled=true;r.textContent='Ověřuji připojení…';try{let v=await fetch(location.pathname,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({callback:document.getElementById('callback').value})});let j=await v.json();r.textContent=j.message;if(j.ok)document.getElementById('callback').value='';else b.disabled=false;}catch(e){r.textContent='Připojení se nepodařilo. Zkus znovu.';b.disabled=false;}};</script></html>'''
class Handler(BaseHTTPRequestHandler):
 def log_message(self,*a):pass
 def reply(self,status,body,typ='application/json'):
  self.send_response(status);self.send_header('Content-Type',typ+'; charset=utf-8');self.send_header('Cache-Control','no-store');self.send_header('Referrer-Policy','no-referrer');self.end_headers();self.wfile.write(body.encode())
 def do_GET(self):
  if self.path=='/':
   self.send_response(302);self.send_header('Location','/'+ACCESS);self.send_header('Cache-Control','no-store');self.end_headers();return
  if self.path!='/'+ACCESS:return self.reply(404,'Not found','text/plain')
  self.reply(200,PAGE.replace('AUTH_URL',AUTH.replace('&','&amp;')),'text/html')
 def do_POST(self):
  global DONE
  if self.path!='/'+ACCESS:return self.reply(404,'{}')
  try:
   if DONE:raise ValueError('Účet je již připojen. Další autorizace nebyla provedena.')
   n=int(self.headers.get('Content-Length',0))
   if n>16000:raise ValueError('Příliš dlouhá adresa.')
   url=urllib.parse.urlparse(json.loads(self.rfile.read(n))['callback'].strip());q=urllib.parse.parse_qs(url.query)
   if url.scheme!='http' or url.hostname!='localhost' or url.port!=8765 or url.path!='/':raise ValueError('Vlož celou návratovou adresu http://localhost:8765/ z této autorizace.')
   if not secrets.compare_digest(q.get('state',[''])[0],STATE):raise ValueError('Nesouhlasí ověření state. Otevři přihlášení znovu tlačítkem na této stránce.')
   if 'error' in q:raise ValueError('Google přístup nepovolil. Zkontroluj testovací uživatele a oprávnění projektu.')
   code=q.get('code',[''])[0]
   if not code:raise ValueError('V adrese chybí autorizační kód.')
   r=requests.post('https://oauth2.googleapis.com/token',data={'client_id':CLIENT['client_id'],'client_secret':CLIENT['client_secret'],'code':code,'code_verifier':VERIFIER,'redirect_uri':REDIRECT,'grant_type':'authorization_code'},timeout=40)
   if r.status_code!=200:raise ValueError('Google odmítl výměnu kódu (HTTP '+str(r.status_code)+'). Kód může být prošlý nebo již použitý; začni přihlášení znovu.')
   token=r.json()
   if not token.get('refresh_token'):raise ValueError('Google nevrátil obnovovací token; zopakuj souhlas s offline přístupem.')
   granted=set(token.get('scope','').split())
   if not set(SCOPES.split()).issubset(granted):raise ValueError('Nebyla udělena obě požadovaná oprávnění. Zopakuj souhlas.')
   check=requests.get('https://www.googleapis.com/youtube/v3/channels',params={'part':'snippet','mine':'true'},headers={'Authorization':'Bearer '+token['access_token']},timeout=30)
   channel=None
   if check.status_code==200:
    items=check.json().get('items',[])
    if items:channel={'id':items[0]['id'],'title':items[0]['snippet']['title']}
   record={'token':token,'channel':channel,'client_id':CLIENT['client_id']}
   fd=os.open(TOKEN,os.O_WRONLY|os.O_CREAT|os.O_TRUNC,0o600)
   with os.fdopen(fd,'w') as f:json.dump(record,f)
   os.chmod(TOKEN,0o600);DONE=True
   msg=('Připojeno: '+channel['title']+'\nID kanálu: '+channel['id'] if channel else 'Token je uložen, ale kanál se zatím nepodařilo ověřit (YouTube API HTTP '+str(check.status_code)+'). Zkontrolujeme aktivaci YouTube Data API v3 a existenci kanálu.')
   print('OAUTH_COMPLETE '+(json.dumps(channel,ensure_ascii=False) if channel else 'channel_unverified'),flush=True)
   self.reply(200,json.dumps({'ok':True,'message':msg+'\nNic nebylo nahráno ani zveřejněno.'}))
  except ValueError as e:self.reply(400,json.dumps({'ok':False,'message':str(e)}))
  except Exception:self.reply(500,json.dumps({'ok':False,'message':'Síťová nebo interní chyba. Žádné přihlašovací údaje nebyly vypsány. Zkus znovu.'}))
if __name__=='__main__':
 print('CONNECT_PATH=/'+ACCESS,flush=True)
 HTTPServer(('0.0.0.0',8080),Handler).serve_forever()
