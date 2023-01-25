# Subtitles

<p>This is a program writen in python that translates SRT format subtitles. The program was created as part of course work.</p>

# Used packages
<ul>
<li>
<a href="https://pypi.org/project/srt/">srt</a> - library that stores srt subtitles as objects
</li>
<li>
<a href="https://github.com/tilde-nlp/mt-api-python-demo">tilde MT API</a> - library that allows the use of tilde MT in solutiuon. Requires client_id.
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

# Using the translatior
<p>With command prompt</p>
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

<p>With VS code</p>
<ol>
<li>in "SubtitleTranslator/main.py" comment out "execute(sys.argv[1])" in line 39 and insert following: execute(filename) where filename is the name of the file wihtout extension.</li>
<li>Make sure that the file is located in "SubtitleTranslator/Subtitles" folder.</li>
<li>Click "Run python file" for file main.py in root folder. Translations will be saved in "Results" folder.</li>
</ol>
