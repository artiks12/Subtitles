from Caption import Caption
from Sentences import Sentences

combined = []                 # List with combined captions
combinedLast = -1             # Last sentence checked
combinedUnfinished = -1       # Last unfinished sentence (ends with 3 dots)
combinedContinue = 2          # Checks if sentence continues. 0 - Yes; 1 - Unfinished; 2 - No


# Main combined function for combining captions.
def addToCombined(t):
    global combined
    global combinedLast
    global combinedUnfinished
    global combinedContinue

    # If caption starts a new sentence.
    if (t.newSentence() and combinedContinue >= 1) or t.isEffect():
        combined.append(Sentences(t,t.getLabel()))
        if not(t.isEffect()):
            combinedLast = len(combined)-1

    # If caption continues previous caption.
    elif t.contSentence() or combinedContinue <= 1:
        combined[combinedLast].addCaption(t)

    # If caption continues previous unfinished caption.
    else:
        combined[combinedUnfinished].addCaption(t)
    
    # If caption has unfinished meaning (...).
    if combined[combinedLast].inEnclosing() == True:
        combinedContinue = 0
    elif t.unfinishedSentence():
        combinedUnfinished = combinedLast
        combinedContinue = 1
    # If caption ends sentence.
    elif t.endsSentence():
        combinedContinue = 2
    # If caption continues sentence.
    else:
        combinedContinue = 0

# Starts combining captions
def combiner(subtitles):
    global combined
    global combinedLast
    global combinedUnfinished
    global combinedContinue
    combined = []                 # List with combined captions
    combinedLast = -1             # Last sentence checked
    combinedUnfinished = -1       # Last unfinished sentence (ends with 3 dots)
    combinedContinue = 2          # Checks if sentence continues. 0 - Yes; 1 - Unfinished; 2 - No
    
    captions = []
    index = 1
    for s in subtitles:
        t = Caption(s,index)
        captions.append(t)
        index += t.getRowCount()
        # Caption has one speaker
        if t.hasMultipleSpeakers() == 1:
            addToCombined(t)
        # Caption has multiple speakers
        else:
            for i in range(t.hasMultipleSpeakers()):
                newCaption = t.getCopyWithOneSpeaker(i)
                addToCombined(newCaption)
    
    return (combined,captions)