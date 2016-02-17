# Stemmer for russian texts
---
## Features
---
Cleanup text using multilevel stopwords lists and stem text with morphological analyzer for Russian language Yandex Mystem 3.0
## Requirements
* [Python_ 2.7.x](http://python.org)
* [pymystem3](https://github.com/Digsolab/pymystem3)  

## Installation  
download `stemmer.py` to your working directory   
## Usage example
```python
import stemmer
text = 'Ещё одно слабое звено товарных рынков – алюминий, чьи биржевые запасы ' \
        'в Китае достигли исторических максимумов,  и поэтому котировки на «летучий ' \
        'металл» могут снизиться до конца октября до диапазона 1870-1880 долларов ' \
        'за тонну.'
cleaned_text = stemmer.cleaning(text)
print(stemmer.stemming(cleaned_text))
```
Output
```
еще один слабый звено товарный рынок   алюминий  чей биржевой запас 
китай достигать исторический максимум  поэтому котировка  летучий
металл  мочь снижаться конец октябрь диапазон 1870 1880 доллар
тонна
```
