import srt
import re

def check(file):
    f = open('MT_test_data/Original/'+file+'.srt', encoding='utf-8-sig')
    original = list(srt.parse(f.read()))
    f.close()

    f = open('MT_test_data/Validated/'+file+'_validated'+'.srt',encoding='utf-8-sig')
    validated = list(srt.parse(f.read()))
    f.close()

    for s in range(len(validated)):
        o = re.sub(r'<.*?>','',original[s].content).replace('– ','').replace('\n',' ')
        v = re.sub(r'<.*?>','',validated[s].content).replace('– ','').replace('\n',' ')
        if not(o==v):
            print(s)

def validate(file):
    f = open('MT_test_data/Original/'+file+'.srt', encoding='utf-8-sig')
    subtitles = list(srt.parse(f.read()))
    f.close()

    new = []

    for s in subtitles:
        if len(s.content) > 0:
            s.content = s.content.replace('- ','– ')
            if s.content[0] == ' ':
                s.content = s.content[1:]
            new.append(s)

    r = open('MT_test_data/Validated/'+file+'_validated'+'.srt','w',encoding='utf-8-sig')
    r.write(srt.compose(new))
    r.close()

validate('Shantaram.S01E01_EN')
validate('Shantaram.S01E01_LV')
validate('Bad.Sisters.S01E09_EN')
validate('Bad.Sisters.S01E09_LV')
validate('Echo.3.S01E04_EN')
validate('Echo.3.S01E04_LV')
validate('See.S03E08._EN')
validate('See.S03E08._LV')


# check('Shantaram.S01E01_EN')
# check('Shantaram.S01E01_LV')
# check('Bad.Sisters.S01E09_EN')
# check('Bad.Sisters.S01E09_LV')
# check('Echo.3.S01E04_EN')
# check('Echo.3.S01E04_LV')
# check('See.S03E08._EN')
# check('See.S03E08._LV')
