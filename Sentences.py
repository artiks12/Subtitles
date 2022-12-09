from Caption import Caption
from Caption import specialClosingSymbols
from Caption import closing
from Caption import tags
import re
import Translator

class Sentences():
    def __init__(self, subtitle: Caption, label = None, multiple = False) -> None:
        self.__captions: list = [subtitle]
        self.multipleSpeakers = multiple
        self.label = label
        self.unfinished = False

    # Add caption that continues previous caption
    def addCaption(self,caption: Caption):
        self.__captions.append(caption)

    # Gets the last added caption
    def getLastCaption(self):
        return self.__captions[-1]

    # Checks if the last sentence can be continued
    def canAdd(self):
        return self.__captions[-1].toContSentence()

    # Checks if the last sentence is an unfinished sentence
    def canFinish(self):
        return self.__captions[-1].unfinishedSentence()

    # Gets caption indexes
    def getIndexes(self):
        result = []
        for i in self.__captions:
            result.append(i.index)
        return result

<<<<<<< Updated upstream
=======
    def getSpecificIndexes(self,start,end):
        startIndex = self.getIndexes().index(start)
        endIndex = self.getIndexes().index(end)
        return self.getIndexes()[startIndex:endIndex+1]

    def getSpecificIndex(self,index):
        return self.getIndexes().index(index)


>>>>>>> Stashed changes
    def areBuffersEmpty(self,bracketsBuffer,tagsBuffer):
        for b in bracketsBuffer.values():
            if b > 0:
                return False

        for b in tagsBuffer.values():
            if b > 0:
                return False

        return True

    # Get combination of all captions within
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

<<<<<<< Updated upstream

    def getWholeSentences(self):
        result = []
        bracketsBuffer = {
            "(" : 0,
            "{" : 0,
            "[" : 0
        }
        tagsBuffer={
            '<fo': 0,
            '<b>': 0,
            '<i>': 0,
            '<u>': 0,
        }
        specialBuffer={
            '"': False,
            '#': False,
            '♪': False
        }
        temp = [[],[],[],[],[]]
        enclosing = {
            "(" : [],
            "{" : [],
            "[" : [],
            "#" : [],
            '"' : [],
            "♪" : []
        }
        lst = self.combine()
        endOfSentence = False
        threeDots = ''
        indexCaption = 0
        indexRow = 0
        for l in range(len(lst[0])):
            if l == 0:
                temp[0] = [self.getIndexes()[indexCaption],indexRow]
            # Opening bracket/tag
            if lst[1][l] == 'bracket open':
                bracketsBuffer[lst[0][l]] += 1
                for e in enclosing:
                    if e=='(' or e=='{' or e=='[':
                        for sub in enclosing[e]:
                            sub.append(lst[0][l])
                    else:
                        if specialBuffer[e] == True:
                            enclosing[e].append(lst[0][l])
                enclosing[lst[0][l][0]].append([lst[0][l]])
            if lst[1][l] == 'tag open':
                tagsBuffer[lst[0][l][:3]] += 1

            # Closing bracket/tag
            if lst[1][l] == 'bracket close':
                key = list(closing.keys())[list(closing.values()).index(lst[0][l][0])]
                bracketsBuffer[key] -= 1
                bracket = []
                for e in enclosing[key][-1]:
                    bracket.append(e)
                bracket.append(lst[0][l])
                temp[4].append(bracket)
                enclosing[key].pop()
                for e in enclosing:
                    if e=='(' or e=='{' or e=='[':
                        for sub in enclosing[e]:
                            sub.append(lst[0][l])
                    else:
                        if specialBuffer[e] == True:
                            enclosing[e].append(lst[0][l])
            if lst[1][l] == 'tag close':
                key = list(tags.keys())[list(tags.values()).index(lst[0][l])][:3]
                tagsBuffer[key] -= 1

            # Special enclosing symbol
            if lst[1][l] == 'special':
                if specialBuffer[lst[0][l]] == False:
                    enclosing[lst[0][l]].append(lst[0][l])
                    specialBuffer[lst[0][l]] = True
                else:
                    special = []
                    for e in enclosing[lst[0][l]]:
                        special.append(e)
                    special.append(lst[0][l])
                    temp[4].append(special)
                    enclosing[lst[0][l]] = []
                    specialBuffer[lst[0][l]] = False
                for e in enclosing:
                    if e=='(' or e=='{' or e=='[':
                        for sub in enclosing[e]:
                            sub.append(lst[0][l])
                    else:
                        if specialBuffer[e] == True and not(e==lst[0][l]) :
                            enclosing[e].append(lst[0][l])

            if lst[1][l] == 'label' or lst[1][l] == 'dash':
                temp[3].append(lst[0][l])

            if lst[1][l] == 'word':
                for e in enclosing:
                    if e=='(' or e=='{' or e=='[':
                        for sub in enclosing[e]:
                            sub.append(lst[0][l])
                    else:
                        if specialBuffer[e] == True:
                            enclosing[e].append(lst[0][l])
                
                punctuation = self.__getPunctuation(lst[0][l])
                if 1 in punctuation:
                    endOfSentence = True
                if 2 in punctuation:
                    threeDots = '<img src="T"/>'
                if 3 in punctuation:
                    threeDots = '<img src="F"/>'
                if 2 in punctuation and 3 in punctuation:
                    threeDots = '<img src="B"/>'

            if lst[1][l] == 'newline':
                indexRow += 1
                for e in enclosing:
                    if e=='(' or e=='{' or e=='[':
                        for sub in enclosing[e]:
                            sub.append(lst[0][l])
                    else:
                        if specialBuffer[e] == True:
                            enclosing[e].append(lst[0][l])

            if lst[1][l] == 'newcaption':
                indexCaption += 1
                indexRow = 0
                for e in enclosing:
                    if e=='(' or e=='{' or e=='[':
                        for sub in enclosing[e]:
                            sub.append(lst[0][l])
                    else:
                        if specialBuffer[e] == True:
                            enclosing[e].append(lst[0][l])

            if threeDots == '<img src="F"/>' or threeDots == '<img src="B"/>':
                temp[2].append('<img src="F"/>')
            temp[2].append(self.getWordWithoutMultipoints(lst[0][l]))
            if threeDots == '<img src="T"/>' or threeDots == '<img src="B"/>':
                temp[2].append('<img src="T"/>')
            threeDots = ''
                

            if endOfSentence == True:
                nextSentence = True
                for b in bracketsBuffer.values():
                    if not(b == 0):
                        nextSentence = False
                        break
                for b in tagsBuffer.values():
                    if not(b == 0):
                        nextSentence = False
                        break
                for b in specialBuffer.values():
                    if not(b == False):
                        nextSentence = False
                        break
                if nextSentence == True:
                    temp[1] = [self.getIndexes()[indexCaption],indexRow]
                    result.append(temp)
                    temp = [[],[],[],[],[]]
                    temp[0] = [self.getIndexes()[indexCaption],indexRow]
                    endOfSentence = False

            if l+1 == len(lst[0]) and not(temp[2] == []):
                temp[1] = [self.getIndexes()[indexCaption],indexRow]
                result.append(temp)

=======
    # option = 1 - with tags <br/> <hr/>
    # option = 2 - without tags <br/> <hr/>
    def getWholeSentences(self,option = 2):
        result = []
        bracketsBuffer = {
            "(" : 0,
            "{" : 0,
            "[" : 0
        }
        tagsBuffer={
            '<fo': 0,
            '<b>': 0,
            '<i>': 0,
            '<u>': 0,
        }
        specialBuffer={
            '"': False,
            '#': False,
            '♪': False
        }
        temp = [[],[],[],[],[],[]]
        enclosing = {
            "(" : [],
            "{" : [],
            "[" : [],
            "#" : [],
            '"' : [],
            "♪" : []
        }
        lst = self.combine()
        endOfSentence = False
        threeDots = -1
        unfinished = -1
        indexCaption = 0
        indexRow = 0
        punctuation = []
        word = 0
        temp[0] = [self.getIndexes()[indexCaption],indexRow]
        for l in range(len(lst[0])):
            # Put next element in all enclosings
            for e in enclosing:
                if e=='(' or e=='{' or e=='[':
                    for sub in enclosing[e]:
                        sub.append(lst[0][l])
                else:
                    if specialBuffer[e] == True:
                        if lst[1][l] == 'special' and not(e==lst[0][l]):
                            enclosing[e].append(lst[0][l])
                        elif lst[1][l] == 'newcaption' or lst[1][l] == 'newline':
                            if option == 1:
                                enclosing[e].append(lst[0][l])
                    
            
            # Opening bracket
            if lst[1][l] == 'bracket open':
                bracketsBuffer[lst[0][l]] += 1
                enclosing[lst[0][l][0]].append([lst[0][l]])
            
            # Opening tag
            if lst[1][l] == 'tag open':
                tagsBuffer[lst[0][l][:3]] += 1

            # Closing bracket
            if lst[1][l] == 'bracket close':
                key = list(closing.keys())[list(closing.values()).index(lst[0][l][0])] # get key
                bracketsBuffer[key] -= 1
                bracket = []
                for e in enclosing[key][-1]:
                    bracket.append(e)
                temp[4].append(bracket)
                enclosing[key].pop()
            
            # Closing tag
            if lst[1][l] == 'tag close':
                key = list(tags.keys())[list(tags.values()).index(lst[0][l])][:3] # get key
                tagsBuffer[key] -= 1

            # Special enclosing symbol
            if lst[1][l] == 'special':
                if specialBuffer[lst[0][l]] == False:
                    enclosing[lst[0][l]].append(lst[0][l])
                    specialBuffer[lst[0][l]] = True
                else:
                    special = []
                    for e in enclosing[lst[0][l]]:
                        special.append(e)
                    temp[4].append(special)
                    enclosing[lst[0][l]] = []
                    specialBuffer[lst[0][l]] = False

            if lst[1][l] == 'label' or lst[1][l] == 'dash':
                temp[3].append([lst[0][l],self.__captions[indexCaption].index])  

            if lst[1][l] == 'word':
                punctuation = self.__getPunctuation(lst[0][l])
                if endOfSentence == True and self.checkBuffers(bracketsBuffer,tagsBuffer,specialBuffer):
                    if lst[0][l].islower() or 3 in punctuation:
                        last = result[unfinished]
                        last[1] = []
                        last[2].extend(temp[2])
                        last[3].extend(temp[3])
                        last[4].extend(temp[4])
                        last[5].extend(temp[5])
                        if lst[0][l].islower() and not(3 in punctuation):
                            last[5][-1].append([self.__captions[indexCaption].index,indexRow,word+1])
                        temp = last
                        temp[2][threeDots] = self.getWordWithoutMultipoints(temp[2][threeDots])
                        result.pop()
                    else:
                        word = 0
                    unfinished = -1
                    endOfSentence = False

                word += 1
                
                if 1 in punctuation:
                    endOfSentence = True
                if 3 in punctuation:
                    temp[5][-1].append([self.__captions[indexCaption].index,indexRow,word])
                    threeDots = -1
                if 2 in punctuation:
                    temp[5].append([[self.__captions[indexCaption].index,indexRow,word]])
                    threeDots = len(temp[2])
                    endOfSentence = True
                
                

            if lst[1][l] == 'newline':
                indexRow += 1

            if lst[1][l] == 'newcaption':
                indexCaption += 1
                indexRow = 0

            if not(lst[1][l] == 'label' or lst[1][l] == 'dash'):
                if lst[1][l] == 'newline':
                    if option == 1:
                        temp[2].append(lst[0][l])
                elif lst[1][l] == 'word':
                    if 3 in punctuation:
                        temp[2].append(self.getWordWithoutMultipoints(lst[0][l],3))
                    else:
                        temp[2].append(lst[0][l])
                else:
                    temp[2].append(lst[0][l])
                

            if (endOfSentence == True and unfinished == -1) or ((lst[1][l] == 'tag close' or lst[1][l] == 'bracket close') and self.isBracket(temp[2][0])):
                nextSentence = self.checkBuffers(bracketsBuffer,tagsBuffer,specialBuffer)
                if nextSentence == True:
                    temp[1] = [self.getIndexes()[indexCaption],indexRow]
                    result.append(temp)
                    if not(threeDots == -1):
                        unfinished = len(result)-1
                    temp = [[],[],[],[],[],[]]
                    temp[0] = [self.getIndexes()[indexCaption],indexRow]
                    if not(l == len(lst[0])-1):
                        if lst[1][l+1] == 'newline':
                            temp[0][1] += 1
                        if lst[1][l+1] == 'newcaption':
                            temp[0][0] = self.getIndexes()[indexCaption+1]
                    if 1 in punctuation:
                        endOfSentence = False
                        word = 0

            if l+1 == len(lst[0]) and not(temp[2] == []):
                temp[1] = [self.getIndexes()[indexCaption],indexRow]
                result.append(temp)

        return result

    def isBracket(self,symbol):
        if symbol in closing:
            return True
        if len(symbol) > 2:
            if symbol[:3] in tags:
                return True
        return False

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

    def prepeareDataForTranslation(self):
        result = []
        temp = self.getWholeSentences()
        sentence = [[],[],[],[],[],[]]
        for t in temp:
            sentence[0] = t[0]
            sentence[1] = t[1]
            sentence[2] = self.getListOfSentences(t[2],t[0],t[1],t[5])
            sentence[3] = t[3]
            sentence[4] = t[4]
            sentence[5] = t[5]
            result.append(sentence)
            sentence = [[],[],[],[],[],[]]
        return result

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

    def getTranslations(self):
        result = []
        temp = self.prepeareDataForTranslation()
        for t in temp:
            translation = []
            translation = Translator.Translator(t)
            result.append(translation)
        return result

    def getCaptionContentAfterTranslationUsingTags(self):
        temp = self.getTranslations()
        indexes = self.getIndexes()
        indexCurrent = 0
        result = []
        enclosings = self.__captions[indexCurrent].getWholeEnclosingContent()
        caption = [indexes[indexCurrent],'']
        if not(len(enclosings[0]) == 0):
            caption[1] += ''.join(enclosings[0])

        for t in temp:
            fixed = t[2].replace('<img src="T"/>','...').replace('<img src="F"/> ','..').replace('<br/>.','.<br/>').replace('<br/>,',',<br/>')

            brackets = re.findall(r'\([^\(\{\[]*\)|\[[^\(\{\[]*\]|\{[^\(\{\[]*\}',fixed) # Gets all bracket text
            for b in range(len(brackets)):
                fixed = fixed.replace(brackets[b],t[4][b], 1)
            
            text = fixed.split('<hr/>')

            if len(text) > 1:
                for c in range(len(text)):
                    caption[1] += text[c]
                    if not(c+1 == len(text)): 
                        if not(len(enclosings[1]) == 0):
                            caption[1] += ''.join(enclosings[1])
                        result.append(caption)
                        indexCurrent+=1
                        caption = [indexes[indexCurrent],'']
                        enclosings = self.__captions[indexCurrent].getWholeEnclosingContent()
                        if not(len(enclosings[0]) == 0):
                            caption[1] += ''.join(enclosings[0])
            else:
                caption[1] += text[0]
        if not(caption == [[],[]]):
            if not(len(enclosings[1]) == 0):
                caption[1] += ''.join(enclosings[1])
            result.append(caption)
        return result

    def getCaptionContentAfterTranslationSavingSentenceOrigins(self):
        temp = self.getTranslations()
        result = []
        indexes = self.getIndexes()
        for i in indexes:
            cap = [i,'']
            result.append(cap)

        index = 0
        for t in temp:
            if not(indexes[index] == t[0][0]):
                index += 1 
            captions = t[2][0]
            text = t[2][1]
            labels = t[3]
            enclosings = t[4]
            counts = []
            count = 0

            text = self.replaceTextInEnclosings(text,enclosings)

            if len(captions) == 1:
                if len(labels) > 0:
                    result[index][1] += labels[0][0] + ' '
                result[index][1] += self.fullSentence(captions[0],text,result[index][0]) + ' '
            else:
                partLengths = self.getCharacterCountsForCaptions(captions)
                proportion = len(text)/sum(partLengths)
                newCaptionCharacters = list(map(lambda x: x*proportion, partLengths))
                
                partTexts = self.getCharactersForCaptions(newCaptionCharacters,text,indexes)

                unfinished = False
                for p in range(len(partTexts)):
                    if unfinished:
                        result[p][1] = '..' + self.fullSentence(captions[p],partTexts[p][1],result[p][0]) + ' '
                    else:
                        result[p][1] = self.fullSentence(captions[p],partTexts[p][1],result[p][0]) + ' '
                    if len(labels) > 0:
                        for l in labels:
                            if l[1] == result[p][0]:
                                result[p][1] = l[0] + ' ' + result[p][1]
                    i = self.getSpecificIndex(result[p][0])
                    unfinished = self.__captions[i].unfinishedSentence()
                    if unfinished:
                        result[p][1] = result[p][1][:-1] + '... '

        for r in result:
            r[1] = r[1][:-1]
            r[1] = self.wrapText(r)
            # TODO split into rows
            r[1] = self.getTextInRows(r)

        return result

    def getTextInRows(self,pair):
        caption = self.__captions[self.getSpecificIndex(pair[0])]
        counts = self.getProperRowCount(caption,pair[1])
        result = ''
        length = 0
        index = 0
        for elem in pair[1].replace(' ',' _').split('_'):
            length += len(re.sub(r'<.*>','',elem))
            if not(index == len(counts)):
                if length > counts[index]:
                    before = length - len(re.sub(r'<.*>','',elem)) - 1
                    after = length - 1
                    if abs(before-counts[index]) >= abs(after-counts[index]) and after<=37:
                        result += elem.replace(' ','') +'\n'
                        length = 0
                    else:
                        result = result[:-1] + '\n' + elem
                        length = len(re.sub(r'<.*>','',elem))
                    index += 1
                else:
                    result += elem
            else:
                if length > 37:
                    result = result[:-1] + '\n' + elem
                    length = len(re.sub(r'<.*>','',elem))
                else:
                    result += elem
        if result[-1:] == '\n' or result[-1:] == ' ':
            result = result[:-1]
        return result


        

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

    def wrapText(self,pair):
        index = self.getSpecificIndex(pair[0])
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
        return begin + pair[1] + end

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

    def getCharactersForCaptions(self,counts,text,indexes):
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
>>>>>>> Stashed changes
        return result
    
    def fullSentence(self,parts,text,index):
        if len(parts) == 1:
            return text

        originalCaptionCharacters = list(map(lambda x: len(x), parts))

        textLength = len(re.sub(r'<.*>','',text))

<<<<<<< Updated upstream
    def prepeareDataForTranslation(self):
        result = []
        temp = self.getWholeSentences()
        sentence = [[],[],[],[],[]]
        for t in temp:
            sentence[0] = t[0]
            sentence[1] = t[1]
            sentence[2] = ' '.join(t[2])
            sentence[3] = t[3]
            sentence[4] = t[4]
            result.append(sentence)
            sentence = [[],[],[],[],[]]
        return result

    def getTranslations(self):
        result = []
        temp = self.prepeareDataForTranslation()
        for t in temp:
            translation = []
            translation = Translator.Translator(t)
            result.append(translation)
        return result

    def getCaptionContentAfterTranslationUsingTags(self):
        temp = self.getTranslations()
        indexes = self.getIndexes()
        indexCurrent = 0
        result = []
        enclosings = self.__captions[indexCurrent].getWholeEnclosingContent()
        caption = [indexes[indexCurrent],'']
        if not(len(enclosings[0]) == 0):
            caption[1] += ''.join(enclosings[0])

        for t in temp:
            fixed = t[2].replace('<img src="T"/>','...').replace('<img src="F"/> ','..').replace('<br/>.','.<br/>').replace('<br/>,',',<br/>')

            brackets = re.findall(r'\([^\(\{\[]*\)|\[[^\(\{\[]*\]|\{[^\(\{\[]*\}',fixed) # Gets all bracket text
            for b in range(len(brackets)):
                fixed = fixed.replace(brackets[b],t[4][b], 1)
            
            
            text = fixed.split('<hr/>')

            

            if len(text) > 1:
                for c in range(len(text)):
                    caption[1] += text[c]
                    if not(c+1 == len(text)): 
                        if not(len(enclosings[1]) == 0):
                            caption[1] += ''.join(enclosings[1])
                        result.append(caption)
                        indexCurrent+=1
                        caption = [indexes[indexCurrent],'']
                        enclosings = self.__captions[indexCurrent].getWholeEnclosingContent()
                        if not(len(enclosings[0]) == 0):
                            caption[1] += ''.join(enclosings[0])
            else:
                caption[1] += text[0]
        if not(caption == [[],[]]):
            if not(len(enclosings[1]) == 0):
                caption[1] += ''.join(enclosings[1])
            result.append(caption)
        return result

    def getCaptionContentAfterTranslationUsingWordCount(self):
        temp = self.getTranslations()
        indexes = self.getIndexes()
        indexCurrent = 0
        result = []
        enclosings = self.__captions[indexCurrent].getWholeEnclosingContent()
        caption = [indexes[indexCurrent],'']
        if not(len(enclosings[0]) == 0):
            caption[1] += ''.join(enclosings[0])

        for t in temp:
            threeDots = re.findall(r'<img src="[T|F]"/>',t[2])
            noTags = t[2].replace('<br/>','').replace('<hr/>','')

            brackets = re.findall(r'\([^\(\{\[]*\)|\[[^\(\{\[]*\]|\{[^\(\{\[]*\}',fixed) # Gets all bracket text
            for b in range(len(brackets)):
                fixed = fixed.replace(brackets[b],t[4][b], 1)
            
            
            text = fixed.split('<hr/>')



            

            if len(text) > 1:
                for c in range(len(text)):
                    caption[1] += text[c]
                    if not(c+1 == len(text)): 
                        if not(len(enclosings[1]) == 0):
                            caption[1] += ''.join(enclosings[1])
                        result.append(caption)
                        indexCurrent+=1
                        caption = [indexes[indexCurrent],'']
                        enclosings = self.__captions[indexCurrent].getWholeEnclosingContent()
                        if not(len(enclosings[0]) == 0):
                            caption[1] += ''.join(enclosings[0])
            else:
                caption[1] += text[0]
        if not(caption == [[],[]]):
            if not(len(enclosings[1]) == 0):
                caption[1] += ''.join(enclosings[1])
            result.append(caption)
        return result
            



            


=======
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
>>>>>>> Stashed changes

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

<<<<<<< Updated upstream
    def getWordWithoutMultipoints(self,text: str):
        result = text
        if  len(text) > 2:
            if text[-3:] == '...':
                result = text[:-3]
            if len(result) > 2:
                if result[0:3] == '...':
                    result = result[3:]
                elif result[0:2] == '..':
=======
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
>>>>>>> Stashed changes
                    result = result[2:]
        return result




