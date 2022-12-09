from tilde import translate
import re

system_id = 'smt-ad429a53-17cd-44af-affe-b684cf65f9ae'

def Translator(lst):
<<<<<<< Updated upstream
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
=======
    result = [[],[],[],[],[],[]]
    result[0] = lst[0]
    result[1] = lst[1]
    temp = []
    for l in lst[2][0]:
        temp.append(l.replace(' ..',' ').split('... '))
    result[2].append(temp)
    result[2].append(translate.translate(lst[2][1])['translation']) 
    unfinishedInSingleCaption(result)
    for label in lst[3]:
        if not(re.match(r"-+",label[0])):
            text = label[0][0:-1]
            trans = translate.translate(text)['translation']
            result[3].append([trans+':',label[1]])
        else:
            result[3].append([label[0],label[1]])
>>>>>>> Stashed changes
    for enclosings in lst[4]:
        enc = enclosings[0]
        text = ' '.join(enclosings[1:-1])
        trans = translate.translate(text)['translation']
        enc += trans + enclosings[-1]
        result[4].append(enc)
<<<<<<< Updated upstream
    return result
=======
    result[5] = lst[5]
    return result

def unfinishedInSingleCaption(result):
    found = False
    # temp = ''
    # for l in result[0]:
    #     if len(l) > 1:
    #         found = True
    #         for c in range(len(l)):
    #             if c+1 == len(l):
    #                 temp += l[c] + ' '
    #             else:
    #                 temp += l[c] + '... '
    #     else:
    #         temp += l[0]
        
>>>>>>> Stashed changes
