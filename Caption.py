import srt
import re

closing={
    '(':')',
    '[':']',
    '{':'}',
}

tags={
    '<f':'</font>',
    '<b':'</b>',
    '<i':'</i>',
    '<u':'</u>'
}

specialClosingSymbols = ['♪','"']

class Caption(srt.Subtitle):
    # Constructor. Gets info on caption.
    def __init__(self, *args) -> None:
        if len(args) == 1:
            self.__caption = self.__spaces(args[0])
            self.index = args[0].index
            self.start = args[0].start
            self.end = args[0].end
        else:
            self.__caption = args[0]
            self.index = args[1]
            self.start = args[2]
            self.end = args[3]

    # Creates spaces around tags and brackets
    def __spaces(self, subtitle):
        result = self.__spacesForTags(subtitle.content)
        result = self.__spacesForBrackets(result)
        return result

    # Creates spaces around tags
    def __spacesForTags(self, text: str):
        temp = re.findall(r'<.*?>',text)
        result = text
        for t in temp:
            n = ' '+t+' '
            result = result.replace(t,n)
        return result

    # Creates spaces around brackets
    def __spacesForBrackets(self, text: str):
        return text.replace('(','( ').replace(')',' )').replace('{','{ ').replace('}',' }').replace('[','[ ').replace(']',' ]').replace('"',' " ')

    # Checks if element is speaker identifier
    def __isSpeakerIdentifier(self,elem):
        return self.__isLabel(elem) or self.__isDash(elem)

    # Checks if first element of a row is a label
    def __isLabel(self, first):
        return first[-1] == ':'

    # Checks if first element of a row is a label
    def __isDash(self, first):
        return re.match(r"-+",first)

    # Checks if element is a styling tag
    def __isTag(self, elem):
        return self.__isTagOpen(elem) or self.__isTagClose(elem)

    # Checks if element is an opening tag
    def __isTagOpen(self, elem):
        if re.match(r'<.*?>',elem) == None:
            return False
        else:
            return True

    # Checks if element is a closing tag
    def __isTagClose(self, elem):
        if re.match(r'</.*?>',elem) == None:
            return False
        else:
            return True

    # Checks if element is a special symbol
    def __isSpecial(self,elem):
        return elem in specialClosingSymbols

    # Get all rows, that start seperate speakers. If one speaker, then return empty list
    def __getSpeakerRows(self):
        result = []
        row = 0
        for l in self.getAllRowsAsListsWithoutSpecials():
            if self.__isSpeakerIdentifier(l[0]):
                result.append(row)
            row+=1
        return result

    # Remove spaces for brackets
    def __fixBrackets(self, text):
        return text.replace('( ','(').replace(' )',')').replace('{ ','{').replace(' }','}').replace('[ ','[').replace(' ]',']').replace(' " ','"')
    
    # Gets a speaker label from caption. Returns None if there is no lable
    def getLabel(self):
        result = None
        for row in self.getAllRowsAsLists():
            for elem in row:
                if self.__isLabel(elem):
                    return elem
        return None

    # Get caption as a single row, where newline is shown with '(\\n)'
    def getAllRows(self) -> list:
        return self.__caption.replace('\n',' (\\n) ')

    # Get caption as list of rows
    def getAllRowsAsList(self) -> list:
        return self.getAllRows().split()

    # Get caption as lists of row elements
    def getAllRowsAsLists(self) -> list:
        result = []
        for row in self.__caption.split('\n'):
            result.append(row.split())
        return result

    # Get all rows as lists of row elements seperated by element technical information
    def getAllRowsAsListSeperated(self,lst) -> list:
        if lst == 'getEverythingInEnclosing':
            fun = self.getEverythingInEnclosing
        if lst == 'getAllRowsAsList':
            fun = self.getAllRowsAsList
        tech = self.getTechnical(fun())
        result = [fun(),fun(),fun(),fun(),fun(),fun(),fun(),tech]
        for i in range(len(fun())):
            index = -1
            if tech[i] == 'bracket open' or tech[i] == 'bracket close':
                index = 2
            elif tech[i] == 'tag open' or tech[i] == 'tag close':
                index = 5
            elif tech[i] == 'label' or tech[i] == 'dash':
                index = 4
            elif tech[i] == 'special':
                index = 3
            elif tech[i] == 'newline' or tech[i] == 'newcaption':
                index = 6 
            else:
                index = 1
            for k in range(1,7):
                if not(index == k):
                    result[k][i] = ''
        return result

    # Get all rows as lists of row elements without special symbols and tags
    def getAllRowsAsListsWithoutSpecials(self):
        result = []
        for row in self.getAllRowsAsLists():
            rowTemp = []
            for elem in row:
                if not(self.__isSpecial(elem) or self.__isTag(elem)):
                    rowTemp.append(elem)
            result.append(rowTemp)
        return result

    # # Get all rows as lists of row elements without speaker identifiers
    # def getAllRowsAsListsWithoutSpeakerId(self):
    #     result = []
    #     for row in self.getAllRowsAsLists():
    #         rowTemp = []
    #         for elem in row:
    #             if not(self.__isSpeakerIdentifier(elem)):
    #                 rowTemp.append(elem)
    #         result.append(rowTemp)
    #     return result

    # Get all rows as lists of row elements without special symbols, speaker identifiers and tags
    def getAllRowsAsListsPure(self):
        result = []
        for row in self.getAllRowsAsLists():
            rowTemp = []
            for elem in row:
                if not(self.__isSpeakerIdentifier(elem) or self.__isTag(elem) or self.__isSpecial(elem)):
                    rowTemp.append(elem)
            result.append(rowTemp)
        return result

    # Might be obsolete
    def __getAllSpeakersBase(self,lists):
        lst = self.__getSpeakerRows()
        if lst == []:
            return [lists]
        result = []
        count = 0
        for i in lst:
            end = -1
            if count+1==len(lst):
                end = len(lists)
            else:
                end = lst[count+1]
            result.append(lists[i:end])
            count+=1
        return result

    # Might be obsolete
    def getAllSpeakers(self):
        return self.__getAllSpeakersBase(self.__caption.split('\n'))

    # Might be obsolete
    def getAllSpeakersAsLists(self):
        return self.__getAllSpeakersBase(self.getAllRowsAsLists())

    # Might be obsolete
    def getAllSpeakersAsListsWithoutSpecials(self):
        return self.__getAllSpeakersBase(self.getAllRowsAsListsWithoutSpecials())

    # Might be obsolete
    def getAllSpeakersAsListsPure(self):
        return self.__getAllSpeakersBase(self.getAllRowsAsListsPure())

    # def getAllSpeakersAsListsWithoutSpeakerId(self):
    #     return self.__getAllSpeakersBase(self.getAllRowsAsListsWithoutSpeakerId())

    # Might be obsolete
    def getSingleSpeaker(self,id):
        temp = self.getAllSpeakers()
        if id >= len(temp):
            return None
        return temp[id]

    # Might be obsolete
    def getSingleSpeakerAsLists(self,id):
        temp = self.getAllSpeakersAsListsWithoutSpecials()[id]
        if id >= len(temp):
            return None
        return temp[id]

    # Might be obsolete
    def getSingleSpeakerAsListsWithoutSpecials(self,id):
        temp = self.getAllSpeakersAsListsWithoutSpecials()[id]
        if id >= len(temp):
            return None
        return temp[id]

    # Might be obsolete
    def getSingleSpeakerAsListsBase(self,id):
        temp = self.getAllSpeakersAsListsBase()[id]
        if id >= len(temp):
            return None
        return temp[id]

    # Might be obsolete
    def getSentences(self):
        result = []
        speakers = self.getAllSpeakersAsListsPure()
        for speaker in speakers:
            line = []
            for row in speaker:
                line.extend(row)
            temp = ' '.join(line)
            temp = self.__fixBrackets(temp)
            result.append(temp)
        return result

    # Checks if the caption starts a new sentence
    def newSentence(self):
        temp: list = self.getAllRowsAsListsPure()
        if temp[0][0].islower():
            return False
        return True

    # Checks if the caption continues a previous caption
    def contSentence(self):
        temp: list = self.getAllRowsAsListsPure()
        if temp[0][0].islower() and not(self.finishedSentence()):
            return True
        return False
    
    # Checks if the caption is unfinished
    def unfinishedSentence(self):
        temp: str = self.getAllRowsAsListsPure()
        if temp[-1][-1][-3:] == '...':
            return True
        return False

    # Checks if the caption continues an unfinished caption
    def finishedSentence(self):
        temp: str = self.getAllRowsAsListsPure()
        if (temp[0][0][0:3] == '...' or temp[0][0][0:2] == '..'):
            return True
        return False

    # Check if caption has multiple speakers
    def hasMultipleSpeakers(self):
        temp = self.__getSpeakerRows()
        if temp == []:
            return 1
        return len(temp)

    # Makes a copy of caption where only one speaker is taken
    def getCopyWithOneSpeaker(self,id):
        if id < self.hasMultipleSpeakers():
            text = '\n'.join(self.getAllSpeakers()[id])
            return Caption(text,self.index,self.start,self.end)

    # Gets the index of row, where the speaker begins
    def getSpeakerRow(self,id):
        temp = self.__getSpeakerRows()
        if temp == []:
            return 0
        return temp[id]

    # Checks if two captions have identical content
    def Equals(self,caption):
        if self.__caption == caption.getCaption():
            return True
        return False

    def getCaption(self):
        return self.__caption

    # def getTechnical(self,lst):
    #     result = []
    #     for row in lst:
    #         rowTemp = []
    #         for elem in row:
    #             if elem in closing:
    #                 rowTemp.append('bracket open')
    #             elif elem in closing.values():
    #                 rowTemp.append('bracket close')
    #             elif self.__isTagOpen(elem):
    #                 rowTemp.append('tag open')
    #             elif self.__isTagClose(elem):
    #                 rowTemp.append('tag close')
    #             elif self.__isLabel(elem):
    #                 rowTemp.append('label')
    #             elif self.__isDash(elem):
    #                 rowTemp.append('dash')
    #             elif self.__isSpecial(elem):
    #                 rowTemp.append('special')
    #             else:
    #                 rowTemp.append('word')
    #         result.append(rowTemp)
    #     return result

    # def getTechnicalSpeakers(self,lst):
    #     result = []
    #     for speaker in lst:
    #         result.append(self.getTechnical(speaker))
    #     return result

    # Get technical information about caption elements
    def getTechnical(self,lst):
        temp = lst
        for i in range(len(temp)):
            if temp[i] == '(\\n)':
                temp[i] = 'newline'
            elif temp[i] == '(\\c)':
                temp[i] = 'newcaption'
            elif temp[i][0] in closing:
                temp[i] = 'bracket open'
            elif temp[i][0] in closing.values():
                temp[i] = 'bracket close'
            elif self.__isTagOpen(temp[i]):
                temp[i] = 'tag open'
            elif self.__isTagClose(temp[i]):
                temp[i] = 'tag close'
            elif self.__isLabel(temp[i]):
                temp[i] = 'label'
            elif self.__isDash(temp[i]):
                temp[i] = 'dash'
            elif self.__isSpecial(temp[i]):
                temp[i] = 'special'
            else:
                temp[i] = 'word'
        return temp

    # Get list of indexes with enclosing symbols that enclose the whole caption
    def getEnclosing(self):
        result = [[],[]]
        temp = self.getAllRowsAsList()
        start = 0
        end = len(temp)-1
        while start < end:
            found = False
            # Should speaker identifiers be ignored?
            if self.__isSpeakerIdentifier(temp[start]):
                start+=1
                continue

            # if temp[start] in closing or temp[start] in specialClosingSymbols or self.__isTag(temp[start]):
            #     if temp[start] in closing and temp[end] == closing[temp[start]]:
            #         found = True
            #     if temp[start] in specialClosingSymbols and temp[end] == temp[start]:
            #         found = True
            #     if self.__isTag(temp[start]) and temp[end] == tags[temp[start][0:2]]:
            #         found = True

            if self.__isTag(temp[start]) and temp[end] == tags[temp[start][0:2]]:
                found = True
                

            
            if found == True:
                result[0].append(start)
                result[1].append(end)
                start+=1
                end-=1
            else:
                break

        return result


    def getEverythingInEnclosing(self):
        enclosings = self.getEnclosing()
        elements = self.getAllRowsAsList()
        result = []
        for i in range(len(elements)):
            if not(i in enclosings[0] or i in enclosings[1]):
                result.append(elements[i])
        return result



    # def __getPunctuation(self,text: str):
    #     if text[-1] == '!' or text[-1] == '?' or (text[-1] == '.' and not(text[-3:] == '...')):
    #         return 1
    #     if text[-3:] == '...':
    #         return 2
    #     if text[0:3] == '...' or text[0:2] == '..':
    #         return 3
    #     if text[-1] == ',' or text[-1] == ';':
    #         return 4
    #     return 0    

                



    

def getTime(self) -> float:
    timeSplit = str(self).replace(':','.').split('.')
    hours = int(timeSplit[0])
    minutes = int(timeSplit[1])
    seconds = int(timeSplit[2])
    miliseconds = int(timeSplit[3][0:3])

    print(hours)
    print(minutes)
    print(seconds)
    print(miliseconds)

    return ((hours*60)+minutes+((seconds+(miliseconds/1000))/60))



def removeNonWords(self):
    temp = removeNotes(self)
    temp = removeTags(temp)
    return __getCaptionWithNewLine(temp)

def getWordCount(self):
    temp = removeNonWords(self)
    return len(temp)

def getWPM(self: srt.Subtitle):
    wordCount = getWordCount(self.content)
    print(self.start)
    print(self.end)
    time = getTime(self.end) - getTime(self.start)
    return wordCount/time




def withoutLabel(self):
    if(self.haveLabel() == True):
        temp = self.replace(self.getLabel()+' ','')
        return temp

def getLabel(self) -> str:
    if(self.haveLabel() == True):
        temp = self.split(' ')
        return temp[0]

def sentenceDone(self):
    if(not(self[-1] == '.') or not(self[-1] == '?') or not(self[-1] == '!')):
        return False
    return True