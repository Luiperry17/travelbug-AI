"""Monitor public JSON feeds explicitly authorized by their publishers.
Feed format: [{"id":"...","title":"...","kind":"flight|hotel", "price":123,
"currency":"EUR", "date":"2027-02-01", "url":"https://..."}]
Only EUR prices are compared; no exchange-rate assumptions.
"""
import json, os, pathlib, statistics, urllib.request, urllib.parse
from datetime import datetime, timezone
ROOT=pathlib.Path(__file__).parent

def load(path, default):
    try: return json.loads(path.read_text(encoding='utf-8'))
    except (FileNotFoundError, ValueError): return default

def save(path,obj): path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def valid_url(u):
    try: return urllib.parse.urlsplit(u).scheme=='https' and bool(urllib.parse.urlsplit(u).hostname)
    except (TypeError,ValueError): return False

def notify(message):
    token=os.getenv('TELEGRAM_BOT_TOKEN','');chat=os.getenv('TELEGRAM_CHAT_ID','')
    if not (token and chat): return
    data=urllib.parse.urlencode({'chat_id':chat,'text':message,'disable_web_page_preview':'true'}).encode()
    req=urllib.request.Request('https://api.telegram.org/bot'+token+'/sendMessage',data=data,method='POST')
    try:
        with urllib.request.urlopen(req,timeout=15): pass
    except Exception as exc: print('Telegram error:',exc)

def main():
    sources=load(ROOT/'sources.json',[]); history=load(ROOT/'data/history.json',{}); previous=load(ROOT/'data/deals.json',[])
    deals=[]; alerts=[]
    for src in sources:
        url=src.get('url',''); name=src.get('name','Fonte')
        if not valid_url(url): print('Skipping invalid source',name);continue
        try:
            req=urllib.request.Request(url,headers={'User-Agent':'TravelBugAI/1.0 (authorized JSON feed)'})
            with urllib.request.urlopen(req,timeout=20) as response:
                if int(response.headers.get('Content-Length','0'))>1_000_000: raise ValueError('Feed too large')
                payload=response.read(1_000_001)
                if len(payload)>1_000_000: raise ValueError('Feed too large')
            items=json.loads(payload)
            if not isinstance(items,list): raise ValueError('Expected JSON list')
        except Exception as exc: print('Source failed',name,exc);continue
        for d in items[:200]:
            if not isinstance(d,dict):continue
            try: price=float(d['price'])
            except (KeyError,ValueError,TypeError):continue
            if not (0<price<100000) or d.get('currency','EUR')!='EUR' or d.get('kind') not in ('flight','hotel') or not valid_url(d.get('url')):continue
            ident=str(d.get('id') or d.get('url'))[:300]; key=name+'|'+ident
            past=history.get(key,[]); baseline=statistics.median(past) if len(past)>=3 else None
            flag=bool(baseline and price<=baseline*.65)
            deal={'id':key,'title':str(d.get('title','Offerta'))[:160],'kind':d['kind'],'price':round(price,2),'currency':'EUR','date':str(d.get('date',''))[:60],'url':d['url'],'source':name,'flag':flag,'checked_at':datetime.now(timezone.utc).isoformat()}
            deals.append(deal)
            old=next((x for x in previous if x.get('id')==key),None)
            if flag and (not old or not old.get('flag') or old.get('price',float('inf'))>price):alerts.append(deal)
            history[key]=(past+[price])[-30:]
    # Retain previously verified data if every source temporarily fails? No: show only fresh observations.
    deals.sort(key=lambda d:(not d['flag'],d['price']))
    save(ROOT/'data/deals.json',deals[:200]);save(ROOT/'data/history.json',history)
    for d in alerts[:10]:notify(f"🚨 Possibile anomalia (non confermata)\n{d['title']}\n€{d['price']} · {d['source']}\n{d['url']}")
    print(f'{len(deals)} deals, {len(alerts)} alerts, {len(sources)} configured sources')
if __name__=='__main__':main()
