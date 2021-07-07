from vepar import *
from robolang import P

f_izađi = ''' 
    Program(){
        ponovi(i=0,i<10,1){
            ako(i!=5) ispis(i)
            inače izađi
        },
        vrati Istina
    }
'''

f_izađi2 = '''
    Program(){
        i = 5,
        dok(i > 0){
            ispis(i),
            i = i - 1,
            ako(i == 2) izađi
        },
        vrati Istina
    }
'''


f_nastavi = ''' 
Program(){
        ponovi(i=0,i<10,1){
            ako(i==5) nastavi
            inače ispis(i)
        },
        vrati Istina
    }'''


f_negacija = '''
    Program(){
        X = !Istina,
        ispis(X),
        vrati Istina
    }
'''

f_negacija2 = '''
    Program(){
        X = !!(Istina & Laž),
        ispis(X),
        vrati Istina
    }
'''

f_disjunkcija = '''
    Program(){
        X = Istina | Neodređeno | Laž,
        ispis(X),
        vrati Istina
    }
'''

f_disj_konj_neg = '''
    Program(){
        X = !(Laž | ((Istina & Neodređeno)&(Neodređeno | Laž))),
        ispis(X),
        vrati Istina
    }
'''

f_kast_logubroj = '''
        Program(){
            X = Laž,
            Y = Istina,
            Z = Neodređeno,
            x = logubroj(X),
            y = logubroj(Y),
            z = logubroj(Z),
            ispis(x),
            ispis(y),
            ispis(z),
            vrati Y
        }
    '''

f_kast_arulog_true = '''
        Program(){
            x = 3,
            Y = arulog(x),
            vrati Y
        }
    '''

f_kast_arulog_false = '''
        Program(){
            x = -5,
            Y = arulog(x),
            vrati Y
        }
    '''

f_kast_arulog_none = '''
        Program(){
            x = 0,
            Y = arulog(x),
            vrati Y
        }
    '''

f_kast_liu = '''
        Program(){
            lista L1,
            ubaci L1 1 0,
            ubaci L1 2 1,
            ubaci L1 2 1,
            x = liubroj(L1),
            ispis(x),
            lista L3,
            y = liubroj(L3),
            ispis(y),
            Y = liulog(L3),
            lista L1,
            Z = liulog(L1),
            vrati Y
        }
    '''

f_kast_uli = '''
        Program(){
            lista L1,
            z = 3,
            aruli(z L1),
            w = koliko L1,
            ispis(w),
            i = 0,
            aruli(i L2),
            j = koliko L2,
            ispis(j),
            X = Istina,
            loguli(X L3),
            k = koliko L3,
            ispis(k),
            vrati Istina
        }
    '''

f_lista = '''
        Program(){
            lista L3,
            ubaci L3 -45 0,
            ubaci L3 2 1,
            ispisilistu L3,
            x = koliko L3,
            ispis(x),
            ubaci L3 3 2,
            ubaci L3 2 3,
            x = koliko L3,
            ispis(x),
            lista L1,
            ubaci L1 -4 0,
            ubaci L3 L1 4,
            ubaci L1 5 1,
            ubaci L3 L1 5,
            ispisilistu L3,
            izbaci L3 4,
            ispisilistu L3,
            izbaci L3 2,
            ispisilistu L3,
            y = dohvati L3 2,
            ispis(y),
            lista L1,
            L1 = dohvati L3 3,
            ispisilistu L1,
            x = koliko L3,
            ubaci L1 x 1,
            ispisilistu L1,
            ispis(x),
            vrati Istina
        }
    '''

f_liste = '''
    Program(){
        Y = Istina,
        lista L1,
        ubaci L1 3 0,
        x = 5,
        ubaci L1 x 1,
        ubaci L1 2 2,
        y=0,
        dok (y < dohvati L1 0){
            y=y+1,
        },
        x=0,
        dok(x < dohvati L1 1){
            x=x+1,
            ispis(x)
        },
        ubaci L1 Y 3,
        X = Istina,
        a=0,
        dok(X == dohvati L1 3){
            ispis(X),
            a=a+1,
            ako (a==3) X=Laž
        },
        dok(dohvati L1 1){
            a=a+1,
            ispis(a),
            ako(a==10) izađi
        },
        vrati Istina
    }
'''

f_bez_parametara = '''
        Program(){
            vrati Istina
        }
        '''

f_s_parametrima = '''
        Program(a,b){
            vrati Istina
        }
        '''

f_pridruživanje_jednost_arizraz = '''
        Program(){
            x = 4*2+3,
            ispis(x),
            vrati Istina
        }
    '''

f_pridruživanje_kompliciraniji_arizraz = '''
        Program(){
            x = 4*(2+3)^4/3,
            ispis(x),
            vrati Istina
        }
    '''

f_pridruživanje_logizraz = '''
        Program(){
            T = Istina,
            F = Laž,
            U = (((T | F) & Istina) == T),
            vrati U
        }
    '''

f_petlja_ponovi_bez_naredbi = '''
        Program(){
            ponovi(i=0, i < 10, 1){
            },
            vrati Istina
        }
    '''

f_petlja_ponovi_s_jednom_naredbom = '''
        Program(){
            x=2,
            ponovi(i=0, i < 10, 1) x=x+2,
            ispis(x),
            vrati Istina
        }
    '''

f_petlja_ponovi_s_više_naredbi = '''
        Program(){
            x=0,
            y=1,
            ponovi(i=0, i < 10, 1){
                x= x+2,
                y= y*3
            },
            ispis(x,y),
            vrati Istina
        }
    '''

f_petlja_dok_bez_naredbi = '''
        Program(){
            x=0,
            dok(x < 5){
            },
            vrati Istina
        }
    '''

f_petlja_dok_s_jednom_naredbom = '''
        Program(){
            x = 0,
            dok(x<5){
                x = x + 1
            },
            ispis(x),
            vrati Istina
        }
    '''

f_petlja_dok_s_više_naredbi = '''
        Program(){
            x=0,
            dok(x<10){
                x = x + 1,
                Y = Neodređeno,
                ispis(x, Y)
            },
            vrati Istina 
        }
    '''

f_grananje = '''
        Program(){
            x=0,
            U = (3<=3<4)==Istina,
            ako (U) {
                x=2
            },
            ispis(x),
            vrati U
        }
    '''

f_pridruživanje_greška = '''
        Program(){
            x = Istina
            vrati Istina
        }
    '''


funkcija1 = ''' 
     f(n){
        vrati n
    }
    Program(){
        x = f(5)+f(6),
        ispis(x),
        vrati Istina
    }   
     '''

lista_nelokalna_kontrola_toka = [f_izađi, f_izađi2, f_nastavi]

lista_logika = [f_negacija, f_negacija2, f_disjunkcija, f_disj_konj_neg]

lista_ulaza_jedna_funkcija = [
    f_bez_parametara,
    f_s_parametrima
]

lista_ulaza_pridruživanje = [f_pridruživanje_jednost_arizraz,
                             f_pridruživanje_kompliciraniji_arizraz, f_pridruživanje_logizraz]

lista_ulaza_petlja_ponovi = [
    f_petlja_ponovi_bez_naredbi,
    f_petlja_ponovi_s_jednom_naredbom,
    f_petlja_ponovi_s_više_naredbi
]

lista_ulaza_petlja_dok = [
    # f_petlja_dok_bez_naredbi
    f_petlja_dok_s_jednom_naredbom, f_petlja_dok_s_više_naredbi
]

lista_ulaza_grananje = [f_grananje]

lista_ulaza_kastanje = [f_kast_logubroj, f_kast_arulog_true, f_kast_arulog_false,
                        f_kast_arulog_none, f_lista, f_kast_liu, f_kast_uli, f_liste]

lista_ulaza_funkcije = [funkcija1]

lista_testovi = lista_logika + lista_nelokalna_kontrola_toka + lista_ulaza_kastanje + lista_ulaza_jedna_funkcija + \
    lista_ulaza_pridruživanje + lista_ulaza_petlja_ponovi + \
    lista_ulaza_petlja_dok + lista_ulaza_grananje + lista_ulaza_funkcije

lista_očekivana_sintaksna_greška = [f_pridruživanje_greška]


def testiraj_parser(lista_ulaza):
    for ulaz in lista_ulaza:
        print('-' * 60)
        print(ulaz)
        print()
        P.tokeniziraj(ulaz)
        print()
        prikaz(P(ulaz))


def testiraj_izvršavanje(lista_ulaza):
    for ulaz in lista_ulaza:
        print('-' * 60)
        print(ulaz)
        prikaz(test := P(ulaz))
        izvrši(test)
        print()


def izvrši(funkcije, *argv):
    print('\nProgram je vratio:', funkcije['Program'].pozovi(argv))
