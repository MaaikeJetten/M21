import json as json
from json import loads

def detect(array):
    detect_array = []
    for a in array:
        cX = (a[0]+a[2])/2
        cY = (a[1]+a[3])/2
        detect_array.append([cX, cY, a[4], a[5]])
    return detect_array

labels = [
"acteren",
"alles-mag-alles-kan",
"brainstorm",
"begrijpen",
"checkpunt",
"data-analyse",
"delen",
"de-wereld-in",
"doelgroep-leren-kennen",
"doe-maar-duurzaam",
"door-de-ogen-van",
"duiveltje",
"echt-nep",
"eindpunt",
"engeltje",
"enquete",
"experts-betrekken",
"filmen",
"gebruikerstest",
"gedachten-parkeren",
"herhaal",
"hypothese",
"inspiratie-opdoen",
"je-gevoel-volgen",
"je-zintuigen-gebruiken",
"keuzes-maken",
"kwaliteitscontrole",
"literatuur-lezen",
"maken",
"mindmap",
"moodboard",
"nabespreken",
"nieuw-leven-inblazen",
"ondernemingsplan",
"onderzoeken",
"ontdekken",
"ontwerpen",
"organiseren",
"persona",
"planning",
"presenteren",
"programma-van-eisen",
"prototype",
"reflecteren",
"samen-sterk",
"samenvatten",
"scenario",
"schetsen",
"succes-bepalen",
"tentoonstellen",
"verslag",
"vertrekpunt",
"vrije-activiteit",
"waarom-vragen-stellen"]

token_id_list = """{
  "phases": [
    { "id": 1, "name": "Begrijpen" },
    { "id": 2, "name": "Ontdekken" },
    { "id": 3, "name": "Ontwerpen" },
    { "id": 4, "name": "Maken" },
    { "id": 5, "name": "Delen" },
    { "id": 6, "name": "Vertrekpunt" },
    { "id": 7, "name": "Eindpunt" }
  ],
  "activities": [
    { "id": 1, "name": "Groowy" },
    { "id": 2, "name": "Herhaal" },
    { "id": 3, "name": "Checkpunt" },
    { "id": 4, "name": "Acteren" },
    { "id": 5, "name": "Alles-mag-alles-kan" },
    { "id": 6, "name": "Brainstorm" },
    { "id": 7, "name": "De-wereld-in" },
    { "id": 8, "name": "Doe-maar-duurzaam" },
    { "id": 9, "name": "Doelgroep-leren-kennen" },
    { "id": 10, "name": "Door-de-ogen-van" },
    { "id": 11, "name": "Duiveltje" },
    { "id": 12, "name": "Echt-nep" },
    { "id": 13, "name": "Engeltje" },
    { "id": 14, "name": "Enquete" },
    { "id": 15, "name": "Experts-betrekken" },
    { "id": 16, "name": "Filmen" },
    { "id": 17, "name": "Gebruikerstest" },
    { "id": 18, "name": "Gedachten-parkeren" },
    { "id": 19, "name": "Inspiratie-opdoen" },
    { "id": 20, "name": "Je-gevoel-volgen" },
    { "id": 21, "name": "Je-zintuigen-gebruiken" },
    { "id": 22, "name": "Keuzes-maken" },
    { "id": 23, "name": "Kwaliteitscontrole" },
    { "id": 24, "name": "Mindmap" },
    { "id": 25, "name": "Moodboard" },
    { "id": 26, "name": "Nabespreken" },
    { "id": 27, "name": "Nieuw-leven-inblazen" },
    { "id": 28, "name": "Ondernemingsplan" },
    { "id": 29, "name": "Onderzoeken" },
    { "id": 30, "name": "Organiseren" },
    { "id": 31, "name": "Persona" },
    { "id": 32, "name": "Planning" },
    { "id": 33, "name": "Presenteren" },
    { "id": 34, "name": "Prototype" },
    { "id": 35, "name": "Reflecteren" },
    { "id": 36, "name": "Samen-sterk" },
    { "id": 37, "name": "Samenvatten" },
    { "id": 38, "name": "Scenario" },
    { "id": 39, "name": "Schetsen" },
    { "id": 40, "name": "Succes-bepalen" },
    { "id": 41, "name": "Tentoonstellen" },
    { "id": 42, "name": "Verslag" },
    { "id": 43, "name": "Waarom-vragen-stellen" },
    { "id": 44, "name": "Blij" },
    { "id": 45, "name": "Boos" },
    { "id": 46, "name": "Content" },
    { "id": 47, "name": "Tevreden" },
    { "id": 48, "name": "Verbaasd" },
    { "id": 49, "name": "Verdrietig" },
    { "id": 50, "name": "Verward" },
    { "id": 51, "name": "Geïnteresseerd" },
    { "id": 52, "name": "Vrije-activiteit" },
    { "id": 53, "name": "Data-analyse" },
    { "id": 54, "name": "Hypothese" },
    { "id": 55, "name": "Literatuur-lezen" },
    { "id": 56, "name": "Programma-van-eisen" }
  ]
}"""

tokens = json.loads(token_id_list)
phase_tokens = tokens.get("phases")
activity_tokens = tokens.get("activities")