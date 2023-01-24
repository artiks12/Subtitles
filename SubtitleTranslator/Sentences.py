from Caption import Caption
from Caption import specialClosingSymbols
from Caption import closing
from Caption import tags
import re
import Translator
import math

class Sentences():
    def __init__(self, subtitle: Caption, label = None, multiple = False) -> None:
        self.__captions: list = [subtitle]
        self.multipleSpeakers = multiple
        self.label = label
        self.unfinished = False

    # Gets all captions
    def getCaptions(self):
        return self.__captions

    # Is text within brackets and Quotes
    def inEnclosing(self):
        buffer = {
            "(" : 0,
            "{" : 0,
            "[" : 0,
            "“" : 0,
        }
        for c in self.__captions:
            temp = c.getBracketAndQuoteCount()
            for t in temp:
                buffer[t] += temp[t]
        for t in buffer:
            if buffer[t] > 0:
                return True
        return False

    # Add caption that continues previous caption
    def addCaption(self,caption: Caption):
        self.__captions.append(caption)

    # Checks if the last sentence can be continued
    def canAdd(self):
        return self.__captions[-1].toContSentence()

    # Checks if the last sentence is an unfinished sentence
    def canFinish(self):
        return self.__captions[-1].unfinishedSentence()

    # Gets caption indexes
    def getIndexes(self) -> list:
        result = []
        for i in self.__captions:
            result.append(i.index)
        return result

    # Gets specific caption indexes
    def getSpecificIndexes(self,start,end):
        startIndex = self.getIndexes().index(start)
        endIndex = self.getIndexes().index(end)
        return self.getIndexes()[startIndex:endIndex+1]

    # Gets specific caption index
    def getSpecificIndex(self,index):
        return self.getIndexes().index(index)

    # Are there any tags and brackets left?
    def areBuffersEmpty(self,bracketsBuffer,tagsBuffer):
        for b in bracketsBuffer.values():
            if b > 0:
                return False

        for b in tagsBuffer.values():
            if b > 0:
                return False

        return True

    # Get combination of all captions with technical
    def combine(self):
        result = [[],[]]
        count = 0
        for caption in self.__captions:
            text = caption.getTextWithinWholeEnclosings()
            technical = caption.getTechnical(caption.getTextWithinWholeEnclosings())
            result[0].extend(text)
            result[1].extend(technical)
            count += 1
            if count < len(self.__captions):
                result[0].append('<hr/>')
                result[1].append('newcaption')
        return result

    # option = 1 - with tags <br/> <hr/>
    # option = 2 - without tags <br/> <hr/>
    def getWholeSentences(self,option = 2):
        result = []
        # Difference between opening and closing brackets/quotes
        bracketsBuffer = {
            "(" : 0,
            "{" : 0,
            "[" : 0,
            "“" : 0,
        }
        # Difference between opening and closing tags
        tagsBuffer={
            '<fo': 0,
            '<b>': 0,
            '<i>': 0,
            '<u>': 0,
        }
        # Special enclosing symbol active (true) or not (false)
        specialBuffer={
            '#': False,
            '♪': False
        }
        # Temporary result
        sentence = {
            "start":[],
            "end":[],
            "text":[],
            "speakers":[],
            "enclosings":[],
            "unfinished":[],
        }
        # Text within enclosings
        enclosing = {
            "(" : [],
            "{" : [],
            "[" : [],
            "“" : [],
            "#" : [],
            "♪" : []
        }
        combined = self.combine()   # Get all captions with technical combined
        endOfSentence = False   # Is end of sentence
        threeDots = -1
        unfinished = -1
        indexCaption = 0    # current caption index
        indexRow = 0    # current row in captoion
        punctuation = []    # punctuations in last element
        word = 0    # current element
        sentence["start"] = [self.getIndexes()[indexCaption],indexRow]
        for l in range(len(combined[0])):
            # Put next element in all enclosings
            for e in enclosing:
                if e=='(' or e=='{' or e=='[' or e=='“':
                    for sub in enclosing[e]:
                        sub.append(combined[0][l])
                else:
                    if specialBuffer[e] == True:
                        if combined[1][l] == 'special' and not(e==combined[0][l]):
                            enclosing[e].append(combined[0][l])
                        elif combined[1][l] == 'newcaption' or combined[1][l] == 'newline':
                            if option == 1:
                                enclosing[e].append(combined[0][l])
                    
            
            # Opening bracket
            if combined[1][l] == 'bracket open':
                bracketsBuffer[combined[0][l]] += 1
                enclosing[combined[0][l][0]].append([combined[0][l]])
            
            # Opening tag
            if combined[1][l] == 'tag open':
                tagsBuffer[combined[0][l][:3]] += 1

            # Closing bracket
            if combined[1][l] == 'bracket close':
                key = list(closing.keys())[list(closing.values()).index(combined[0][l][0])] # get key
                bracketsBuffer[key] -= 1
                bracket = []
                for e in enclosing[key][-1]:
                    bracket.append(e)
                sentence["enclosings"].append(bracket)
                enclosing[key].pop()
            
            # Closing tag
            if combined[1][l] == 'tag close':
                key = list(tags.keys())[list(tags.values()).index(combined[0][l])][:3] # get key
                tagsBuffer[key] -= 1

            # Special enclosing symbol
            if combined[1][l] == 'special':
                if specialBuffer[combined[0][l]] == False:
                    enclosing[combined[0][l]].append(combined[0][l])
                    specialBuffer[combined[0][l]] = True
                else:
                    special = []
                    for e in enclosing[combined[0][l]]:
                        special.append(e)
                    sentence["enclosings"].append(special)
                    enclosing[combined[0][l]] = []
                    specialBuffer[combined[0][l]] = False

            # Speasker identifier
            if combined[1][l] == 'speaker':
                sentence["speakers"].append([combined[0][l],self.__captions[indexCaption].index])

            # Text
            if combined[1][l] == 'word':
                punctuation = self.__getPunctuation(combined[0][l])
                if endOfSentence == True and self.checkBuffers(bracketsBuffer,tagsBuffer,specialBuffer):
                    if combined[0][l].islower() or 3 in punctuation:
                        last = result[unfinished]
                        last["end"] = []
                        last["text"].extend(sentence["text"])
                        last["speakers"].extend(sentence["speakers"])
                        last["enclosings"].extend(sentence["enclosings"])
                        last["unfinished"].extend(sentence["unfinished"])
                        if combined[0][l].islower() and not(3 in punctuation):
                            last["unfinished"][-1].append([self.__captions[indexCaption].index,indexRow,word+1])
                        sentence = last
                        sentence["text"][threeDots] = self.getWordWithoutMultipoints(sentence["text"][threeDots])
                        result.pop()
                    else:
                        word = 0
                    unfinished = -1
                    endOfSentence = False

                word += 1
                
                if 1 in punctuation:
                    endOfSentence = True
                if 3 in punctuation:
                    sentence["unfinished"]
                    sentence["unfinished"][-1].append([self.__captions[indexCaption].index,indexRow,word])
                    threeDots = -1
                if 2 in punctuation:
                    sentence["unfinished"].append([[self.__captions[indexCaption].index,indexRow,word]])
                    threeDots = len(sentence["text"])
                    endOfSentence = True
                
            if combined[1][l] == 'newline':
                indexRow += 1

            if combined[1][l] == 'newcaption':
                indexCaption += 1
                indexRow = 0

            if not(combined[1][l] == 'speaker'):
                if combined[1][l] == 'newline':
                    if option == 1:
                        sentence["text"].append(combined[0][l])
                elif combined[1][l] == 'word':
                    if 3 in punctuation:
                        sentence["text"].append(self.getWordWithoutMultipoints(combined[0][l],3))
                    else:
                        sentence["text"].append(combined[0][l])
                else:
                    sentence["text"].append(combined[0][l])
                

            if (endOfSentence == True and unfinished == -1) or ((combined[1][l] == 'tag close' or combined[1][l] == 'bracket close') and self.isBracket(sentence["text"][0])):
                nextSentence = self.checkBuffers(bracketsBuffer,tagsBuffer,specialBuffer)
                if nextSentence == True:
                    sentence["end"] = [self.getIndexes()[indexCaption],indexRow]
                    result.append(sentence)
                    if not(threeDots == -1):
                        unfinished = len(result)-1
                    sentence = {
                        "start":[],
                        "end":[],
                        "text":[],
                        "speakers":[],
                        "enclosings":[],
                        "unfinished":[],
                    }
                    sentence["start"] = [self.getIndexes()[indexCaption],indexRow]
                    if not(l == len(combined[0])-1):
                        if combined[1][l+1] == 'newline':
                            sentence["start"][1] += 1
                        if combined[1][l+1] == 'newcaption':
                            sentence["start"][0] = self.getIndexes()[indexCaption+1]
                    if 1 in punctuation:
                        endOfSentence = False
                        word = 0

            if l+1 == len(combined[0]) and not(sentence["text"] == []):
                sentence["end"] = [self.getIndexes()[indexCaption],indexRow]
                result.append(sentence)

        return result

    # Is symbol a bracket, quote or tag
    def isBracket(self,symbol):
        if symbol in closing:
            return True
        if len(symbol) > 2:
            if symbol[:3] in tags:
                return True
        return False

    # Are there any brackets, tags or special enclosing symbols left.
    def checkBuffers(self,brackets,tags,specials):
        for b in brackets.values():
            if not(b == 0):
                return False
        for b in tags.values():
            if not(b == 0):
                return False
        for b in specials.values():
            if not(b == False):
                return False
        return True

    # Prepares sentences for machine translating.
    def prepeareDataForTranslation(self):
        result = []
        sentences = self.getWholeSentences()
        for sentence in sentences:
            sentence["text"] = self.getListOfSentences(sentence["text"],sentence["start"],sentence["end"],sentence["unfinished"])
            result.append(sentence)
        return result

    # Get sentnece parts in different subtitles. Used later for dividing text in subtitles.
    def getListOfSentences(self,text,start,end,multiDots):
        indexes = self.getSpecificIndexes(start[0],end[0])
        captions = [[],[]]
        temp = ['']
        index = 0
        word = 0
        unfinished = 0
        quotes = False
        for c in text:
            if c=='<hr/>':
                if len(temp[0])>0:
                    if temp[0][-1] == ' ':
                        temp[0] = temp[0][:-1]
                captions[0].append(temp[0])
                temp[0] = ''
                index += 1
            else:
                captions[1].append(c)
                if re.match(r'<.*?>',c) or c=='(' or c=='{' or c=='[' or (c=='"' and quotes == False):
                    temp[0] += c
                    if c=='"':
                        quotes = True
                elif c==')' or c=='}' or c==']' or (c=='"' and quotes == True):
                    temp[0] = temp[0][:-1]
                    temp[0] += c + ' '
                    if c=='"':
                        quotes = False
                else:
                    if not(c in specialClosingSymbols or re.match(r"-+",c) or c[-1] == ':'):
                        word += 1
                    if len(multiDots) > 0:
                        if word == multiDots[0][unfinished][2] and indexes[index] == multiDots[0][unfinished][0]:
                            if unfinished == 0:
                                if not(c[-3:] == '...'):
                                    temp[0] += c + '... '
                                else:
                                    temp[0] += c + ' '
                                if len(multiDots[0]) > 1:
                                    unfinished = 1
                                else:
                                    multiDots.pop(0)
                            else:
                                if multiDots[0][0][0] == multiDots[0][1][0]:
                                    temp[0] += c + ' '
                                else:
                                    temp[0] += '..' + c + ' '
                                unfinished = 0
                                multiDots.pop(0)
                        else:
                            temp[0] += c + ' '
                    else:
                        temp[0] += c + ' '
        if not(temp[0] == ''):
            if temp[0][-1] == ' ':
                temp[0] = temp[0][:-1]
            captions[0].append(temp[0])
        captions[1] = ' '.join(captions[1])
        return captions

    # Sends sentences to MT system
    def getTranslations(self):
        result = []
        temp = self.prepeareDataForTranslation()
        for t in temp:
            translation = []
            translation = Translator.Translator(t)
            result.append(translation)
        return result

    # Prepares translated text for subtitles.
    def getCaptionContentAfterTranslationSavingSentenceOrigins(self,mode,translations):
        result = {}
        indexes = self.getIndexes()
        for i in indexes:
            result[i] = ''

        for t in translations:
            captions = t["text"][0]
            text = t["text"][1]
            labels = t["speakers"]
            enclosings = t["enclosings"]
            index = indexes.index(t["start"][0])

            text = self.replaceTextInEnclosings(text,enclosings)

            if len(captions) == 1:
                if len(labels) > 0:
                    result[indexes[index]] += labels[0][0] + ' '
                result[indexes[index]] += self.fullSentence(captions[0],text,indexes[index]) + ' '
            else:
                partLengths = self.getCharacterCountsForCaptions(captions)
                proportion = len(text)/sum(partLengths)
                newCaptionCharacters = list(map(lambda x: x*proportion, partLengths))
                
                partTexts = self.getTextForCaptions(newCaptionCharacters,text,indexes)

                unfinished = False
                for p in range(len(partTexts)):
                    if not(captions[p] == ['']):
                        tempResult = ''
                        if unfinished:
                            tempResult = '..' + self.fullSentence(captions[p],partTexts[p][1],indexes[index]) + ' '
                        else:
                            tempResult = self.fullSentence(captions[p],partTexts[p][1],indexes[index]) + ' '
                        if len(labels) > 0:
                            for l in labels:
                                if l[1] == indexes[index]:
                                    tempResult = l[0] + ' ' + tempResult
                        i = self.getSpecificIndex(indexes[index])
                        unfinished = self.__captions[i].unfinishedSentence()
                        if unfinished:
                            tempResult = tempResult[:-1] + '... '
                        result[indexes[index]] += tempResult
                        index+=1

        for r in result.keys():
            result[r] = result[r][:-1]
            result[r] = self.wrapText(r,result[r])
            if mode == 'proportional':
                result[r] = self.getTextInRowsProportional(r,result[r])
            if mode == 'proper':
                result[r] = self.getTextInRowsProper(r,result[r])
            if mode == 'symbols':
                result[r] = self.getTextInRows37Symbols(r,result[r])
            if mode == 'rows':
                result[r] = self.getTextInRows2Rows(r,result[r])
        
        return result

    # Proportionaly divides text in rows for subtitle.
    def getTextInRowsProportional(self,i,text):
        caption = self.__captions[self.getSpecificIndex(i)]
        counts = self.getProportionalRowCount(caption,text)
        result = ''
        length = 0
        index = 0
        lst = text.replace(' ',' _').split('_')
        lst[-1] += ' '
        for elem in lst:
            length += len(re.sub(r'<.*>','',elem))
            if index < len(counts)-1:
                if length-1 > counts[index]:
                    before = length - len(re.sub(r'<.*>','',elem)) - 1
                    after = length - 1
                    if abs(before-counts[index]) >= abs(after-counts[index]):
                        result += elem[:-1] +'\n'
                        length = 0
                    else:
                        result = result[:-1] + '\n' + elem
                        length = len(re.sub(r'<.*>','',elem))
                    index += 1
                else:
                    result += elem
            else:
                result += elem
        if result[-1] == '\n' or result[-1] == ' ':
            result = result[:-1]
        return result

    # Proportionaly divides text in rows for subtitle taking 37 character limit for rows.
    def getTextInRowsProper(self,i,text):
        caption = self.__captions[self.getSpecificIndex(i)]
        counts = self.getProperRowCount(caption,text)
        result = ''
        length = 0
        index = 0
        lst = text.replace(' ',' _').split('_')
        lst[-1] += ' '
        for elem in lst:
            length += len(re.sub(r'<.*>','',elem))
            if index < len(counts)-1:
                if length-1 > counts[index]:
                    before = length - len(re.sub(r'<.*>','',elem)) - 1
                    after = length - 1
                    if abs(before-counts[index]) >= abs(after-counts[index]) and after<=37:
                        result += elem[:-1] +'\n'
                        length = 0
                    else:
                        result = result[:-1] + '\n' + elem
                        length = len(re.sub(r'<.*>','',elem))
                    index += 1
                else:
                    result += elem
            else:
                if length-1 > 37:
                    result = result[:-1] + '\n' + elem
                    length = len(re.sub(r'<.*>','',elem))
                else:
                    result += elem
        if result[-1] == '\n' or result[-1] == ' ':
            result = result[:-1]
        return result

    # Divides text in rows for subtitle taking 37 character limit for rows.
    def getTextInRows37Symbols(self,i,text):
        caption = self.__captions[self.getSpecificIndex(i)]
        result = ''
        length = 0
        index = 0
        lst = text.replace(' ',' _').split('_')
        lst[-1] += ' '
        for elem in lst:
            length += len(re.sub(r'<.*>','',elem))
            if length-1 > 37:
                result = result[:-1] + '\n' + elem
                length = len(re.sub(r'<.*>','',elem))
            else:
                result += elem
        if result[-1] == '\n' or result[-1] == ' ':
            result = result[:-1]
        return result

    # Divides text in rows equally and no more than 2 rows.
    def getTextInRows2Rows(self,i,text):
        caption = self.__captions[self.getSpecificIndex(i)]
        counts = self.getEqualRowCount(caption,text)
        result = ''
        length = 0
        index = 0
        lst = text.replace(' ',' _').split('_')
        lst[-1] += ' '
        for elem in lst:
            length += len(re.sub(r'<.*>','',elem))
            if index < len(counts)-1:
                if length-1 > counts[index]:
                    before = length - len(re.sub(r'<.*>','',elem)) - 1
                    after = length - 1
                    if abs(before-counts[index]) >= abs(after-counts[index]):
                        result += elem[:-1] +'\n'
                        length = 0
                    else:
                        result = result[:-1] + '\n' + elem
                        length = len(re.sub(r'<.*>','',elem))
                    index += 1
                else:
                    result += elem
            else:
                result += elem
        if result[-1] == '\n' or result[-1] == ' ':
            result = result[:-1]
        return result

    # Gets portencial text length in rows with equal character count per row. 
    def getEqualRowCount(self,caption,text):
        textLength = len(re.sub(r'<.*?>','',text).replace('\n',''))
        rowCount = 0
        if caption.divided == True:
            rowCount = 1
        else:
            if caption.getRowCount() > 2 or textLength > 37:
                rowCount = 2
            else:
                rowCount = caption.getRowCount()
        result = []
        for i in range(rowCount):
            result.append(math.ceil(textLength/rowCount))
        return result

    # Gets portencial text length in rows with proportional character count per row. 
    def getProportionalRowCount(self,caption,text):
        originalCharacterCount = caption.getCharacterCountInRows()
        proportion = len(text)/sum(originalCharacterCount)
        rowCharacterCount = list(map(lambda x: x*proportion, originalCharacterCount))
        return rowCharacterCount

    # Gets portencial text length in rows with proportional character count per row and without exceeding 37 symbols per row. 
    def getProperRowCount(self,caption,text):
        originalCharacterCount = caption.getCharacterCountInRows()
        proportion = len(text)/sum(originalCharacterCount)
        rowCharacterCount = list(map(lambda x: x*proportion, originalCharacterCount))
        
        for i in range(len(rowCharacterCount)):
            if rowCharacterCount[i] > 37:
                extra = rowCharacterCount[i]-37
                for b in reversed(range(i)):
                    if rowCharacterCount[b]<37:
                        canAdd = 37-rowCharacterCount[b]
                        if canAdd>=extra:
                            rowCharacterCount[b]+=extra
                            rowCharacterCount[i]-=extra
                            extra = 0
                        else:
                            rowCharacterCount[b]+=canAdd
                            rowCharacterCount[i]-=canAdd
                            extra -= canAdd
                    if extra == 0:
                        break
                if extra > 0:
                    for b in range(i+1,len(rowCharacterCount)):
                        if rowCharacterCount[b]<37:
                            canAdd = 37-rowCharacterCount[b]
                            if canAdd>=extra:
                                rowCharacterCount[b]+=extra
                                rowCharacterCount[i]-=extra
                                extra = 0
                            else:
                                rowCharacterCount[b]+=canAdd
                                rowCharacterCount[i]-=canAdd
                                extra -= canAdd
                        if extra == 0:
                            break
                if extra > 0:
                    while extra > 0:
                        if extra > 37:
                            rowCharacterCount.append(37)
                            rowCharacterCount[i]-=37
                            extra -= 37
                        else:
                            rowCharacterCount.append(extra)
                            rowCharacterCount[i]-=extra
                            extra = 0
        return rowCharacterCount

    # Puts whole enclosings in translated text.
    def wrapText(self,index,text):
        index = self.getSpecificIndex(index)
        caption = self.__captions[index]

        enclosings = caption.getWholeEnclosingContent()
        begin = ''
        end = ''
        lastTag = True
        for e in enclosings[0]:
            if lastTag:
                begin += e
            else:
                begin += ' ' + e
            if re.match(r'<.*?>',e):
                lastTag = True
            else:
                lastTag = False
        for e in enclosings[1]:
            if re.match(r'<.*?>',e):
                lastTag = True
            else:
                lastTag = False
            if lastTag:
                end += e
            else:
                end += e
        return begin + text + end

    # Replace all text in enclosings (brackets and double quotes)
    def replaceTextInEnclosings(self,text,enclosings):
        result = text
        brackets = re.findall(r'\([^\(\{\[]*\)|\[[^\(\{\[]*\]|\{[^\(\{\[]*\}|\"[^\(\{\[]*\"',result) # Gets all bracket text
        for b in range(len(brackets)):
            result = result.replace(brackets[b], enclosings[b], 1)
        return result

    # Get character count for each original caption
    def getCharacterCountsForCaptions(self,captions):
        result = []
        for c in captions:
            if type(c)==list:
                result.append(sum(list(map(lambda x: len(x), c))))
            else:
                result.append(len(c))
        return result

    # Gets text for each caption
    def getTextForCaptions(self,counts,text,indexes):
        index = 0
        temp = ''
        length = 0
        result = []
        over = False
        for elem in text.replace(' ',' _').split('_'):
            if not(index == len(counts)):
                length += len(re.sub(r'<.*>','',elem))
                if length > counts[index]:
                    before = length - len(re.sub(r'<.*>','',elem))
                    after = length
                    if (abs(before-counts[index]) > abs(after-counts[index])):
                        temp += elem.replace(' ','')
                        result.append([indexes[index],temp])
                        temp = ''
                        length = 0
                    else:
                        temp = temp[:-1]
                        result.append([indexes[index],temp])
                        temp = elem
                        length = len(re.sub(r'<.*>','',elem))
                    index += 1
                else:
                    temp += elem
            else:
                if over==False:
                    result[-1][1] += ' '
                    over = True
                result[-1][1] += elem
        if not(temp == ''):
            if index == len(counts):
                result[-1][1] += ' ' + temp
            else:
                result.append([indexes[index],temp])
        return result
    
    # Gets text divided for subtitles
    def fullSentence(self,parts,text,index):
        if len(parts) == 1:
            return text

        originalCaptionCharacters = list(map(lambda x: len(x), parts))

        textLength = len(re.sub(r'<.*>','',text))

        originalLength = sum(originalCaptionCharacters)

        proportion = textLength/originalLength

        newCaptionCharacters = list(map(lambda x: x*proportion, originalCaptionCharacters))

        result = ''
        length = 0
        index = 0
        for elem in text.replace(' ',' _').split('_'):
            length += len(elem)
            if index+1 < len(newCaptionCharacters):
                if length > newCaptionCharacters[index]:
                    before = length - len(re.sub(r'<.*>','',elem))
                    after = length
                    if (abs(before-newCaptionCharacters[index]) >= abs(after-newCaptionCharacters[index])):
                        if elem[-2] == ',':
                            result += elem[:-2] + '... '
                        else:
                            result += elem.replace(' ','') + '... '
                        length = 0
                    else:
                        if result[-2] == ',':
                            result = result[:-2] + '... ' + elem
                        else:
                            result = result[:-1] + '... ' + elem
                        length = len(re.sub(r'<.*>','',elem))
                    index += 1
                else:
                    result += elem
            else:
                result += elem
        return result

    # Gets punctuation types for text
    def __getPunctuation(self,text: str):
        result = []
        # Sentnece ends with . ! ?
        if text[-1] == '!' or text[-1] == '?' or (text[-1] == '.' and not(text[-3:] == '...')):
            result.append(1)
        # Sentnece ends with ...
        if text[-3:] == '...':
            result.append(2)
        # Sentnece resumes with .. ...
        if text[0:3] == '...' or text[0:2] == '..':
            result.append(3)
        # Sentnece has , ;
        if text[-1] == ',' or text[-1] == ';':
            result.append(4)
        return result 

    # option = 1 - only end.
    # option = 2 - end and start
    # option = 3 - only start.
    def getWordWithoutMultipoints(self,text: str, option = 1):
        result = text
        if  len(text) > 2:
            if text[-3:] == '...' and option < 3:
                result = text[:-3]
            if len(result) > 2:
                if result[0:3] == '...' and option > 1:
                    result = result[3:]
                elif result[0:2] == '..' and option > 1:
                    result = result[2:]
        return result

    # Gets row indexes for captions
    def getRowIndexes(self):
        rows = []
        combined = []
        result = ''
        for i in self.__captions:
            rows.append(i.getRowIndexes())
        for i in rows:
            if combined == []:
                combined.append(i)
            else:
                if i[0]-combined[-1][-1] == 1:
                    if len(combined[-1]) == 1:
                        combined[-1].append(combined[-1][-1])
                    combined[-1][-1] = i[-1]
                else:
                    combined.append(i)
        for i in combined:
            if result == '':
                result += str(i[0]) + '-' + str(i[-1])
            else:
                result += ';' + str(i[0]) + '-' + str(i[-1])
        return result

    # Combines captiopn content. Used for MT translation evaluation.
    def getSentencesForTranslationEvaluation(self):
        sentencesWithEnclosings = []
        sentencesWithoutEnclosings = []
        startEnd = self.getRowIndexes()
        capsWithEnclosings = []
        capsWithoutEnclosings = []
        for c in self.__captions:
            textWithEnclosings = c.getOriginal().replace('\n',' ')
            textWithoutEnclosings = c.getOriginalWithoutEnclosings().replace('\n',' ')
            
            tempWithout = re.sub(r'<.*?>','',textWithoutEnclosings).split()
            if tempWithout[0] == '–' or tempWithout[0][-1] == ':':
                textWithoutEnclosings = ' '.join(tempWithout[1:])
            else:
                textWithoutEnclosings = ' '.join(tempWithout)

            capsWithEnclosings.append(textWithEnclosings)
            capsWithoutEnclosings.append(textWithoutEnclosings)

        sentencesWithEnclosings.append([startEnd,' '.join(capsWithEnclosings)])
        sentencesWithoutEnclosings.append([startEnd,' '.join(capsWithoutEnclosings)])

        return (sentencesWithEnclosings,sentencesWithoutEnclosings)
