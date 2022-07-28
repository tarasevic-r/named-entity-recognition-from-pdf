# General

Invoice information extraction from pdf invoices

## Demo requirments
Possibility to extract the following entities from a pdf invoice:
1. Tiekejo pavadinimas
2. Tiekejo im. kodas
3. Pirkejo pavadinimas
4. Pirkejo im. kodas
5. Saskaitos serija
6. Saskaitos numeris
7. Data
8. Suma be PVM
9. PVM suma
10. Bendra suma

# Setup

1. `spacy` Lithuanian language:
`python -m spacy download lt_core_news_lg`


2. `tesseract` Lithuanian language:

`sudo cp -i ./Downloads/lit.traineddata /usr/share/tesseract-ocr/4.00/tessdata/`
_lit.traineddata_ downloaded from https://github.com/tesseract-ocr/tessdata