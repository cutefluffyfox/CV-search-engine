import os
from typing import Iterator
from typing import Union
from typing import List
from typing import Tuple

import nltk
import PyPDF2
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(stopwords.words('english'))


def find(path: str) -> Iterator[str]:
    for root, dirs, files in os.walk(path):
        if dirs:
            continue
        
        for file_name in files:
            yield os.path.join(root, file_name)


def parse_pdf(pdf_path: str) -> str:
    result = []
    with open(pdf_path, 'rb') as pdf:
        pdf = PyPDF2.PdfReader(pdf_path)
        
        for page in pdf.pages:
            result.extend(page.extract_text().split("\n"))
    
    result = list(filter(lambda x: x != " ", result))
    result = list(map(lambda x: x.strip(), result))
    result = ' '.join(result)
    
    return result


def preprocess(text: str) -> str:
    word_tokens = word_tokenize(text)
    filtered_sentence = []

    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)
    
    for i in range(len(filtered_sentence) - 1):
        filtered_sentence[i:i+2] = combine_dates(filtered_sentence[i:i+2])
        
    filtered_sentence = list(filter(lambda x: x != " ", filtered_sentence))
    
    return ' '.join(filtered_sentence)


def is_year(year: str) -> bool:
    return len(year) == 4 and all(map(lambda digit: digit.isdigit(), year))


def combine_dates(month_year_list: List[str]) -> Union[str, Tuple[str, str]]:
    months_cut = [
        "Jan", 
        "Feb", 
        "Mar", 
        "Apr", 
        "May", 
        "Jun", 
        "Jul", 
        "Aug", 
        "Sep", 
        "Oct", 
        "Nov", 
        "Dec"
    ]
    months_full = [
        "January", 
        "February", 
        "March", 
        "April", 
        "May", 
        "June", 
        "July", 
        "August", 
        "September", 
        "October", 
        "November", 
        "December"
    ]
    
    month, year = month_year_list
    
    if (month in months_cut or month in months_full) and is_year(year):
        return month + year, " "
    else:
        return month, year

