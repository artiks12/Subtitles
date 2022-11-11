from Caption import Caption

class Sentences():
    def __init__(self, subtitle: Caption) -> None:
        self.__captions: list = [subtitle]
        self.__translation: str = ''

    def addCaption(self,caption: Caption):
        self.__captions.append(caption)

    def printSentences(self):
        result = []
        for i in self.__captions:
            if result == []:
                result = i.getOneLinePure()
            else:
                result = result + ' ' + i.getOneLinePure()
        return result

    def printIndexes(self):
        result = []
        for i in self.__captions:
            result.append(i.index)
        return result
