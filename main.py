from Caption import Caption
from Sentences import Sentences
import srt

f = open("sample.srt", encoding='utf-8-sig')

generator = srt.parse(f.read())

subtitles = list(generator)
captions = []


stage1 = []
stage1last = -1
stage1unfinished = -1
isMultiple = False

# for s in subtitles:
#     t = Caption(s)
#     t.changeCaptionToOneSpeaker(2)
#     print(t.getAllRows())


for s in subtitles:
    t = Caption(s)
    captions.append(t)

    if t.hasMultipleSpeakers() == 1:
        isMultiple = False
        if t.newSentenceForCaption():
            stage1.append(Sentences(t))
            stage1last+=1
        elif t.contSentenceForCaption():
            stage1[stage1last].addCaption(t)
        else:
            stage1[stage1unfinished].addCaption(t)
        if t.unfinishedSentenceForCaption() or t.finishedSentenceForCaption():
            stage1unfinished = stage1last
    else:
        if isMultiple == False:
            isMultiple = True
            stage1.append(Sentences(t,t.hasMultipleSpeakers()))
            stage1last+=1
        else:
            stage1[stage1last].addCaption(t)


for s in stage1:
   print(s.getSentences())
                

# for s in stage1[6].getListOfCaptions():
#     for c in s:
#         print(c.getStartRow())
#         print(c.getCaptions())