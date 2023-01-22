import re
import sys
sys.path.insert(0, 'c:/Users/Artis/Documents/GitHub/Subtitles/SubtitleTranslator')

from Caption import Caption
from Sentences import Sentences
from Combiner import combiner
import srt

def getCombinedCaptionCount(stage1,captions):
    last = 0
    count = 0
    for s in stage1:
        indexes = s.getIndexes()
        if not(indexes[0] == last):
            count += 1
        last = indexes[0]
    return count


def preperation(filename):
    language = filename[-2:].lower()
    f = open("MT_test_data/Common/"+filename+"_common.srt", encoding='utf-8-sig')

    # f = open("Subtitles/Sample.srt", encoding='utf-8-sig')
    generator = srt.parse(f.read())

    f.close()

    subtitles = list(generator)
    captions = []

    rowsWithFormating = []
    rowsWithoutFormating = []
    subtitlesWithFormating = []
    subtitlesWithoutFormating = []
    sentencesWithFormating = []
    sentencesWithoutFormating = []

    index = 1
    (stage1,captions) = combiner(subtitles)
    if language == 'en':
        for t in captions:
            if t.hasMultipleSpeakers() == 1:
                textWithFormating = t.getOriginal().split('\n')
                textWithoutFormating = re.sub(r'<.*?>','',t.getOriginalWithoutEnclosings().replace('…','...')).split('\n')

                start = index
                length = len(textWithFormating)
                
                tempWithFormating = [str(start)+'-','']
                tempWithoutFormating = [str(start)+'-','']
                
                subtitleWithFormating = []
                subtitleWithoutFormating = []
                for i in range(length):
                    rowsWithFormating.append([start+i,textWithFormating[i]])
                    rowsWithoutFormating.append([start+i,textWithoutFormating[i]])
                    
                    subtitleWithFormating.append(textWithFormating[i])
                    subtitleWithoutFormating.append(textWithoutFormating[i])
                index += length
                tempWithFormating[0] += str(index-1)
                tempWithoutFormating[0] += str(index-1)
                
                tempWithFormating[1] = ' '.join(subtitleWithFormating)
                tempWithoutFormating[1] = ' '.join(subtitleWithoutFormating)

                subtitlesWithFormating.append(tempWithFormating)
                subtitlesWithoutFormating.append(tempWithoutFormating)
            else:
                for i in range(t.hasMultipleSpeakers()):
                    newCaption = t.getCopyWithOneSpeaker(i)
                    
                    textWithFormating = newCaption.getOriginal().replace('…','...').split('\n')
                    textWithoutFormating = re.sub(r'<.*?>','',newCaption.getOriginalWithoutEnclosings().replace('…','...')).split('\n')

                    for j in range(len(textWithoutFormating)):
                        tempWithout = textWithoutFormating[j].split()
                        if tempWithout[0] == '–' or tempWithout[0][-1] == ':':
                            textWithoutFormating[j] = ' '.join(tempWithout[1:])

                    start = index
                    length = len(textWithFormating)
                    
                    tempWithFormating = [str(start)+'-','']
                    tempWithoutFormating = [str(start)+'-','']
                    
                    subtitleWithFormating = []
                    subtitleWithoutFormating = []
                    for i in range(length):
                        rowsWithFormating.append([start+i,textWithFormating[i]])
                        rowsWithoutFormating.append([start+i,textWithoutFormating[i]])
                        
                        subtitleWithFormating.append(textWithFormating[i])
                        subtitleWithoutFormating.append(textWithoutFormating[i])
                    index += length
                    tempWithFormating[0] += str(index-1)
                    tempWithoutFormating[0] += str(index-1)
                    
                    tempWithFormating[1] = ' '.join(subtitleWithFormating)
                    tempWithoutFormating[1] = ' '.join(subtitleWithoutFormating)

                    subtitlesWithFormating.append(tempWithFormating)
                    subtitlesWithoutFormating.append(tempWithoutFormating)
        
        r = open('MT_test_data/Segmentated/WithFormating/'+filename[:-2]+'_rowsWithFormating'+'.'+language,'w',encoding='utf-8-sig')
        for elem in rowsWithFormating:
            r.write(str(elem[0]) + '\t' + elem[1].replace('\t',' ') + '\n')
        r.close()

        r = open('MT_test_data/Segmentated/WithoutFormating/'+filename[:-2]+'_rowsWithoutFormating'+'.'+language,'w',encoding='utf-8-sig')
        for elem in rowsWithoutFormating:
            r.write(str(elem[0]) + '\t' + elem[1].replace('\t',' ') + '\n')
        r.close()

        r = open('MT_test_data/Segmentated/WithFormating/'+filename[:-2]+'_subtitlesWithFormating'+'.'+language,'w',encoding='utf-8-sig')
        for elem in subtitlesWithFormating:
            r.write(str(elem[0]) + '\t' + elem[1].replace('\t',' ') + '\n')
        r.close()

        r = open('MT_test_data/Segmentated/WithoutFormating/'+filename[:-2]+'_subtitlesWithoutFormating'+'.'+language,'w',encoding='utf-8-sig')
        for elem in subtitlesWithoutFormating:
            r.write(str(elem[0]) + '\t' + elem[1].replace('\t',' ') + '\n')
        r.close()

    stage1count = getCombinedCaptionCount(stage1,captions)
    print(filename + " " + str(len(captions)) + " " + str(stage1count))    
    for s in stage1:
        if type(s)==dict:
            for i in s.values():
                if not(i==None):
                    (sentenceWithFormating,sentenceWithoutFormating) = i.getSentencesForTranslationEvaluation()
                    sentencesWithFormating.extend(sentenceWithFormating)
                    sentencesWithoutFormating.extend(sentenceWithoutFormating)
        else:
            (sentenceWithFormating,sentenceWithoutFormating) = s.getSentencesForTranslationEvaluation()
            sentencesWithFormating.extend(sentenceWithFormating)
            sentencesWithoutFormating.extend(sentenceWithoutFormating)

    if language == 'en':
        r = open('MT_test_data/Segmentated/WithFormating/'+filename[:-2]+'_sentencesWithFormating'+'.'+language,'w',encoding='utf-8-sig')
        for elem in sentencesWithFormating:
            r.write(str(elem[0]) + '\t' + elem[1].replace('\t',' ') + '\n')
        r.close()

    r = open('MT_test_data/Segmentated/WithoutFormating/'+filename[:-2]+'_sentencesWithoutFormating'+'.'+language,'w',encoding='utf-8-sig')
    for elem in sentencesWithoutFormating:
        r.write(str(elem[0]) + '\t' + elem[1].replace('\t',' ') + '\n')
    r.close()

preperation('Bad.Sisters.S01E09_EN')
preperation('Echo.3.S01E04_EN')
preperation('See.S03E08._EN')
preperation('Shantaram.S01E01_EN')

preperation('Bad.Sisters.S01E09_LV')
preperation('Echo.3.S01E04_LV')
preperation('See.S03E08._LV')
preperation('Shantaram.S01E01_LV')