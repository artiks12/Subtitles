import sys
sys.path.insert(0, 'c:/Users/Artis/Documents/GitHub/Subtitles/')

from tilde import translate
import re

system_id = 'smt-ad429a53-17cd-44af-affe-b684cf65f9ae'

def fixText(text):
    opening = text.replace('( ','(').replace('[ ','[').replace('{ ','{').replace('“ ','"')
    closing = opening.replace(' )',')').replace(' ]',']').replace(' }','}').replace(' ”','"')
    return closing

# Function that sends text to Tilde MT.
# lst[0] - text starts in caption;row
# lst[1] - text ends in caption;row
# lst[2] - text to translate
def Translator(lst):
    result = {
        "start":[],
        "end":[],
        "text":[],
        "speakers":[],
        "enclosings":[],
        "unfinished":[],
    }
    result["start"] = lst["start"]
    result["end"] = lst["end"]
    temp = []
    for l in lst["text"][0]:
        temp.append(l.replace(' ..',' ').split('... '))
    result["text"].append(temp)
    result["text"].append(translate.translate(fixText(lst["text"][1]))['translation'])
    for label in lst["speakers"]:
        if not(re.match(r"–+",label[0])) and not(re.match(r"-+",label[0])):
            text = label[0][0:-1]
            trans = translate.translate(text)['translation']
            result["speakers"].append([trans+':',label[1]])
        else:
            result["speakers"].append([label[0],label[1]])
    for enclosings in lst["enclosings"]:
        enc = enclosings[0]
        text = ' '.join(enclosings[1:-1])
        trans = translate.translate(text)['translation']
        enc += trans + enclosings[-1]
        result["enclosings"].append(enc)
    result["unfinished"] = lst["unfinished"]
    return result
        
# def setTranslations(combined,captions,mode):
#     index = 0
#     last = 0
#     for s in combined:
#         translations = s.getCaptionContentAfterTranslationSavingSentenceOrigins(mode)
#         print(translations)
#         for t in translations:
#             if last == t:
#                 captions[t-1].translation += '\n'
#             captions[t-1].translation += translations[t]
#             last = t
#         index += 1
    
#     return captions

# Function that gets translations for caption groups.
def setTranslations(combined):
    result = []
    for s in combined:
        # print(s.getIndexes())
        result.append(s.getTranslations())
        # print(result[-1])
    return result

# Function that gets translations for caption groups for each row division type.
def insertTranslations(combined,translations):
    index = 0
    result = {
        'proportional':{},
        'proper':{},
        'symbols':{},
        'rows':{},
    }
    modes = ['proportional','proper','symbols','rows']
    for s in range(len(combined)):
        for mode in modes:
            temp = combined[s].getCaptionContentAfterTranslationSavingSentenceOrigins(mode,translations[s])
            for t in temp:
                if t-1 in result[mode]:
                    result[mode][t-1] += '\n' + temp[t]
                else:
                    result[mode][t-1] = temp[t]
        index += 1
    return result