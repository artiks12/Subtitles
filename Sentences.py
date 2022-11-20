from Caption import Caption
from Caption import specialSymbols
from Caption import closing
import re

class Sentences():
    def __init__(self, subtitle: Caption, multiple = 1, startRow = 0) -> None:
        self.__captions: list = [subtitle]
        self.__translation: str = ''
        self.multipleSpeakers = multiple
        self.__startRow = startRow

    def addCaption(self,caption: Caption):
        self.__captions.append(caption)

    def getCaptions(self):
        return self.__captions

    def getStartRow(self):
        return self.__startRow

    def getLists(self) -> list:
        result: list = []
        for i in self.__captions:
            if result == []:
                result = i.getAllSpeakersAsLists()
            else:
                result.extend(i.getAllSpeakersAsLists())
        return result

    def getIndexes(self):
        result = []
        for i in self.__captions:
            result.append(i.index)
        return result

    
    def getListOfCaptions(self):
        if self.multipleSpeakers > 1:
            return self.__getListOfCaptionsForMultipleSpeakers()
        return self.__getListOfCaptionsForSingleSpeaker()
    
    def __getListOfCaptionsForSingleSpeaker(self):
        result = []
        for c in self.__captions:
            sentences = [c.getAllSpeakersAsLists()]
            result.extend(sentences)
        return [result]

    def __getListOfCaptionsForMultipleSpeakers(self):
        result = []

        for i in range(self.multipleSpeakers):
            temp = []
            resultlast = -1
            resultunfinished = -1
            for c in self.__captions:
                newCaption = c.getCopyWithOneSpeaker(i)
                row = c.getSpeakerRow(i)
                if newCaption.newSentenceForCaption():
                    temp.append(Sentences(newCaption,1,row))
                    resultlast+=1
                elif newCaption.contSentenceForCaption():
                    temp[resultlast].addCaption(newCaption)
                else:
                    temp[resultunfinished].addCaption(newCaption)
                if newCaption.unfinishedSentenceForCaption() or newCaption.finishedSentenceForCaption():
                    resultunfinished = resultlast
            result.append(temp)
        return result

    

    def getCaptionsFromList(self):
        if self.multipleSpeakers == 1:
            return self.__getListOfCaptionsForSingleSpeaker()
        speakers = self.__getListOfCaptionsForMultipleSpeakers()
        result = []
        for s in range(len(speakers)):
            result.append([])
            for c in range(len(speakers[s])):
                result[s].append(speakers[s][c].getLists())
        return result

    def getSentences(self):
        temp = self.getListOfCaptions()
        captions = self.getCaptionsFromList()
        if(len(temp) == 1):
            return self.__getSentencesForSingleSpeaker(temp[0],captions[0])
        return self.__getSentencesForMultipleSpeakers(temp,captions)


    def __getSentencesForMultipleSpeakers(self, speakers, captions):
        result = []
        indexSpeaker = 0
        for speaker in speakers:
            temp = []
            indexCaption = 0
            for sentence in speaker:
                print(sentence.getStartRow())
                print(sentence.getIndexes())
                temp.append(self.__getSentencesForSingleSpeaker(sentence,[captions[indexSpeaker][indexCaption]],sentence.getStartRow(),sentence.getIndexes()))
                indexCaption += 1
            indexSpeaker+=1
            result.append(temp)
        return result

    def __getSentencesForSingleSpeaker(self, speaker, captions, startRow = -1, indexList = -1):
        if(indexList == -1):
            indexes = self.getIndexes()
        else:
            indexes = indexList
        result = []
        sentence = []
        start = []
        end = []

        currentCaption = 0
        punctuation = -1
        startNew = True
        begin = True
        unfinished = False
        for caption in captions:
            if(startRow == -1):
                currentRow = self.__startRow
            else:
                currentRow = startRow
            for row in caption:
                for words in row:
                    for word in words:
                        if not(self.__isSpecial(word)):
                            if unfinished:
                                punctuation = self.__getPunctuation(word)
                                if not(punctuation == 3):
                                    startNew = True
                                unfinished = False

                            if startNew == True and begin == False:
                                temp = []
                                temp.append(start)
                                temp.append(end)
                                temp.append(sentence)
                                result.append(temp)
                                
                                sentence = []
                                start = []
                                start.append(indexes[currentCaption])
                                start.append(currentRow)
                                end = []
                                
                                startNew = False
                            
                            elif begin == True:
                                sentence = []
                                start = []
                                start.append(indexes[currentCaption])
                                start.append(currentRow)
                                end = []
                                begin = False
                                startNew = False
                            
                            punctuation = self.__getPunctuation(word)
                            if(punctuation == 1):
                                startNew = True
                                sentence.append(word)
                            elif(punctuation == 2):
                                unfinished = True
                                sentence.append(word)
                            elif(punctuation == 3):
                                sentence[-1] = self.getWordWithoutPunctuation(sentence[-1])
                                sentence.append(self.getWordWithoutPunctuation(word))
                            elif(punctuation == 4):
                                sentence.append(word)
                            else:
                                sentence.append(word)
                        else:
                            if re.match(r'-+',word) and begin == False:
                                temp = []
                                temp.append(start)
                                temp.append(end)
                                temp.append(sentence)
                                result.append(temp)
                                
                                sentence = []
                                start = []
                                start.append(indexes[currentCaption])
                                start.append(currentRow)
                                end = []
                                
                                startNew = False

                            elif begin == True:
                                sentence = []
                                start = []
                                start.append(indexes[currentCaption])
                                start.append(currentRow)
                                end = []
                                begin = False
                                startNew = False

                            sentence.append(word)
                        end = []
                        end.append(indexes[currentCaption])
                        end.append(currentRow)
                    currentRow =+ 1
            currentCaption+=1
        
        temp = []
        temp.append(start)
        temp.append(end)
        temp.append(sentence)
        result.append(temp)
        return result

    def __isSpecial(self,word):
        if re.match(r'<.*?>',word) or word in closing or word in closing.values() or word in specialSymbols or re.match(r"-+",word):
            return True
        return False
        
        

    def __getPunctuation(self,text: str):
        if text[-1] == '!' or text[-1] == '?' or (text[-1] == '.' and not(text[-3:] == '...')):
            return 1
        if text[-3:] == '...':
            return 2
        if text[0:3] == '...' or text[0:2] == '..':
            return 3
        if text[-1] == ',' or text[-1] == ';':
            return 4
        return 0     

    def getWordWithoutPunctuation(self, text):
        if text[-3:] == '...':
            return text[:-3]
        if text[0:3] == '...':
            return text[3:]
        if not(text[0:3] == '...') and text[0:2] == '..':
            return text[2:]
        if text[-1] == '!' or text[-1] == '?' or (text[-1] == '.' and not(text[-3:] == '...')) or text[-1] == ',' or text[-1] == ';':
            return text[:-1]
        return text   

