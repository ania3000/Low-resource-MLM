# Components
## Corpus pre-processing
### Ossetic
1. Local deduplication
2. Removing HTML and JS code blocks
3. Global deduplication by lines
4. Removing source artifacts
5. Short document filtering
6. LSH deduplication
   
### Tajik
1. Local deduplication
2. Global deduplication by lines
3. Short document filtering
4. LSH deduplication

## Corpus post-processing
1. Sentence segmentation (via nltk for Tajik, via regular expression for Ossetic)
2. Deletion of garbage at the beginning of a sentence
3. Deletion of ÀÂÃÄÇÊ and other examples of wrong encoding
4. Filtering sentences containing only 1 letter
5. Filtering sentences not containing cyrillic or lowercase letters
6. FIltering sentences containing cyrillic and latin letters within one token
7. Case normalisation

## Training on MLM task
To be continued...

# Installation
```bash
git clone https://github.com/ania3000/Low-resource-MLM.git
cd Low-resource-MLM
pip install -r requirements.txt
```
## Pre-processing 
2 modes ('m' argument) available: tajik and ossetic. Pass 'min-chars' and 'lsh-threshold' arguments to change the default value.
```bash
python clean_corpus.py -i input.txt -o input-preproc.txt -m tajik
```
## Post-processing
2 modes ('m' argument) available: tajik and ossetic.
```bash
python process_sentences.py -i input-preproc.txt -o output.txt -m tajik
```
