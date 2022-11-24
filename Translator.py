from tilde import translate

system_id = 'smt-ad429a53-17cd-44af-affe-b684cf65f9ae'

def Translator(lst):
    result = []
    for l in lst:
        temp = [[],[],[],[],[]]
        temp[0] = l[0]
        temp[1] = l[1]
        temp[2] = translate.translate(l[2])['translation']
        for label in l[3]:
            text = label[0:-1]
            trans = translate.translate(text)['translation']
            temp[3].append(trans)
        for enclosings in l[4]:
            enc = enclosings[0]
            text = ' '.join(enclosings[1:-1])
            trans = translate.translate(text)['translation']
            enc += trans + enclosings[-1]
            temp[4].append(enc)
        result.append(temp)
    return result