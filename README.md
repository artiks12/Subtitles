# Subtitles

<p>This is a program writen in python that translates SRT format subtitles. The program was created as part of university course work and seminar work.</p>

# Used packages
<ul>
<li>
<a href="https://pypi.org/project/srt/">srt</a> - library that stores srt subtitles as objects
</li>
<li>
<a href="https://github.com/tilde-nlp/mt-api-python-demo">tilde MT API</a> - library that allows the use of tilde MT in solutiuon. Requires client_id.
</li>
<li>
<a href="https://pypi.org/project/sacrebleu/">sacreBLEU</a> - used for MT system evaluation.
</li>
</ul>

# File Structure
<p>BBC_Evaluation - stores csv files showing the results of subtitle guideline evaluations. There are 3 subfolders</p>
<ul>
<li>
Percentage - shows the total scores of evaluation for each subtitle file in percentage format (how many percent of subtitles follow said criteria)
</li>
<li>
Raw - shows the raw data for each subtitle in every subtitle file
</li>
<li>
Total - shows the total scores of evaluation for each subtitle file in sum format (how many subtitles follow said criteria)
</li>
</ul>
<p>MT_Evaluation - contains results of MT system evaluation</p>
<p>MT_Test_Data - contains test data used for research and code that aquires said test data</p>
<ul>
<li>
Common - contains subtitle files with common subtitles between langauages
</li>
<li>
Original - contains subtitle file originals
</li>
<li>
Validated - contains fixed subtitles. Used for BBC guideline evaluation
</li>
<li>
Segmentated - contains test data for MT evaluation
  <ul>
  <li>
  WithFormating - text with tags and formating
  </li>
  <li>
  WithoutFormating - text without tags and formating
  </li>
  </ul>
</li>
<li>
Equal.py - code that checks if subtitle files in Common folder have equal ammount of subtitles and text rows
</li>
<li>
Second.py - code that uses subtile files in "Common" folder to create test cases in "Segmentated" folder
</li>
<li>
Segmentation.py - code that uses subtitle files in "Validated" folder to create subtitles stored in "Common" folder
</li>
<li>
Validation.py - code that uses subtitle files in "Original" folder to create subtitles stored in "Validated" folder
</li>
</ul>
<p>Results - Stored translated subtitles</p>
<ul>
<li>
MT_Evaluation_Results - stores translations from files in "MT_Test_data/Segmentated" folder
</li>
<li>
Subtitle_translations - stores translations from files in "MT_Test_data/Validated" folder
</li>
</ul>
<p>SubtitleTranslation - Stores the solution for subtitle translatior</p>
<ul>
<li>
Subtitles - Stores subtitle samples
</li>
<li>
Translations - Stores translations generated with the program (if ran from command line).
</li>
<li>
Caption.py - Stores the code for "Caption" class that extends the "srt.Subtitle" class in package "srt"
</li>
<li>
Combiner.py - Stores the code that groups subtitles together.
</li>
<li>
Constants.py - Stores constants used in solution
</li>
<li>
Evaluator.py - Stores the code that creates new subtitle files for translations and gets evaluation data stored in "BBC_Evaluation" folder
</li>
<li>
main.py - This is where the translation starts to execute
</li>
<li>
Sentences.py - Stores the code for "Sentences" class that stores combined captions, translates them and splits text in captions
</li>
<li>
Translator.py - Stores the code that sends text to tilde MT system.
</li>
</ul>

<p>CheckWholeSentences.py - Stores the code that checks if Test data in "MT_Test_Data/Segmentated" folder where subtitles are combined in sentences has equal amount of sentences in both languages and if their row ids match.</p>
<p>MT_Evaluation.py - Stores the code that does MT evaluation and aquires scores stored in "MT_Evaluation" folder</p>

# Using the translator
## With command prompt
<ul>
<li>
Run the following script in "SubtitleTranslator" folder:
  <ul>
  <li>
  python main.py filename
  </li>
  </ul>
where filename is the name of the file wihtout extension.
</li>
<li>Make sure that the file is located in "SubtitleTranslator/Subtitles" folder.</li>
<li>Translations will be saved in "SubtitleTranslator/Results" folder.</li>
</ul>

## With VS code
<ol>
<li>in "SubtitleTranslator/main.py" comment out "execute(sys.argv[1])" in line 39 and insert following: execute(filename) where filename is the name of the file wihtout extension.</li>
<li>Make sure that the file is located in "SubtitleTranslator/Subtitles" folder.</li>
<li>Click "Run python file" for file main.py in root folder. Translations will be saved in "Results" folder.</li>
</ol>

# Getting evaluation data
## For subtitle guideline evaluation.
<ol>
<li>in "SubtitleTranslator/main.py" comment out "execute(sys.argv[1])" in line 39 as well as lines 12 and 33 and remove comments in the same file from lines 14, 30 and 40 through 43</li>
<li>Click "Run python file" for file main.py in root folder with VS code.</li>
<li>Evaluation data will be saved in "BBC_Evaluation" folder (see file structure).</li>
</ol>

## For MT translations
<p>Click "Run python file" for file MT_Evaluation.py in root folder with VS code. Evaluation data will be saved in "MT_Evaluation" folder (see file structure).</p>

## Preparing test data for MT evaluation
<p>Put subtitle files in "MT_test_data/Original" folder and click "Run python file" for all listed python files in given order:</p>
<ol>
<li>Validation.py</li>
<li>Segmentation.py</li>
<li>Second.py</li>
</ol>
<p>Run the equal.py program the same way to check whether reference and hypotheses have equal amount of data and whether it is correct. If any of the test cases print out the number 0 then test data is correct.</p>
