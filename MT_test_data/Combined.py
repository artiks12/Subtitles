from Segmentation import segmentation
from Equal import equalRows, equalSpeakers
from Second import preperation
from CheckWholeSentences import CheckWholeSentences

# print('------------------------------------------------------------')
# segmentation('Shantaram.S01E01_EN','Shantaram.S01E01_LV',43)
# segmentation('Bad.Sisters.S01E09_EN','Bad.Sisters.S01E09_LV',43)
# segmentation('Echo.3.S01E04_EN','Echo.3.S01E04_LV',43)
# segmentation('See.S03E08._EN','See.S03E08._LV',43)
# segmentation('Wednesday.S01E03_EN','Wednesday.S01E03_LV',0)

# print('------------------------------------------------------------')
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

# print('------------------------------------------------------------')
# preperation('Wednesday.S01E03_EN')
# preperation('Bad.Sisters.S01E09_EN')
# preperation('Echo.3.S01E04_EN')
# preperation('See.S03E08._EN')
# preperation('Shantaram.S01E01_EN')

# preperation('Wednesday.S01E03_LV')
# preperation('Bad.Sisters.S01E09_LV')
# preperation('Echo.3.S01E04_LV')
# preperation('See.S03E08._LV')
# preperation('Shantaram.S01E01_LV')

# print('------------------------------------------------------------')
# print(CheckWholeSentences("With","Bad.Sisters.S01E09"))
# print(CheckWholeSentences("Without","Bad.Sisters.S01E09"))
# print(CheckWholeSentences("With","Wednesday.S01E03"))
# print(CheckWholeSentences("Without","Wednesday.S01E03"))
# print(CheckWholeSentences("With","Echo.3.S01E04"))
# print(CheckWholeSentences("Without","Echo.3.S01E04"))
# print(CheckWholeSentences("With","See.S03E08."))
# print(CheckWholeSentences("Without","See.S03E08."))
# print(CheckWholeSentences("With","Shantaram.S01E01"))
# print(CheckWholeSentences("Without","Shantaram.S01E01"))