from MT_Evaluation import getCleanText
from datetime import datetime

# Checks if test cases with whole sentences are equal between hypotheses and reference
def CheckWholeSentences(originalFormating,filename):
    print(filename + " " + originalFormating + " " + "Formating.")
    pathToOriginal = "MT_test_data/Segmentated/"+originalFormating+"Formating/"
    pathToTranslation = "MT_test_data/Segmentated/WithoutFormating/"

    originalSentences = filename+"__sentences"+originalFormating+"Formating.en"
    translated = filename+"__sentencesWithoutFormating.lv"
    f = open(pathToOriginal+originalSentences, encoding='utf-8-sig')

    hypothesesSentences = []
    for line in f:
        temp = line.rstrip().split('\t')
        hypothesesSentences.append([temp[0],getCleanText(temp[1],False)])

    f.close()

    f = open(pathToTranslation+translated, encoding='utf-8-sig')
    reference = []
    for line in f:
        temp = line.rstrip().split('\t')
        reference.append([temp[0],getCleanText(temp[1],False)])

    f.close()

    if len(hypothesesSentences) == len(reference):
        for i in range(len(reference)):
            if not(hypothesesSentences[i][0] == reference[i][0]):
                print(hypothesesSentences[i][0] + ' and ' + reference[i][0])
                return 1
        return 0
    for i in range(len(reference)):
        if not(hypothesesSentences[i][0] == reference[i][0]):
            print(hypothesesSentences[i][0] + ' and ' + reference[i][0])
            return 2

print(CheckWholeSentences("With","Bad.Sisters.S01E09"))
print(CheckWholeSentences("Without","Bad.Sisters.S01E09"))
print(CheckWholeSentences("With","Echo.3.S01E04"))
print(CheckWholeSentences("Without","Echo.3.S01E04"))
print(CheckWholeSentences("With","See.S03E08."))
print(CheckWholeSentences("Without","See.S03E08."))
print(CheckWholeSentences("With","Shantaram.S01E01"))
print(CheckWholeSentences("Without","Shantaram.S01E01"))