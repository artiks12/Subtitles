import srt
import re

closing={
    '<b>':'</b>',
    '<i>':'</i>',
    '<u>':'</u>',
    '<font>':'</font>',
    '(':')',
    '[':']',
    '{':'}',
}

specialSymbols = ['♪']

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
        return text.replace('(','( ').replace(')',' )').replace('{','{ ').replace('}',' }').replace('[','[ ').replace(']',' ]')

    # Checks if there is a speaker identifier for a given row
    def __hasSpeaker(self, row):
        return self.__hasLabel(row) or self.__hasDash(row)

    def __isSpeakerIdentifier(self,elem):
        return self.__isLabel(elem) or self.__isDash(elem)

    # Checks if first element of a row is a label
    def __isLabel(self, first):
        return first[-1] == ':'

    # Checks if first element of a row is a label
    def __isDash(self, first):
        return re.match(r"-+",first)

    # Checks if there is a speaker label for a given row
    def __hasLabel(self, row):
        if(self.__isLabel(row[0])):
            return True
        return False

    # Checks if there is a dash identifier for a given row
    def __hasDash(self, row):
        if(self.__isDash(row[0])):
            return True
        return False

    # Get caption with newline symbol
    def __getCaptionWithNewLine(self):
        return self.__caption.replace('\n'," (\\n) ").split()

    # Get caption with newline symbol and without styling tags
    def __getCaptionWithNewLineWithoutSpecials(self):
        temp = self.__caption.replace('\n'," (\\n) ")
        temp = re.sub(r'<.*?>','',temp)
        temp = temp.split()
        return [x for x in temp if x not in specialSymbols]

    # Checks if element is a styling tag
    def __isTag(self, elem):
        if re.match(r'<.*?>',elem) == None:
            print("No Match")
        else:
            print("found Match")

    # Checks if element is a special symbol
    def __isSpecial(self,elem):
        return elem in specialSymbols

    # Get all rows, that start seperate speakers. If one speaker, then return empty list
    def __getSpeakerRows(self):
        result = []
        row = 0
        for l in self.getAllRowsAsListsWithoutSpecials():
            if self.__isSpeakerIdentifier(l[0]):
                result.append(row)
            row+=1
        return result

    def __fixBrackets(self, text):
        return text.replace('( ','(').replace(' )',')').replace('{ ','{').replace(' }','}').replace('[ ','[').replace(' ]',']').replace('"',' " ')
    

    # Get all rows as list elements
    def getAllRows(self) -> list:
        return self.__caption.split('\n')

    # Get all rows as lists of row elements
    def getAllRowsAsLists(self) -> list:
        result = []
        temp = []
        lst = self.__getCaptionWithNewLine()
        count = 1
        for l in lst:
            if not(l=='(\\n)'):
                temp.append(l)
            if l=='(\\n)' or count == len(lst):
                result.append(temp)
                temp = []
            count+=1
        return result

    # Get all rows as lists of row elements without special symbols
    def getAllRowsAsListsWithoutSpecials(self):
        result = []
        temp = []
        lst = self.__getCaptionWithNewLineWithoutSpecials()
        count = 1
        for l in lst:
            if not(l=='(\\n)'):
                temp.append(l)
            if l=='(\\n)' or count == len(lst):
                result.append(temp)
                temp = []
            count+=1
        return result

    # Get all rows as lists of row elements without special symbols
    def getAllRowsAsListsPure(self):
        result = []
        temp = []
        lst = self.__getCaptionWithNewLineWithoutSpecials()
        count = 1
        for l in lst:
            if not(l=='(\\n)'):
                if not((count==1 or lst[count-2] == '(\\n)') and l == '-') and not(self.__isLabel(l)):
                    temp.append(l)
            if l=='(\\n)' or count == len(lst):
                result.append(temp)
                temp = []
            count+=1
        return result

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

    def getAllSpeakers(self):
        return self.__getAllSpeakersBase(self.getAllRows())

    def getAllSpeakersAsLists(self):
        return self.__getAllSpeakersBase(self.getAllRowsAsLists())

    def getAllSpeakersAsListsWithoutSpecials(self):
        return self.__getAllSpeakersBase(self.getAllRowsAsListsWithoutSpecials())

    def getAllSpeakersAsListsPure(self):
        return self.__getAllSpeakersBase(self.getAllRowsAsListsPure())

    def getSingleSpeaker(self,id):
        temp = self.getAllSpeakers()
        if id >= len(temp):
            return None
        return temp[id]

    def getSingleSpeakerAsLists(self,id):
        temp = self.getAllSpeakersAsListsWithoutSpecials()[id]
        if id >= len(temp):
            return None
        return temp[id]

    def getSingleSpeakerAsListsWithoutSpecials(self,id):
        temp = self.getAllSpeakersAsListsWithoutSpecials()[id]
        if id >= len(temp):
            return None
        return temp[id]

    def getSingleSpeakerAsListsBase(self,id):
        temp = self.getAllSpeakersAsListsBase()[id]
        if id >= len(temp):
            return None
        return temp[id]

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

    def newSentenceForCaption(self):
        temp: list = self.getAllRowsAsListsPure()
        if temp[0][0].islower():
            return False
        return True

    def contSentenceForCaption(self):
        temp: list = self.getAllRowsAsListsPure()
        if temp[0][0].islower() and not(self.finishedSentenceForCaption()):
            return True
        return False
    
    def unfinishedSentenceForCaption(self):
        temp: str = self.getAllRowsAsListsPure()
        if temp[-1][-1][-3:] == '...':
            return True
        return False

    def finishedSentenceForCaption(self):
        temp: str = self.getAllRowsAsListsPure()
        if (temp[0][0][0:3] == '...' or temp[0][0][0:2] == '..'):
            return True
        return False

    def newSentenceForSpeaker(self,id):
        if id >= self.hasMultipleSpeakers():
            return False
        temp: list = self.getAllRowsAsListsPure()[id]
        if temp[0].islower():
            return False
        return True

    def contSentenceForSpeaker(self,id):
        if id >= self.hasMultipleSpeakers():
            return False
        temp: list = self.getAllRowsAsListsPure()[id]
        if temp[0].islower() and not(self.finishedSentenceForSpeaker(id)):
            return True
        return False
    
    def unfinishedSentenceForSpeaker(self,id):
        if id >= self.hasMultipleSpeakers():
            return False
        temp: str = self.getAllRowsAsListsPure()[id]
        if temp[-1][-3:] == '...':
            return True
        return False

    def finishedSentenceForSpeaker(self,id):
        if id >= self.hasMultipleSpeakers():
            return False
        temp: str = self.getAllRowsAsListsPure()[id]
        if (temp[0][0:3] == '...' or temp[0][0:2] == '..'):
            return True
        return False

     # Check if caption has multiple speakers
    def hasMultipleSpeakers(self):
        temp = self.getAllRowsAsLists()
        count = 0
        for i in temp:
            if(self.__hasSpeaker(i)):
                count+=1
        if(count != 0):
            return count
        else:
            return 1

    def getCopyWithOneSpeaker(self,id):
        if id < self.hasMultipleSpeakers():
            text = '\n'.join(self.getAllSpeakers()[id])
            return Caption(text,self.index,self.start,self.end)
            
    

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
    if(self[-1] != '.' or self[-1] != '?' or self[-1] != '!'):
        return False
    return True