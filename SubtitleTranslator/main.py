from Combiner import combiner
from Translator import setTranslations
from Translator import insertTranslations
from Evaluator import getEvaluationData
from Caption import Caption
import srt


def execute(file):
    f = open('Subtitles/Sample.srt', encoding='utf-8-sig')

    # f = open('MT_test_data/Validated/'+file+'_validated.srt', encoding='utf-8-sig')
    subtitles = list(srt.parse(f.read()))
    f.close()

    (combined,captions) = combiner(subtitles)

    # for s in combined:
    #     print(s.getIndexes())
    #     for c in s.getCaptions():
    #         print(c.index)
    #         print(c.getCaption())

    translations = setTranslations(combined)
    translationDict = insertTranslations(combined,translations)

    for mode in translationDict:
        getEvaluationData(captions,translationDict[mode],subtitles,file,mode)

        r = open('Results/'+file+'_translated_'+mode+'.srt','w',encoding='utf-8-sig')
        r.write(srt.compose(subtitles))
        r.close()

execute('Sample')
# execute('Bad.Sisters.S01E09_EN')
# execute('Echo.3.S01E04_EN')
# execute('See.S03E08._EN')
# execute('Shantaram.S01E01_EN')
# execute('Wednesday.S01E03_EN')