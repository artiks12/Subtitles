from Caption import Caption
from Sentences import Sentences
import srt

f = open("Sample.srt", encoding='utf-8-sig')

generator = srt.parse(f.read())

subtitles = list(generator)
captions = []

multipleTemp = []
stage1 = []
stage1last = [-1]
stage1unfinished = [-1]
isMultiple = False

def createStage1IndexesForMultipleSpeakers(count):
    global stage1last
    global stage1unfinished

    last = stage1last[0]
    unfinished = stage1unfinished[0]
    
    stage1last = []
    stage1unfinished = []

    for i in range(count):
        stage1last.append(last)
        stage1unfinished.append(unfinished)





def addToStage1(t,mode,speaker = 0):
    global multipleTemp
    global stage1
    global stage1last
    global stage1unfinished
    global isMultiple
    global currentIndex

    if mode > 1:
        if isMultiple == False: 
            isMultiple = True
            createStage1IndexesForMultipleSpeakers(mode)
        if speaker == 0:
            multipleTemp = {}
            for i in range(mode):
                multipleTemp[i] = None
    
    if mode > 1 and type(stage1[stage1last[speaker]]) == dict:
        if stage1[stage1last[speaker]][speaker].getLastCaption().getCaption() == t.getCaption():
            return None

    if isMultiple == True and mode == 1:
        isMultiple = False
        for i in stage1last:
            found = False
            for j in range(len(stage1last)):
                if(type(stage1[i]) == dict):
                    if not(stage1[i][j] == None):
                        if stage1[i][j].canAdd():
                            stage1last[speaker] = stage1last[j]
                            found = True
                            break
            if found:
                break
        for i in stage1unfinished:
            found = False
            for j in range(len(stage1unfinished)):
                if(type(stage1[i]) == dict):
                    if not(stage1[i][j] == None):
                        if stage1[i][j].canFinish():
                            stage1unfinished[speaker] = stage1unfinished[j]
                            found = True
                            break
            if found:
                break

    
    if t.newSentence():
        if mode == 1:
            stage1.append(Sentences(t,t.getLabel()))
            stage1last[speaker] = len(stage1)-1
        else:
            multipleTemp[speaker] = Sentences(t,t.getLabel())
            stage1last[speaker]+=1
    elif t.contSentence():
        if mode == 1:
            if (type(stage1[stage1last[speaker]]) == dict):
                for i in stage1[stage1last[speaker]]:
                    if not(stage1[stage1last[speaker]][i] == None):
                        if stage1[stage1last[speaker]][i].canAdd():
                            stage1[stage1last[speaker]][i].addCaption(t)
                            break
            else:
                stage1[stage1last[speaker]].addCaption(t)
        else:
            stage1[stage1last[speaker]][speaker].addCaption(t)
    else:
        if mode == 1:
            if (type(stage1[stage1unfinished[speaker]]) == dict):
                for i in stage1[stage1unfinished[speaker]]:
                    if not(stage1[stage1unfinished[speaker]][i] == None):
                        if stage1[stage1unfinished[speaker]][i].canFinish():
                            stage1[stage1unfinished[speaker]][i].addCaption(t)
                            break
            else:
                stage1[stage1unfinished[speaker]].addCaption(t)
        else:
            stage1[stage1unfinished[speaker]][speaker].addCaption(t)
    if t.unfinishedSentence():
        stage1unfinished[speaker] = stage1last[speaker]


for s in subtitles:
    t = Caption(s)
    captions.append(t)

    if t.hasMultipleSpeakers() == 1:
        addToStage1(t,t.hasMultipleSpeakers())
    else:
        for i in range(t.hasMultipleSpeakers()):
            newCaption = t.getCopyWithOneSpeaker(i)
            addToStage1(newCaption,t.hasMultipleSpeakers(),i)
            if i+1 == t.hasMultipleSpeakers():
                New = False
                for i in multipleTemp.values():
                    if not(i == None):
                        New = True
                if New:
                    stage1.append(multipleTemp)


print(stage1[-1].getTranslation())