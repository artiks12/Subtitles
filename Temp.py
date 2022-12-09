<<<<<<< Updated upstream
# Get combination of all captions within
def getWholeSentences(self):
    result = []
    combined = self.combine()
    temp = [[],[],[],[],[],[],[],[]]

    sentenceFinished = False
    unfinished = -1

    brackets = []
    tags = []
    start = 0
    for i in range(len(combined[0])):
        if sentenceFinished == True:
            newSentence = False
            if not(combined[1][i] == '') and len(brackets) == 0:
                newSentence = True
            
            elif not(combined[2][i] == ''):
                if combined[7][i] == 'bracket open' and len(brackets) == 0:
                    newSentence = True

            elif combined[6][i] == '':
                newSentence = True
            
            if newSentence == True:
                for m in range(8):
                    temp[m] = combined[m][start:i]
                result.append(temp)
                temp = [[],[],[],[],[],[],[],[]]
                start = i
                sentenceFinished = False


        # Words
        if not(combined[1][i] == ''): 
            if 1 in self.__getPunctuation(combined[1][i]):
                if len(brackets) == 0:
                    sentenceFinished = True
            if 3 in self.__getPunctuation(combined[1][i]):
                if not(combined[1][unfinished] == ''):
                    combined[1][unfinished] = self.getWordWithoutPunctuation(combined[1][unfinished])
                else:
                    combined[2][unfinished] = self.getWordWithoutPunctuation(combined[2][unfinished])
                combined[1][i] = self.getWordWithoutPunctuation(combined[1][i])
            if 2 in self.__getPunctuation(combined[1][i]):
                unfinished = i

        # Brackets
        elif not(combined[2][i] == ''):
            if combined[7][i] == 'bracket open':
                brackets.append(i)
            else:
                brackets.remove(brackets[-1])
            if 1 in self.__getPunctuation(combined[2][i]):
                if len(brackets) == 0:
                    sentenceFinished = True
            if 3 in self.__getPunctuation(combined[2][i]):
                if not(combined[1][unfinished] == ''):
                    combined[1][unfinished] = self.getWordWithoutPunctuation(combined[1][unfinished])
                else:
                    combined[2][unfinished] = self.getWordWithoutPunctuation(combined[2][unfinished])
                combined[2][i] = self.getWordWithoutPunctuation(combined[2][i])
            if 2 in self.__getPunctuation(combined[2][i]):
                unfinished = i
        
        if i == len(combined[0])-1:
            for m in range(8):
                temp[m] = combined[m][start:]
            result.append(temp)
        
    return result


def prepareDataForTranslation(self):
    result = []
    sentences = self.getWholeSentences()
    captionIndex = 0
    row = 0
    newLine = False
    newCaption = False
    for sentence in sentences:
        temp = []
        sent = []
        label = []
        brackets = []
        bracket = []
        bracketOn = False
        newSentence = True
        for i in range(len(sentence[0])):
            
            if newLine:
                row += 1
                newLine = False
            if newCaption:
                row = 0
                captionIndex+=1
                newCaption = False
            
            if newSentence:
                newSentence = False
                start = [self.getIndexes()[captionIndex]]
                start.append(row)

            if not(sentence[1][i] == ''):
                sent.append(sentence[1][i])
                if bracketOn == True:
                    bracket.append(sentence[1][i])
            elif not(sentence[2][i] == ''):
                sent.append(sentence[2][i])
                bracket.append(sentence[2][i])
                if sentence[7][i] == 'bracket open':
                    bracketOn = True
                else:
                    bracketOn = False
                    brackets.append(bracket)
                    bracket = []
                
            elif not(sentence[3][i] == ''):
                sent.append(sentence[3][i])
                bracket.append(sentence[3][i])
                if bracketOn == False:
                    bracketOn = True
                else:
                    bracketOn = False
                    brackets.append(bracket)
                    bracket = []
            
            elif not(sentence[6][i] == ''):
                if sentence[7][i] == 'newline':
                    newLine = True
                else:
                    newCaption = True
            
            elif not(sentence[4][i] == ''):
                if sentence[7][i] == 'label':
                    label.append(sentence[4][i])
        end = [self.getIndexes()[captionIndex]]
        end.append(row)
        temp.append(start)
        temp.append(end)
        temp.append(' '.join(sent))
        temp.append(label)
        temp.append(brackets)
        result.append(temp)
    return result

def getTranslation(self):
    temp = self.prepareDataForTranslation()
    return Translator.Translator(temp)

def __getPunctuation(self,text: str):
    result = []
    if text[-1] == '!' or text[-1] == '?' or (text[-1] == '.' and not(text[-3:] == '...')):
        result.append(1)
    if text[-3:] == '...':
        result.append(2)
    if text[0:3] == '...' or text[0:2] == '..':
        result.append(3)
    if text[-1] == ',' or text[-1] == ';':
        result.append(4)
    return result  

def getWordWithoutPunctuation(self, text):
    if text[-3:] == '...':
        return text[:-3]
    if text[0:3] == '...':
        return text[3:]
    if not(text[0:3] == '...') and text[0:2] == '..':
        return text[2:]
    # if text[-1] == '!' or text[-1] == '?' or (text[-1] == '.' and not(text[-3:] == '...')) or text[-1] == ',' or text[-1] == ';':
    #     return text[:-1]
    return text   
=======
import stanza

nlp = stanza.Pipeline(lang='lv', processors='tokenize,pos,lemma,depparse')
doc = nlp('Tavs tēvs bija ne tikai “draugs” manai ģimenei.')
print(*[f'id: {word.id}\tword: {word.text}\thead id: {word.head}\thead: {sent.words[word.head-1].text if word.head > 0 else "root"}\tdeprel: {word.deprel}' for sent in doc.sentences for word in sent.words], sep='\n')

>>>>>>> Stashed changes
