import srt

f = open("sample.srt", encoding='utf-8-sig')

generator = srt.parse(f.read())

subtitles = list(generator)

print(subtitles[0])

