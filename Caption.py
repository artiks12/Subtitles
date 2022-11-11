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

class Caption(srt.Subtitle):
    def __init__(self, subtitle: srt.Subtitle) -> None:
        self.__caption = self.__spaces(subtitle)
        self.index = subtitle.index
        self.start = subtitle.start
        self.end = subtitle.end

    def __spaces(self, subtitle):
        result = self.__spacesForTags(subtitle.content)
        result = self.__spacesForBrackets(result)
        return result

    def __spacesForTags(self, text: str):
        temp = re.findall(r'<.*?>',text)
        result = text
        for t in temp:
            n = ' '+t+' '
            result = result.replace(t,n)
        return result

    def __spacesForBrackets(self, text: str):
        return text.replace('(','( ').replace(')',' )').replace('{','{ ').replace('}',' }').replace('[','[ ').replace(']',' ]')

    def getOneList(self):
        temp = self.__caption.replace('\n',r" (\n) ")
        return temp.split()

    def removeNewLines(self) -> list:
        return list(filter(lambda x: x != '(\\n)', self.getOneList()))

    def removeTags(self, text: list):
        p = re.findall(r'<.*?>',self.getOneLine())
        result = []
        for t in text:
            if t not in p:
                result.append(t)
        return result

    def removeNotes(self, text: list):
        return list(filter(lambda x: x != '♪', text))

    def getOneLine(self) -> str:
        return ' '.join(self.removeNewLines())

    def getOneLinePure(self):
        temp = self.removeNewLines()
        temp = self.removeTags(temp)
        temp = self.removeNotes(temp)
        return ' '.join(temp)

    def getAllLists(self) -> list:
        result = []
        temp = []
        lst = self.getOneList()
        count = 1
        for i in lst:
            if(count == len(lst)):
                temp.append(i)
                result.append(temp)
                temp = []
            elif(i != '(\\n)'):
                temp.append(i)
            else:
                result.append(temp)
                temp = []
            count+=1
        return result

    def getAllListsPureText(self):
        result = []
        temp = []
        lst = self.getOneList()
        p = re.findall(r'<.*?>',self.getOneLine())
        count = 1
        for i in lst:
            if(i not in p and not(self.__isLabel(i))):
                if(count == len(lst)):
                    temp.append(i)
                    result.append(temp)
                    temp = []
                elif(i != '(\\n)'):
                    temp.append(i)
                else:
                    result.append(temp)
                    temp = []
            else:
                if(count == len(lst)):
                    result.append(temp)
                    temp = []
            count+=1
        return result

    def haveMultipleSpeakers(self):
        temp = self.getAllLists()
        count = 0
        for i in temp:
            if(self.__hasSpeaker(i)):
                count+=1
        if(count != 0):
            return count
        else:
            return 1

    def __hasSpeaker(self, lst):
        return self.__hasLabel(lst) or self.__hasDash(lst)

    def __isLabel(self, item):
        return item[-1] == ':'

    def __hasLabel(self, lst):
        if(self.__isLabel(lst[0])):
            return True
        return False

    def __hasDash(self, lst):
        if(re.match(r"-+",lst[0])):
            return True
        return False

    def hasLabel(self):
        if(self.getOneList()[0][-1] == ':'):
            return True
        return False

    def getMultipleSpeakers(self):
        if(self.haveMultipleSpeakers() == 1):
            return self.getOneList()
        lists = self.getAllLists()
        result = []
        temp = lists[0]
        count = 1
        for i in lists:
            if(self.__hasDash(i) or self.__hasLabel(i)):
                if(count != 1): 
                    result.append(temp)
                temp = i
            else:
                temp.append('(\\n)')
                temp.extend(i)
            if(count == len(lists)):
                    result.append(temp)
            count+=1
        return result

    def newSentence(self):
        temp: list = self.getAllListsPureText()
        if temp[0][0].islower():
            return False
        return True
    
    def unfinished(self):
        temp: str = self.getAllListsPureText()
        if temp[-1][-3:-1] == '...':
            return True
        return False

    def getsFinished(self):
        temp: str = self.getAllListsPureText()
        if temp[-1][0:2] == '...' or temp[-1][0:1] == '..':
            return True
        return False


    

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
    return getOneList(temp)

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