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

        return result

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

    def getWordWithoutMultipoints(self,text: str):
        result = text
        if  len(text) > 2:
            if text[-3:] == '...':
                result = text[:-3]
            if len(result) > 2:
                if result[0:3] == '...':
                    result = result[3:]
                elif result[0:2] == '..':
                    result = result[2:]
        return result




