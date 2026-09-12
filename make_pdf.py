from pathlib import Path
import re,json,html
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
R=Path(__file__).resolve().parent
pdfmetrics.registerFont(TTFont('Book',str(R/'tmp/japanese.ttf')))
pages=json.loads((R/'tmp/pages.json').read_text())
c=canvas.Canvas(str(R/'output/youjo-no-owari.pdf'),pagesize=(480,800),pageCompression=1)
c.setTitle('ょぅι゛ょ期の終わり');c.setAuthor('ムッキー / ChatGPT');c.setSubject('ほしと てがみの ものがたり')
S=20.5;W=420
def width(a,size=S):
 return sum(size*.23 if ch=='゛' else pdfmetrics.stringWidth(ch,'Book',size) for ch in a)
def draw_plain(x,y,t,size):
 c.setFont('Book',size)
 for ch in t:
  c.drawString(x,y,ch);x+=width(ch,size)

# Each group is kept together with its reading, so ruby never crosses a line.
def tokens(s):
 s=s.replace('<span class="dakuten">','').replace('</span>','')
 s=s.replace('</p><p>','\n\n').replace('<p>','').replace('</p>','').replace('<br>','\n')
 out=[]
 for x in re.split(r'(<ruby>.*?</ruby>)',s):
  m=re.fullmatch(r'<ruby>(.*?)<rt>(.*?)</rt></ruby>',x)
  if m:out.append((html.unescape(m[1]),html.unescape(m[2])))
  else:out.extend((ch,'') for ch in html.unescape(x))
 return out
def lines(ts):
 result=[];cur=[];line_width=0
 for a,b in ts:
  if a=='\n': result.append(cur);cur=[];line_width=0;continue
  tw=width(a)
  if line_width+tw>W and cur:
   if a in '。、」』！？':
    last=cur.pop();result.append(cur);cur=[last];line_width=width(last[0])
   else:result.append(cur);cur=[];line_width=0
  cur.append((a,b));line_width+=tw
 result.append(cur)
 return result
checks=[]
for p in pages:
 c.setFillColor(HexColor('#fff9e9'));c.rect(0,0,480,800,fill=1,stroke=0)
 c.drawImage(str(R/f"assets/{p['image']+1:02}.png"),0,480,480,320)
 c.setFillColor(HexColor('#182c40'))
 if p['n']==0:
  c.setFillColor(HexColor('#cc5a34'));c.rect(32,405,40,4,fill=1,stroke=0)
  c.setFillColor(HexColor('#182c40'));c.setFont('Book',39)
  draw_plain(32,337,'ょぅι゛ょ期の',39);c.drawString(32,271,'終わり')
  c.setFont('Book',17);c.drawString(34,385,'ようじょきの');c.drawString(34,310,'おわり')
  c.setFont('Book',18);c.drawString(33,186,'ほしと てがみの ものがたり')
 else:
  ls=lines(tokens(p['html']))
  height=sum(16 if not line else 34 for line in ls)
  y=440-max(0,(385-height)/2)
  first=y
  for line in ls:
   if not line:y-=16;continue
   x=30
   for a,b in line:
    tw=width(a)
    c.setFont('Book',S);c.drawString(x,y,a)
    if b:
     c.setFont('Book',8.7);rw=pdfmetrics.stringWidth(b,'Book',8.7);c.drawString(x+(tw-rw)/2,y+22,b)
    x+=tw
   y-=34
  checks.append({'page':p['n'],'lines':len(ls),'last_y':y+34,'first_y':first})
  assert y+34>=38,(p['n'],y)
  if p['n']==23:
   c.setFont('Book',12);c.setFillColor(HexColor('#9c492e'));c.drawString(30,max(38,y-12),'おしまい')
  c.setFont('Book',11);c.setFillColor(HexColor('#64707a'));c.drawRightString(454,20,f"{p['n']:02}")
 c.showPage()
c.save()
(R/'tmp/pdf-layout.json').write_text(json.dumps(checks,indent=2))
print('PDF written; min text baseline:',min(x['last_y'] for x in checks))
