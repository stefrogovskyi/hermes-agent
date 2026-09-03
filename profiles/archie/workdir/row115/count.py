import json
rows=json.load(open('/tmp/all.json'))
queued=0
for i,r in enumerate(rows,start=2):
    status = r[3] if len(r)>3 else ''
    link = r[1] if len(r)>1 else ''
    if status in ('','В очереди') and link.strip():
        queued+=1
print("rows:",len(rows),"remaining in queue:",queued)
