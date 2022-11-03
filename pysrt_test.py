import pysrt

subs = pysrt.open('sample.srt', encoding='utf-8-sig')

print(subs.text)