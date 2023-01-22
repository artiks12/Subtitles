import srt
import re
import Constants

closing={
    '(':')',
    '[':']',
    '{':'}',
    '“':'”',
}

tags={
    '<fo':'</font>',
    '<b>':'</b>',
    '<i>':'</i>',
    '<u>':'</u>'
}

specialClosingSymbols = ['♪','#']

class Caption(srt.Subtitle):
    # Constructor. Gets info on caption.
    def __init__(self, subtitle: srt.Subtitle, row: int, caption: list = None, divided: bool = False) -> None:
        self.__row = row
        self.index = subtitle.index
        self.start = subtitle.start
        self.end = subtitle.end
        self.__original = subtitle.content.replace('…','...')
        self.translation = ''
        self.divided = divided
        if caption == None:
            temp = self.__spaces(subtitle.content.replace('…','...'))
            self.__caption = self.__getAllRowsAsLists(temp)
        else:
            self.__caption = caption

    ##########          Private methods         ##########
    # Creates spaces around tags and brackets
    def __spaces(self, content: str):
        result = self.__spacesForTags(content)
        result = self.__spacesForBrackets(result)
        result = self.__replaceQuotes(result)
        return result

    # Creates spaces around tags
    def __spacesForTags(self, text: str):
        temp = re.findall(r'<.*?>',text)
        result = text
        for t in temp:
            n = ' '+t+' '
            result = result.replace(t,n)
        return result

    # Replaces quotes for styling
    def __replaceQuotes(self, text: str):
        result = []
        rows = text.split('\n')
        for row in rows:
            temp = []
            words = row.split()
            for word in words:
                new = word
                if len(new) > 0:
                    if new[0] == '"':
                        new = '“ ' + new[1:]
                    if new.find('"') > -1:
                        new = new.replace('"',' ”')
                temp.append(new)
            result.append(' '.join(temp))
        return '\n'.join(result)

    # Creates spaces around brackets and quotes
    def __spacesForBrackets(self, text: str):
        return text.replace('(','( ').replace(')',' )').replace('{','{ ').replace('}',' }').replace('[','[ ').replace(']',' ]')

    # Checks if element is speaker identifier
    def __isSpeakerIdentifier(self,elem):
        return self.__isLabel(elem) or self.__isDash(elem)

    # Checks if first element of a row is a label
    def __isLabel(self, first):
        return first[-1] == ':' and first[:-1].upper()

    # Checks if first element of a row is a dash
    def __isDash(self, first):
        return re.match(r"-+",first) or re.match(r"–+",first)

    # Checks if element is a styling tag
    def __isTag(self, elem):
        if re.match(r'<.*?>',elem) == None:
            return False
        return True

    # Checks if element is an opening styling tag
    def __isTagOpen(self, elem):
        if re.match(r'<[^/].*?>',elem) == None:
            return False
        return True

    # Checks if element is a closing styling tag
    def __isTagClose(self, elem):
        if re.match(r'</.*?>',elem) == None:
            return False
        return True

    # Checks if element is a special enclosing symbol
    def __isSpecial(self,elem):
        return elem in specialClosingSymbols

    # Get all rows, that start seperate speakers. If one speaker, then return empty list
    def __getSpeakerRows(self):
        result = []
        currentRow = 0
        for row in self.__caption:
            tech = self.getTechnical(row)
            for i in range(len(row)):
                if tech[i] == 'speaker':
                    result.append(currentRow)
            currentRow+=1
        return result

    # Base function for getting all speaker texts
    def __getAllSpeakersBase(self,lists):
        rowIndexes = self.__getSpeakerRows()
        if rowIndexes == []:
            return [lists]
        result = []
        count = 0
        for rowIndex in rowIndexes:
            end = -1
            if count+1==len(rowIndexes):
                end = len(lists)
            else:
                end = rowIndexes[count+1]
            result.append(lists[rowIndex:end])
            count+=1
        return result
    
    # Get caption as lists of row elements
    def __getAllRowsAsLists(self,text: str) -> list:
        result = []
        for row in text.split('\n'):
            result.append(row.split())
        return result

    ##########          Get fields         ##########
    # Check if whole text is a sound effect
    def isEffect(self):
        return self.__original.isupper()

    # Get text as list
    def getCaption(self):
        return self.__caption
    
    # Get original text
    def getOriginal(self):
        return self.getTextStringFromList(self.__caption,False)

    # Get indexes for caption rows. Used for MT evaluation.
    def getRowIndexes(self):
        rows = self.getRowCount()
        result = []
        for i in range(rows):
            result.append(i+self.__row)
        return result

    # Gets a speaker label from caption. Returns None if there is no label
    def getLabel(self):
        result = None
        for row in self.__caption:
            tech = self.getTechnical(row)
            for i in range(len(row)):
                if tech[i] == 'speaker' and self.__isLabel(row[i]):
                    return row[i]
        return None

    def getBracketAndQuoteCount(self):
        result = {
            "(" : 0,
            "{" : 0,
            "[" : 0,
            "“" : 0,
        }
        for row in self.__caption:
            for elem in row:
                if elem[0] in closing.keys():
                    result[elem[0]] += 1
                if elem[0] in closing.values():
                    key = list(closing.keys())[list(closing.values()).index(elem[0])]
                    result[key] -= 1
        return result

    ##########          Get Text (Base functions)         ##########
    # Get caption as list of elements. Newlines are replaced with <br/>.
    def getAllRowsAsListWithBreaks(self,lst) -> list:
        result = []
        for row in lst:
            if len(result) > 0:
                result.append('<br/>')
            result.extend(row)
        return result
    
    def getAllRowsAsListWithoutBreaks(self,lst) -> list:
        result = []
        for row in lst:
            result.extend(row)
        return result

    # Get caption as lists of row elements excluding elements by technical
    def getAllRowsAsListsExcludingByTechnical(self,exclude: list) -> list:
        result = []
        for row in self.__caption:
            rowTemp = []
            tech = self.getTechnical(row)
            for i in range(len(row)):
                if not(tech[i] in exclude):
                    rowTemp.append(row[i])
            result.append(rowTemp)
        return result

    # Get caption as lists of row elements excluding elements by lement id
    def getAllRowsAsListsExcludingById(self,exclude: list) -> list:
        result = []
        index = 0
        for row in self.__caption:
            rowTemp = []
            for i in range(len(row)):
                if not(index in exclude):
                    rowTemp.append(row[i])
                index += 1
            result.append(rowTemp)
        return result

    ##########          Enclosing Functions         ##########
    # Get all enclosing pair ids.
    def getEnclosings(self):
        bracketBuffer={
            '(':[],
            '{':[],
            '[':[],
            '“':[]
        }
        specialBuffer={
            '#':[],
            '♪':[]
        }
        tagBuffer={
            '<b>':[],
            '<i>':[],
            '<u>':[],
            '<fo':[]
        }
        result = []
        temp = self.getAllRowsAsListWithoutBreaks(self.__caption)
        for i in range(len(temp)):
            # # Special symbol that starts enclosing (brackets and specials)
            # if temp[i] in bracketBuffer:
            #     bracketBuffer[temp[i]].append([i-newlines])
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
                if len(tagBuffer[key]) > 0:
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

    # Get enclosings that cover the whole subtitle.
    def getWholeEnclosings(self):
        temp = self.getEnclosings()
        count = len(self.getAllRowsAsListWithoutBreaks(self.__caption))
        result = []
        for t in temp:
            if t[0]+t[1] == count-1:
                result.append(t)
            else:
                break
        return result

    # Keeps track of brackets and validifies them.
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

    ##########          Get Text String From List         ##########
    # Gets a string from list. Oneline - should the text be on one line
    def getTextStringFromList(self,lst,oneline):
        result = ''
        for row in lst:
            if not(result == ''):
                if oneline == False:
                    result= result[:-1] + '\n'
            tech = self.getTechnical(row)
            for i in range(len(row)):
                if tech[i] == Constants.CAPTION_TECHNICAL_BRACKET_CLOSE or tech[i] == Constants.CAPTION_TECHNICAL_TAG_CLOSE:
                    if row[i] == '”':
                        result = result[:-1] + '"' + ' '
                    else:
                        result = result[:-1] + row[i] + ' '
                elif tech[i] == Constants.CAPTION_TECHNICAL_BRACKET_OPEN or tech[i] == Constants.CAPTION_TECHNICAL_TAG_OPEN:
                    if row[i] == '“':
                        result += '"'
                    else:
                        result += row[i]
                elif tech[i] == Constants.CAPTION_TECHNICAL_NEWLINE and oneline == False:
                    result = result[:-1] + '\n'
                else:
                    result += row[i] + ' '
        if result[-1] == ' ':
            return result[:-1]
        return result

    ##########          Get Text (List Search functions)         ##########
    # Get all rows as lists of row elements without special symbols and tags
    def getAllTextWithinEnclosingsRowsAsLists(self):
        enclosings = []
        for e in self.getWholeEnclosings():
            enclosings.extend(e)
        return self.getAllRowsAsListsExcludingById(enclosings)

    # Get all rows as lists of row elements without special symbols, speaker identifiers and tags
    def getAllRowsAsListsPure(self):
        excludes = [
            Constants.CAPTION_TECHNICAL_TAG_OPEN,
            Constants.CAPTION_TECHNICAL_TAG_CLOSE,
            Constants.CAPTION_TECHNICAL_SPEAKER,
            Constants.CAPTION_TECHNICAL_SPECIAL
        ]
        return self.getAllRowsAsListsExcludingByTechnical(excludes)
    
    # Get all text seperated by speakers
    def getAllSpeakers(self):
        return self.__getAllSpeakersBase(self.getAllTextWithinEnclosingsRowsAsLists())

    def getTextWithinWholeEnclosings(self):
        temp = self.getAllTextWithinEnclosingsRowsAsLists()
        return self.getAllRowsAsListWithBreaks(temp)

    ##########          Subtitle State Functions (Begining)         ##########
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

    ##########          Subtitle State Functions (End)         ##########
    # Checks if the caption is unfinished
    def unfinishedSentence(self):
        temp: str = self.getAllRowsAsListsPure()
        if temp[-1][-1][-3:] == '...':
            return True
        elif temp[-1][-1] in closing.values():
            if temp[-1][-2][-3:] == '...':
                return True
        return False

    # Checks if the caption is unfinished
    def endsSentence(self):
        temp: str = self.getAllRowsAsListsPure()
        if (temp[-1][-1][-1] == '.' and not(self.unfinishedSentence())) or temp[-1][-1][-1] == '!' or temp[-1][-1][-1] == '?':
            return True
        elif temp[-1][-1] in closing.values():
            if (temp[-1][-2][-1] == '.' and not(self.unfinishedSentence())) or temp[-1][-2][-1] == '!' or temp[-1][-2][-1] == '?':
                return True
        elif  temp[-1][-1][-1] in closing.values() and not(temp[-1][-1][-1] == '”'):
            return self.bracketCount(temp)
        return False

    # Checks if the caption continues in next caption
    def toContSentence(self):
        return not(self.unfinishedSentence() or self.endsSentence())

    # Gets difference between opening and closing quotes.
    def quoteCount(self):
        count = 0
        for elem in self.getAllRowsAsListWithoutBreaks(self.__caption):
            count += (elem.count('“') - elem.count('”'))
        return count

    ##########          Multiple Speaker Functions         ##########
    # Check if caption has multiple speakers
    def hasMultipleSpeakers(self):
        temp = self.__getSpeakerRows()
        if temp == []:
            return 1
        return len(temp)

    # Gets start rows for every speaker
    def getRowIndexesForAllSpeakers(self):
        if self.__getSpeakerRows() == []:
            return self.getRowIndexes()
        result = []
        for r in self.__getSpeakerRows():
            result.append(r+self.__row)
        return result 

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
            text = self.getAllSpeakers()[id]
            row = self.getRowIndexesForAllSpeakers()[id]
            newCaption = srt.Subtitle(self.index,self.start,self.end,original)
            return Caption(newCaption,row,text,True)

    # Gets the index of row, where the speaker begins
    def getSpeakerRow(self,id):
        temp = self.__getSpeakerRows()
        if temp == []:
            return 0
        return temp[id]


    ##########          Technical Functions         ##########
    # Checks if two captions have identical content
    def Equals(self,caption):
        if self.__caption == caption.getCaption():
            return True
        return False

    # Get technical information about caption elements
    def getTechnical(self,lst):
        result = []
        first = True
        for i in range(len(lst)):
            if lst[i] == '<br/>':
                result.append(Constants.CAPTION_TECHNICAL_NEWLINE)
                first = True
            elif lst[i] == '<hr/>':
                result.append(Constants.CAPTION_TECHNICAL_NEWCAPTION)
                first = True
            elif lst[i][0] in closing:
                result.append(Constants.CAPTION_TECHNICAL_BRACKET_OPEN)
                first = False
            elif lst[i][0] in closing.values():
                result.append(Constants.CAPTION_TECHNICAL_BRACKET_CLOSE)
                first = False
            elif self.__isTagOpen(lst[i]):
                result.append(Constants.CAPTION_TECHNICAL_TAG_OPEN)
            elif self.__isTagClose(lst[i]):
                result.append(Constants.CAPTION_TECHNICAL_TAG_CLOSE)
            elif self.__isLabel(lst[i]) and first==True:
                result.append(Constants.CAPTION_TECHNICAL_SPEAKER)
                first = False
            elif self.__isDash(lst[i]) and first==True:
                result.append(Constants.CAPTION_TECHNICAL_SPEAKER)
                first = False
            elif self.__isDash(lst[i]) and first==False:
                result.append(Constants.CAPTION_TECHNICAL_DASH)
                first = False
            elif self.__isSpecial(lst[i]):
                result.append(Constants.CAPTION_TECHNICAL_SPECIAL)
            else:
                result.append(Constants.CAPTION_TECHNICAL_WORD)
                first = False
        return result

    ##########          Get Text (String Search functions)         ##########
    # Get all text in whole enclosings as string in one line.
    def getWholeCaptionWithoutWholeEnclosing(self):
        text = [self.getTextWithinWholeEnclosings()]
        return self.getTextStringFromList(text,False)

    # Gets whole enclosings. Used for translation construction.
    def getWholeEnclosingContent(self):
        temp = self.getWholeEnclosings()
        text = self.getAllRowsAsListWithoutBreaks(self.__caption)
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

    # Get text excluding tags and extra whitespaces, that appear before first non-empty symbol and after last non-empty symbol. Used for evaluation.
    def getTextWithoutTagsAndExtraSpaces(self,caption):
        text = re.sub(r'<.*?>','',caption).split('\n')
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

    # Get original subtitle without whole enclosings.
    def getOriginalWithoutEnclosings(self):
        temp = self.getTextWithinWholeEnclosings()
        result = ''
        quote = False
        for t in temp:
            if t == '<br/>':
                result = result[:-1] + '\n'
            elif self.__isTag(t) or t in closing:
                result += t
            elif t[0] in closing.values():
                result = result[:-1] + t + ' '
            elif t == '"':
                if quote == False:
                    result += t
                    quote = True
                else:
                    result = result[:-1] + t + ' '
                    quote = False
            else:
                result += t + ' '
        if result[-1] == ' ':
            result = result[:-1]
        return result

    # Get translation to put in subtitle file.
    def getTranslation(self):
        return self.translation 

    # Get all rows as lists of row elements without speaker identifiers
    def getOriginalWithoutSpeakerIdentifier(self):
        return self.getTextStringFromList(self.getAllRowsAsListsExcludingByTechnical([Constants.CAPTION_TECHNICAL_SPEAKER]),True)

    ##########          Evaluation Functions         ##########
    # Gets amount of rows for caption.
    def getRowCount(self, caption = None):
        if caption == None:
            return len(self.__caption)
        return len(caption)

    # Gets character count in each row (excluding tags).
    def getCharacterCountInRows(self, caption = None):
        text = ''
        if caption == None:
            text = self.getTextWithoutTagsAndExtraSpaces(self.__original).split('\n')
        else:
            text = self.getTextWithoutTagsAndExtraSpaces(caption).split('\n')
        result = []
        for row in text:
            result.append(len(row))
        return result

    # Gets character count in whole subtitle row (excluding tags).
    def getCharacterCount(self, caption = None):
        return sum(self.getCharacterCountInRows(caption))

    # Get word count in subtitle
    def getWordCount(self, caption = None):
        lst = []
        if caption == None:
            lst = self.getAllRowsAsListWithBreaks(self.__caption)
        else:
            lst = caption
        temp = self.getTechnical(lst)
        words = list(filter(lambda tech: tech == 'word', temp))
        return len(words)

    # Get amount of time from timedelta in minutes
    def getTimeInMinutesFromString(self,time) -> float:
        timeSplit = str(time).replace(':','.').split('.')
        hours = int(timeSplit[0])
        minutes = int(timeSplit[1])
        seconds = int(timeSplit[2])
        miliseconds = 0
        if len(timeSplit) == 4:
            miliseconds = int(timeSplit[3])/1000

        return ((hours*60)+minutes+((seconds+(miliseconds/1000))/60))

    # Get amount of time to display subtitle in minutes
    def getTimeInMinutes(self):
        start = self.getTimeInMinutesFromString(self.start)
        end = self.getTimeInMinutesFromString(self.end)
        return end-start

    # Get subtitle WPM (words per minute)
    def getWPM(self,caption = None):
        time = self.getTimeInMinutes()
        words = self.getWordCount(caption)
        return round(words/time,3)

    # Get amount of time from timedelta in minutes
    def getTimeInSecondsFromString(self,time) -> float:
        timeSplit = str(time).replace(':','.').split('.')
        hours = int(timeSplit[0])
        minutes = int(timeSplit[1])
        seconds = int(timeSplit[2])
        miliseconds = 0
        if len(timeSplit) == 4:
            miliseconds = int(timeSplit[3])/1000

        return (hours*3660)+(minutes*60)+seconds+(miliseconds/1000)

    # Get subtitle WPM (words per minute)
    def getCPS(self,caption = None):
        time = self.getTimeInSeconds()
        count = self.getCharacterCount(caption)
        return round(count/time,3)

    # Get amount of time to display subtitle in minutes
    def getTimeInSeconds(self):
        start = self.getTimeInSecondsFromString(self.start)
        end = self.getTimeInSecondsFromString(self.end)
        return end-start

    # Get all calculated evaluation data for original
    def getEvaluationDataForOriginal(self):
        wpm = self.getWPM()
        cps = self.getCPS()
        characterCounts = self.getCharacterCountInRows()

        wpmRes = 180 - wpm >= 0
        cpsRes = 17 - cps >= 0
        rowRes = 3 - len(characterCounts) >= 0
        charRes = all(37 - c >= 0 for c in characterCounts)

        return [wpm,cps,len(characterCounts),characterCounts,wpmRes,cpsRes,rowRes,charRes]

    # Get all calculated evaluation data for translation
    def getEvaluationDataForTranslation(self):
        withSpaces = self.__spaces(self.translation)
        translationAsList = withSpaces.replace('\n',' <br/> ').split()
        
        wpm = self.getWPM(translationAsList)
        cps = self.getCPS(self.translation)
        characterCounts = self.getCharacterCountInRows(self.translation)
        originalRows = len(self.getCharacterCountInRows(self.__original))
        
        wpmRes = 150 - wpm >= 0
        cpsRes = 17 - cps >= 0
        rowRes = originalRows - len(characterCounts) >= 0 or 2 - len(characterCounts) >= 0
        charRes = all(37 - c >= 0 for c in characterCounts)

        return [wpm,cps,len(characterCounts),characterCounts,wpmRes,cpsRes,rowRes,charRes]
            
    # Get all calculated evaluation data
    def getEvaluationData(self):
        original = self.getEvaluationDataForOriginal()
        translation = self.getEvaluationDataForTranslation()

        originalValues = original[:4]
        originalValues[-1] = sum(originalValues[-1])
        translationValues = translation[:4]
        translationValues[-1] = sum(translationValues[-1])

        originalIsGood = original[4:8]
        translationIsGood = translation[4:8]

        isOriginalGoodWPM = original[4] and original[6] and original[7]
        isTranslationGoodWPM = translation[4] and translation[6] and translation[7]
        isOriginalGoodCPS = original[5] and original[6] and original[7]
        isTranslationGoodCPS = translation[5] and translation[6] and translation[7]

        return [self.index,originalValues,translationValues,originalIsGood,translationIsGood,isOriginalGoodWPM,isTranslationGoodWPM,isOriginalGoodCPS,isTranslationGoodCPS]

    # Gets all evaluation data as string for csv file
    def evaluationDataToString(self,data):
        originalValues = ','.join(map(str,data[1]))
        translationValues = ','.join(map(str,data[2]))

        originalIsGood = ','.join(map(str,data[3]))
        translationIsGood = ','.join(map(str,data[4]))

        isOriginalGoodWPM = str(data[5])
        isTranslationGoodWPM = str(data[6])
        isOriginalGoodCPS = str(data[7])
        isTranslationGoodCPS = str(data[8])

        result = [str(data[0]),originalValues,translationValues,originalIsGood,translationIsGood,isOriginalGoodWPM,isTranslationGoodWPM,isOriginalGoodCPS,isTranslationGoodCPS]

        return ','.join(result)
