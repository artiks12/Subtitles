from Caption import Caption
from Sentences import Sentences
import srt

f = open("Sample.srt", encoding='utf-8-sig')

generator = srt.parse(f.read())

f.close()

subtitles = list(generator)
captions = []

multipleTemp = []           # Dictionary that stores information about multiple speakers. Will be insert in stage1 list.
stage1 = []                 # List with combined captions
stage1last = [-1]           # Last sentence checked
stage1unfinished = [-1]     # Last unfinished sentence (ends with 3 dots)
stage1Continue = [False]    # Checks if sentence continues.
isMultiple = False          # Are we dealing with multiple speakers

# Creates a list which keeps track of last used subtitle and last unfinished subtitle for all speakers
def createStage1IndexesForMultipleSpeakers(count):
    global stage1last
    global stage1unfinished
    global stage1Continue

    last = stage1last[0]
    unfinished = stage1unfinished[0]
    Continue = stage1Continue[0]
    
    stage1last = []
    stage1unfinished = []
    stage1Continue = []

    for i in range(count):
        stage1last.append(last)
        stage1unfinished.append(unfinished)
        stage1Continue.append(Continue)


# Main stage1 function for combining captions.
def addToStage1(t,mode,speaker = 0):
    global multipleTemp
    global stage1
    global stage1last
    global stage1unfinished
    global isMultiple
    global currentIndex

    # If subcaption is from caption with multiple speakers 
    if mode > 1:
        # Change to multiple speaker mode
        if isMultiple == False: 
            isMultiple = True
            createStage1IndexesForMultipleSpeakers(mode)
        # Create multipleTemp dictionary.
        if speaker == 0:
            multipleTemp = {}
            for i in range(mode):
                multipleTemp[i] = None
    
    # If subcaption is from caption with multiple speakers and last checked caption is a caption with multiple speakers
    if mode > 1 and type(stage1[stage1last[speaker]]) == dict:
        if stage1[stage1last[speaker]][speaker].getLastCaption().getCaption() == t.getCaption():
            return None

    # If caption has one speaker and if we were checking captions with multiople speakers.
    # Set to single speaker mode and set last checked sentence and last unfinished sentence indexes correctly.
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

    last = stage1last[speaker]
    unfinished = stage1unfinished[speaker]

    # If caption begins with big letter.
<<<<<<< Updated upstream
    if t.newSentence() and stage1Continue[speaker] == False:
=======
    if (t.newSentence() and stage1Continue[speaker] == False) or t.isEffect():
>>>>>>> Stashed changes
        if mode == 1:
            stage1.append(Sentences(t,t.getLabel()))
            if not(t.isEffect()):
                stage1last[speaker] = len(stage1)-1
        else:
            multipleTemp[speaker] = Sentences(t,t.getLabel())
<<<<<<< Updated upstream
            stage1last[speaker]+=1
=======
            if not(t.isEffect()):
                stage1last[speaker]+=1
>>>>>>> Stashed changes

    elif t.contSentence() or stage1Continue[speaker] == True:
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
            if (type(stage1[stage1last[speaker]]) == dict):
                stage1[stage1last[speaker]][speaker].addCaption(t)
            else:
                stage1[stage1last[speaker]].addCaption(t)     
    
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
            if (type(stage1[stage1unfinished[speaker]]) == dict):
                stage1[stage1unfinished[speaker]][speaker].addCaption(t)
            else:
                stage1[stage1unfinished[speaker]].addCaption(t)
    
    if t.unfinishedSentence():
        stage1unfinished[speaker] = stage1last[speaker]
    elif t.endsSentence():
        stage1Continue[speaker] = False
    else:
        stage1Continue[speaker] = True


for s in subtitles:
    t = Caption(s)
    captions.append(t)
    print(t.index)
    print(t.getOriginalWithoutTagsAndExtraSpaces())
    print(t.geCharacterCountInRows())

    if t.hasMultipleSpeakers() == 1:
        addToStage1(t,t.hasMultipleSpeakers())
    else:
        for i in range(t.hasMultipleSpeakers()):
            newCaption = t.getCopyWithOneSpeaker(i)
            addToStage1(newCaption,t.hasMultipleSpeakers(),i)
            # Sometimes one sentence in multiple speakers can appear in multiple captions or none of those captions have new sentence.
            if i+1 == t.hasMultipleSpeakers():
                New = False
                for i in multipleTemp.values():
                    if not(i == None):
                        New = True
                if New:
                    stage1.append(multipleTemp)

# for s in stage1:
#     if type(s) == dict:
#         for i in s.values():
#             if not(i==None):
#                 print(i.getIndexes())
#                 # print(i.prepeareDataForTranslation())
#                 # print(i.getTranslations())
#                 print(i.getCaptionContentAfterTranslationSavingSentenceOrigins())
#             else:
#                 print('None')
#     else:
#         print(s.getIndexes())
#         # print(s.prepeareDataForTranslation())
#         # print(s.getTranslations())
#         print(s.getCaptionContentAfterTranslationSavingSentenceOrigins())



for s in stage1:
    if type(s) == dict:
        for i in s.values():
            if not(i==None):
                translations = i.getCaptionContentAfterTranslationSavingSentenceOrigins()
                for t in translations:
                    if captions[t[0]-1].translation == '':
                        captions[t[0]-1].translation += t[1]
                    else:
                        captions[t[0]-1].translation += '\n' + t[1]
                        
    else:
        translations = s.getCaptionContentAfterTranslationSavingSentenceOrigins()
        for t in translations:
            captions[t[0]-1].translation += t[1]

# for c in captions:
#     print(c.index)
#     print(c.getCaption())
#     print(c.translation)
#     print(c.getTranslation())

for index in range(len(captions)):
    text = captions[index].getTranslation()
    begin = 0
    for i in range(len(text)):
        if text[i] == ' ':
            begin += 1
        else:
            break
    subtitles[index].content = text[begin:]

r = open('result.srt','w',encoding='utf-8-sig')
r.write(srt.compose(subtitles))
r.close()


<<<<<<< Updated upstream
# for s in stage1:
#     if type(s) == dict:
#         for i in s.values():
#             if not(i==None):
#                 translations = i.getCaptionContentAfterTranslation()
#                 for t in translations:
#                     if not(captions[t[0]-1].translation == ''):
#                         captions[t[0]-1].translation += '<br/>' + t[1] + ' '
#                     else:
#                         captions[t[0]-1].translation += t[1] + ' '
#     else:
#         translations = s.getCaptionContentAfterTranslation()
#         for t in translations:
#             captions[t[0]-1].translation += t[1] + ' '

# # for c in captions:
# #     print(c.index)
# #     print(c.getCaption())
# #     print(c.translation)

# for index in range(len(captions)):
#     text = captions[index].translation.replace('<br/> ','\n').replace('<br/>','\n')
#     begin = 0
#     for i in range(len(text)):
#         if text[i] == ' ':
#             begin += 1
#         else:
#             break
#     subtitles[index].content = text[begin:]

r = open('result.srt','w',encoding='utf-8-sig')
r.write(srt.compose(subtitles))
r.close()


=======
>>>>>>> Stashed changes
# print(captions[0].getWholeEnclosings())
# print(captions[0].getTextWithinWholeEnclosings())
# print(captions[1].getWholeEnclosings())
# print(captions[1].getTextWithinWholeEnclosings())
