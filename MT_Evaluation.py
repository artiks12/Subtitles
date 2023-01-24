from tilde import translate
from datetime import datetime
from sacrebleu.metrics import BLEU, CHRF, TER

specialClosingSymbols = ['♪','#']

# Get translation and remove special symbols and tags
def getCleanText(text,toTranslate):
    translation = text
    if toTranslate == True:
        translation = translate.translate(text)['translation']
    temp = translation.replace(r'<.*?>','').replace('♪','').replace('#','').split()
    print(temp)
    if temp[0] == '–' or temp[0][-1] == ':':
        return ' '.join(temp[1:])
    return ' '.join(temp)

# Combines text in translated hypotheses together to match reference
def joinHypothesesInSentences(hypotheses,reference,mode):
    result = []
    if mode == 'sentences':
        return [item[1] for item in hypotheses]
    else:
        for r in reference:
            intervals = r[0].split(';')
            temp = []
            stop = 0
            for i in intervals:
                start = int(i.split('-')[0])
                end = int(i.split('-')[1])
                if mode == 'rows':
                    for x in range(start-1,end):
                        temp.append(hypotheses[x][1])
                elif mode == 'subtitles':
                    removed = 0
                    stop = 0
                    for x in range(len(hypotheses)):
                        hStart = int(hypotheses[x-removed][0].split('-')[0])
                        hEnd = int(hypotheses[x-removed][0].split('-')[1])
                        if start<=hStart and hEnd<=end:
                            temp.append(hypotheses[x-removed][1])
                            hypotheses.remove([hypotheses[x-removed][0],hypotheses[x-removed][1]])
                            removed += 1
                            stop = hEnd
                        if hEnd == end:
                            break
                    if stop == end:
                        continue
            result.append(' '.join(temp))
    return result

# Main evaluation function
def evaluation(originalFormating,filename):
    log = open("MT_Evaluation_"+filename+"_"+originalFormating+".txt",'w', encoding='utf-8-sig')

    log.write(filename + " " + originalFormating + " " + "Formating at " + str(datetime.now())+'\n')
    pathToOriginal = "MT_test_data/Segmentated/"+originalFormating+"Formating/"
    pathToTranslation = "MT_test_data/Segmentated/WithoutFormating/"

    originalRows = filename+"__rows"+originalFormating+"Formating.en"
    originalSentences = filename+"__sentences"+originalFormating+"Formating.en"
    originalSubtitles = filename+"__subtitles"+originalFormating+"Formating.en"
    translated = filename+"__sentencesWithoutFormating.lv"

    f = open(pathToOriginal+originalRows, encoding='utf-8-sig')

    hypothesesRows = []
    for line in f:
        temp = line.rstrip().split('\t')
        hypothesesRows.append([temp[0],getCleanText(temp[1],True)])

    f.close()

    f = open(pathToOriginal+originalSubtitles, encoding='utf-8-sig')

    hypothesesSubtitles = []
    for line in f:
        temp = line.rstrip().split('\t')
        hypothesesSubtitles.append([temp[0],getCleanText(temp[1],True)])

    f.close()

    f = open(pathToOriginal+originalSentences, encoding='utf-8-sig')

    hypothesesSentences = []
    for line in f:
        temp = line.rstrip().split('\t')
        hypothesesSentences.append([temp[0],getCleanText(temp[1],True)])

    f.close()

    f = open(pathToTranslation+translated, encoding='utf-8-sig')
    reference = []
    for line in f:
        temp = line.rstrip().split('\t')
        reference.append([temp[0],getCleanText(temp[1],False)])

    f.close()

    hypothesesRows = joinHypothesesInSentences(hypothesesRows,reference,'rows')
    hypothesesSubtitles = joinHypothesesInSentences(hypothesesSubtitles,reference,'subtitles')
    hypothesesSentences = joinHypothesesInSentences(hypothesesSentences,reference,'sentences')
    reference = [item[1] for item in reference]

    log.write(filename + " " + originalFormating + " " + "Formating at " + str(datetime.now())+'\n')
    log.write("---------------"+'\n')
    bleu = BLEU()
    log.write("Row evaluation: " + str(bleu.corpus_score(hypothesesRows, [reference]))+'\n')
    log.write("Subtitle evaluation: " + str(bleu.corpus_score(hypothesesSubtitles, [reference]))+'\n')
    log.write("Sentences evaluation: " + str(bleu.corpus_score(hypothesesSentences, [reference]))+'\n')
    log.write(str(bleu.get_signature())+'\n')
    log.write("-----"+'\n')
    chrf = CHRF()
    log.write("Row evaluation: " + str(chrf.corpus_score(hypothesesRows, [reference]))+'\n')
    log.write("Subtitle evaluation: " + str(chrf.corpus_score(hypothesesSubtitles, [reference]))+'\n')
    log.write("Sentences evaluation: " + str(chrf.corpus_score(hypothesesSentences, [reference]))+'\n')
    log.write(str(chrf.get_signature())+'\n')
    log.write("-----"+'\n')
    ter = TER()
    log.write("Row evaluation: " + str(ter.corpus_score(hypothesesRows, [reference]))+'\n')
    log.write("Subtitle evaluation: " + str(ter.corpus_score(hypothesesSubtitles, [reference]))+'\n')
    log.write("Sentences evaluation: " + str(ter.corpus_score(hypothesesSentences, [reference]))+'\n')
    log.write(str(ter.get_signature())+'\n')
    log.write("---------------"+'\n')
    log.close()

    f = open('Results/MT_Evaluation/'+filename+'_'+originalFormating+'_'+'Rows'+'.txt', 'w',encoding='utf-8-sig')
    for line in hypothesesRows:
        f.write(line+'\n')
    f.close()

    f = open('Results/MT_Evaluation/'+filename+'_'+originalFormating+'_'+'Subtitles'+'.txt', 'w',encoding='utf-8-sig')
    for line in hypothesesSubtitles:
        f.write(line+'\n')
    f.close()

    f = open('Results/MT_Evaluation/'+filename+'_'+originalFormating+'_'+'Sentences'+'.txt', 'w',encoding='utf-8-sig')
    for line in hypothesesSentences:
        f.write(line+'\n')
    f.close()

    f = open('Results/MT_Evaluation/'+filename+'_Reference'+'.txt', 'w',encoding='utf-8-sig')
    for line in reference:
        f.write(line+'\n')
    f.close()

evaluation("With","Bad.Sisters.S01E09")
evaluation("Without","Bad.Sisters.S01E09")
evaluation("With","Echo.3.S01E04")
evaluation("Without","Echo.3.S01E04")
evaluation("With","See.S03E08.")
evaluation("Without","See.S03E08.")
evaluation("With","Shantaram.S01E01")
evaluation("Without","Shantaram.S01E01")
