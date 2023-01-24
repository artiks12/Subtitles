# Subtitles

This is a program writen in python that translates SRT format subtitles. The program was created as part of course work.

# Used packages
srt - library that stores srt subtitles as objects (https://pypi.org/project/srt/)<br/>
tilde MT API - library that allows the use of tilde MT in solutiuon. Requires client_id. (https://github.com/tilde-nlp/mt-api-python-demo)<br/>

# File Structure
BBC_Evaluation - stores csv files showing the results of subtitle guideline evaluations. There are 3 subfolders<br/>
-) Percentage - shows the total scores of evaluation for each subtitle file in percentage format (how many percent of subtitles follow said criteria)<br/>
-) Raw - shows the raw data for each subtitle in every subtitle file<br/>
-) Total - shows the total scores of evaluation for each subtitle file in sum format (how many subtitles follow said criteria)<br/>
<br/>
MT_Evaluation - contains results of MT system evaluation<br/>
<br/>
MT_Test_Data - contains test data used for research and code that aquires said test data<br/>
-) Common - contains subtitle files with common subtitles between langauages<br/>
-) Original - contains subtitle file originals<br/>
-) Validated - contains fixed subtitles. Used for BBC guideline evaluation<br/>
-) Segmentated - contains test data for MT evaluation<br/>
  -) WithFormating - text with tags and formating<br/>
  -) WithoutFormating - text without tags and formating<br/>
-) Equal.py - code that checks if subtitle files in Common folder have equal ammount of subtitles and text rows<br/>
-) Second.py - code that uses subtile files in "Common" folder to create test cases in "Segmentated" folder<br/>
-) Segmentation.py - code that uses subtitle files in "Validated" folder to create subtitles stored in "Common" folder<br/>
-) Validation.py - code that uses subtitle files in "Original" folder to create subtitles stored in "Validated" folder<br/>
<br/>
Results - Stored translated subtitles<br/>
-) MT_Evaluation_Results - stores translations from files in "MT_Test_data/Segmentated" folder<br/>
-) Subtitle_translations - stores translations from files in "MT_Test_data/Validated" folder<br/>
<br/>
SubtitleTranslation - Stores the solution for subtitle translatior<br/>
-) Subtitles - Stores subtitle samples<br/>
-) Translations - Stores translations generated with the program (if ran from command line).
-) Caption.py - Stores the code for "Caption" class that extends the "srt.Subtitle" class in package "srt"<br/>
-) Combiner.py - Stores the code that groups subtitles together.<br/>
-) Constants.py - Stores constants used in solution<br/>
-) Evaluator.py - Stores the code that creates new subtitle files for translations and gets evaluation data stored in "BBC_Evaluation" folder<br/>
-) main.py - This is where the translation starts to execute<br/>
-) Sentences.py - Stores the code for "Sentences" class that stores combined captions, translates them and splits text in captions<br/>
-) Translator.py - Stores the code that sends text to tilde MT system.<br/>
<br/>
CheckWholeSentences.py - Stores the code that checks if Test data in "MT_Test_Data/Segmentated" folder where subtitles are combined in sentences has equal amount of sentences in both languages and if their row ids match.<br/>
<br/>
MT_Evaluation.py - Stores the code that does MT evaluation and aquires scores stored in "MT_Evaluation" folder<br/>

# Using the translatior
-) With command prompt<br/>
Run the following script in "SubtitleTranslator" folder:<br/>
python main.py filename<br/>
where filename is the name of the file wihtout extension.<br/>
Make sure that the file is located in "SubtitleTranslator/Subtitles" folder.<br/>
Translations will be saved in "SubtitleTranslator/Results" folder.<br/>
<br/>
-) With VS code<br/>
1) in "SubtitleTranslator/main.py" comment out "execute(sys.argv[1])" in line 39 and insert following: execute(filename) where filename is the name of the file wihtout extension.
2) Make sure that the file is located in "SubtitleTranslator/Subtitles" folder.
3) Click "Run python file" for file main.py in root folder. Translations will be saved in "Results" folder.


