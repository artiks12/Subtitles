import srt

# Gets text to insert in subtitle files and evaluation data.
def getEvaluationData(captions,translations,subtitles,file,mode):
    totalSubtitles = 0

    originalGoodWPM = 0
    originalGoodCPS = 0
    originalGoodRowCount = 0
    originalGoodCharacterCount = 0
    originalGoodSubtitlesWPM = 0
    originalGoodSubtitlesCPS = 0

    translationGoodWPM = 0
    translationGoodCPS = 0
    translationGoodRowCount = 0
    translationGoodCharacterCount = 0
    translationGoodSubtitlesWPM = 0
    translationGoodSubtitlesCPS = 0

    e = open('BBC_Evaluation/Raw/'+'evaluation_'+file+'_raw_'+mode+'.csv','w',encoding='utf-8-sig')

    e.write('SubtitleIndex,OriginalWPM,OriginalCPM,OriginalRowCount,OriginalCharactersPerRow,TranslationWPM,TranslationCPM,TranslationRowCount,TranslationCharactersPerRow,isOriginalWPMGood,isOriginalCPSGood,isOriginalRowCountGood,isOriginalCharacterCountGood,isTranslationWPMGood,isTranslationCPSGood,isTranslationRowCountGood,isTranslationCharacterCountGood,isOriginalGoodWPM,isTranslationGoodWPM,isOriginalGoodCPS,isTranslationGoodCPS\n')
    for index in range(len(captions)):
        captions[index].translation = translations[index]
        text = captions[index].getTranslation()
        begin = 0
        for i in range(len(text)):
            if text[i] == ' ':
                begin += 1
            else:
                break
        subtitles[index].content = text[begin:]

        data = captions[index].getEvaluationData()
        string = captions[index].evaluationDataToString(data)
        e.write(string + '\n')

        totalSubtitles += 1

        originalGoodWPM = originalGoodWPM+1 if data[3][0] == True else originalGoodWPM
        originalGoodCPS = originalGoodCPS+1 if data[3][1] == True else originalGoodCPS
        originalGoodRowCount = originalGoodRowCount+1 if data[3][2] == True else originalGoodRowCount
        originalGoodCharacterCount = originalGoodCharacterCount+1 if data[3][3] == True else originalGoodCharacterCount
        originalGoodSubtitlesWPM = originalGoodSubtitlesWPM+1 if data[5] == True else originalGoodSubtitlesWPM
        originalGoodSubtitlesCPS = originalGoodSubtitlesCPS+1 if data[7] == True else originalGoodSubtitlesCPS
        
        translationGoodWPM = translationGoodWPM+1 if data[4][0] == True else translationGoodWPM
        translationGoodCPS = translationGoodCPS+1 if data[4][1] == True else translationGoodCPS
        translationGoodRowCount = translationGoodRowCount+1 if data[4][2] == True else translationGoodRowCount
        translationGoodCharacterCount = translationGoodCharacterCount+1 if data[4][3] == True else translationGoodCharacterCount
        translationGoodSubtitlesWPM = translationGoodSubtitlesWPM+1 if data[6] == True else translationGoodSubtitlesWPM
        translationGoodSubtitlesCPS = translationGoodSubtitlesCPS+1 if data[8] == True else translationGoodSubtitlesCPS

    e.close()

    e = open('BBC_Evaluation/Total/'+'evaluation_'+file+'_total_'+mode+'.csv','w',encoding='utf-8-sig')
    e.write('SubtitleCount,GoodOriginalWPMCount,GoodOriginalCPSCount,GoodOriginalRowCount,GoodOriginalCharactersPerRowCount,GoodTranslationWPMCount,GoodTranslationCPSCount,GoodTranslationRowCount,GoodTranslationCharactersPerRowCount,GoodOriginalSubtitleCountWPM,GoodTranslationSubtitleCountWPM,GoodOriginalSubtitleCountCPS,GoodTranslationSubtitleCountCPS\n')
    temp = [str(totalSubtitles),str(originalGoodWPM),str(originalGoodCPS),str(originalGoodRowCount),str(originalGoodCharacterCount),str(translationGoodWPM),str(translationGoodCPS),str(translationGoodRowCount),str(translationGoodCharacterCount),str(originalGoodSubtitlesWPM),str(translationGoodSubtitlesWPM),str(originalGoodSubtitlesCPS),str(translationGoodSubtitlesCPS)]
    e.write(','.join(temp))
    e.close()

    e = open('BBC_Evaluation/Percentage/'+'evaluation_'+file+'_percentage_'+mode+'.csv','w',encoding='utf-8-sig')
    e.write('GoodOriginalWPMCount,GoodOriginalCPSCount,GoodOriginalRowCount,GoodOriginalCharactersPerRowCount,GoodTranslationWPMCount,GoodTranslationCPSCount,GoodTranslationRowCount,GoodTranslationCharactersPerRowCount,GoodOriginalSubtitleCountWPM,GoodTranslationSubtitleCountWPM,GoodOriginalSubtitleCountCPS,GoodTranslationSubtitleCountCPS\n')
    temp = [str(round(originalGoodWPM/totalSubtitles,3)),str(round(originalGoodCPS/totalSubtitles,3)),str(round(originalGoodRowCount/totalSubtitles,3)),str(round(originalGoodCharacterCount/totalSubtitles,3)),str(round(translationGoodWPM/totalSubtitles,3)),str(round(translationGoodCPS/totalSubtitles,3)),str(round(translationGoodRowCount/totalSubtitles,3)),str(round(translationGoodCharacterCount/totalSubtitles,3)),str(round(originalGoodSubtitlesWPM/totalSubtitles,3)),str(round(translationGoodSubtitlesWPM/totalSubtitles,3)),str(round(originalGoodSubtitlesCPS/totalSubtitles,3)),str(round(translationGoodSubtitlesCPS/totalSubtitles,3))]
    e.write(','.join(temp))
    e.close()

# Gets text to insert in subtitle files.
def getSubtitleContentInFiles(translations,captions,subtitles):
    for index in range(len(subtitles)):
        captions[index].translation = translations[index]
        text = captions[index].getTranslation()
        begin = 0
        for i in range(len(text)):
            if text[i] == ' ':
                begin += 1
            else:
                break
        subtitles[index].content = text[begin:]