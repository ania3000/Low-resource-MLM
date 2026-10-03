# Low-resource-MLM
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
1. Deletion of garbage at the beginning of a sentence
2. Deletion of ÀÂÃÄÇÊ and other examples of wrong encoding
3. Filtering sentences containing only 1 letter
4. Filtering sentences not containing cyrillic or lowercase letters
5. FIltering sentences containing cyrillic and latin letters within one token
6. Case normalisation

## Training on MLM task
To be continued...
