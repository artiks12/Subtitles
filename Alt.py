def getCaptionContentAfterTranslationUsingProportionalCharacterCount(self):
    temp = self.getTranslations()
    result = []

    data = self.prepareDataForChunking(temp)

    originalCaptionCharacters = self.getCharacterCountForEachCaption()

    proportion = len(data[0])/self.getCharacterCountFromAll()

    newCaptionCharacters = list(map(lambda x: x*proportion, originalCaptionCharacters))

    textInCaptions = self.getTextInCaptions(data,newCaptionCharacters)

    for t in textInCaptions:
        charactersInCaption = self.__captions[t[0]].getCharacterCount()
        charactersPerRow = self.__captions[t[0]].getCharacterCountInRows()

        proportion = len(t[1])/charactersInCaption
        newCharactersPerRow = list(map(lambda x: x*proportion, charactersPerRow))
        
        result.append([self.getIndexes()[t[0]],self.getTextInRows(t[1],newCharactersPerRow)])

    return result

def getTextInRows(self,data,counts):
    result = ''
    length = 0
    index = 0
    for elem in data.replace(' ',' _').split('_'):
        length += len(re.sub(r'<.*>','',elem))
        if not(index == len(counts)):
            if length > counts[index]:
                before = length - len(re.sub(r'<.*>','',elem))
                after = length
                if (abs(before-counts[index]) >= abs(after-counts[index])):
                    result += elem.replace(' ','') +'\n'
                    length = 0
                else:
                    result = result[:-1] + '\n' + elem
                    length = len(re.sub(r'<.*>','',elem))
                index += 1
            else:
                result += elem
        else:
            result += elem
    if result[-1:] == '\n' or result[-1:] == ' ':
        result = result[:-1]
    return result

def getTextInCaptions(self,data,counts):
    indexes = self.getIndexes()
    index = 0
    temp = ''
    length = 0
    result = []
    over = False
    for elem in data[0].replace(' ',' _').split('_'):
        if len(data[1]) > 0:
            if data[1][0][1] == indexes[index]:
                temp += data[1][0][0] + ' '
                length = len(re.sub(r'<.*>','',temp))
                data[1].pop(0)
        
        if not(index == len(counts)):
            length += len(re.sub(r'<.*>','',elem))
            if length > counts[index]:
                before = length - len(re.sub(r'<.*>','',elem))
                after = length
                if (abs(before-counts[index]) > abs(after-counts[index])):
                    temp += elem.replace(' ','')
                    result.append([index,temp])
                    temp = ''
                    length = 0
                else:
                    temp = temp[:-1]
                    result.append([index,temp])
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
            result.append([index,temp])
    return result

def prepareDataForChunking(self,translation):
    result = ['',[]]
    for t in translation:
        fixed = t[2][1]
        brackets = re.findall(r'\([^\(\{\[]*\)|\[[^\(\{\[]*\]|\{[^\(\{\[]*\}',fixed) # Gets all bracket text
        for b in range(len(brackets)):
            fixed = fixed.replace(brackets[b],t[4][b], 0)
        result[0] += fixed + ' '
        if not(t[3] == []):
            result[1].extend(t[3])
    result[0] = result[0][:-1]
    return result

def getCharacterCountFromAll(self):
    Sum = 0
    for c in self.__captions:
        Sum += c.getCharacterCount()
    return Sum

def getCharacterCountForEachCaption(self):
    result = []
    for c in self.__captions:
        result.append(c.getCharacterCount())
    return result


# if unfinished == 0:
#     if not(c[-3:] == '...'):
#         temp[0] += c + '... '
#     else:
#         temp[0] += c + ' '
#     if len(multiDots[0]) > 1:
#         unfinished = 1
#     else:
#         multiDots.pop(0)
# else:
#     if multiDots[0][0][0] == multiDots[0][1][0]:
#         temp[0] += c + ' '
#     else:
#         temp[0] += '..' + c + ' '
#     unfinished = 0
#     multiDots.pop(0)