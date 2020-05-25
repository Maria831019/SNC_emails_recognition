#klasa zawiera funkcje decydowania o jezyku
#klasa zwiera decydowanie o incydent/request
from langdetect import detect
import re
from vats1 import vat
import pickle
import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
import string


class CaseText:
    def __init__(self,caller,sh_description,description):
        self.caller = caller
        self.description=self.clean(description)
        self.sh_description=sh_description
        self.language_sh_desc=self.language(self.sh_description)
        self.language_desc = self.language(self.description)
#nie wiem czy do klasy jako funkcja tego nie dodac, i głosowanie dziedziczyc tu


    def cutTheCrap(self,table):
        try:
            lang = detect(table[0])

            tmlList = list()

            for element in table:
                if detect(element) == lang:
                    tmlList.append(element)

            return tmlList
        except:
            return table


    def clean(self,text):

        sentences = re.compile(r'[A-Z].*?[\.?!]')
        table_of_sentences = sentences.findall(text)

        if table_of_sentences:  ##table of sentences exist

            tmp_table = self.cutTheCrap(table_of_sentences)
            tmp = ' '.join(tmp_table)
            text = tmp
        else:
            text = text
        return text  # clean text

    def language(self,text):
        try:
            return detect(text)
        except:
            return ''

    def returnToDeSE(self):
        print(self.language_desc)
        if self.language_desc in ['de','da']:
            return {"u_assignment_group":"724e61934f982e00be4b24d18110c7b8","u_work_notes":"German language, please check"}
        elif self.language_desc in ['se','hr','sv']:
            return {"u_assignment_group":"464372410f16f100c8d729a703050e49","u_work_notes":"Swedish language, please check"}
        else:
            return ''

    def getVat(self, text):

        tunus = re.compile(r'Y-Tunnus:.*?,')
        tmp = tunus.findall(text)

        if tmp:
            t = tmp[0]
            t1 = t.replace('Y-Tunnus: ', '')
            t2 = t1.replace(',', '')
            t3 = t2.replace('-', '')
            t = t3
            return 'FI' + t
        else:
            return ''

    def checkMeseVat(self, text):
        tmpVat = getVat(text)

        if tmpVat in vat:
            return True
        else:
            return False

    def staticRules(self):
        if 'postiluotto@intrum.com' in self.caller:
            if checkMeseVat(self.description):
                return {"call_type": "Transferred to MESE"}  # move to mese data
            elif 'Nimi muuttunut' in self.sh_description:
                return {"call_type": "Request", "u_service": "0ef71052dbb6670447ff303c7c9619e2",
                        "request_item": "e6d119d1b50fa100a3fe2d5895880487", "u_sr_category": "Support Request",
                        "u_assignment_group": "90ea8cb50f663100c8d729a703050eff"}
            else:
                return {"call_type": "Request", "u_service": "0ef71052dbb6670447ff303c7c9619e2",
                        "request_item": "e6d119d1b50fa100a3fe2d5895880487", "u_sr_category": "Support Request",
                        "u_assignment_group": "90ea8cb50f663100c8d729a703050eff"}
        else:
            return ''  # false if static rule not defined

    def text_processing(self,text,language):
        #language = 'english'
        stemmer = SnowballStemmer(language)
        stems = [stemmer.stem(word.lower()) for word in nltk.word_tokenize(text)]
        stems = [word for word in stems if word.isalpha()]
        stems = [word for word in stems if word not in set(stopwords.words(language))]
        stems = [word for word in stems if word not in string.punctuation]

        return stems


    def predict_(self,file,text,language):

        inc = 0
        req = 0

        if language == 'fi':
            language = 'finnish'
        else:
            language = 'english'
        t = self.text_processing(text,language)
        f = open(file,'rb')
        classifier = pickle.load(f)
        f.close()

        wynik = classifier.predict(t)

        for e in wynik:
            if 'inc' in e.lower():
                inc = inc +1
            else:
                req=req +1

        if inc >=req:
            return 'incidet'
        else:
            return 'request'

    def decideType(self):
        inc = 0
        req = 0
        data = dict()

        if self.language_sh_desc == 'fi':
            if 'inc' in self.predict_('NB_FI_SH_DESC.pickle', self.sh_description,'fi'):
                inc = inc +1
            else:
                req = req + 1
        else:
            if 'inc' in self.predict_('NB_EN_SH_DESC.pickle', self.sh_description,'en'):
                inc = inc + 1
            else:
                req = req + 1

        if self.language_desc == 'fi':
            if 'inc' in self.predict_('NB_FI_DESC.pickle', self.description,'fi'):
                inc = inc + 1
            else:
                req = req + 1
        else:
            if 'inc' in self.predict_('NB_EN_DESC.pickle', self.description,'en'):
                inc = inc + 1
            else:
                req = req + 1

        if inc >= req:
            return {"call_type":"Incident","u_service":"0ef71052dbb6670447ff303c7c9619e2"}
        else:
            return {"call_type": "Request", "u_service": "0ef71052dbb6670447ff303c7c9619e2",
                        "request_item": "e6d119d1b50fa100a3fe2d5895880487", "u_sr_category": "Support Request",
                        "u_assignment_group": "90ea8cb50f663100c8d729a703050eff"}
