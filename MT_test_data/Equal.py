import srt
import re
import math

def findCaptionByTime(start,end,captions):
    for i in captions:
        if i.start == start and i.end == end:
            return i.index
    return None

def equalRows(filename):
    # f = open("MT_test_data/Common/"+filename+"_common.srt", encoding='utf-8-sig')

    f = open("MT_test_data/Common/"+filename+"_EN_common.srt", encoding='utf-8-sig')
    generator = srt.parse(f.read())

    f.close()

    en = list(generator)

    f = open("MT_test_data/Common/"+filename+"_LV_common.srt", encoding='utf-8-sig')
    generator = srt.parse(f.read())

    f.close()

    lv = list(generator)

    
    f = open("MT_test_data/Validated/"+filename+"_EN_validated.srt", encoding='utf-8-sig')
    generator = srt.parse(f.read())

    f.close()

    validatedEN = list(generator)

    f = open("MT_test_data/Validated/"+filename+"_LV_validated.srt", encoding='utf-8-sig')
    generator = srt.parse(f.read())

    f.close()

    validatedLV = list(generator)

    result = []
    for i in range (len(en)):
        enL = len(en[i].content.split('\n'))
        lvL = len(lv[i].content.split('\n'))
        if not(enL == lvL):
            result.append([i+1,enL-lvL,findCaptionByTime(en[i].start,en[i].end,validatedEN),findCaptionByTime(lv[i].start,lv[i].end,validatedLV)])
    print(filename)
    for r in result:
        print(r)
        if r[1] == 1:
            temp = validatedLV[r[3]-1].content.split()
            if len(temp) > 1:
                middle = math.ceil(len(temp)/2)
                validatedLV[r[3]-1].content = ' '.join(temp[:middle]) + '\n' + ' '.join(temp[middle:])
            else:
                print(temp)
                print("Too small.")
        elif r[1] == -1:
            validatedLV[r[3]-1].content = validatedLV[r[3]-1].content.replace('\n',' ')
        # tempEN = validatedEN[r[2]-1].content.replace('\n',' <br/> ').split()
        # tempLV = validatedLV[r[3]-1].content.replace('\n',' <br/> ').split()
        # print(tempEN)
        # print(tempLV)
        # action = input("What to do? (split/merge): ")
        # if action == 'merge':
        #     validatedLV[r[3]-1].content = validatedLV[r[3]-1].content.replace('\n',' ')
        #     print(validatedLV[r[3]-1].content)
        # elif action == 'skip':
        #     continue
        # elif type(int(action)) == int:
        #     data = int(action)
        #     validatedLV[r[3]-1].content = ' '.join(tempLV[:data+1]) + '\n' + ' '.join(tempLV[data+1:])
        #     print(validatedLV[r[3]-1].content)

    print(len(result))

    r = open('MT_test_data/Validated/'+filename+'_LV_validated'+'.srt','w',encoding='utf-8-sig')
    r.write(srt.compose(validatedLV))
    r.close()

def equalSpeakers(filename):
    # f = open("MT_test_data/Common/"+filename+"_common.srt", encoding='utf-8-sig')

    f = open("MT_test_data/Common/"+filename+"_EN_common.srt", encoding='utf-8-sig')
    generator = srt.parse(f.read())

    f.close()

    en = list(generator)

    f = open("MT_test_data/Common/"+filename+"_LV_common.srt", encoding='utf-8-sig')
    generator = srt.parse(f.read())

    f.close()

    lv = list(generator)

    result = []
    for i in range (len(en)):
        temp = []
        enRows = re.sub(r"<.*?>",'',en[i].content).split('\n')
        lvRows = re.sub(r"<.*?>",'',lv[i].content).split('\n')

        if len(enRows)==2:
            if enRows[0][0:2] == '– ' or enRows[1][0:2] == '– ':
                temp.append(i+1)
            elif enRows[0][0] == '–' or enRows[1][0] == '–':
                temp.append(str(i+1)+'_')
            else:
                temp.append(-1)
        else:
            temp.append(-1)
        
        if len(lvRows)==2:
            if lvRows[0][0:2] == '– ' or lvRows[1][0:2] == '– ':
                temp.append(i+1)
            elif lvRows[0][0] == '–' or lvRows[1][0] == '–':
                temp.append(str(i+1)+'_')
            else:
                temp.append(-1)
        else:
            temp.append(-1)

        if len(temp)==2:
            if not(temp[0] == -1 and temp[1] == -1):
                if str(temp[0])[-1] == '_' or str(temp[1])[-1] == '_':
                    result.append(temp)
                elif str(temp[0]) == '-1' or str(temp[1]) == '-1':
                    result.append(temp)

    print(filename)
    for r in result:
        print(r)

# equalRows('Bad.Sisters.S01E09')
# equalSpeakers('Bad.Sisters.S01E09')

# equalRows('Echo.3.S01E04')
# equalSpeakers('Echo.3.S01E04')

# equalRows('See.S03E08.')
# equalSpeakers('See.S03E08.')

# equalRows('Shantaram.S01E01')
# equalSpeakers('Shantaram.S01E01')

# equalRows('Wednesday.S01E03')
# equalSpeakers('Wednesday.S01E03')