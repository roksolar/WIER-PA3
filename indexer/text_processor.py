import string
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from bs4.element import Comment
from nltk.corpus import stopwords

stop_words_slovene = set(stopwords.words("slovenian")).union(
    {"ter", "nov", "novo", "nova", "zato", "še", "zaradi", "a", "ali", "april", "avgust", "b", "bi", "bil", "bila",
     "bile", "bili", "bilo", "biti", "blizu", "bo", "bodo", "bojo", "bolj", "bom", "bomo", "boste", "bova", "boš",
     "brez", "c", "cel", "cela", "celi", "celo", "d", "da", "daleč", "dan", "danes", "datum", "december", "deset",
     "deseta", "deseti", "deseto", "devet", "deveta", "deveti", "deveto", "do", "dober", "dobra", "dobri", "dobro",
     "dokler", "dol", "dolg", "dolga", "dolgi", "dovolj", "drug", "druga", "drugi", "drugo", "dva", "dve", "e", "eden",
     "en", "ena", "ene", "eni", "enkrat", "eno", "etc.", "f", "februar", "g", "g.", "ga", "ga.", "gor", "gospa",
     "gospod", "h", "halo", "i", "idr.", "ii", "iii", "in", "iv", "ix", "iz", "j", "januar", "jaz", "je", "ji", "jih",
     "jim", "jo", "julij", "junij", "jutri", "k", "kadarkoli", "kaj", "kajti", "kako", "kakor", "kamor", "kamorkoli",
     "kar", "karkoli", "katerikoli", "kdaj", "kdo", "kdorkoli", "ker", "ki", "kje", "kjer", "kjerkoli", "ko", "koder",
     "koderkoli", "koga", "komu", "kot", "kratek", "kratka", "kratke", "kratki", "l", "lahka", "lahke", "lahki",
     "lahko", "le", "lep", "lepa", "lepe", "lepi", "lepo", "leto", "m", "maj", "majhen", "majhna", "majhni", "malce",
     "malo", "manj", "marec", "me", "med", "medtem", "mene", "mesec", "mi", "midva", "midve", "mnogo", "moj", "moja",
     "moje", "mora", "morajo", "moram", "moramo", "morate", "moraš", "morem", "mu", "n", "na", "nad", "naj", "najina",
     "najino", "najmanj", "naju", "največ", "nam", "narobe", "nas", "nato", "nazaj", "naš", "naša", "naše", "ne",
     "nedavno", "nedelja", "nek", "neka", "nekaj", "nekatere", "nekateri", "nekatero", "nekdo", "neke", "nekega",
     "neki", "nekje", "neko", "nekoga", "nekoč", "ni", "nikamor", "nikdar", "nikjer", "nikoli", "nič", "nje", "njega",
     "njegov", "njegova", "njegovo", "njej", "njemu", "njen", "njena", "njeno", "nji", "njih", "njihov", "njihova",
     "njihovo", "njiju", "njim", "njo", "njun", "njuna", "njuno", "no", "nocoj", "november", "npr.", "o", "ob", "oba",
     "obe", "oboje", "od", "odprt", "odprta", "odprti", "okoli", "oktober", "on", "onadva", "one", "oni", "onidve",
     "osem", "osma", "osmi", "osmo", "oz.", "p", "pa", "pet", "peta", "petek", "peti", "peto", "po", "pod", "pogosto",
     "poleg", "poln", "polna", "polni", "polno", "ponavadi", "ponedeljek", "ponovno", "potem", "povsod", "pozdravljen",
     "pozdravljeni", "prav", "prava", "prave", "pravi", "pravo", "prazen", "prazna", "prazno", "prbl.", "precej",
     "pred", "prej", "preko", "pri", "pribl.", "približno", "primer", "pripravljen", "pripravljena", "pripravljeni",
     "proti", "prva", "prvi", "prvo", "r", "ravno", "redko", "res", "reč", "s", "saj", "sam", "sama", "same", "sami",
     "samo", "se", "sebe", "sebi", "sedaj", "sedem", "sedma", "sedmi", "sedmo", "sem", "september", "seveda", "si",
     "sicer", "skoraj", "skozi", "slab", "smo", "so", "sobota", "spet", "sreda", "srednja", "srednji", "sta", "ste",
     "stran", "stvar", "sva", "t", "ta", "tak", "taka", "take", "taki", "tako", "takoj", "tam", "te", "tebe", "tebi",
     "tega", "težak", "težka", "težki", "težko", "ti", "tista", "tiste", "tisti", "tisto", "tj.", "tja", "to", "toda",
     "torek", "tretja", "tretje", "tretji", "tri", "tu", "tudi", "tukaj", "tvoj", "tvoja", "tvoje", "u", "v", "vaju",
     "vam", "vas", "vaš", "vaša", "vaše", "ve", "vedno", "velik", "velika", "veliki", "veliko", "vendar", "ves", "več",
     "vi", "vidva", "vii", "viii", "visok", "visoka", "visoke", "visoki", "vsa", "vsaj", "vsak", "vsaka", "vsakdo",
     "vsake", "vsaki", "vsakomur", "vse", "vsega", "vsi", "vso", "včasih", "včeraj", "x", "z", "za", "zadaj", "zadnji",
     "zakaj", "zaprta", "zaprti", "zaprto", "zdaj", "zelo", "zunaj", "č", "če", "često", "četrta", "četrtek", "četrti",
     "četrto", "čez", "čigav", "š", "šest", "šesta", "šesti", "šesto", "štiri", "ž", "že", "svoj", "jesti", "imeti",
     "\u0161e", "iti", "kak", "www", "km", "eur", "pač", "del", "kljub", "šele", "prek", "preko", "znova", "morda",
     "kateri", "katero", "katera", "ampak", "lahek", "lahka", "lahko", "morati", "torej"})


def visible(element):
    #noscript?
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]', 'noscript']:
        return False
    if isinstance(element, Comment):
        return False
    if element == '\n' or element.strip() == "":
        return False
    return True


def process_text(html):
    soup = BeautifulSoup(html, features="lxml")
    texts = soup.findAll(text=True)
    # Get text from html
    visible_texts = filter(visible, texts)
    return get_words(visible_texts)


def process_word(word):
    # Remove punctuation, to lower
    word = word.strip(string.punctuation).lower()
    # Add word if not empty and not a stopword
    if word != '' and word not in stop_words_slovene:
        return word
    return ''


def get_words(list_of_texts):
    words = []
    for text in list_of_texts:
        for word in word_tokenize(text):
            words.append(word)
    return words
