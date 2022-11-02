import pysubs2

subs = pysubs2.load("Batman.The.Long.Halloween.2021.1080p.BluRay.REMUX.AVC.DTS-HD.MA.5.1-FGT.srt", encoding='utf-8-sig')

print(subs[0].text)

print(subs[0].plaintext)