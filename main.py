import srt 
import re

class Text:
    def __init__(self, subtitle):
        self.subtitle = subtitle
    
    def oneLine(self):
        return self.subtitle.content.replace('\n',' ')

    def getList(self):
        temp = self.subtitle.content.replace('\n',r" (\n) ")
        return temp.split(' ')
    
    def haveMultipleSpeakers(self):
        if(self.subtitle.content.find('\n') != -1):
            temp = self.subtitle.content.split('\n')
            print(temp[1])
            if(temp[0][0] == '-' and temp[1][0] == '-' ):
                return True
            return False
    
    def haveLabel(self):
        temp = self.subtitle.content.split(' ')
        if(temp[0][-1] == ':'):
            return True
        return False

    def withoutLabel(self):
        if(self.haveLabel() == True):
            temp = self.subtitle.content.replace(self.getLabel()+' ','')
            return temp

    def getLabel(self) -> str:
        if(self.haveLabel() == True):
            temp = self.subtitle.content.split(' ')
            return temp[0]

    def sentenceDone(self):
        if(self.subtitle.content[-1] != '.' or self.subtitle.content[-1] != '?' or self.subtitle.content[-1] != '!'):
            return False
        return True

    def removeTags(self):
        p = re.compile(r'<.*?>')
        return p.sub('',self.subtitle.content)

    def removeNotes(self):
        p = re.compile(r'♪')
        return p.sub('',self.subtitle.content)



f = open("sample.srt", encoding='utf-8-sig')

generator = srt.parse(f.read())

subtitles = list(generator)

t = Text(subtitles[3])

print(t.getList())