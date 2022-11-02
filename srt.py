import srt
from srt import functools

f = open("Batman.The.Long.Halloween.2021.1080p.BluRay.REMUX.AVC.DTS-HD.MA.5.1-FGT.srt", encoding='utf-8-sig')

data = f.read()

generator = srt.parse(data)

subtitles = list(generator)

print(subtitles[0].content)

