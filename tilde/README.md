# Tilde MT API Demonstration Scripts

## Requirements

In order to use the Tilde MT API, you have to obtain a `client_id`. In order to acquire a `client_id`, please contact mt@tilde.com.

The scripts are written in `python3`. You will need it to run the example scripts.

## System List

To be able to execute translation requests, an MT system ID is necessary.

To identify the systems that are accessible to you, execute the script `get-system-list.py`.

```bash
python3 get-system-list.py [CLIENT_ID]
```

The script will list the MT systems and their IDs so that you can use them further, e.g.:

```
System for en-lv: 'English-Latvian NMT system'
ID: smt-16dra887-317f-4ef4-976c-90bd8c5e1a46

System for lv-en: 'Latvian-English NMT system'
ID: smt-707fe5ce-98e4-46ae-b03a-03080a0db25c
```

## Translation Request

When you know the ID of the MT system you want to send your translation requests to, translation of a paragraph (word, phrase, sentence, multiple sentences) can be executed with the script `translate-text.py`.

Tilde MT API translates both plain text as well as rich text (i.e., with various formatting tags (HTML, XML) data.

```bash
python3 translate-text.py [CLIENT_ID] [SYSTEM_ID] "<div>This is an <b>example</b> of a translation request <img src=\"http://letsmt.eu/images/tilde.svg\" /> with formatting tags.</div>"
```

The script will send the translation request to Tilde MT and it will be translated with the specified MT system. The result will be printed in a JSON format in the standard output stream.

```
{'confidentWordAlignment': [[0, 0], [1, 1], [2, 2], [6, 2], [7, 3], [3, 4], [4, 5], [5, 5], [8, 5], [9, 6], [10, 7], [11, 8]], 'countSentences': 1, 'countTokens': 12, 'originalSentenceRanges': [[0, 131]], 'phraseAlignment': [[[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], [0, 1, 2, 3, 4, 5, 6, 7, 8]]], 'qualityEstimate': 0, 'sourceWordRanges': [[5, 9], [10, 12], [13, 15], [19, 26], [31, 33], [34, 35], [36, 47], [48, 55], [104, 108], [109, 119], [120, 124], [124, 125]], 'targetWordRanges': [[5, 8], [9, 11], [12, 22], [23, 35], [39, 46], [51, 53], [100, 111], [112, 118], [118, 119]], 'translation': '<div>Šis ir tulkošanas pieprasījuma <b>piemērs</b> ar<img src="http://letsmt.eu/images/tilde.svg"/> formatējuma tagiem.</div>', 'translationSentenceRanges': [[0, 125]], 'wordAlignment': [[0, 0], [1, 1], [2, 2], [6, 2], [7, 3], [3, 4], [4, 5], [5, 5], [8, 5], [9, 6], [10, 7], [11, 8]]}
```

The output contains also word alignment information that may be useful for further processing tasks (e.g., to correctly reinsert the translation into a document).

## Updating of Translations

Some systems in Tilde MT feature dynamic learning capabilities (i.e., they can improve over time) and all systems feature an internal translation memory. If a translator corrects a translation of an MT translation, the corrected translation can be sent to the MT system using the script `update-translation.py` (thereby ensuring that the system will continuously improve).

```bash
python3 update-translation.py [CLIENT_ID] [SYSTEM_ID] "Let us translate this text." "Pārtulkosim šo tekstu."
```

Tilde MT will return the status code `200` [OK] if the request will be executed successfully.
