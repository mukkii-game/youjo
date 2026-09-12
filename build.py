from pathlib import Path
import re,json,base64,shutil,html
from fontTools import subset
ROOT=Path(__file__).resolve().parent
(ROOT/'tmp').mkdir(exist_ok=True)
if (ROOT/'tmp/image-map.json').exists():
 for i,p in enumerate(json.loads((ROOT/'tmp/image-map.json').read_text())):
  if Path(p).exists(): shutil.copyfile(p,ROOT/f'assets/{i+1:02}.png')
md=(ROOT/'manuscript.md').read_text()
parts=re.findall(r'## (\d+) \| ([^\n]+)\n<!-- image: (\d+) -->\n(.*?)(?=\n## |\Z)',md,re.S)
assert len(parts)==24
pages=[{'n':int(n),'title':t,'image':int(im)-1,'text':tx.strip()} for n,t,im,tx in parts]
readings={'終わり':'おわり','期':'き','六さい':'ろくさい','六ねん':'ろくねん','五十ねん':'ごじゅうねん','五ふん':'ごふん','一つ':'ひとつ','一人':'ひとり','女の子':'おんなのこ','子ども':'こども','学校':'がっこう','空':'そら','小さい':'ちいさい','小さな':'ちいさな','古い':'ふるい','赤い':'あかい','白い':'しろい','大きな':'おおきな','入る':'はいる','入れ':'いれ','中':'なか','海':'うみ','手':'て','紙':'かみ','字':'じ','花':'はな','水':'みず','会った':'あった','口':'くち','目':'め','人':'ひと','子':'こ'}
pattern=re.compile('|'.join(map(re.escape,sorted(readings,key=len,reverse=True))))
def ruby(t):
 t=html.escape(t)
 return pattern.sub(lambda m:'<ruby>'+m[0]+'<rt>'+readings[m[0]]+'</rt></ruby>',t).replace('゛','<span class="dakuten">゛</span>')
for p in pages:
 p['html']=''.join('<p>'+ruby(x).replace('\n','<br>')+'</p>' for x in p['text'].split('\n\n'))
font_source=ROOT/'tmp/japanese.ttf'
if not font_source.exists():
 import fitz
 font_source.write_bytes(fitz.Font('japan').buffer)
font=subset.load_font(str(font_source),subset.Options())
s=subset.Subsetter();s.populate(text=md+''.join(readings.values())+'もどるつぎへはじめからページもじ大きく小さくおしまいようじょきのおわり0123456789 /←→ほしとてがみのものがたり')
s.subset(font);font.flavor='woff';font.save(ROOT/'assets/book-font.woff')
images=['data:image/png;base64,'+base64.b64encode((ROOT/f'assets/{i:02}.png').read_bytes()).decode() for i in range(1,9)]
font64=base64.b64encode((ROOT/'assets/book-font.woff').read_bytes()).decode()
(Root:=ROOT/'output') .mkdir(exist_ok=True)
base=(ROOT/'reader-template.html').read_text().replace('__FONT__',font64).replace('__PAGES__',json.dumps(pages,ensure_ascii=False)).replace('__IMAGES__',json.dumps(images))
(ROOT/'output/youjo-no-owari.html').write_text(base)
(ROOT/'tmp/pages.json').write_text(json.dumps(pages,ensure_ascii=False,indent=2))
print('Built 24 pages:',(ROOT/'output/youjo-no-owari.html').stat().st_size,'bytes')

import subprocess,sys
subprocess.run([sys.executable,str(ROOT/'make_pdf.py')],check=True)
