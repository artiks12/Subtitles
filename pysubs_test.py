import pysubs2

subs = pysubs2.load("sample.srt", encoding='utf-8-sig')

print(subs)

# How to insert text within tags. Only works if whole caption is in tags
# test = "\\N".join(line.strip() for line in subs[0].plaintext.splitlines())
# subs[0].text = subs[0].text.replace(test,"New Text")