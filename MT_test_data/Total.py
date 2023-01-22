import srt
from datetime import timedelta

def createTotal(lan,ty):
    titles = ['Shantaram.S01E01','Bad.Sisters.S01E09','Echo.3.S01E04','See.S03E08.','Wednesday.S01E03']
    offset = 1
    result = []
    for t in titles:
        f = open('MT_test_data/Common/'+t+lan+ty+'.srt', encoding='utf-8-sig')
        subtitles = list(srt.parse(f.read()))
        f.close()

        for s in subtitles:
            s.start += timedelta(hours=offset)
            s.end += timedelta(hours=offset)

        result.extend(subtitles)
        offset += 1
    
    f.open('MT_test_data/Common/'+'Total'+lan+ty+'.srt', encoding='utf-8-sig')
    f.write(srt.compose(result))
    f.close()

# createTotal('_EN','_common')
# createTotal('_LV','_common')