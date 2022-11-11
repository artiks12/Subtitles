from Caption import Caption
from Sentences import Sentences
import srt


f = open("sample.srt", encoding='utf-8-sig')

generator = srt.parse(f.read())

subtitles = list(generator)
captions = []

stage1 = []
stage1index = -1
stage1unfinished = -1
isMultiple = False

for s in subtitles:
    t = Caption(s)
    captions.append(t)
    
    if t.haveMultipleSpeakers() == 1:
        isMultiple = False
        if not(t.newSentence()):
            stage1[stage1index].addCaption(t)
        else:
            stage1.append(Sentences(t))
            stage1index+=1
        if t.getsFinished():
            stage1[stage1unfinished].addCaption(t)
        if t.unfinished():
            stage1unfinished = stage1index
    else:
        if isMultiple == False:
            isMultiple = True
            stage1.append(Sentences(t))
            stage1index+=1
        else:
            stage1[stage1index].addCaption(t)

        
    
for s in stage1:
    print(s.printSentences())
    print(s.printIndexes())
