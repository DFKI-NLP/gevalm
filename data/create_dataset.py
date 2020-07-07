import nltk
from nltk import grammar, parse
from nltk.parse.generate import generate
from pattern.de import conjugate
from pattern.de import INFINITIVE, PRESENT, PAST, SG, PL, SUBJUNCTIVE
import os
import sys
import json


def testing(case, n=25):
    count = 0
    for sentence in generate(case):
        print(sentence)
        count +=1
    print(count)

def dump_jsonl(data, output_path, append = False):
    mode ='a+' if append else 'w'
    with open(output_path, mode) as f:
        json_record = json.dumps(data, ensure_ascii=False)
        f.write(json_record + '\n')


# ---------- 1.1. Simple Sentences: Der Autor *lacht.

SimplSent_sg =  grammar.CFG.fromstring("""
    % start S
    S -> NP FV '.'
    NP -> ART_m NN_m | PPER | ART_f NN_f | ART_n NN_n
    ART_m -> 'Der'
    NN_m -> 'Autor' | 'Pilot' | 'Kunde' | 'Lehrer' | 'Senator'
    ART_f -> 'Die'
    NN_f -> 'Senatorin' | 'Beraterin' | 'Frau'| 'Polizistin' | 'Richterin'
    ART_n -> 'das'
    NN_n -> 'Kind'
    PPER -> 'er' | 'es'
    FV -> 'lacht' | 'schwimmt' |  'redet'| 'bleibt' | 'trinkt'
    """)

SimplSent_pl =  grammar.CFG.fromstring("""
    % start S
    S -> NP FV '.'
    NP -> ART NN
    ART -> 'Die'
    NN -> 'Autoren' | 'Piloten' | 'Kunden' | 'Lehrer'  | 'Senatorinnen' | 'Beraterinnen' |'Frauen' | 'Polizistinnen' | 'Richterinnen' |  'Kinder'

    FV -> 'lachen' | 'schwimmen' |  'reden'| 'bleiben' | 'trinken'
    """)

jsn_SimplSent = {}
def json_SimplSent(case, number):
    path = './input/SimplSent'
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        print('{} already exists.'.format(path))

    '''generates jsonl file with examples.
    case defines the grammar used to create the sentences. number (=SG or PL) is the 'wrong' (e.g. not congruent to subject) number of the tested'''
    for sentence in generate(case):
        jsn_SimplSent['text'] = ' '.join(sentence)
        sentence2 = sentence[:]
        sentence2[-2] = '[MASK]'
        jsn_SimplSent['text_masked'] = ' '.join(sentence2)
        # try-except neccesary because of bug in pattern.de library
        try:
            wrong_num = conjugate(sentence[-2], PRESENT, 3, number)
        except:
            wrong_num = conjugate(sentence[-2], PRESENT, 3, number)
        candidates = []
        candidates.append(sentence[-2])
        candidates.append(wrong_num)
        jsn_SimplSent['candidates'] = candidates
        jsn_SimplSent['indexMASK'] = -2
        if case == SimplSent_sg:
            jsn_SimplSent['case'] = "SimplSent_sg"
            dump_jsonl(jsn_SimplSent, path+'/SimplSent_sg.jsonl', append=True)
        elif case == SimplSent_pl:
            jsn_SimplSent['case'] = "SimplSent_pl"
            dump_jsonl(jsn_SimplSent, path+'/SimplSent_pl.jsonl', append=True)
        

    
# ---------- 1.2. S-V-Agreement in a sentential complement: Der Verteter sagte, dass der Autor *lacht.

SVinSentCompl_sgsg =  grammar.CFG.fromstring("""
    % start S
    S -> NP_sg FV_sg_3_past ',' S_COMPL '.'
    NP_sg -> ART_sg_m NN_sg_m |ART_sg_f NN_sg_f
    ART_sg_m -> 'Der'
    NN_sg_m  -> 'Vertreter' | 'Politiker' | 'Arbeiter'
    ART_sg_f -> 'Die'
    NN_sg_f  -> 'Vertreterin'| 'Politikerin' | 'Arbeiterin'
    FV_sg_3_past -> 'sagte' | 'dachte' | 'wusste'
    
    S_COMPL -> KOUS COM_NP_sg COM_FV_sg
    COM_NP_sg -> COM_ART_sg_m COM_NN_sg_m | COM_ART_sg_f COM_NN_sg_f

    KOUS -> 'dass'
    COM_ART_sg_m -> 'der'
    COM_NN_sg_m -> 'Autor' | 'Pilot' | 'Kunde' | 'Lehrer' | 'Senator'
    COM_ART_sg_f -> 'die'
    COM_NN_sg_f ->  'Senatorin' | 'Beraterin' |'Frau' | 'Polizistin' | 'Richterin'
    COM_FV_sg -> 'lacht' | 'schwimmt' |  'redet'| 'bleibt' | 'trinkt'
""")

SVinSentCompl_sgsg =  grammar.CFG.fromstring("""
    % start S
    S -> NP_sg FV_sg_3_past ',' S_COMPL '.'
    NP_sg -> ART_sg_m NN_sg_m
    ART_sg_m -> 'Der'
    NN_sg_m  -> 'Vertreter' | 'Politiker' | 'Arbeiter'
    FV_sg_3_past -> 'sagte' | 'dachte' | 'wusste'
    
    S_COMPL -> KOUS COM_NP_sg COM_FV_sg
    COM_NP_sg -> COM_ART_sg_m COM_NN_sg_m | COM_ART_sg_f COM_NN_sg_f

    KOUS -> 'dass'
    COM_ART_sg_m -> 'der'
    COM_NN_sg_m -> 'Autor' | 'Pilot' | 'Kunde' | 'Lehrer' | 'Senator'
    COM_FV_sg -> 'lacht' | 'schwimmt' |  'redet'| 'bleibt' | 'trinkt'
""")


SVinSentCompl_plpl =  grammar.CFG.fromstring("""
    % start S
    S -> NP_pl FV_pl_3_past ',' S_COMPL '.'

     NP_pl -> ART_pl NN_pl
     ART_pl -> 'Die'
     NN_pl -> 'Vertreter' | 'Politiker' | 'Arbeiterinnen'
     FV_pl_3_past -> 'sagten' | 'dachten' | 'wussten'
     
    S_COMPL -> KOUS COM_NP_pl COM_FV_pl
    KOUS -> 'dass'
    COM_NP_pl -> COM_ART_pl COM_NN_pl
    
    COM_ART_pl -> 'die'
    COM_NN_pl -> 'Autoren' | 'Piloten' | 'Kunden' | 'Lehrer'  | 'Senatorinnen' | 'Beraterinnen' |'Frauen' | 'Polizistinnen' | 'Richterinnen' |  'Kinder'
    COM_FV_pl -> 'lachen' | 'schwimmen' |  'reden'| 'bleiben' | 'trinken'
""")

        
SVinSentCompl_sgpl =  grammar.CFG.fromstring("""
    % start S
    S -> NP_pl FV_pl_3_past ',' S_COMPL '.'
    NP_pl -> ART_pl NN_pl
    ART_pl -> 'Die'
    NN_pl -> 'Vertreter' | 'Politiker' | 'Arbeiterinnen'
    FV_pl_3_past -> 'sagten' | 'dachten' | 'wussten'
    S_COMPL -> KOUS COM_NP_sg COM_FV_sg
    COM_NP_sg -> COM_ART_sg_m COM_NN_sg_m | COM_ART_sg_f COM_NN_sg_f
    KOUS -> 'dass'
    COM_ART_sg_m -> 'der'
    COM_NN_sg_m -> 'Autor' | 'Pilot' | 'Kunde' | 'Lehrer' | 'Senator'
    COM_ART_sg_f -> 'die'
    COM_NN_sg_f -> 'Senatorin' | 'Beraterin' |'Frau' | 'Polizistin' | 'Richterin'
    COM_FV_sg -> 'lacht' | 'schwimmt' |  'redet'| 'bleibt' | 'trinkt'
""")

SVinSentCompl_plsg =  grammar.CFG.fromstring("""
    % start S
    S -> NP_sg FV_sg_3_past ',' S_COMPL '.'
    NP_sg -> ART_sg_m NN_sg_m |ART_sg_f NN_sg_f
    ART_sg_m -> 'Der'
    NN_sg_m  -> 'Vertreter' | 'Politiker' | 'Arbeiter'
    ART_sg_f -> 'Die'
    NN_sg_f  -> 'Vertreterin'| 'Politikerin' | 'Arbeiterin'
    FV_sg_3_past -> 'sagte' | 'dachte' | 'wusste'
         
    S_COMPL -> KOUS COM_NP_pl COM_FV_pl
    KOUS -> 'dass'
    COM_NP_pl -> COM_ART_pl COM_NN_pl
         
    COM_ART_pl -> 'die'
    COM_NN_pl -> 'Autoren' | 'Piloten' | 'Kunden' | 'Lehrer'  | 'Senatorinnen' | 'Beraterinnen' |'Frauen' | 'Polizistinnen' | 'Richterinnen' |  'Kinder'
    COM_FV_pl -> 'lachen' | 'schwimmen' |  'reden'| 'bleiben' | 'trinken'
""")


jsn_SVinSentCompl = {}
def json_SVinSentCompl(case, number):
    path = './input/SVinSentCompl'
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        print('{} already exists.'.format(path))
    '''generates jsonl file with examples.
    case defines the grammar used to create the sentences. number (=SG or PL) is the 'wrong' (e.g. not congruent to subject) number of the tested'''
    for sentence in generate(case):
        jsn_SVinSentCompl['text'] = ' '.join(sentence)
        sentence2 = sentence[:]
        sentence2[-2] = '[MASK]'
        jsn_SVinSentCompl['text_masked'] = ' '.join(sentence2)
        # try-except neccesary because of bug in pattern.de library
        try:
            wrong_num = conjugate(sentence[-2], PRESENT, 3, number)
        except:
            wrong_num = conjugate(sentence[-2], PRESENT, 3, number)
        candidates = []
        candidates.append(sentence[-2])
        candidates.append(wrong_num)
        jsn_SVinSentCompl['candidates'] = candidates
        jsn_SVinSentCompl['indexMASK'] = -2
        if case == SVinSentCompl_sgsg:
            jsn_SVinSentCompl['case'] = "SVinSentCompl_sgsg"
            dump_jsonl(jsn_SVinSentCompl, path+'/SVinSentCompl_sgsg.jsonl', append=True)
        elif case == SVinSentCompl_plpl:
            jsn_SVinSentCompl['case'] = "SVinSentCompl_plpl"
            dump_jsonl(jsn_SVinSentCompl, path+'/SVinSentCompl_plpl.jsonl', append=True)
        elif case == SVinSentCompl_sgpl:
            jsn_SVinSentCompl['case'] = "SVinSentCompl_sgpl"
            dump_jsonl(jsn_SVinSentCompl, path+'/SVinSentCompl_sgpl.jsonl', append=True)
        elif case == SVinSentCompl_plsg:
            jsn_SVinSentCompl['case'] = "SVinSentCompl_plsg"
            dump_jsonl(jsn_SVinSentCompl, path+'/SVinSentCompl_plsg.jsonl', append=True)


# ----------  1.3. Short VP coordination: Der Senator schmunzelt und *lacht. // Medium VP coordination: Der Senator redet mit Dieter und *lacht.

SVshortVPCoord_sg =  grammar.CFG.fromstring("""
    % start CS
    CS -> S KON FV_sg_3_2 '.'
    S -> NP_sg FV_sg_3_1
    
    NP_sg -> ART_sg_m NN_sg_m | ART_sg_f NN_sg_f
    ART_sg_m -> 'Der'
    NN_sg_m -> 'Autor' | 'Pilot' | 'Kunde' | 'Lehrer' | 'Senator'
    ART_sg_f -> 'Die'
    NN_sg_f -> 'Senatorin'|'Beraterin'| 'Frau'|'Polizistin'| 'Richterin'
    FV_sg_3_1 -> 'schwimmt' | 'redet' | 'bleibt' | 'trinkt'
    KON -> 'und'
    FV_sg_3_2 -> 'lacht'| 'liest' | 'lauscht'

""")

SVshortVPCoord_pl =  grammar.CFG.fromstring("""
    % start CS
    CS -> S KON FV_pl_3_2 '.'
    S -> NP_pl FV_pl_3_1
    
    NP_pl -> ART_pl_m NN_pl_m
    ART_pl_m -> 'Die'
    NN_pl_m -> 'Autoren' | 'Piloten' | 'Kunden' | 'Lehrer'  | 'Senatorinnen' | 'Beraterinnen' |'Frauen' | 'Polizistinnen' | 'Richterinnen' |  'Kinder'
    FV_pl_3_1 -> 'schwimmen' | 'reden' | 'bleiben' | 'trinken'
    KON -> 'und'
    FV_pl_3_2 -> 'lachen'| 'lesen' | 'lauschen'

""")


SVmediumVPCoord_sgsg =  grammar.CFG.fromstring("""
    % start CS
    CS -> S KON FV_sg_3_2 '.'
    S -> NP_sg FV_sg_3_1
    
    NP_sg -> ART_sg_m NN_sg_m | ART_sg_f NN_sg_f
    ART_sg_m -> 'Der'
    NN_sg_m -> 'Autor' | 'Pilot' | 'Kunde' | 'Lehrer' | 'Senator'
    ART_sg_f -> 'Die'
    NN_sg_f -> 'Senatorin'|'Beraterin'| 'Frau'|'Polizistin'| 'Richterin'
    FV_sg_3_1 -> 'redet mit Dieter' | 'liest eine Zeitung' | 'spielt ein Brettspiel' | 'verfolgt das Fernsehprogramm'
    KON -> 'und'
    FV_sg_3_2 -> 'lacht'| 'liest' | 'lauscht'
""")

SVmediumVPCoord_sgpl =  grammar.CFG.fromstring("""
    % start CS
    CS -> S KON FV_sg_3_2 '.'
    S -> NP_sg FV_sg_3_1
    
    NP_sg -> ART_sg_m NN_sg_m | ART_sg_f NN_sg_f
    ART_sg_m -> 'Der'
    NN_sg_m -> 'Autor' | 'Pilot' | 'Kunde' | 'Lehrer' | 'Senator'
    ART_sg_f -> 'Die'
    NN_sg_f -> 'Senatorin'|'Beraterin'| 'Frau'|'Polizistin'| 'Richterin'
    FV_sg_3_1 -> 'redet mit Menschen' | 'liest viele Zeitungen' | 'spielt gerne Brettspiele' | 'verfolgt die Fernsehprogramme'
    KON -> 'und'
    FV_sg_3_2 -> 'lacht'| 'liest' | 'lauscht'
""")

SVmediumVPCoord_plpl =  grammar.CFG.fromstring("""
    % start CS
    CS -> S KON FV_pl_3_2 '.'
    S -> NP_pl FV_pl_3_1
    
    NP_pl -> ART_pl_m NN_pl_m
    ART_pl_m -> 'Die'
    NN_pl_m -> 'Autoren' | 'Piloten' | 'Kunden' | 'Lehrer'  | 'Senatorinnen' | 'Beraterinnen' |'Frauen' | 'Polizistinnen' | 'Richterinnen' |  'Kinder'
    FV_pl_3_1 -> 'reden mit Menschen' | 'lesen viele Zeitungen' | 'spielen gerne Brettspiele' | 'verfolgen die Fernsehprogramme'
    KON -> 'und'
    FV_pl_3_2 -> 'lachen'| 'lesen' | 'lauschen'

""")

SVmediumVPCoord_plsg =  grammar.CFG.fromstring("""
    % start CS
    CS -> S KON FV_pl_3_2 '.'
    S -> NP_pl FV_pl_3_1
    
    NP_pl -> ART_pl_m NN_pl_m
    ART_pl_m -> 'Die'
    NN_pl_m -> 'Autoren' | 'Piloten' | 'Kunden' | 'Lehrer'  | 'Senatorinnen' | 'Beraterinnen' |'Frauen' | 'Polizistinnen' | 'Richterinnen' |  'Kinder'
    FV_pl_3_1 -> 'reden mit Dieter' | 'lesen eine Zeitung' | 'spielen ein Brettspiel' | 'verfolgen das Fernsehprogramm'
    KON -> 'und'
    FV_pl_3_2 -> 'lachen'| 'lesen' | 'lauschen'

""")


jsn_SVshortVPCoord = {}
def json_SVshortVPCoord(case, number):
    path = './input/SVshortVPCoord/'
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        print('{} already exists.'.format(path))
    for sentence in generate(case):
        jsn_SVshortVPCoord['text'] = ' '.join(sentence)
        sentence2 = sentence[:]
        sentence2[-2] = '[MASK]'
        jsn_SVshortVPCoord['text_masked'] = ' '.join(sentence2)
        # try-except neccesary because of bug in pattern.de library
        try:
            wrong_num = conjugate(sentence[-2], PRESENT, 3, number)
        except:
            wrong_num = conjugate(sentence[-2], PRESENT, 3, number)
        candidates = []
        candidates.append(sentence[-2])
        candidates.append(wrong_num)
        jsn_SVshortVPCoord['candidates'] = candidates
        jsn_SVshortVPCoord['indexMASK'] = -2
        if case == SVshortVPCoord_sg:
            jsn_SVshortVPCoord['case'] = "SVshortVPCoord_sg"
            dump_jsonl(jsn_SVshortVPCoord, path+'/SVshortVPCoord_sg.jsonl', append = True)
        elif case == SVshortVPCoord_pl:
            jsn_SVshortVPCoord['case'] = "SVshortVPCoord_pl"
            dump_jsonl(jsn_SVshortVPCoord, path+'/SVshortVPCoord_pl.jsonl', append = True)
            
jsn_SVmediumVPCoord = {}
def json_SVmediumVPCoord(case, number):
    path = './input/SVmediumVPCoord/'
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        print('{} already exists.'.format(path))
    for sentence in generate(case):
        jsn_SVmediumVPCoord['text'] = ' '.join(sentence)
        sentence2 = sentence[:]
        sentence2[-2] = '[MASK]'
        jsn_SVmediumVPCoord['text_masked'] = ' '.join(sentence2)
        try:
            wrong_num = conjugate(sentence[-2], PRESENT, 3, number)
        except:
            wrong_num = conjugate(sentence[-2], PRESENT, 3, number)
        candidates = []
        candidates.append(sentence[-2])
        candidates.append(wrong_num)
        jsn_SVmediumVPCoord['candidates'] = candidates
        jsn_SVmediumVPCoord['indexMASK'] = -2
        if case == SVmediumVPCoord_sgsg:
            jsn_SVmediumVPCoord['case'] = "SVmediumVPCoord_sgsg"
            dump_jsonl(jsn_SVshortVPCoord, path+'/SVmediumVPCoord_sgsg.jsonl', append = True)
        elif case == SVmediumVPCoord_plpl:
            jsn_SVmediumVPCoord['case'] = "SVmediumVPCoord_plpl"
            dump_jsonl(jsn_SVshortVPCoord, path+'/SVmediumVPCoord_plpl.jsonl', append = True)
        elif case == SVmediumVPCoord_sgpl:
            jsn_SVmediumVPCoord['case'] = "SVmediumVPCoord_sgpl"
            dump_jsonl(jsn_SVshortVPCoord, path+'/SVmediumVPCoord_sgpl.jsonl', append = True)
        elif case == SVmediumVPCoord_plsg:
            jsn_SVmediumVPCoord['case'] = "SVmediumVPCoord_plsg"
            dump_jsonl(jsn_SVmediumVPCoord, path+'/SVmediumVPCoord_plsg.jsonl', append = True)
        

# ---------- 1.4. Long VP coordination: Der Manager redet mit Dieter und *verfolgt das Fernsehprogramm.

SVlongVPCoord_sgsg1 =  grammar.CFG.fromstring("""
    % start CS
    CS -> S1 KON S2 '.'
    S1 -> NP_sg VP_sg_long
    NP_sg -> ART_sg_m NN_sg_m | ART_sg_f NN_sg_f
    ART_sg_m -> 'Der'
    NN_sg_m -> 'Autor' | 'Pilot' | 'Kunde' | 'Lehrer' | 'Senator'
    ART_sg_f -> 'Die'
    NN_sg_f -> 'Senatorin'|'Beraterin'| 'Frau'|'Polizistin'| 'Richterin'
    VP_sg_long -> 'redet mit Dieter' | 'liest eine Zeitung' | 'spielt ein Brettspiel'
    
    KON -> 'und'
    
    S2 -> FV_sg NP_acc
    FV_sg -> 'verfolgt'
    NP_acc -> 'das Fernsehprogramm'
""")

SVlongVPCoord_sgsg2 =  grammar.CFG.fromstring("""
    % start CS
    CS -> S1 KON S2 '.'
    S1 -> NP_sg VP_sg_long
    NP_sg -> ART_sg_m NN_sg_m | ART_sg_f NN_sg_f
    ART_sg_m -> 'Der'
    NN_sg_m -> 'Autor' | 'Pilot' | 'Kunde' | 'Lehrer' | 'Senator'
    ART_sg_f -> 'Die'
    NN_sg_f -> 'Senatorin'|'Beraterin'| 'Frau'|'Polizistin'| 'Richterin'
    VP_sg_long ->  'liest eine Zeitung' | 'spielt ein Brettspiel'   | 'verfolgt das Fernsehprogramm'
    KON -> 'und'
    
    S2 -> FV_sg NP_acc
    FV_sg -> 'redet'
    NP_acc -> 'mit Dieter'
""")


SVlongVPCoord_sgsg3 =  grammar.CFG.fromstring("""
    % start CS
    CS -> S1 KON S2 '.'
    S1 -> NP_sg VP_sg_long
    NP_sg -> ART_sg_m NN_sg_m | ART_sg_f NN_sg_f
    ART_sg_m -> 'Der'
    NN_sg_m -> 'Autor' | 'Pilot' | 'Kunde' | 'Lehrer' | 'Senator'
    ART_sg_f -> 'Die'
    NN_sg_f -> 'Senatorin'|'Beraterin'| 'Frau'|'Polizistin'| 'Richterin'
    VP_sg_long ->'spielt heute ein Brettspiel'   | 'verfolgt das Fernsehprogramm'  | 'redet mit Dieter'
    KON -> 'und'
    
    S2 -> FV_sg NP_acc
    FV_sg -> 'liest'
    NP_acc -> 'eine Zeitung'
""")

SVlongVPCoord_sgsg4 =  grammar.CFG.fromstring("""
    % start CS
    CS -> S1 KON S2 '.'
    S1 -> NP_sg VP_sg_long
    NP_sg -> ART_sg_m NN_sg_m | ART_sg_f NN_sg_f
    ART_sg_m -> 'Der'
    NN_sg_m -> 'Autor' | 'Pilot' | 'Kunde' | 'Lehrer' | 'Senator'
    ART_sg_f -> 'Die'
    NN_sg_f -> 'Senatorin'|'Beraterin'| 'Frau'|'Polizistin'| 'Richterin'
    VP_sg_long -> 'verfolgt das Fernsehprogramm'  | 'redet mit Dieter'  | 'liest eine Zeitung'
    KON -> 'und'
    
    S2 -> FV_sg NP_acc
    FV_sg -> 'spielt'
    NP_acc -> 'ein Brettspiel'
""")

SVlongVPCoord_sgpl1 =  grammar.CFG.fromstring("""
    % start CS
    CS -> S1 KON S2 '.'
    S1 -> NP_sg VP_sg_long
    NP_sg -> ART_sg_m NN_sg_m | ART_sg_f NN_sg_f
    ART_sg_m -> 'Der'
    NN_sg_m -> 'Autor' | 'Pilot' | 'Kunde' | 'Lehrer' | 'Senator'
    ART_sg_f -> 'Die'
    NN_sg_f -> 'Senatorin' | 'Beraterin' | 'Frau' | 'Polizistin' | 'Richterin'
    VP_sg_long -> 'redet mit Menschen' | 'liest viele Zeitungen' | 'spielt gerne Brettspiele'
    
    KON -> 'und'
    
    S2 -> FV_sg NP_acc
    FV_sg -> 'verfolgt'
    NP_acc -> 'die Fernsehprogramme'
""")

SVlongVPCoord_sgpl2 =  grammar.CFG.fromstring("""
    % start CS
    CS -> S1 KON S2 '.'
    S1 -> NP_sg VP_sg_long
    NP_sg -> ART_sg_m NN_sg_m | ART_sg_f NN_sg_f
    ART_sg_m -> 'Der'
    NN_sg_m -> 'Autor' | 'Pilot' | 'Kunde' | 'Lehrer' | 'Senator'
    ART_sg_f -> 'Die'
    NN_sg_f -> 'Senatorin'|'Beraterin'| 'Frau'|'Polizistin'| 'Richterin'
    VP_sg_long ->  'liest viele Zeitungen' | 'spielt gerne Brettspiele'   | 'verfolgt die Fernsehprogramme'
    KON -> 'und'
    
    S2 -> FV_sg NP_acc
    FV_sg -> 'redet'
    NP_acc -> 'mit Menschen'
""")


SVlongVPCoord_sgpl3 =  grammar.CFG.fromstring("""
    % start CS
    CS -> S1 KON S2 '.'
    S1 -> NP_sg VP_sg_long
    NP_sg -> ART_sg_m NN_sg_m | ART_sg_f NN_sg_f
    ART_sg_m -> 'Der'
    NN_sg_m -> 'Autor' | 'Pilot' | 'Kunde' | 'Lehrer' | 'Senator'
    ART_sg_f -> 'Die'
    NN_sg_f -> 'Senatorin'|'Beraterin'| 'Frau'|'Polizistin'| 'Richterin'
    VP_sg_long ->'spielt gerne Brettspiele'   | 'verfolgt die Fernsehprogramme'  | 'redet mit Menschen'
    KON -> 'und'
    
    S2 -> FV_sg NP_acc
    FV_sg -> 'liest'
    NP_acc -> 'viele Zeitungen'
""")

SVlongVPCoord_sgpl4 =  grammar.CFG.fromstring("""
    % start CS
    CS -> S1 KON S2 '.'
    S1 -> NP_sg VP_sg_long
    NP_sg -> ART_sg_m NN_sg_m | ART_sg_f NN_sg_f
    ART_sg_m -> 'Der'
    NN_sg_m -> 'Autor' | 'Pilot' | 'Kunde' | 'Lehrer' | 'Senator'
    ART_sg_f -> 'Die'
    NN_sg_f -> 'Senatorin'|'Beraterin'| 'Frau'|'Polizistin'| 'Richterin'
    VP_sg_long -> 'liest viele Zeitungen'  | 'verfolgt die Fernsehprogramme'  | 'redet mit Menschen'
    KON -> 'und'
    
    S2 -> FV_sg NP_acc
    FV_sg -> 'spielt'
    NP_acc -> 'gerne Brettspiele'
""")




SVlongVPCoord_plpl1 =  grammar.CFG.fromstring("""
    % start CS
    CS -> S1 KON S2 '.'
    S1 -> NP_pl VP_pl_long
    NP_pl -> ART_pl NN_pl
    ART_pl -> 'Die'
    NN_pl ->  'Autoren' | 'Piloten' | 'Kunden' | 'Lehrer'  | 'Senatorinnen' | 'Beraterinnen' |'Frauen' | 'Polizistinnen' | 'Richterinnen' |  'Kinder'
    VP_pl_long -> 'reden mit Menschen' | 'lesen viele Zeitungen' | 'spielen gerne Brettspiele'
    
    KON -> 'und'
    
    S2 -> FV_pl NP_acc
    FV_pl -> 'verfolgen'
    NP_acc -> 'die Fernsehprogramme'
""")

SVlongVPCoord_plpl2 =  grammar.CFG.fromstring("""
    % start CS
    CS -> S1 KON S2 '.'
    S1 -> NP_pl VP_pl_long
    NP_pl -> ART_pl NN_pl
    ART_pl -> 'Die'
    NN_pl ->  'Autoren' | 'Piloten' | 'Kunden' | 'Lehrer'  | 'Senatorinnen' | 'Beraterinnen' |'Frauen' | 'Polizistinnen' | 'Richterinnen' |  'Kinder'
    VP_pl_long ->  'lesen viele Zeitungen' | 'spielen gerne Brettspiele' | 'verfolgen die Fernsehprogramme'
    
    KON -> 'und'
    
    S2 -> FV_pl NP_acc
    FV_pl -> 'reden'
    NP_acc -> 'mit Menschen'
""")


SVlongVPCoord_plpl3 =  grammar.CFG.fromstring("""
    % start CS
    CS -> S1 KON S2 '.'
    S1 -> NP_pl VP_pl_long
    NP_pl -> ART_pl NN_pl
    ART_pl -> 'Die'
    NN_pl ->  'Autoren' | 'Piloten' | 'Kunden' | 'Lehrer'  | 'Senatorinnen' | 'Beraterinnen' |'Frauen' | 'Polizistinnen' | 'Richterinnen' |  'Kinder'
    VP_pl_long -> 'verfolgen die Fernsehprogramme' | 'reden mit Menschen' |  'lesen viele Zeitungen'
    KON -> 'und'
    
    S2 -> FV_pl NP_acc
    FV_pl -> 'spielen'
    NP_acc -> 'gerne Brettspiele'
""")

SVlongVPCoord_plpl4 =  grammar.CFG.fromstring("""
    % start CS
    CS -> S1 KON S2 '.'
    S1 -> NP_pl VP_pl_long
    NP_pl -> ART_pl NN_pl
    ART_pl -> 'Die'
    NN_pl ->  'Autoren' | 'Piloten' | 'Kunden' | 'Lehrer'  | 'Senatorinnen' | 'Beraterinnen' |'Frauen' | 'Polizistinnen' | 'Richterinnen' |  'Kinder'
    VP_pl_long -> 'verfolgen die Fernsehprogramme' | 'reden mit Menschen' |  'spielen gerne Brettspiele'
    KON -> 'und'
    
    S2 -> FV_pl NP_acc
    FV_pl -> 'lesen'
    NP_acc -> 'viele Zeitungen'
""")

SVlongVPCoord_plsg1 =  grammar.CFG.fromstring("""
    % start CS
    CS -> S1 KON S2 '.'
    S1 -> NP_pl VP_pl_long
    NP_pl -> ART_pl NN_pl
    ART_pl -> 'Die'
    NN_pl ->  'Autoren' | 'Piloten' | 'Kunden' | 'Lehrer'  | 'Senatorinnen' | 'Beraterinnen' |'Frauen' | 'Polizistinnen' | 'Richterinnen' |  'Kinder'
    VP_pl_long -> 'reden mit Dieter' | 'lesen eine Zeitung' | 'spielen ein Brettspiel'
    
    KON -> 'und'
    
    S2 -> FV_pl NP_acc
    FV_pl -> 'verfolgen'
    NP_acc -> 'das Fernsehprogramm'
""")

SVlongVPCoord_plsg2 =  grammar.CFG.fromstring("""
    % start CS
    CS -> S1 KON S2 '.'
    S1 -> NP_pl VP_pl_long
    NP_pl -> ART_pl NN_pl
    ART_pl -> 'Die'
    NN_pl ->  'Autoren' | 'Piloten' | 'Kunden' | 'Lehrer'  | 'Senatorinnen' | 'Beraterinnen' |'Frauen' | 'Polizistinnen' | 'Richterinnen' |  'Kinder'
    VP_pl_long ->  'lesen eine Zeitung' | 'spielen ein Brettspiel' | 'verfolgen das Fernsehprogramm'
    
    KON -> 'und'
    
    S2 -> FV_pl NP_acc
    FV_pl -> 'reden'
    NP_acc -> 'mit Dieter'
""")


SVlongVPCoord_plsg3 =  grammar.CFG.fromstring("""
    % start CS
    CS -> S1 KON S2 '.'
    S1 -> NP_pl VP_pl_long
    NP_pl -> ART_pl NN_pl
    ART_pl -> 'Die'
    NN_pl ->  'Autoren' | 'Piloten' | 'Kunden' | 'Lehrer'  | 'Senatorinnen' | 'Beraterinnen' |'Frauen' | 'Polizistinnen' | 'Richterinnen' |  'Kinder'
    VP_pl_long -> 'verfolgen das Fernsehprogramm' | 'reden mit Dieter' |  'lesen eine Zeitung'
    KON -> 'und'
    
    S2 -> FV_pl NP_acc
    FV_pl -> 'spielen'
    NP_acc -> 'ein Brettspiel'
""")

SVlongVPCoord_plsg4 =  grammar.CFG.fromstring("""
    % start CS
    CS -> S1 KON S2 '.'
    S1 -> NP_pl VP_pl_long
    NP_pl -> ART_pl NN_pl
    ART_pl -> 'Die'
    NN_pl ->  'Autoren' | 'Piloten' | 'Kunden' | 'Lehrer'  | 'Senatorinnen' | 'Beraterinnen' |'Frauen' | 'Polizistinnen' | 'Richterinnen' |  'Kinder'
    VP_pl_long -> 'verfolgen das Fernsehprogramm' | 'reden mit Dieter' |  'spielen ein Brettspiel'
    KON -> 'und'
    
    S2 -> FV_pl NP_acc
    FV_pl -> 'lesen'
    NP_acc -> 'eine Zeitung'
""")


jsn_SVlongVPCoord = {}
def json_SVlongVPCoord(case, number):
    '''generates jsonl file with examples.
    case defines the grammar used to create the sentences. number (=SG or PL) is the 'wrong' (e.g. not congruent to subject) number of the tested'''

    path = './input/SVlongVPCoord'
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        print('{} already exists.'.format(path))
        
    for sentence in generate(case):
        jsn_SVlongVPCoord['text'] = ' '.join(sentence)
        sentence2 = sentence[:]
        sentence2[-3] = '[MASK]'
        jsn_SVlongVPCoord['text_masked'] = ' '.join(sentence2)
        # try-except neccesary because of bug in pattern.de library
        try:
            wrong_num = conjugate(sentence[-3], PRESENT, 3, number)
        except:
            wrong_num = conjugate(sentence[-3], PRESENT, 3, number)
        candidates = []
        candidates.append(sentence[-3])
        candidates.append(wrong_num)
        jsn_SVlongVPCoord['candidates'] = candidates
        jsn_SVlongVPCoord['indexMASK'] = 8

        if case == SVlongVPCoord_sgsg1 or case == SVlongVPCoord_sgsg2 or case == SVlongVPCoord_sgsg3 or case == SVlongVPCoord_sgsg4:
            jsn_SVlongVPCoord['case'] = "SVlongVPCoord_sgsg"
            dump_jsonl(jsn_SVlongVPCoord, path+'/SVlongVPCoord_sgsg.jsonl', append = True)
        elif case == SVlongVPCoord_plpl1 or case == SVlongVPCoord_plpl2 or case == SVlongVPCoord_plpl3 or case == SVlongVPCoord_plpl4:
            jsn_SVlongVPCoord['case'] = "SVlongVPCoord_plpl"
            dump_jsonl(jsn_SVlongVPCoord, path+'/SVlongVPCoord_plpl.jsonl', append = True)
        elif case == SVlongVPCoord_sgpl1 or case == SVlongVPCoord_sgpl2 or case == SVlongVPCoord_sgpl3 or case == SVlongVPCoord_sgpl4:
            jsn_SVlongVPCoord['case'] = "SVlongVPCoord_sgpl"
            dump_jsonl(jsn_SVlongVPCoord, path+'/SVlongVPCoord_sgpl.jsonl', append = True)
        elif case == SVlongVPCoord_plsg1 or case == SVlongVPCoord_plsg2 or case == SVlongVPCoord_plsg3 or case == SVlongVPCoord_plsg4:
            jsn_SVlongVPCoord['case'] = "SVlongVPCoord_plsg"
            dump_jsonl(jsn_SVlongVPCoord, path+'/SVlongVPCoord_plsg.jsonl', append = True)

# ---------- 1.5. S-V-Agreement across a prepositional phrase: Der Autor neben dem Landstrich *lacht.

SVPP_sgsg =  grammar.CFG.fromstring("""
    % start S
    S -> NP_sg FV_sg_3 '.'
    NP_sg -> ART_sg_m NN_sg_m PP_sg_dat | ART_sg_f NN_sg_f PP_sg_dat
    ART_sg_m -> 'Der'
    NN_sg_m -> 'Autor' | 'Pilot' | 'Kunde' | 'Lehrer' | 'Senator'
    ART_sg_f -> 'Die'
    NN_sg_f -> 'Senatorin' | 'Beraterin' |'Frau' | 'Polizistin' | 'Richterin'

    PP_sg_dat -> APPR_dat ART_sg_m_dat NN_sg_m_dat | APPR_dat ART_sg_f_dat NN_sg_f_dat
    APPR_dat -> 'neben'| 'hinter' | 'vor'

    ART_sg_m_dat -> 'dem'
    NN_sg_m_dat -> 'Landstrich'|'Assistenten'|'Architekten'
    ART_sg_f_dat -> 'der'
    NN_sg_f_dat -> 'Ministerin' | 'Fahrradfahrerin' | 'Wiese'
    FV_sg_3 -> 'lacht' | 'schwimmt' |  'redet'| 'bleibt' | 'trinkt'
""")

SVPP_plpl =  grammar.CFG.fromstring("""
    % start S
    S -> NP_pl FV_pl_3 '.'
    NP_pl -> ART_pl NN_pl PP_pl_dat
    ART_pl -> 'Die'
    NN_pl -> 'Autoren' | 'Piloten' | 'Kunden' | 'Lehrer'  | 'Senatorinnen' | 'Beraterinnen' |'Frauen' | 'Polizistinnen' | 'Richterinnen' |  'Kinder'
    PP_pl_dat -> APPR_dat ART_pl_dat NN_pl_dat
    
    APPR_dat -> 'neben'| 'hinter' | 'vor'
    ART_pl_dat -> 'den'
    NN_pl_dat -> 'Landstrichen'|'Assistenten'|'Architekten'| 'Ministerinnen' | 'Fahrradfahrerinnen' | 'Wiesen'
 
    FV_pl_3 -> 'lachen' | 'schwimmen' |  'reden'| 'bleiben' | 'trinken'
""")

SVPP_sgpl =  grammar.CFG.fromstring("""
    % start S
    S -> NP_sg FV_sg_3 '.'
    NP_sg -> ART_sg_m NN_sg_m PP_pl_dat | ART_sg_f NN_sg_f PP_pl_dat
    ART_sg_m -> 'Der'
    NN_sg_m -> 'Autor' | 'Pilot' | 'Kunde' | 'Lehrer' | 'Senator'
    ART_sg_f -> 'Die'
    NN_sg_f -> 'Senatorin' | 'Beraterin' |'Frau' | 'Polizistin' | 'Richterin'
    PP_pl_dat -> APPR_dat ART_pl_dat NN_pl_dat

    APPR_dat -> 'neben'| 'hinter' | 'vor'
    ART_pl_dat -> 'den'
    NN_pl_dat -> 'Landstrichen'|'Assistenten'|'Architekten'| 'Ministerinnen' | 'Fahrradfahrerinnen' | 'Wiesen'

    FV_sg_3 -> 'lacht' | 'schwimmt' |  'redet'| 'bleibt' | 'trinkt'
""")


SVPP_plsg =  grammar.CFG.fromstring("""
    % start S
    S -> NP_pl FV_pl_3 '.'
    NP_pl -> ART_pl NN_pl PP_sg_dat
    ART_pl -> 'Die'
    NN_pl -> 'Autoren' | 'Piloten' | 'Kunden' | 'Lehrer'  | 'Senatorinnen' | 'Beraterinnen' |'Frauen' | 'Polizistinnen' | 'Richterinnen' |  'Kinder'

    PP_sg_dat -> APPR_dat ART_sg_m_dat NN_sg_m_dat | APPR_dat ART_sg_f_dat NN_sg_f_dat
    APPR_dat -> 'neben'| 'hinter' | 'vor'

    ART_sg_m_dat -> 'dem'
    NN_sg_m_dat -> 'Landstrich'|'Assistenten'|'Architekten'
    ART_sg_f_dat -> 'der'
    NN_sg_f_dat -> 'Ministerin' | 'Fahrradfahrerin' | 'Wiese'
    FV_pl_3 -> 'lachen' | 'schwimmen' |  'reden'| 'bleiben' | 'trinken'
""")



jsn_SVPP = {}
def json_SVPP(case, number):
    '''generates jsonl file with examples.
    case defines the grammar used to create the sentences. number (=SG or PL) is the 'wrong' (e.g. not congruent to subject) number of the tested'''
    path = './input/SVPP'
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        print('{} already exists.'.format(path))
        
    for sentence in generate(case):
        jsn_SVPP['text'] = ' '.join(sentence)
        sentence2 = sentence[:]
        sentence2[-2] = '[MASK]'
        jsn_SVPP['text_masked'] = ' '.join(sentence2)
        # try-except neccesary because of bug in pattern.de library
        try:
            wrong_num = conjugate(sentence[-2], PRESENT, 3, number)
        except:
            wrong_num = conjugate(sentence[-2], PRESENT, 3, number)
        candidates = []
        candidates.append(sentence[-2])
        candidates.append(wrong_num)
        jsn_SVPP['candidates'] = candidates
        jsn_SVPP['indexMASK'] = -2
        jsn_SVPP['case'] = 'SVPP'
        if case == SVPP_sgsg:
            jsn_SVPP['case'] = "SVPP_sgsg"
            dump_jsonl(jsn_SVPP, path+'/SVPP_sgsg.jsonl', append = True)
        elif case == SVPP_plpl:
            jsn_SVPP['case'] = "SVPP_plpl"
            dump_jsonl(jsn_SVPP, path+'/SVPP_plpl.jsonl', append = True)
        elif case == SVPP_sgpl:
            jsn_SVPP['case'] = "SVPP_sgpl"
            dump_jsonl(jsn_SVPP, path+'/SVPP_sgpl.jsonl', append = True)
        elif case == SVPP_plsg:
            jsn_SVPP['case'] = "SVPP_plsg"
            dump_jsonl(jsn_SVPP, path+'/SVPP_plsg.jsonl', append = True)
    



# ---------- 1.6. SV-Agreement across a subject relative clause: Der Autor, der den Architekten liebt, *lacht.

SVSubjRelC_sgsg =  grammar.CFG.fromstring("""
    % start S
    S -> NP_sg ',' FV_sg_3 '.' | NP_sg_f ',' FV_sg_3 '.'
    NP_sg  -> ART_sg_m  NN_sg_m  ',' SRC_sg_m_acc | ART_sg_f  NN_sg_f  ',' SRC_sg_f_acc

    ART_sg_m -> 'Der'
    NN_sg_m -> 'Autor' | 'Pilot' | 'Kunde' | 'Lehrer' | 'Senator'
    ART_sg_f -> 'Die'
    NN_sg_f -> 'Senatorin' | 'Beraterin' |'Frau' | 'Polizistin' | 'Richterin'
    
    SRC_sg_m_acc -> PRELS_sg_m NP_sg_acc FV_sg_3_acc
    SRC_sg_f_acc -> PRELS_sg_f NP_sg_acc FV_sg_3_acc
    PRELS_sg_m -> 'der'
    PRELS_sg_f -> 'die'
    NP_sg_acc -> ART_sg_acc NN_sg_acc
    ART_sg_acc -> 'den'
    NN_sg_acc -> 'Architekten'| 'Assistenten' | 'Landstrich'
    FV_sg_3_acc -> 'liebt'| 'bewundert'| 'sieht'|'kennt'
    FV_sg_3 ->  'lacht' | 'schwimmt' |  'redet'| 'bleibt' | 'trinkt'
    
""")

SVSubjRelC_plpl =  grammar.CFG.fromstring("""
    % start S
    S -> NP_pl ',' FV_pl_3 '.'
    
    NP_pl -> ART_pl NN_pl ',' SRC_pl_acc
    ART_pl -> 'Die'
    NN_pl -> 'Autoren' | 'Piloten' | 'Kunden' | 'Lehrer'  | 'Senatorinnen' | 'Beraterinnen' |'Frauen' | 'Polizistinnen' | 'Richterinnen' |  'Kinder'
    SRC_pl_acc -> PRELS_pl NP_pl_acc FV_pl_3_acc
    PRELS_pl -> 'die'
    NP_pl_acc -> ART_pl_acc NN_pl_acc
    ART_pl_acc -> 'die'
    NN_pl_acc -> 'Architekten'| 'Assistenten' | 'Landstriche'
    FV_pl_3_acc -> 'lieben'| 'bewundern'| 'sehen'|'kennen'
    FV_pl_3 ->  'lachen' | 'schwimmen' |  'reden'| 'bleiben' | 'trinken'
    
""")

SVSubjRelC_sgpl =  grammar.CFG.fromstring("""
    % start S
    S -> NP_sg ',' FV_sg_3 '.'
    NP_sg  -> ART_sg_m  NN_sg_m  ',' SRC_m_pl_acc | ART_sg_f  NN_sg_f  ',' SRC_f_pl_acc

    ART_sg_m -> 'Der'
    NN_sg_m -> 'Autor' | 'Pilot' | 'Kunde' | 'Lehrer' | 'Senator'
    ART_sg_f -> 'Die'
    NN_sg_f -> 'Senatorin' | 'Beraterin' |'Frau' | 'Polizistin' | 'Richterin'
    
    SRC_m_pl_acc -> PRELS_sg_m NP_pl_acc FV_sg_3_acc
    SRC_f_pl_acc -> PRELS_sg_f NP_pl_acc FV_sg_3_acc
    PRELS_sg_m -> 'der'
    PRELS_sg_f -> 'die'
    NP_pl_acc -> ART_pl_acc NN_pl_acc
    ART_pl_acc -> 'die'
    NN_pl_acc ->  'Architekten'| 'Assistenten' | 'Landstriche'
    FV_sg_3_acc -> 'liebt'| 'bewundert'| 'sieht'|'kennt'
    FV_sg_3 ->   'lacht' | 'schwimmt' |  'redet'| 'bleibt' | 'trinkt'
    
""")

SVSubjRelC_plsg =  grammar.CFG.fromstring("""
    % start S
    S -> NP_pl ',' FV_pl_3 '.'
    
    NP_pl -> ART_pl NN_pl ',' SRC_pl_acc
    ART_pl -> 'Die'
    NN_pl -> 'Autoren' | 'Piloten' | 'Kunden' | 'Lehrer'  | 'Senatorinnen' | 'Beraterinnen' |'Frauen' | 'Polizistinnen' | 'Richterinnen' |  'Kinder'
    SRC_pl_acc -> PRELS_pl NP_sg_acc FV_pl_3_acc
    PRELS_pl -> 'die'
    NP_sg_acc -> ART_sg_acc NN_sg_acc
    ART_sg_acc -> 'den'
    NN_sg_acc -> 'Architekten'| 'Assistenten' | 'Landstrich'
    FV_pl_3_acc -> 'lieben'| 'bewundern'| 'sehen'|'kennen'
    FV_pl_3 ->   'lachen' | 'schwimmen' |  'reden'| 'bleiben' | 'trinken'
    
""")




jsn_SVSubjRelC = {}
def json_SVSubjRelC(case, number):
    path = './input/SVSubjRelC'
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        print('{} already exists.'.format(path))
        
    for sentence in generate(case):
        jsn_SVSubjRelC['text'] = ' '.join(sentence)
        sentence2 = sentence[:]
        sentence2[-2] = '[MASK]'
        jsn_SVSubjRelC['text_masked'] = ' '.join(sentence2)
        # try-except neccesary because of bug in pattern.de library
        try:
            wrong_num = conjugate(sentence[-2], PRESENT, 3, number)
        except:
            wrong_num = conjugate(sentence[-2], PRESENT, 3, number)
        candidates = []
        candidates.append(sentence[-2])
        candidates.append(wrong_num)
        jsn_SVSubjRelC['candidates'] = candidates
        jsn_SVSubjRelC['indexMASK'] = -2
        jsn_SVSubjRelC['case'] = 'SVSubjRelC'
        if case == SVSubjRelC_sgsg:
            jsn_SVSubjRelC['case'] = "SVSubjRelC_sgsg"
            dump_jsonl(jsn_SVSubjRelC, path+'/SVSubjRelC_sgsg.jsonl', append = True)
        elif case == SVSubjRelC_plpl:
            jsn_SVSubjRelC['case'] = "SVSubjRelC_plpl"
            dump_jsonl(jsn_SVSubjRelC, path+'/SVSubjRelC_plpl.jsonl', append = True)
        elif case == SVSubjRelC_sgpl:
            jsn_SVSubjRelC['case'] = "SVSubjRelC_sgpl"
            dump_jsonl(jsn_SVSubjRelC, path+'/SVSubjRelC_sgpl.jsonl', append = True)
        elif case == SVSubjRelC_plsg:
            jsn_SVSubjRelC['case'] = "SVSubjRelC_plsg"
            dump_jsonl(jsn_SVSubjRelC, path+'/SVSubjRelC_plsg.jsonl', append = True)



# ---------- 1.7. Agreement across and inside object relative clauses: Der Autor, den der Vertreter kennt, *lacht. // Der Autor, den der Vertreter *kennt, lacht.

SVObjRelC_sgsg =  grammar.CFG.fromstring("""
    % start S
    S -> NP_sg_m ',' FV_sg_3 '.' | NP_sg_f ',' FV_sg_3 '.'

    NP_sg_m -> ART_sg_m NN_sg_m ',' ORC_sg_m
    NP_sg_f -> ART_sg_f NN_sg_f ',' ORC_sg_f
    
    ART_sg_m -> 'Der'
    NN_sg_m -> 'Autor' | 'Pilot' | 'Kunde' | 'Lehrer' | 'Senator'
    ART_sg_f -> 'Die'
    NN_sg_f -> 'Senatorin' | 'Beraterin' |'Frau' | 'Polizistin' | 'Richterin'
    
    ORC_sg_m -> PRELS_sg_m_acc NP_sg_m_nom FV_sg_3_acc
    ORC_sg_f -> PRELS_sg_f_acc NP_sg_m_nom FV_sg_3_acc

    PRELS_sg_m_acc -> 'den'
    PRELS_sg_f_acc -> 'die'
    
    NP_sg_m_nom -> ART_sg_m_nom NN_sg_m_nom
    ART_sg_m_nom -> 'der'
    NN_sg_m_nom -> 'Vertreter' | 'Arbeiter' | 'Politiker'
    FV_sg_3_acc -> 'kennt'|'liebt'|'sieht'
    
    FV_sg_3 -> 'lacht' | 'schwimmt' |  'redet'| 'bleibt' | 'trinkt'
""")

SVObjRelC_plpl =  grammar.CFG.fromstring("""
    % start S
    S -> NP_pl ',' FV_pl_3 '.'
    NP_pl -> ART_pl NN_pl ',' ORC_pl
    ART_pl -> 'Die'
    NN_pl -> 'Autoren' | 'Piloten' | 'Kunden' | 'Lehrer'  | 'Senatorinnen' | 'Beraterinnen' |'Frauen' | 'Polizistinnen' | 'Richterinnen' |  'Kinder'
    ORC_pl -> PRELS_pl_acc NP_pl_nom FV_pl_3_acc
    PRELS_pl_acc -> 'die'
    NP_pl_nom -> ART_pl_nom NN_pl_nom
    ART_pl_nom -> 'die'
    NN_pl_nom -> 'Vertreter' | 'Arbeiter' | 'Politiker'
    FV_pl_3_acc -> 'kennen'|'lieben'|'sehen'
    FV_pl_3 -> 'lachen' | 'schwimmen' |  'reden'| 'bleiben' | 'trinken'
""")


SVObjRelC_sgpl = grammar.CFG.fromstring("""
    % start S
    S -> NP_sg_m ',' FV_sg_3 '.' | NP_sg_f ',' FV_sg_3 '.'

    NP_sg_m -> ART_sg_m NN_sg_m ',' ORC_sg_m
    NP_sg_f -> ART_sg_f NN_sg_f ',' ORC_sg_f
    
    ART_sg_m -> 'Der'
    NN_sg_m -> 'Autor' | 'Pilot' | 'Kunde' | 'Lehrer' | 'Senator'
    ART_sg_f -> 'Die'
    NN_sg_f -> 'Senatorin' | 'Beraterin' |'Frau' | 'Polizistin' | 'Richterin'
    
    ORC_sg_m -> PRELS_sg_m_acc NP_pl_nom FV_pl_3_acc
    ORC_sg_f -> PRELS_sg_f_acc NP_PL_nom FV_pl_3_acc

    PRELS_sg_m_acc -> 'den'
    PRELS_sg_f_acc -> 'die'
    
    NP_pl_nom -> ART_pl_nom NN_pl_nom
    ART_pl_nom -> 'die'
    NN_pl_nom -> 'Vertreter' | 'Arbeiter' | 'Politiker'
    FV_pl_3_acc -> 'kennen'|'lieben'|'sehen'

    FV_sg_3 -> 'lacht' | 'schwimmt' |  'redet'| 'bleibt' | 'trinkt'
""")


SVObjRelC_plsg = grammar.CFG.fromstring("""
    % start S
    S -> NP_pl ',' FV_pl_3 '.'
    NP_pl -> ART_pl NN_pl ',' ORC_m
    ART_pl -> 'Die'
    NN_pl -> 'Autoren' | 'Piloten' | 'Kunden' | 'Lehrer'  | 'Senatorinnen' | 'Beraterinnen' |'Frauen' | 'Polizistinnen' | 'Richterinnen' | 'Kinder'
    ORC_m -> PRELS_pl_acc NP_sg_m_nom FV_sg_3_acc
    PRELS_pl_acc -> 'die'
    NP_sg_m_nom -> ART_sg_m NN_sg_m
    ART_sg_m -> 'der'
    NN_sg_m -> 'Vertreter' | 'Arbeiter' | 'Politiker'
 
    FV_sg_3_acc -> 'kennt'|'liebt'|'sieht'
    FV_pl_3 -> 'lachen' | 'schwimmen' |  'reden'| 'bleiben' | 'trinken'
""")



jsn_SVacrossObjRelC = {}
def json_SVacrossObjRelC(case, number):
    path = './input/SVacrossObjRelC'
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        print('{} already exists.'.format(path))
    for sentence in generate(case):
        jsn_SVacrossObjRelC['text'] = ' '.join(sentence)
        sentence2 = sentence[:]
        sentence2[-2] = '[MASK]'
        jsn_SVacrossObjRelC['text_masked'] = ' '.join(sentence2)
        # try-except neccesary because of bug in pattern.de library
        try:
            wrong_num = conjugate(sentence[-2], PRESENT, 3, number)
        except:
            wrong_num = conjugate(sentence[-2], PRESENT, 3, number)
        candidates = []
        candidates.append(sentence[-2])
        candidates.append(wrong_num)
        jsn_SVacrossObjRelC['candidates'] = candidates
        jsn_SVacrossObjRelC['indexMASK'] = -2
        if case == SVObjRelC_sgsg:
            jsn_SVacrossObjRelC['case'] = "SVacrossObjRelC_sgsg"
            dump_jsonl(jsn_SVacrossObjRelC, path+'/SVacrossObjRelC_sgsg.jsonl', append = True)
        elif case == SVObjRelC_plpl:
            jsn_SVacrossObjRelC['case'] = "SVacrossObjRelC_plpl"
            dump_jsonl(jsn_SVacrossObjRelC, path+'/SVacrossObjRelC_plpl.jsonl', append = True)
        elif case == SVObjRelC_sgpl:
            jsn_SVacrossObjRelC['case'] = "SVacrossObjRelC_sgpl"
            dump_jsonl(jsn_SVacrossObjRelC, path+'/SVacrossObjRelC_sgpl.jsonl', append = True)
        elif case == SVObjRelC_plsg:
            jsn_SVacrossObjRelC['case'] = "SVacrossObjRelC_plsg"
            dump_jsonl(jsn_SVacrossObjRelC, path+'/SVacrossObjRelC_plsg.jsonl', append = True)

        
    


jsn_SVinObjRelC = {}
def json_SVinObjRelC(case, number):
    path = './input/SVinObjRelC'
    if not os.path.exists(path):
        os.makedirs(path)
    for sentence in generate(case):
        jsn_SVinObjRelC['text'] = ' '.join(sentence)
        sentence2 = sentence[:]
        sentence2[6] = '[MASK]'
        jsn_SVinObjRelC['text_masked'] = ' '.join(sentence2)
        # try-except neccesary because of bug in pattern.de library
        try:
            wrong_num = conjugate(sentence[6], PRESENT, 3, number)
        except:
            wrong_num = conjugate(sentence[6], PRESENT, 3, number)
        candidates = []
        candidates.append(sentence[6])
        candidates.append(wrong_num)
        jsn_SVinObjRelC['candidates'] = candidates
        jsn_SVinObjRelC['indexMASK'] = 6

        if case == SVObjRelC_sgsg:
            jsn_SVinObjRelC['case'] = "SVinObjRelC_sgsg"
            dump_jsonl(jsn_SVinObjRelC, path+'/SVinObjRelC_sgsg.jsonl', append = True)
        elif case == SVObjRelC_plpl:
            jsn_SVinObjRelC['case'] = "SVinObjRelC_plpl"
            dump_jsonl(jsn_SVinObjRelC, path+'/SVinObjRelC_plpl.jsonl', append = True)
        elif case == SVObjRelC_sgpl:
            jsn_SVinObjRelC['case'] = "SVinObjRelC_sgpl"
            dump_jsonl(jsn_SVinObjRelC, path+'/SVinObjRelC_plsg.jsonl', append = True)
        elif case == SVObjRelC_plsg:
            jsn_SVinObjRelC['case'] = "SVinObjRelC_plsg"
            dump_jsonl(jsn_SVinObjRelC, path+'/SVinObjRelC_sgpl.jsonl', append = True)
        




# ---------- 2. Additional Case for German
# ---------- 2.1. Modifier and Extended Modifier: Der suchende Autor lacht. / Der die Pflanze liebende Autor lacht.

SVModifier_sg=grammar.CFG.fromstring("""
    % start S
    S -> NP FV_sg_3 '.'
    NP -> ART_sg_m AP NN_sg_m | ART_sg_f AP NN_sg_f
    ART_sg_m -> 'Der'
    ART_sg_f -> 'Die'
    AP -> 'suchende' | 'wartende' | 'lesende' | 'sich beeilende'

    NN_sg_m -> 'Autor' | 'Pilot' | 'Kunde' | 'Lehrer' | 'Senator'
    NN_sg_f ->'Senatorin' | 'Beraterin' |'Frau' | 'Polizistin' | 'Richterin'

    FV_sg_3 -> 'lacht' | 'schwimmt' |  'redet'| 'bleibt' | 'trinkt'
""")
SVModifier_pl = grammar.CFG.fromstring("""
    % start S
    S -> NP FV_pl_3 '.'
    NP -> ART_pl AP NN_pl
    ART_pl -> 'Die'
    AP -> 'suchenden' | 'wartenden' | 'lesenden' | 'sich beeilenden'

    NN_pl -> 'Autoren' | 'Piloten' | 'Kunden' | 'Lehrer'  | 'Senatorinnen' | 'Beraterinnen' |'Frauen' | 'Polizistinnen' | 'Richterinnen' | 'Kinder'

    FV_pl_3 -> 'lachen' | 'schwimmen' |  'reden'| 'bleiben' | 'trinken'
""")

SVextendedModifier_sgsg = grammar.CFG.fromstring("""
    % start S
    S -> NP FV_sg_3 '.'
    NP -> ART_sg_m AP NN_sg_m | ART_sg_f AP NN_sg_f
    ART_sg_m -> 'Der'
    ART_sg_f -> 'Die'
    AP -> 'die Pflanze liebende' | 'den Sportler bewundernde' | 'das winkende Kind sehende' | 'sich wegen des Hilferufs beeilende'

    NN_sg_m -> 'Autor' | 'Pilot' | 'Kunde' | 'Lehrer' | 'Senator'
    NN_sg_f ->'Senatorin' | 'Beraterin' |'Frau' | 'Polizistin' | 'Richterin'

    FV_sg_3 -> 'lacht' | 'schwimmt' |  'redet'| 'bleibt' | 'trinkt'
""")

SVextendedModifier_plpl = grammar.CFG.fromstring("""
    % start S
    S -> NP FV_pl_3 '.'
    NP -> ART_pl AP NN_pl
    ART_pl -> 'Die'
    AP -> 'die Pflanzen liebenden' | 'die Sportler bewundernden' | 'die winkenden Kinder sehenden' | 'sich wegen der Hilferufe beeilenden'

    NN_pl -> 'Autoren' | 'Piloten' | 'Kunden' | 'Lehrer'  | 'Senatorinnen' | 'Beraterinnen' |'Frauen' | 'Polizistinnen' | 'Richterinnen' | 'Kinder'

    FV_pl_3 -> 'lachen' | 'schwimmen' |  'reden'| 'bleiben' | 'trinken'
""")

SVextendedModifier_plsg = grammar.CFG.fromstring("""
    % start S
    S -> NP FV_pl_3 '.'
    NP -> ART_pl AP NN_pl
    ART_pl -> 'Die'
   AP -> 'die Pflanze liebenden' | 'den Sportler bewundernden' | 'die winkenden Kinder nicht sehenden' | 'sich wegen des Hilferufs beeilenden'

    NN_pl -> 'Autoren' | 'Piloten' | 'Kunden' | 'Lehrer'  | 'Senatorinnen' | 'Beraterinnen' |'Frauen' | 'Polizistinnen' | 'Richterinnen' | 'Kinder'

    FV_pl_3 -> 'lachen' | 'schwimmen' |  'reden'| 'bleiben' | 'trinken'
""")

SVextendedModifier_sgpl = grammar.CFG.fromstring("""
    % start S
    S -> NP FV_sg_3 '.'
    NP -> ART_sg_m AP NN_sg_m | ART_sg_f AP NN_sg_f
    ART_sg_m -> 'Der'
    ART_sg_f -> 'Die'
    AP -> 'die Pflanzen liebende' | 'die Sportler bewundernde' | 'die winkenden Kinder sehende' | 'sich wegen der Hilferufe beeilende'

    NN_sg_m -> 'Autor' | 'Pilot' | 'Kunde' | 'Lehrer' | 'Senator'
    NN_sg_f ->'Senatorin' | 'Beraterin' |'Frau' | 'Polizistin' | 'Richterin'

    FV_sg_3 -> 'lacht' | 'schwimmt' |  'redet'| 'bleibt' | 'trinkt'
""")

jsn_SVModifier = {}
def json_SVModifier(case, number):
    path = './input/SVModifier'
    if not os.path.exists(path):
        os.makedirs(path)
    for sentence in generate(case):
        jsn_SVModifier['text'] = ' '.join(sentence)
        sentence2 = sentence[:]
        sentence2[-2] = '[MASK]'
        jsn_SVModifier['text_masked'] = ' '.join(sentence2)
        # try-except neccesary because of bug in pattern.de library
        try:
            wrong_num = conjugate(sentence[-2], PRESENT, 3, number)
        except:
            wrong_num = conjugate(sentence[-2], PRESENT, 3, number)
        candidates = []
        candidates.append(sentence[-2])
        candidates.append(wrong_num)
        jsn_SVModifier['candidates'] = candidates
        jsn_SVModifier['indexMASK'] = -2
        if case == SVModifier_sg:
            jsn_SVModifier['case'] = "SVModifier_sg"
            dump_jsonl(jsn_SVextendedModifier, path+'/SVModifier_sg.jsonl', append = True)
        elif case == SVModifier_pl:
            jsn_SVModifier['case'] = "SVModifier_pl"
            dump_jsonl(jsn_SVModifier, path+'/SVModifier_pl.jsonl', append = True)


jsn_SVextendedModifier = {}
def json_SVextendedModifier(case, number):
    path = './input/SVextendedModifier'
    if not os.path.exists(path):
        os.makedirs(path)
    for sentence in generate(case):
        jsn_SVextendedModifier['text'] = ' '.join(sentence)
        sentence2 = sentence[:]
        sentence2[-2] = '[MASK]'
        jsn_SVextendedModifier['text_masked'] = ' '.join(sentence2)
        # try-except neccesary because of bug in pattern.de library
        try:
            wrong_num = conjugate(sentence[-2], PRESENT, 3, number)
        except:
            wrong_num = conjugate(sentence[-2], PRESENT, 3, number)
        candidates = []
        candidates.append(sentence[-2])
        candidates.append(wrong_num)
        jsn_SVextendedModifier['candidates'] = candidates
        jsn_SVextendedModifier['indexMASK'] = -2
        if case == SVextendedModifier_sgsg:
            jsn_SVextendedModifier['case'] = "SVextendedModifier_sgsg"
            dump_jsonl(jsn_SVextendedModifier, path+'/SVextendedModifier_sgsg.jsonl', append = True)
        
        elif case == SVextendedModifier_plpl:
            jsn_SVextendedModifier['case'] = "SVextendedModifier_plpl"
            dump_jsonl(jsn_SVextendedModifier, path+'/SVextendedModifier_plpl.jsonl', append = True)
        
        elif case == SVextendedModifier_plsg:
            jsn_SVextendedModifier['case'] = "SVextendedModifier_plsg"
            dump_jsonl(jsn_SVextendedModifier, path+'/SVextendedModifier_plsg.jsonl', append = True)
        
        elif case == SVextendedModifier_sgpl:
            jsn_SVextendedModifier['case'] = "SVextendedModifier_sgpl"
            dump_jsonl(jsn_SVextendedModifier, path+'/SVextendedModifier_sgpl.jsonl', append = True)



# ---------- 2.2. Additional Case for German: Object in Prefield (Vorfeld): Diesen Roman *empfahl der Autor.



SVVorf_sgsg =  grammar.CFG.fromstring("""
    % start S
    S -> NP_OBJ VVFIN NP_SUBJ '.'
    NP_OBJ -> 'Diesen Roman' |'Diesen Film'| 'Diese Zeitschrift' | 'Diese Bank'
    VVFIN -> 'empfahl' | 'gab'  | 'schenkte' | 'schickte' | 'verkaufte'
    NP_SUBJ -> ART_m NN_m | ART_f NN_f
    ART_m -> 'der'
    ART_f -> 'die'
    NN_m -> 'Autor' | 'Pilot' | 'Kunde' | 'Lehrer' | 'Senator'
    NN_f ->'Senatorin' | 'Beraterin' |'Frau' | 'Polizistin' | 'Richterin'
""")


# exclude fem because acc and nom is similar in German
SVVorf_sgpl =  grammar.CFG.fromstring("""
    % start S
    S -> NP_OBJ VVFIN NP_SUBJ '.'
    NP_OBJ -> 'Diese Romane' |'Diese Filme'| 'Diese Zeitschriften' | 'Diese Banken'
    VVFIN -> 'empfahl' | 'gab'  | 'schenkte' | 'schickte' | 'verkaufte'
    NP_SUBJ -> ART_m NN_m
    ART_m -> 'der'
    NN_m -> 'Autor' | 'Pilot' | 'Kunde' | 'Lehrer' | 'Senator' | 'Berater' |'Junge' | 'Polizist' | 'Richter'

""")

SVVorf_plsg =  grammar.CFG.fromstring("""
    % start S
    S -> NP_OBJ VVFIN NP_SUBJ '.'
    NP_OBJ -> 'Diesen Roman' |'Diesen Film'| 'Diese Zeitschrift' | 'Diese Bank'
     VVFIN -> 'empfahlen' | 'gaben'  | 'schenkten' | 'schickten' | 'verkauften'
    NP_SUBJ -> ART_pl NN_pl
    ART_pl -> 'die'
    NN_pl -> 'Autoren' | 'Piloten' | 'Kunden' | 'Lehrer'  | 'Senatorinnen' | 'Beraterinnen' |'Frauen' | 'Polizistinnen' | 'Richterinnen' | 'Kinder'
""")



jsn_SVVorf = {}
def json_SVVorf(case, number):
    path = './input/SVVorf'
    if not os.path.exists(path):
        os.makedirs(path)
    for sentence in generate(case):
        jsn_SVVorf['text'] = ' '.join(sentence)
        sentence2 = sentence[:]
        sentence2[-4] = '[MASK]'
        jsn_SVVorf['text_masked'] = ' '.join(sentence2)
        # try-except neccesary because of bug in pattern.de library
        try:
            wrong_num = conjugate(sentence[-4], PAST, 3, number)
        except:
            wrong_num = conjugate(sentence[-4], PAST, 3, number)
        candidates = []
        candidates.append(sentence[-4])
        candidates.append(wrong_num)
        jsn_SVVorf['candidates'] = candidates
        jsn_SVVorf['indexMASK'] = -4
        jsn_SVVorf['case'] = 'SVVorf'
        if case == SVVorf_sgsg:
              jsn_SVVorf['case'] = "SVVorf_sgsg"
              dump_jsonl(jsn_SVVorf, path+'/SVVorf_sgsg.jsonl', append = True)

        elif case == SVVorf_sgpl:
            jsn_SVVorf['case'] = "SVVorf_sgpl"
            dump_jsonl(jsn_SVVorf, path+'/SVVorf_sgpl.jsonl', append = True)
        elif case == SVVorf_plsg:
            jsn_SVVorf['case'] = "SVVorf_plsg"
            dump_jsonl(jsn_SVVorf, path+'/SVVorf_plsg.jsonl', append = True)
        



# ---------- 2.3 Reflexive anaphora: Reflective verbs with reflexive pronoun. The reflexive pronoun refers back to the subject in the sentence. Ich bedanke *mich.



ReflVerbs_simple_acc = grammar.CFG.fromstring("""
    S -> PPER_VVFIN_1sg PRF_1sg '.' | PPER_VVFIN_2sg PRF_2sg '.' | NP_VVFIN_3sg PRF_3sg '.' | PPER_VVFIN_1pl PRF_1pl '.'  | PPER_VVFIN_2pl PRF_2pl '.'| PPER_VVFIN_3pl PRF_3pl '.'
    PPER_VVFIN_1sg -> 'Ich bedanke' | 'Ich beeile' | 'Ich erhole'|'Ich freue'| 'Ich irre' | 'Ich konzentriere' |'Ich wundere'|'Ich verbeuge'|'Ich verliebe'

    PPER_VVFIN_2sg -> 'Du bedankst' | 'Du beeilst' | 'Du erholst'|'Du freust'| 'Du irrst' | 'Du konzentrierst'|'Du wunderst'|'Du verbeugst'|'Du verliebst'
    NP_VVFIN_3sg -> 'Der Autor bedankt' | 'Der Autor beeilt'  | 'Der Autor erholt'|'Der Autor freut'| 'Der Autor irrt' | 'Der Autor konzentriert' |'Der Autor wundert'|'Der Autor verbeugt' |'Der Autor verliebt'| 'Sie bedankt' | 'Sie beeilt'  | 'Sie erholt'|'Sie freut'| 'Sie irrt' | 'Sie konzentriert'|'Sie wundert'|'Sie verbeugt'|'Sie verliebt'
    PPER_VVFIN_1pl -> 'Wir bedanken'| 'Wir beeilen'  | 'Wir erholen'|'Wir freuen'| 'Wir irren' | 'Wir konzentrieren'|'Wir wundern'|'Wir verbeugen'|'Wir verlieben'
    PPER_VVFIN_2pl -> 'Ihr bedankt'| 'Ihr beeilt' |  'Ihr erholt'|'Ihr freut'| 'Ihr irrt' | 'Ihr konzentriert'|'Ihr wundert'|'Ihr verbeugt'|'Ihr verliebt'
    PPER_VVFIN_3pl -> 'Die Autoren bedanken'| 'Die Autoren beeilen'  | 'Die Autoren erholen'|'Die Autoren freuen'| 'Die Autoren irren' | 'Die Autoren konzentrieren'|'Die Autoren wundern'|'Die Autoren verbeugen'|'Die Autoren verlieben'|'Sie bedanken'| 'Sie beeilen'  | 'Sie erholen'|'Sie freuen'| 'Sie irren' | 'Sie konzentrieren'|'Sie wundern'|'Sie verbeugen'|'Sie verlieben'
    PRF_1sg -> 'mich'
    PRF_2sg -> 'dich'
    PRF_3sg -> 'sich'
    PRF_1pl -> 'uns'
    PRF_2pl -> 'euch'
    PRF_3pl -> 'sich'
""")

#  Reflexive  Verb Agreement across a relative clause
ReflVerbs_longer_acc = grammar.CFG.fromstring("""
    S -> PPER_1sg ',' RelCl_sg ',' VVFIN_1sg PRF_1sg '.' | PPER_2sg ',' RelCl_sg ',' VVFIN_2sg PRF_2sg '.' | PPER_3sg ',' RelCl_sg ',' VVFIN_3sg PRF_3sg '.' | PPER_1pl ',' RelCl_pl ',' VVFIN_pl PRF_1pl '.'  | PPER_2pl ',' RelCl_2pl ',' VVFIN_2pl PRF_2pl '.' |  PPER_3pl ',' RelCl_pl ',' VVFIN_pl PRF_3pl '.'
    PPER_1sg -> 'Ich'
    PPER_2sg -> 'Du'
    PPER_3sg -> 'Der Autor' |'Er'
    PPER_1pl -> 'Wir'
    PPER_2pl -> 'Ihr'
    PPER_3pl -> 'Sie'
    RelCl_sg -> 'der Hannah gestern besuchte'|'der gerne das Fernsehprogramm beobachtet' | 'der gerne viele verschiedene Sprachen kennt'| 'der zwanzig Jahre alt ist' | 'der jeden Tag in eine Zeitung schreibt'
    RelCl_pl -> 'die Hannah gestern besuchten'|'die gerne das Fernsehprogramm beobachten' | 'die gerne viele verschiedene Sprachen kennen'| 'die zwanzig Jahre alt sind' | 'die jeden Tag in eine Zeitung schreiben'
    RelCl_2pl -> 'die Hannah gestern besuchtet'|'die gerne das Fernsehprogramm beobachtet' | 'die gerne viele verschiedene Sprachen kennt'| 'die zwanzig Jahre alt seid' | 'die jeden Tag in eine Zeitung schreibt'
    VVFIN_1sg  -> 'bedanke' | 'beeile' | 'erhole'|'freue'| 'irre' | 'konzentriere' |'wundere'|'verbeuge'|'verliebe'
    VVFIN_2sg  -> 'bedankst' | 'beeilst' | 'erholst'|'freust'| 'irrst' | 'konzentrierst' |'wunderst'|'verbeugst'|'verliebst'
    VVFIN_3sg  -> 'bedankt' | 'beeilt' | 'erholt'|'freut'| 'irrt' | 'konzentriert' |'wundert'|'verbeugt'|'verliebt'
    VVFIN_pl  -> 'bedanken' | 'beeilen' | 'erholen'|'freuen'| 'irren' | 'konzentrieren' |'wundern'|'verbeugen'|'verlieben'
    VVFIN_2pl  -> 'bedankt' | 'beeilt' | 'erholt'|'freut'| 'irrt' | 'konzentriert' |'wundert'|'verbeugt'|'verliebt'
    PRF_1sg -> 'mich'
    PRF_2sg -> 'dich'
    PRF_3sg -> 'sich'
    PRF_1pl -> 'uns'
    PRF_2pl -> 'euch'
    PRF_3pl -> 'sich'
    
""")

# ReflVerbs-Subject-Agreemeent in a sentential complement

ReflVerbs_SentCompl_acc = grammar.CFG.fromstring("""
    S -> NP VVFIN ',' KOUS NP_SentComp '.'
    NP -> ART_m NN_m | ART_f NN_f
    ART_m -> 'Der'
    ART_f -> 'Die'
    NN_m -> 'Autor' | 'Pilot' | 'Kunde' | 'Lehrer' | 'Senator'
    NN_f ->'Senatorin' | 'Beraterin' |'Frau' | 'Polizistin' | 'Richterin'
    VVFIN -> 'sagte' | 'dachte' | 'wusste'
    KOUS -> 'dass'
    NP_SentComp  -> PPER_1sg PRF_1sg VVFIN_1sg | PPER_2sg PRF_2sg VVFIN_2sg| PPER_3sg PRF_3sg VVFIN_3sg| PPER_1pl PRF_1pl VVFIN_1pl| PPER_2pl PRF_2pl VVFIN_2pl| PPER_3pl PRF_3pl VVFIN_3pl
    PPER_1sg -> 'Ich'
    PPER_2sg -> 'Du'
    PPER_3sg -> 'Der Autor' |'Er'
    PPER_1pl -> 'Wir'
    PPER_2pl -> 'Ihr'
    PPER_3pl -> 'Sie'
    PRF_1sg -> 'mich'
    PRF_2sg -> 'dich'
    PRF_3sg -> 'sich'
    PRF_1pl -> 'uns'
    PRF_2pl -> 'euch'
    PRF_3pl -> 'sich'
    VVFIN_1sg  -> 'bedanke' | 'beeile' | 'erhole'|'freue'| 'irre' | 'konzentriere' |'wundere'|'verbeuge'|'verliebe'
    VVFIN_2sg  -> 'bedankst' | 'beeilst' | 'erholst'|'freust'| 'irrst' | 'konzentrierst' |'wunderst'|'verbeugst'|'verliebst'
    VVFIN_3sg  -> 'bedankt' | 'beeilt' | 'erholt'|'freut'| 'irrt' | 'konzentriert' |'wundert'|'verbeugt'|'verliebt'
    VVFIN_pl  -> 'bedanken' | 'beeilen' | 'erholen'|'freuen'| 'irren' | 'konzentrieren' |'wundern'|'verbeugen'|'verlieben'
    VVFIN_2pl  -> 'bedankt' | 'beeilt' | 'erholt'|'freut'| 'irrt' | 'konzentriert' |'wundert'|'verbeugt'|'verliebt'
""")


# ---------- 2.4. Reflexive anaphora: Testing LM on case sensitivity: Verbs govern an acc, we will test same genus but dativ case (only 1st and 2nd person sg: mich(acc)/mir(dat) and dich(acc)/dir(dat))


jsn_RA = {}
def json_RA(case, index):
    path = './input/RA_acc'
    if not os.path.exists(path):
        os.makedirs(path)
    for sentence in generate(case):
        jsn_RA['text'] = ' '.join(sentence)
        sentence2 = sentence[:]
        sentence2[index] = '[MASK]'
        jsn_RA['text_masked'] = ' '.join(sentence2)
        if sentence[index]=='mich':
            wrong_num = 'sich'
        elif sentence[index]=='dich':
            wrong_num = 'euch'
        elif sentence[index]=='sich':
            wrong_num = 'mich'
        else:
            wrong_num = 'dich'
        
        candidates = []
        candidates.append(sentence[index])
        candidates.append(wrong_num)
        jsn_RA['candidates'] = candidates
        jsn_RA['indexMASK'] = index
        if case == ReflVerbs_simple_acc:
               jsn_RA['case'] = "ReflVerbs_simple_acc"
               dump_jsonl(jsn_RA, path+'/ReflVerbs_simple_acc.jsonl', append = True)
         
        elif case == ReflVerbs_longer_acc:
            jsn_RA['case'] = "ReflVerbs_longer_acc"
            dump_jsonl(jsn_RA, path+'/ReflVerbs_longer_acc.jsonl', append = True)

        elif case == ReflVerbs_SentCompl_acc:
            jsn_RA['case'] = "ReflVerbs_SentCompl_acc"
            dump_jsonl(jsn_RA, path+'/ReflVerbs_SentCompl_acc.jsonl', append = True)
        
jsn_RA = {}
def json_RA_case(case, index):
    path = './input/RA_case'
    if not os.path.exists(path):
        os.makedirs(path)
    for sentence in generate(case):
        
        if sentence[index] == 'mich' or sentence[index] == 'dich':
            jsn_RA['text'] = ' '.join(sentence)
            sentence2 = sentence[:]
            sentence2[index] = '[MASK]'
            jsn_RA['text_masked'] = ' '.join(sentence2)
            if sentence[index]=='mich':
                wrong_num = 'mir'
            elif sentence[index]=='dich':
                wrong_num = 'dir'
            
            candidates = []
            candidates.append(sentence[index])
            candidates.append(wrong_num)
            jsn_RA['candidates'] = candidates
            jsn_RA['indexMASK'] = index
            if case == ReflVerbs_simple_acc:
                   jsn_RA['case'] = "ReflVerbs_simple_case"
                   dump_jsonl(jsn_RA, path+'/ReflVerbs_simple_case.jsonl', append = True)
             
            elif case == ReflVerbs_longer_acc:
                jsn_RA['case'] = "ReflVerbs_longer_case"
                dump_jsonl(jsn_RA, path+'/ReflVerbs_longer_case.jsonl', append = True)

            elif case == ReflVerbs_SentCompl_acc:
                jsn_RA['case'] = "ReflVerbs_SentCompl_case"
                dump_jsonl(jsn_RA, path+'/ReflVerbs_SentCompl_case.jsonl', append = True)





if __name__ == "__main__":
    
    json_SimplSent(SimplSent_sg, PL)
    json_SimplSent(SimplSent_pl, SG)
    
    
    json_SVinSentCompl(SVinSentCompl_sgsg, PL)
    json_SVinSentCompl(SVinSentCompl_plpl, SG)
    json_SVinSentCompl(SVinSentCompl_sgpl, SG)
    json_SVinSentCompl(SVinSentCompl_plsg, PL)
    
    json_SVshortVPCoord(SVshortVPCoord_sg, PL)
    json_SVshortVPCoord(SVshortVPCoord_pl, SG)
    json_SVshortVPCoord(SVmediumVPCoord_sgsg, PL)
    json_SVmediumVPCoord(SVmediumVPCoord_plpl, SG)
    json_SVmediumVPCoord(SVmediumVPCoord_sgpl, PL)
    json_SVmediumVPCoord(SVmediumVPCoord_plsg, SG)

    json_SVlongVPCoord(SVlongVPCoord_sgsg1, PL)
    json_SVlongVPCoord(SVlongVPCoord_sgsg2, PL)
    json_SVlongVPCoord(SVlongVPCoord_sgsg3, PL)
    json_SVlongVPCoord(SVlongVPCoord_sgsg4, PL)
    json_SVlongVPCoord(SVlongVPCoord_sgpl1, PL)
    json_SVlongVPCoord(SVlongVPCoord_sgpl2, PL)
    json_SVlongVPCoord(SVlongVPCoord_sgpl3, PL)
    json_SVlongVPCoord(SVlongVPCoord_sgpl4, PL)
    json_SVlongVPCoord(SVlongVPCoord_plpl1, SG)
    json_SVlongVPCoord(SVlongVPCoord_plpl2, SG)
    json_SVlongVPCoord(SVlongVPCoord_plpl3, SG)
    json_SVlongVPCoord(SVlongVPCoord_plpl4, SG)
    json_SVlongVPCoord(SVlongVPCoord_plsg1, SG)
    json_SVlongVPCoord(SVlongVPCoord_plsg2, SG)
    json_SVlongVPCoord(SVlongVPCoord_plsg3, SG)
    json_SVlongVPCoord(SVlongVPCoord_plsg4, SG)
    
    
    json_SVPP(SVPP_sgsg, PL)
    json_SVPP(SVPP_plpl, SG)
    json_SVPP(SVPP_sgpl, PL)
    json_SVPP(SVPP_plsg, SG)

    json_SVSubjRelC(SVSubjRelC_sgsg, PL)
    json_SVSubjRelC(SVSubjRelC_plpl, SG)
    json_SVSubjRelC(SVSubjRelC_sgpl, PL)
    json_SVSubjRelC(SVSubjRelC_plsg, SG)

    json_SVacrossObjRelC(SVObjRelC_sgsg, PL)
    json_SVacrossObjRelC(SVObjRelC_plpl, SG)
    json_SVacrossObjRelC(SVObjRelC_sgpl, PL)
    json_SVacrossObjRelC(SVObjRelC_plsg, SG)
    
    json_SVinObjRelC(SVObjRelC_sgpl, SG)
    json_SVinObjRelC(SVObjRelC_plsg, PL)
    json_SVinObjRelC(SVObjRelC_sgsg, PL)
    json_SVinObjRelC(SVObjRelC_plpl, SG)
    
    json_SVModifier(SVModifier_sg, PL)
    json_SVModifier(SVModifier_pl, SG)
    json_SVextendedModifier(SVextendedModifier_sgsg, PL)
    json_SVextendedModifier(SVextendedModifier_plpl, SG)
    json_SVextendedModifier(SVextendedModifier_plsg, SG)
    json_SVextendedModifier(SVextendedModifier_sgpl, PL)
    
    json_SVVorf(SVVorf_sgsg, PL)
    json_SVVorf(SVVorf_sgpl, PL)
    json_SVVorf(SVVorf_plsg, SG)
    
    json_RA(ReflVerbs_simple_acc, -2)
    json_RA(ReflVerbs_longer_acc, -2)
    json_RA(ReflVerbs_SentCompl_acc,  -3)

    json_RA_case(ReflVerbs_simple_acc, -2)
    json_RA_case(ReflVerbs_longer_acc, -2)
    json_RA_case(ReflVerbs_SentCompl_acc,  -3)
    
