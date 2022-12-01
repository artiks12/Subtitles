import srt
import re

closing={
    '(':')',
    '[':']',
    '{':'}',
}

tags={
    '<fo':'</font>',
    '<b>':'</b>',
    '<i>':'</i>',
    '<u>':'</u>'
}

specialClosingSymbols = ['♪','"','#']

class Caption(srt.Subtitle):
    # Constructor. Gets info on caption.
    def __init__(self, subtitle: srt.Subtitle, text = None) -> None:
        self.index = subtitle.index
        self.start = subtitle.start
        self.end = subtitle.end
        self.__original = subtitle.content
        self.translation = ''
        if text == None:
            self.__caption = self.__spaces(subtitle.content)
        else:
            self.__caption = text

    # Creates spaces around tags and brackets
    def __spaces(self, content):
        result = self.__spacesForTags(content)
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
        if re.match(r'<[^/].*?>',elem) == None:
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
        for l in self.getAllTextWithinEnclosingsRowsAsLists():
            for e in l:
                if self.__isSpeakerIdentifier(e):
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
        return self.__caption.replace('\n',' <br/> ')

    # Get caption as list of rows
    def getAllRowsAsList(self) -> list:
        return self.getAllRows().split()

    # Get caption as lists of row elements
    def getAllRowsAsLists(self) -> list:
        result = []
        for row in self.__caption.split('\n'):
            result.append(row.split())
        return result

    # Get all rows as lists of row elements without special symbols and tags
    def getAllTextWithinEnclosingsRowsAsLists(self):
        result = []
        rowTemp = []
        for elem in self.getTextWithinWholeEnclosings():
            if elem == '<br/>':
                result.append(rowTemp)
                rowTemp = []
            else:
                rowTemp.append(elem)
        if not(rowTemp==[]):
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
        return self.__getAllSpeakersBase(self.getWholeCaptionWithoutWholeEnclosing().split('<br/>'))

    def getWholeCaptionWithoutWholeEnclosing(self):
        text = self.getTextWithinWholeEnclosings()
        joined = ' '.join(text)
        return joined

    
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

    # Checks if the caption continues an unfinished caption
    def finishedSentence(self):
        temp: str = self.getAllRowsAsListsPure()
        if (temp[0][0][0:3] == '...' or temp[0][0][0:2] == '..'):
            return True
        return False
    
    # Checks if the caption is unfinished
    def unfinishedSentence(self):
        temp: str = self.getAllRowsAsListsPure()
        if temp[-1][-1][-3:] == '...':
            return True
        return False

    # Checks if the caption is unfinished
    def endsSentence(self):
        temp: str = self.getAllRowsAsListsPure()
        if (temp[-1][-1][-1] == '.' and not(self.unfinishedSentence())) or temp[-1][-1][-1] == '!' or temp[-1][-1][-1] == '?':
            return True
        if  temp[-1][-1][-1] == ')' or temp[-1][-1][-1] == '}' or temp[-1][-1][-1] == ']':
            return self.bracketCount(temp)
        return False

    # Checks if the caption continues in next caption
    def toContSentence(self):
        return not(self.unfinishedSentence() or self.endsSentence())

    # Check if caption has multiple speakers
    def hasMultipleSpeakers(self):
        temp = self.__getSpeakerRows()
        if temp == []:
            return 1
        return len(temp)

    # Makes a copy of caption where only one speaker is taken
    def getCopyWithOneSpeaker(self,id):
        if id < self.hasMultipleSpeakers():
            allRows = self.__getSpeakerRows()
            start = allRows[id]
            end = -1
            if not(id+1 == len(allRows)):
                end = allRows[id+1]
            else:
                end = len(allRows)+1
            allText = self.__original.split('\n')
            original = '\n'.join(allText[start:end])
            text = '\n'.join(self.getAllSpeakers()[id])
            newCaption = srt.Subtitle(self.index,self.start,self.end,original)
            return Caption(newCaption,text)

    # Gets the index of row, where the speaker begins
    def getSpeakerRow(self,id):
        temp = self.____getSpeakerRows()
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

    # Get technical information about caption elements
    def getTechnical(self,lst):
        temp = lst
        for i in range(len(temp)):
            if temp[i] == '<br/>':
                temp[i] = 'newline'
            elif temp[i] == '<hr/>':
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

    def isSpecialDivider(self,symbol):
        temp = self.getAllRowsAsList()
        count = 0
        for t in temp:
            if t == symbol:
                count += 1
        return count%2 == 0

    def getEnclosings(self):
        bracketBuffer={
            '(':[],
            '{':[],
            '[':[]
        }
        specialBuffer={
            '#':[],
            '♪':[],
            '"':[]
        }
        tagBuffer={
            '<b>':[],
            '<i>':[],
            '<u>':[],
            '<fo':[]
        }
        result = []
        temp = self.getAllRowsAsList()
        for i in range(len(temp)):
            # # Special symbol that starts enclosing (brackets and specials)
            # if temp[i] in bracketBuffer:
            #     bracketBuffer[temp[i]].append([i])
            if temp[i] in specialBuffer:
                if len(specialBuffer[temp[i]]) == 0:
                    specialBuffer[temp[i]].append([i])
                elif len(specialBuffer[temp[i]][-1]) < 2:
                    specialBuffer[temp[i]][-1].append(i)
                    if len(specialBuffer[temp[i]][-1]) == 2:
                        r = [specialBuffer[temp[i]][-1][0],specialBuffer[temp[i]][-1][1]]
                        result.append(r)
                else:
                    specialBuffer[temp[i]].append([i])

            # # Bracket ends enclosing
            # elif temp[i] in closing.values():
            #     key = list(closing.keys())[list(closing.values()).index(temp[i])]
            #     
            #     bracketBuffer['('][-1].append(i)
            #     r = [bracketBuffer['('][-1][0],bracketBuffer['('][-1][1]]
            #     result.append(r)
            #     bracketBuffer['('].pop()

            # Tag ends enclosing
            if temp[i] in tags.values():
                key = list(tags.keys())[list(tags.values()).index(temp[i])] # get key for tagBuffer

                tagBuffer[key][-1].append(i)
                r = [tagBuffer[key][-1][0],tagBuffer[key][-1][1]]
                result.append(r)
                tagBuffer[key].pop()
                    

            # Special symbol that starts enclosing (tags). First make sure string length is at least three.
            elif len(temp[i]) > 2:
                if temp[i][:3] in tagBuffer:
                    tagBuffer[temp[i][:3]].append([i])
        result.sort()
        return result

    def getWholeEnclosings(self):
        temp = self.getEnclosings()
        count = len(self.getAllRowsAsList())
        result = []
        for t in temp:
            if t[0]+t[1] == count-1:
                result.append(t)
        return result

    def getTextWithinWholeEnclosings(self):
        temp = self.getAllRowsAsList()
        enclosings = self.getWholeEnclosings()
        if len(enclosings) == 0:
            return temp
        return temp[enclosings[-1][0]+1:enclosings[-1][1]]

    def replaceUnfinished(self):
        temp = self.getAllRowsAsList()
        result = []
        for i in temp:
            if len(i) > 2:
                if i[-3:] == '...':
                    result.append(i[:-3])
                    result.append('<img src="T"/>')
                else:
                    if i[:3] == '...':
                        result.append('<img src="F"/>')
                        result.append(i[3:])
                    elif i[:2] == '..':
                        result.append('<img src="F"/>')
                        result.append(i[2:])
                    else:
                        result.append(i)
            else:
                result.append(i)
        return result

    def getWholeEnclosingContent(self):
        temp = self.getWholeEnclosings()
        text = self.getAllRowsAsList()
        begin = []
        end = []
        for t in temp:
            if text[t[0]] == '♪':
                begin.append('# ')
            else:
                begin.append(text[t[0]])
            if text[t[1]] == '♪':
                end = [' #'] + end
            else:
                end = [text[t[1]]] + end
        return [begin,end]

    def bracketCount(self,lst):
        bracketsBuffer = {
            "(" : 0,
            "{" : 0,
            "[" : 0
        }
        for row in lst:
            for elem in row:
                if elem == '(':
                    bracketsBuffer['('] += 1
                elif elem == '{':
                    bracketsBuffer['{'] += 1
                elif elem == '[':
                    bracketsBuffer['['] += 1
                elif elem == ')':
                    bracketsBuffer['('] -= 1
                elif elem == '}':
                    bracketsBuffer['{'] -= 1
                elif elem == ']':
                    bracketsBuffer['['] -= 1
        for b in bracketsBuffer.values():
            if not(b == 0):
                return False

        return True

    def getOriginalWithoutTagsAndExtraSpaces(self):
        text = re.sub(r'<.*?>','',self.__original).split('\n')
        temp = []
        for row in text:
            start = 0
            end = -1
            for i in range(len(row)):
                if not(row[i] == ' '):
                    start = i
                    break
            for i in reversed(range(len(row))):
                if not(row[i] == ' '):
                    end = i+1
                    break
            temp.append(row[start:end])
        return '\n'.join(temp)


    def geCharacterCountInRows(self):
        text = self.getOriginalWithoutTagsAndExtraSpaces().split('\n')
        result = []
        for row in text:
            result.append(len(row))
        return result

    def getOriginal(self):
        return self.__original






        


                




                



    

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