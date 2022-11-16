from Caption import Caption

class Sentences():
    def __init__(self, subtitle: Caption, multiple = 1) -> None:
        self.__captions: list = [subtitle]
        self.__translation: str = ''
        self.multipleSpeakers = multiple

    def addCaption(self,caption: Caption):
        self.__captions.append(caption)

    def printSentences(self):
        result = []
        for i in self.__captions:
            if result == []:
                result = i.getSentences()
            else:
                result = result + ' ' + i.getSentences()
        return result

    def getList(self) -> list:
        result: list = []
        for i in self.__captions:
            if result == []:
                result = i.getAllSpeakersAsListsPure()
            else:
                result.extend(i.getAllSpeakersAsListsPure())
        return result

    def printIndexes(self):
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
            sentences = c.getSentences()
            result.extend(sentences)
        return result

    def __getListOfCaptionsForMultipleSpeakers(self):
        result = []

        count = len(self.__captions)

        for i in range(self.multipleSpeakers):
            temp = []
            resultlast = -1
            resultindex = -1
            resultunfinished = -1
            lastSentence = ''
            for c in self.__captions:
                newCaption = c.getCopyWithOneSpeaker(i)
                if newCaption.newSentenceForCaption():
                    temp.append(Sentences(newCaption))
                    resultlast+=1
                elif newCaption.contSentenceForCaption():
                    temp[resultlast].addCaption(newCaption)
                else:
                    temp[resultunfinished].addCaption(newCaption)
                if newCaption.unfinishedSentenceForCaption() or newCaption.finishedSentenceForCaption():
                    resultunfinished = resultlast
            result.append(temp)
        return result

    def getCaptionsFromMultipleSpeakers(self):
        if self.multipleSpeakers == 1:
            return self.__getListOfCaptionsForSingleSpeaker()
        speakers = self.__getListOfCaptionsForMultipleSpeakers()
        for s in range(len(speakers)):
            for c in range(len(speakers[s])):
                speakers[s][c] = speakers[s][c].printSentences()
        return speakers

        
        
        




        