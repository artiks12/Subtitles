from tilde import translate
import re

system_id = 'smt-ad429a53-17cd-44af-affe-b684cf65f9ae'

def Translator(lst):
    result = [[],[],[],[],[]]
    result[0] = lst[0]
    result[1] = lst[1]
    result[2] = translate.translate(lst[2])['translation']
    for label in lst[3]:
        if not(re.match(r"-+",label)):
            text = label[0:-1]
            trans = translate.translate(text)['translation']
            result[3].append(trans)
            result[2] = result[2].replace(label,trans+':')
        else:
            result[3].append(label)
    for enclosings in lst[4]:
        enc = enclosings[0]
        text = ' '.join(enclosings[1:-1])
        trans = translate.translate(text)['translation']
        enc += trans + enclosings[-1]
        result[4].append(enc)
    return result