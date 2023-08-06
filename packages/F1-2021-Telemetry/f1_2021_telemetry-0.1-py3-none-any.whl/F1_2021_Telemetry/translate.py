# Translates enum names to user-friendly strings
from enum import Enum

class Case(Enum):
    TITLE = 1
    SENTENCE = 2

def titleCase(string: str):
    string = string.replace("_", " ")
    string = string.title()
    return string

def sentenceCase(string: str):
    string = string.replace("_", " ")
    string = string.capitalize()
    return string

def translate(name: str, case: Case):
    if name in translationTable:
        return translationTable[name]

    elif case is Case.TITLE:
        return titleCase(name)

    elif case is Case.SENTENCE:
        return sentenceCase(name)
    
translationTable = {
    "ONE_SHOT_QUALFYING": "One-shot Qualifying",

    "ART_GP_2019": "Art GP 2019",
    "ART_GP_2020": "Art GP 2020",
    "ART_GP_2021": "Art GP 2021",
    "BWT_2020": "BWT 2020",
    "BWT_2021": "BWT 2021",
    "MCLAREN": "McLaren",
    "MCLAREN_2020": "McLaren 2020",
    "MP_MOTORSPORT_2019": "MP Motorsport 2019",
    "MP_MOTORSPORT_2020": "MP Motorsport 2020",
    "MP_MOTORSPORT_2021": "MP Motorsport 2021",
    "UNI_VIRTUOSI_2019": "Uni-Virtuosi 2019",
    "UNI_VIRTUOSI_2020": "Uni-Virtuosi 2020",
    "UNI_VIRTUOSI_2021": "Uni-Virtuosi 2021",

    "KIMI_RAIKKONEN": "Kimi Räikkönen",
    "MAXIMILIAN_GUNTHER": "Maximilian Günther",
    "SERGIO_SETTE_CAMARA": "Sérgio Sette Câmara",
    "LOUIS_DELETRAZ": "Louis Delétraz",

    "SAKHIR_BAHRAIN": "Sakhir (Bahrain)",
    "BAKU_AZERBAIJAN": "Baku (Azerbaijan)",
    "PORTIMAO": "Portimão",

    "TWO_D": "2D",
    "THREE_D": "3D",
    
    "OK": "OK"
}

