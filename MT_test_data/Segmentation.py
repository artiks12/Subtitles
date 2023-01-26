import srt
# import sys
from datetime import timedelta

def withinRange(LV,EN,offset,range):
    newLV = LV + timedelta(milliseconds=offset)
    return abs(newLV-EN)<timedelta(milliseconds=range)

def intFromTimedelta(time):
    timeSplit = str(time).replace(':','.').split('.')
    hours = int(timeSplit[0])
    minutes = int(timeSplit[1])
    seconds = int(timeSplit[2])
    miliseconds = 0
    if len(timeSplit) == 4:
        miliseconds = int(timeSplit[3])/1000

    return hours*3600000+minutes*60000+seconds*1000+miliseconds

def timeDifference(LV,EN):
    return str(intFromTimedelta(LV) - intFromTimedelta(EN))

def segmentation(EN,LV,offsetLV = 0):
    f = open('MT_test_data/Validated/'+EN+'_validated.srt', encoding='utf-8-sig')
    en = list(srt.parse(f.read()))
    f.close()

    f = open('MT_test_data/Validated/'+LV+'_validated.srt', encoding='utf-8-sig')
    lv = list(srt.parse(f.read()))
    f.close()

    indexLV = 0
    indexEN = 0

    newEN = []
    newLV = []

    while indexLV < len(lv) and indexEN<len(en):
        if withinRange(lv[indexLV].start,en[indexEN].start,offsetLV,500) and withinRange(lv[indexLV].end,en[indexEN].end,offsetLV,500):
            newEN.append(en[indexEN])
            newLV.append(lv[indexLV])
            indexLV += 1
            indexEN += 1
        else:
            if lv[indexLV].start < en[indexEN].start:
                indexLV += 1
            elif lv[indexLV].start > en[indexEN].start:
                indexEN += 1
            else:
                if lv[indexLV].end < en[indexEN].end:
                    indexLV += 1
                else:
                    indexEN += 1

    r = open('MT_test_data/Common/'+EN+'_common'+'.srt','w',encoding='utf-8-sig')
    r.write(srt.compose(newEN))
    r.close()

    r = open('MT_test_data/Common/'+LV+'_common'+'.srt','w',encoding='utf-8-sig')
    r.write(srt.compose(newLV))
    r.close()

# segmentation(sys.argv[1],sys.argv[2],int(sys.argv[3]))

segmentation('Shantaram.S01E01_EN','Shantaram.S01E01_LV',43)
segmentation('Bad.Sisters.S01E09_EN','Bad.Sisters.S01E09_LV',43)
segmentation('Echo.3.S01E04_EN','Echo.3.S01E04_LV',43)
segmentation('See.S03E08._EN','See.S03E08._LV',43)
