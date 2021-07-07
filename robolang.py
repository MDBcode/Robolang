from vepar import *
from okolina import *
from testovi import *

okolina = Okolina()  # konstruktor automatski inicijalizira okolinu


class T(TipoviTokena):
    PONOVI, DOK, ISPIS, AKO, INAČE, VRATI = 'ponovi', 'dok', 'ispis', 'ako', 'inače', 'vrati'
    LISTA, UBACI, IZBACI, KOLIKO, DOHVATI, ISPISILISTU = 'lista', 'ubaci', 'izbaci', 'koliko', 'dohvati', 'ispisilistu'
    LIUBROJ, LOGUBROJ, LIULOG, ARULOG, LOGULI, ARULI = 'liubroj', 'logubroj', 'liulog', 'arulog', 'loguli', 'aruli'
    PLUS, MINUS, PUTA, KROZ, NA = '+-*/^'
    NEG, KONJ, DISJ, OOTV, OZATV, VOTV, VZATV, UOTV, UZATV, ZAREZ = '!&|(){}[],'
    JEDNAKO, MANJE, VEĆE = '=<>'
    MANJEJ, VEĆEJ, JEDNAKOJ, RAZLIČITO = '<=', '>=', '==', '!='
    POMAKNI, ODLETI, POČISTI, PRONAĐIMRLJU, STANJEBATERIJE, STANJESPREMNIKA = 'POMAKNI', 'ODLETI', 'POČISTI', 'PRONAĐIMRLJU', 'STANJEBATERIJE', 'STANJESPREMNIKA'

    class BROJ(Token):
        def vrijednost(self, mem): return int(self.sadržaj)

    class ARIME(Token):
        def vrijednost(self, mem): return mem[self]

    class LOGIME(ARIME):
        pass

    class ID(Token):
        pass

    class ISTINA(Token):
        literal = 'Istina'
        def vrijednost(self, mem): return True

    class NEODREĐENO(Token):
        literal = 'Neodređeno'
        def vrijednost(self, mem): return None

    class LAŽ(Token):
        literal = 'Laž'
        def vrijednost(self, mem): return False

    class BREAK(Token):
        literal = 'izađi'
        def izvrši(self, mem): raise Izađi

    class CONTINUE(Token):
        literal = 'nastavi'
        def izvrši(self, mem): raise Nastavi


def ls(lex):
    for znak in lex:
        if znak.isspace():
            lex.zanemari()
        elif znak == 'L':
            nakonL = lex.čitaj()
            if nakonL.isdecimal():
                n = lex.prirodni_broj(nakonL)
                tok = lex.token(T.ID)
                if 1 <= n <= 9:
                    yield tok
                else:
                    raise tok.krivi_sadržaj('očekivan broj liste između 1 i 9')
        elif znak == '=':
            yield lex.token(T.JEDNAKOJ if lex >= '=' else T.JEDNAKO)
        elif znak == '<':
            yield lex.token(T.MANJEJ if lex >= '=' else T.MANJE)
        elif znak == '>':
            yield lex.token(T.VEĆEJ if lex >= '=' else T.VEĆE)
        elif znak == '!':
            yield lex.token(T.RAZLIČITO if lex >= '=' else T.NEG)
        elif znak.islower():
            lex.zvijezda(str.isalnum)
            yield lex.literal(T.ARIME)
        elif znak.isupper():
            lex.zvijezda(str.isalnum)
            yield lex.literal(T.LOGIME)
        elif znak.isdecimal():
            lex.prirodni_broj(znak)
            yield lex.token(T.BROJ)
        elif znak == '$':  # jednolinijski komentari
            lex.pročitaj_do('\n')
            lex.zanemari()
        else:
            yield lex.literal(T)


# GRAMATIKA
# program -> funkcija | funkcija program
# funkcija -> ime OOTV parametri? OZATV naredba
# parametri -> ime | ime ZAREZ parametri
# ime -> ARIME | LOGIME | ID
# element -> BROJ | LOGIME | ARIME | lista
# lista -> UOTV elementi UZATV
# elementi -> element | element ZAREZ elementi | ''
# naredba -> pridruživanje | petlja | grananje | ispis | BREAK | CONTINUE | VRATI argument
#            | VOTV VZATV | VOTV naredbe VZATV | ime poziv | LISTA ID | UBACI ID arizraz
#            | UBACI ID element | IZBACI ID BROJ | ISPISILISTU ID | ARULI OOTV arizraz ID OZATV | LOGULI OOTV logizraz ID OZATV
#            | (POMAKNI|ODLETI) arizraz ZAREZ arizraz | POČISTI
# naredbe -> naredba | naredba ZAREZ naredbe
# pridruživanje -> ARIME JEDNAKO arizraz | ARIME ZAREZ ARIME JEDNAKO PRONAĐIMRLJU
#                 | LOGIME JEDNAKO logizraz
# petlja -> ponavljaj naredba | dok naredba
# grananje -> AKO OOTV logizraz OZATV naredba | AKO OOTV logizraz OZATV naredba INAČE naredba
# logizraz -> logizraz (JEDNAKOJ|RAZLIČITO) usporednik | usporednik
# usporednik -> usporednik DISJ disjunkt | disjunkt
# disjunkt -> disjunkt KONJ konjunkt | konjunkt
# binvez -> KONJ | DISJ
# konjunkt -> NEG logizraz | usporedba_arizraza
#             | ISTINA | LAŽ | NEODREĐENO | LOGIME | LOGIME poziv | OOTV logizraz OZATV
#             | ARULOG OOTV arizraz OZATV | LIULOG OOTV ID OZATV | DOHVATI ID BROJ
# usporedba_arizraza -> (arizraz|usporedba_arizraza) (MANJE|MANJEJ|JEDNAKOJ|VEĆE|VEĆEJ|RAZLIČITO) arizraz
# ispis -> ISPIS OOTV varijable? OZATV
# ponavljaj -> PONOVI OOTV ime# JEDNAKO BROJ ZAREZ ime# (MANJE|MANJEJ) BROJ ZAREZ BROJ OZATV
# dok -> DOK OOTV logizraz OZATV
# varijable -> ime | ime ZAREZ varijable
# arizraz -> arizraz PLUS član | arizraz MINUS član | član | STANJEBATERIJE | STANJESPREMNIKA
# član -> član PUTA faktor | član KROZ faktor | faktor
# faktor -> baza NA faktor | baza
# baza -> BROJ | ARIME | ARIME poziv | OOTV arizraz OZATV | MINUS faktor
#        | LOGUBROJ OOTV logizraz OZATV | LIUBROJ OOTV ID OZATV | KOLIKO ID | DOHVATI ID BROJ
# poziv -> OOTV argumenti? OZATV
# argumenti -> argument | argument ZAREZ argumenti
# argument -> arizraz | logizraz


class P(Parser):
    def program(self):
        self.funkcije = Memorija(redefinicija=False)
        while not self > KRAJ:
            funkcija = self.funkcija()
            self.funkcije[funkcija.ime] = funkcija
        return self.funkcije

    def funkcija(self):
        atributi = self.imef, self.parametrif = self.ime(
        ), self.parametri()
        return Funkcija(*atributi, self.naredba())

    def ime(self):
        return self >> {T.ARIME, T.LOGIME, T.ID}

    def parametri(self):
        self >> T.OOTV
        if self >= T.OZATV:
            return []
        param = [self.ime()]
        while self >= T.ZAREZ:
            param.append(self.ime())
        self >> T.OZATV
        return param

    def element(self):
        if self >= T.DOHVATI:
            return Dohvati(self >> T.ID, self >> T.BROJ)
        else:
            return self >> {T.BROJ, T.LOGIME, T.ARIME}

    def naredba(self):
        '''naredba može biti bez vitičastih zagrada isključivo ako je samo jedna.
           ako nema naredbi, moraju biti prazne vitičaste zagrade'''
        if self > T.AKO:
            return self.grananje()
        elif self > T.PONOVI:
            return self.ponovi_petlja()
        elif self > T.DOK:
            return self.dok_petlja()
        elif self > T.VOTV:
            return self.blok()
        elif self > T.ISPIS:
            return self.ispis()
        elif self >= T.VRATI:
            return Vrati(self.tipa(self.imef))
        elif br := self >= T.BREAK:
            return br
        elif cont := self >= T.CONTINUE:
            return cont
        elif self >= T.LISTA:
            return Deklaracija(self >> T.ID)
        elif self >= T.UBACI:
            a = self >> T.ID
            if self >= T.MINUS:
                b = self >= T.BROJ
                b = Suprotan(b)
                return Ubaci(a, b, self >> T.BROJ)
            elif b := self >= T.BROJ:
                return Ubaci(a, b, self >> T.BROJ)
            elif b := self >= T.ARIME:
                return Ubaci(a, b, self >> T.BROJ)
            elif b := self >= T.LOGIME:
                return Ubaci(a, b, self >> T.BROJ)
            elif b := self >= T.ID:
                return UbaciListu(a, b, self >> T.BROJ)
        elif self >= T.IZBACI:
            return Izbaci(self >> T.ID, self >> T.BROJ)
        elif self >= T.ISPISILISTU:
            return Ispisi_listu(self >> T.ID)
        elif self >= T.ARULI:
            self >> T.OOTV
            argument = self.arizraz()
            lista = self >> T.ID
            self >> T.OZATV
            return BrojUListu(argument, lista)
        elif self >= T.LOGULI:
            self >> T.OOTV
            argument = self.logizraz()
            lista = self >> T.ID
            self >> T.OZATV
            return LogUListu(argument, lista)
        elif self >= T.POČISTI:
            return Počisti()
        elif self >= T.POMAKNI:
            x = self.arizraz()
            self >> T.ZAREZ
            y = self.arizraz()
            return Pomakni(x, y)
        elif self >= T.ODLETI:
            x = self.arizraz()
            self >> T.ZAREZ
            y = self.arizraz()
            return Odleti(x, y)
        else:
            ime = self.ime()
            if self >= T.JEDNAKO:
                return Pridruživanje(ime, self.tipa(ime))
            elif self >= T.ZAREZ:
                ime2 = self.ime()
                self >> T.JEDNAKO
                self >> T.PRONAĐIMRLJU
                return Pridruživanje2(ime, ime2, PronađiMrlju())
            else:
                return self.možda_poziv(ime)

    def blok(self):
        self >> T.VOTV
        if self >= T.VZATV:
            return Blok([])
        n = [self.naredba()]
        while self >= T.ZAREZ and not self > T.VZATV:
            n.append(self.naredba())
        self >> T.VZATV
        return Blok.ili_samo(n)

    def ponovi_petlja(self):
        kriva_varijabla = SemantičkaGreška(
            'Prva dva dijela petlje moraju imati istu varijablu.')
        self >> T.PONOVI, self >> T.OOTV
        i = self >> T.ARIME
        self >> T.JEDNAKO
        početak = self >> T.BROJ
        self >> T.ZAREZ

        if (self >> T.ARIME) != i:
            raise kriva_varijabla
        self >= {T.MANJE, T.MANJEJ}
        granica = self >> T.BROJ
        self >> T.ZAREZ

        inkrement = self >> T.BROJ
        self >> T.OZATV

        # petlja je naredba - mora imati zarez na kraju ako nije zadnja u bloku, ili viticastu zagradu koja oznacava kraj bloka ili funkcije
        if not self > {T.ZAREZ, T.VZATV}:
            tijelo = self.naredba()
        else:
            tijelo = []
        return PonoviPetlja(i, početak, granica, inkrement, tijelo)

    def dok_petlja(self):
        self >> T.DOK, self >> T.OOTV
        log = self.logizraz()
        self >> T.OZATV
        naredba = self.naredba()
        return DokPetlja(log, naredba)

    def grananje(self):
        self >> T.AKO, self >> T.OOTV
        atributi = [self.logizraz()]
        self >> T.OZATV
        atributi.append(self.naredba())
        if self >= T.INAČE:
            inače = self.naredba()
        else:
            inače = Blok([])
        return Grananje(*atributi, inače)

    def logizraz(self):
        usporednici = [self.usporednik()]
        while True:
            if self >= T.JEDNAKOJ:
                usporednici.append(self.logizraz())
            elif self >= T.RAZLIČITO:
                usporednici.append(Negacija(self.logizraz()))
            else:
                return LogičkaUsporedba.ili_samo(usporednici)

    def usporednik(self):
        disjunkti = [self.disjunkt()]
        while self >= T.DISJ:
            disjunkti.append(self.disjunkt())
        return Disjunkcija.ili_samo(disjunkti)

    def disjunkt(self):
        konjunkti = [self.konjunkt()]
        while self >= T.KONJ:
            konjunkti.append(self.konjunkt())
        return Konjunkcija.ili_samo(konjunkti)

    def konjunkt(self):
        if log := self >= {T.ISTINA, T.LAŽ, T.NEODREĐENO, T.LOGIME}:
            return self.možda_poziv(log)
        elif self >= T.NEG:
            return Negacija(self.logizraz())
        elif self >= T.OOTV:
            u_zagradi = self.logizraz()
            self >> T.OZATV
            return u_zagradi
        elif self >= T.ARULOG:
            self >> T.OOTV
            argument = self.arizraz()
            self >> T.OZATV
            return BrojULog(argument)
        elif self >= T.LIULOG:
            self >> T.OOTV
            argument = self >> T.ID
            self >> T.OZATV
            return ListuULog(argument)
        elif self >= T.DOHVATI:
            return Dohvati(self >> T.ID, self >> T.BROJ)
        else:
            arizrazi = [AritmetičkaUsporedba(self.arizraz(), self >> {
                                             T.JEDNAKOJ, T.RAZLIČITO, T.MANJE, T.MANJEJ, T.VEĆE, T.VEĆEJ}, prethodni := self.arizraz())]
            while True:
                if op := self >= {T.JEDNAKOJ, T.RAZLIČITO, T.MANJE, T.MANJEJ, T.VEĆE, T.VEĆEJ}:
                    arizrazi.append(AritmetičkaUsporedba(
                        prethodni, op, prethodni := self.arizraz()))
                else:
                    return LogičkaUsporedba.ili_samo(arizrazi)

    def argumenti(self, parametri):
        arg = []
        self >> T.OOTV
        for i, parametar in enumerate(parametri):
            if i:
                self >> T.ZAREZ
            arg.append(self.tipa(parametar))
        self >> T.OZATV
        return arg

    def tipa(self, ime):
        if ime ^ T.ARIME:
            return self.arizraz()
        elif ime ^ T.LOGIME:
            return self.logizraz()
        elif ime ^ T.ID:
            return self.element()
        else:
            assert False, f'Nepoznat tip od {ime}'

    def arizraz(self):
        if self >= T.STANJEBATERIJE:
            return StanjeBaterije()
        if self >= T.STANJESPREMNIKA:
            return StanjeSpremnika()
        else:
            članovi = [self.član()]
            while True:
                if self >= T.PLUS:
                    članovi.append(self.član())
                elif self >= T.MINUS:
                    članovi.append(Suprotan(self.član()))
                else:
                    return Zbroj.ili_samo(članovi)

    def član(self):
        faktori = [self.faktor()]
        while True:
            if self >= T.PUTA:
                faktori.append(self.faktor())
            if self >= T.KROZ:
                faktori.append(Recipročan(self.faktor()))
            else:
                return Umnožak.ili_samo(faktori)

    def faktor(self):
        baza = self.baza()
        if self >= T.NA:
            return Potencija(baza, self.faktor())
        else:
            return baza

    def baza(self):
        if self >= T.MINUS:
            return Suprotan(self.faktor())
        elif aritm := self >= T.ARIME:
            return self.možda_poziv(aritm)
        elif self >= T.OOTV:
            u_zagradi = self.arizraz()
            self >> T.OZATV
            return u_zagradi
        elif self >= T.LOGUBROJ:
            self >> T.OOTV
            argument = self.logizraz()
            self >> T.OZATV
            return LogUBroj(argument)
        elif self >= T.LIUBROJ:
            self >> T.OOTV
            argument = self >> T.ID
            self >> T.OZATV
            return ListuUBroj(argument)
        elif self >= T.DOHVATI:
            return Dohvati(self >> T.ID, self >> T.BROJ)
        elif self >= T.KOLIKO:
            return Duljina(self >> T.ID)
        else:
            return self >> T.BROJ

    def možda_poziv(self, ime):
        if ime in self.funkcije:
            funkcija = self.funkcije[ime]
            return Poziv(funkcija, self.argumenti(funkcija.parametri))
        else:
            return ime

    def ispis(self):
        self >> T.ISPIS
        varijable = self.varijable()
        return Ispis(varijable)

    def varijable(self):
        self >> T.OOTV
        if self >= T.OZATV:
            return []
        var = [self.ime()]
        while self >= T.ZAREZ:
            var.append(self.ime())
        self >> T.OZATV
        return var

    start = program
    lexer = ls


def izvrši(funkcije, *argv):
    print('Program je vratio:', funkcije['program'].pozovi(argv))


# AST
# Funkcija: ime:IME parametri:[IME] naredba:naredba
# naredba: Deklaracija: lista:ID
#          Ubaci: lista:ID vrijednost:{arizraz, logizraz} indeks:BROJ
#          UbaciListu: lista:ID lista_ubacena:ID indeks:BROJ
#          Ispisi_listu: lista:ID
#          Izbaci: lista:ID indeks:BROJ
#          Duljina: lista:ID
#          Blok: naredbe:[naredba]
#          Pridruživanje: ime:IME pridruženo:izraz
#          Pridruživanje2: ime1:IME ime2:IME pridruženo:PronađiMrlju
#          PonoviPetlja: varijabla:IME početak:BROJ granica:BROJ inkrement:BROJ tijelo:[naredba]
#          DokPetlja: uvjet: naredba:[naredba]
#          Grananje: uvjet: onda:[naredba] inače:[naredba]
#          Vrati: što:izraz
#          Ispis: što:izraz
#          BrojUListu: broj:arizraz
#          LogUListu: broj:logizraz
# izraz: logizraz: Disjunkcija: disjunkti:[LOGIME]
#                  Konjunkcija: konjunkti:[LOGIME]
#                  LogičkaUsporedba: izrazi:[logizraz]
#                  BrojULog: broj:arizraz
#                  ListuULog: lista:ID
#                  Dohvati: lista:ID indeks:BROJ
#        arizraz: Zbroj: pribrojnici:[arizraz]
#                 Suprotan: od:arizraz
#                 Umnožak: faktori:[arizraz]
#                 Potencija: baza:arizraz eksponent:arizraz
#                 AritmetičkaUsporedba: lijevo:ARIME relacija:MANJE|MANJEJ|JEDNAKOJ|VEĆE|VEĆEJ|RAZLIČITO desno:ARIME|BROJ
#                 LogUBroj: broj:logizraz
#                 ListuUBroj: lista: ID
#                 Dohvati: lista:ID indeks:BROJ
#        Poziv: funkcija:Funkcija argumenti:[izraz]
# element: Lista: elementi:[element]
#          BROJ: Token
#          LOGIME: Token
#          ARIME: Token
# Počisti: ''
# Pomakni: x:arizraz y:arizraz
# Odleti: x:arizraz y:arizraz
# StanjeBaterije: ''
# StanjeSpremnika: ''
# PronađiMrlju: ''

class Funkcija(AST('ime parametri naredba')):
    def pozovi(self, argumenti):
        lokalni = Memorija(dict(zip(self.parametri, argumenti)))
        try:
            self.naredba.izvrši(mem=lokalni)
        except Povratak as exc:
            return exc.preneseno
        else:
            raise GreškaIzvođenja(f'{self.ime} nije ništa vratila')


class Poziv(AST('funkcija argumenti')):
    def vrijednost(self, mem):
        pozvana = self.funkcija
        argumenti = [a.vrijednost(mem) for a in self.argumenti]
        return pozvana.pozovi(argumenti)

    def _asdict(self):  # samo za ispis, da se ne ispiše čitava funkcija
        za_ispis = {'argumenti': self.argumenti}
        za_ispis['*ime'] = self.funkcija.ime
        return za_ispis


class Deklaracija(AST('lista')):
    """Deklaracija liste."""

    def izvrši(self, memorija): memorija[self.lista] = []


class Ubaci(AST('lista element indeks')):
    """Ubacuje vrijednost u listu na zadanom indeksu, ili javlja grešku."""

    def izvrši(self, memorija):
        l, i = memorija[self.lista], self.indeks.vrijednost(memorija)
        if i <= len(l):
            l.insert(i, self.element.vrijednost(memorija))
        else:
            raise self.indeks.iznimka('Prevelik indeks')


class UbaciListu(AST('lista lista_ubacena indeks')):
    """Ubacuje vrijednost u listu na zadanom indeksu, ili javlja grešku."""

    def izvrši(self, memorija):
        l, i = memorija[self.lista], self.indeks.vrijednost(memorija)
        if i <= len(l):
            l.insert(i, memorija[self.lista_ubacena])
        else:
            raise self.indeks.iznimka('Prevelik indeks')


class Izbaci(AST('lista indeks')):
    def izvrši(self, memorija):
        l, i = memorija[self.lista], self.indeks.vrijednost(memorija)
        if i < len(l):
            del l[i]
        else:
            raise self.indeks.iznimka('Prevelik indeks')


class Dohvati(AST('lista indeks')):
    def vrijednost(self, memorija):
        l, i = memorija[self.lista], self.indeks.vrijednost(memorija)
        if i < len(l):
            return l[i]
        else:
            raise self.indeks.iznimka('Prevelik indeks')


class Ispisi_listu(AST('lista')):
    def izvrši(self, memorija):
        l = memorija[self.lista]
        print(l)


class Duljina(AST('lista')):
    """Broj elemenata u listi."""

    def vrijednost(self, memorija): return len(memorija[self.lista])


class Vrati(AST('što')):
    def izvrši(self, mem):
        raise Povratak(self.što.vrijednost(mem))


class Pridruživanje(AST('ime pridruženo')):
    def izvrši(self, mem):
        mem[self.ime] = self.pridruženo.vrijednost(mem)


class Pridruživanje2(AST('ime1 ime2 pridruženo')):
    def izvrši(self, mem):
        mem[self.ime1], mem[self.ime2] = self.pridruženo.vrijednost(mem)


class Izađi(NelokalnaKontrolaToka):
    """Signal koji šalje naredba izađi."""


class Nastavi(NelokalnaKontrolaToka):
    """Signal koji šalje naredba nastavi."""


class Povratak(NelokalnaKontrolaToka):
    """Signal koji šalje naredba vrati."""


class Blok(AST('naredbe')):
    def izvrši(self, mem):
        for naredba in self.naredbe:
            naredba.izvrši(mem)


class PonoviPetlja(AST('varijabla početak granica inkrement tijelo')):
    def izvrši(self, mem):
        kv = self.varijabla  # kontrolna varijabla petlje
        mem[kv] = self.početak.vrijednost(mem)
        while mem[kv] < self.granica.vrijednost(mem):
            try:
                self.tijelo.izvrši(mem)
            except Izađi:
                break
            except Nastavi:
                inkr = self.inkrement
                if inkr is nenavedeno:
                    inkr = 1
                else:
                    inkr = inkr.vrijednost(mem)
                mem[kv] += inkr
                continue
            inkr = self.inkrement
            if inkr is nenavedeno:
                inkr = 1
            else:
                inkr = inkr.vrijednost(mem)
            mem[kv] += inkr


class DokPetlja(AST('uvjet naredba')):  # ne može 'nastavi' u dok petlji, samo 'izađi'
    def izvrši(self, mem):
        while self.uvjet.vrijednost(mem):
            try:
                self.naredba.izvrši(mem)
            except Izađi:
                break


class Grananje(AST('uvjet onda inače')):
    def izvrši(self, mem):
        if self.uvjet.vrijednost(mem):
            self.onda.izvrši(mem)
        else:
            self.inače.izvrši(mem)


class Zbroj(AST('pribrojnici')):
    def vrijednost(self, mem):
        return sum(p.vrijednost(mem) for p in self.pribrojnici)


class Suprotan(AST('od')):
    def vrijednost(self, mem): return -self.od.vrijednost(mem)


class Recipročan(AST('od')):
    def vrijednost(self, mem):
        if self.od.vrijednost(mem) != 0:
            return 1/self.od.vrijednost(mem)
        else:
            raise ArithmeticError('Ne dijeli s nulom')


class Umnožak(AST('faktori')):
    def vrijednost(self, mem):
        p = 1
        for faktor in self.faktori:
            p *= faktor.vrijednost(mem)
        return p


class Disjunkcija(AST('disjunkti')):
    def vrijednost(self, mem):
        vrijednosti = [disjunkt.vrijednost(mem) for disjunkt in self.disjunkti]
        if None in vrijednosti:
            if True not in vrijednosti:
                return None
            else:
                return True
        return any(disjunkt.vrijednost(mem) for disjunkt in self.disjunkti)


class Konjunkcija(AST('konjunkti')):
    def vrijednost(self, mem):
        vrijednosti = [konjunkt.vrijednost(mem) for konjunkt in self.konjunkti]
        if False in vrijednosti:
            return False
        elif None in vrijednosti:
            return None
        return True


class Negacija(AST('od')):
    def vrijednost(self, mem):
        vrijednost = self.od.vrijednost(mem)
        if vrijednost == None:
            return None
        return not vrijednost

    def optim(self):
        ispod_opt = self.od.optim()
        if ispod_opt ^ Negacija:
            return ispod_opt.od
        else:
            return Negacija(ispod_opt)


nula = Token(T.BROJ, '0')
jedan = Token(T.BROJ, '1')
minusjedan = Token(T.BROJ, '-1')


class Potencija(AST('baza eksponent')):
    def vrijednost(self, mem):
        return self.baza.vrijednost(mem) ** self.eksponent.vrijednost(mem)

    def optim(izraz):
        b, e = izraz.baza.optim(), izraz.eksponent.optim()
        if e == nula:
            return jedan
        elif b == nula:
            return nula  # 0^0 je gore, jer prepoznamo sve nule
        elif jedan in {b, e}:
            return b
        else:
            return Potencija(b, e)

    def prevedi(izraz):
        yield from izraz.baza.prevedi()
        yield from izraz.eksponent.prevedi()
        yield ['POW']


class AritmetičkaUsporedba(AST('lijevo relacija desno')):
    def vrijednost(self, mem):
        l = self.lijevo.vrijednost(mem)
        d = self.desno.vrijednost(mem)
        if self.relacija ^ T.JEDNAKOJ:
            return l == d
        elif self.relacija ^ T.RAZLIČITO:
            return not l == d
        elif self.relacija ^ T.MANJE:
            return l < d
        elif self.relacija ^ T.MANJEJ:
            return l < d or l == d
        elif self.relacija ^ T.VEĆE:
            return l > d
        elif self.relacija ^ T.VEĆEJ:
            return l > d or l == d
        else:
            assert False, f'Nepoznata relacija {self.relacija}'


class LogičkaUsporedba(AST('izrazi')):
    def vrijednost(self, mem):
        vrijednosti = [izraz.vrijednost(mem) for izraz in self.izrazi]
        jednaki = vrijednosti.count(vrijednosti[0]) == len(vrijednosti)
        return jednaki


class Ispis(AST('varijable')):
    def izvrši(self, mem):
        if len(self.varijable) == 0:
            print()
        else:
            for var in self.varijable:
                print(var.sadržaj, '=', var.vrijednost(mem), end='\n')


class BrojULog(AST('broj')):
    def vrijednost(self, mem):
        a = self.broj.vrijednost(mem)
        if a > 0:
            return True
        if a < 0:
            return False
        if a == 0:
            return None


class BrojUListu(AST('broj lista')):
    def izvrši(self, memorija):
        a = self.broj.vrijednost(memorija)
        if a != 0:
            memorija[self.lista] = []
            l = memorija[self.lista]
            l.insert(0, a)
        if a == 0:
            memorija[self.lista] = []


class LogUBroj(AST('log')):
    def vrijednost(self, mem):
        a = self.log.vrijednost(mem)
        if a == None:
            return 0
        if a == False:
            return -1
        if a == True:
            return 1


class LogUListu(AST('log lista')):
    def izvrši(self, memorija):
        a = self.log.vrijednost(memorija)
        if a == None:
            memorija[self.lista] = []
        else:
            memorija[self.lista] = []
            l = memorija[self.lista]
            l.insert(0, a)


class ListuUBroj(AST('lista')):
    def vrijednost(self, memorija):
        return len(memorija[self.lista])


class ListuULog(AST('lista')):
    def vrijednost(self, mem):
        a = len(mem[self.lista])
        if a == 0:
            return False
        else:
            return True


class Počisti(AST('')):
    def izvrši(self, mem):
        global okolina
        okolina.počisti()


class Pomakni(AST('x y')):
    def izvrši(self, mem):
        global okolina
        okolina.pomakni(self.x.vrijednost(mem), self.y.vrijednost(mem))


class Odleti(AST('x y')):
    def izvrši(self, mem):
        global okolina
        okolina.odleti(self.x.vrijednost(mem), self.y.vrijednost(mem))


class StanjeBaterije(AST('')):
    def vrijednost(self, mem):
        global okolina
        return okolina.stanje_baterije()


class StanjeSpremnika(AST('')):
    def vrijednost(self, mem):
        global okolina
        return okolina.stanje_spremnika()


class PronađiMrlju(AST('')):
    def vrijednost(self, mem):
        global okolina
        x, y = okolina.pronađi_mrlju()
        if x == -1:
            okolina.stavi_mrlju()
        return okolina.pronađi_mrlju()


primjer1 = ''' 
    Program(){
        x,y = PRONAĐIMRLJU,
        ispis(x,y),
        ODLETI x,y,
        POČISTI,
        baterija = STANJEBATERIJE,
        spremnik = STANJESPREMNIKA,
        ispis(baterija,spremnik),
        vrati Istina
    }
    '''

primjer2 = '''
    Program(){
        lista L3,   $spremamo razinu baterije
        lista L4,   $spremamo kapacitet spremnika
        VidjeliJednoPunjenje = Laž,
        VidjeliJednoPražnjenje = Laž,
        ponovi(brojciscenja=0, brojciscenja < 20, 1){
            ako ((VidjeliJednoPunjenje & VidjeliJednoPražnjenje) == Laž){
                baterija = STANJEBATERIJE,
                ubaci L3 baterija 0,
                spremnik = STANJESPREMNIKA,
                ubaci L4 spremnik 0,
                ako (brojciscenja > 2){
                    nultiBaterija = dohvati L3 0,
                    prviBaterija = dohvati L3 1,
                    $uspoređujemo zadnja 2 stanja baterije - je li bilo punjenje
                    ako (prviBaterija < nultiBaterija)
                        VidjeliJednoPunjenje = Istina,
                    nultiSpremnik = dohvati L4 0,
                    prviSpremnik = dohvati L4 1,
                    $uspoređujemo zadnja 2 stanja spremnika - je li bilo pražnjenje
                    ako (prviSpremnik > nultiSpremnik)
                        VidjeliJednoPražnjenje = Istina,
                },
                $izlazimo tek nakon što se dogodi barem jedno punjenje baterije i barem jedno pražnjenje spremnika
                ako ((VidjeliJednoPunjenje & VidjeliJednoPražnjenje) == Istina) izađi,
                ispis(baterija,spremnik),
                x,y = PRONAĐIMRLJU,
                POMAKNI x,y,
                POČISTI
            },
        },
        baterija = STANJEBATERIJE,
        spremnik = STANJESPREMNIKA,
        ispis(baterija,spremnik),
        ispis (VidjeliJednoPunjenje),
        ispis (VidjeliJednoPražnjenje),
        
        vrati Istina
    }
'''

primjer3 = '''$prikaz rada robota u uredu
    usteda(n){ $n = broj godina
        cijenarobota = 25000,
        cijenajednogpunjenja = 50,
        $pretpostavimo da robot radi 8 sati dnevno (ako se pod prlja samo za vrijeme osmosatnog radnog vremena)
        $neka je u svakom satu, prosijek nastalih mrlja = 2, a punjenje je potrebno nakon svakog 4. ciscenja
        prosijekpunjenjaudanu = 8*2/4,
        nadan = cijenajednogpunjenja * prosijekpunjenjaudanu,
        namjesec = nadan * 25,
        nagodinu = namjesec * 12,
        servis = 0,
        godine = 0,
        $pretpostavimo da je servis/čišćenje robota potrebno obaviti svake 2 godine
        dok(godine < n){
            godine = godine + 2,
            servis = servis + 1000
        },
        $pretportavimo da je osoba koja čisti plaćena 30kn po satu
        osobanadan = 30*8,
        osobanamjesec = osobanadan * 25,
        osobanagodinu = osobanamjesec * 12,
        ušteda = (osobanagodinu - nagodinu ) * n - (cijenarobota + servis),
        vrati ušteda
    }
    Program(){
        lista L1,   $spremamo uštedu
        lista L2,   $spremamo koordinate mrlja
        $prikažimo jedan radni dan u firmi (u prosjeku 16 čišćenja)
        ponovi(brojciscenja=0, brojciscenja < 16, 1){
            baterija = STANJEBATERIJE,
            spremnik = STANJESPREMNIKA,
            ispis(baterija,spremnik),
            x,y = PRONAĐIMRLJU,
            POMAKNI x,y,
            $spremamo sve koordinate mrlja u listu L2
            ubaci L2 y 0,
            ubaci L2 x 0,
            POČISTI
        },
        baterija = STANJEBATERIJE,
        spremnik = STANJESPREMNIKA,
        ispis(baterija,spremnik),
        ponovi(godine = 1, godine < 11, 1){
            ušteda = usteda(godine),
            ubaci L1 ušteda 0
        },
        $ lista L1 prikazuje uštedu u prvih 10 godina (s lijeva na desno od 10. do 1. godine)
        ispisilistu L1,
        u = dohvati L1 0,
        dok( u > 0 ){
            izbaci L1 0,
            u = dohvati L1 0,
            prvihkolikojeminus = koliko L1
        },
        ispis(prvihkolikojeminus),
        ispisilistu L1,         $ispisuje ove godine u kojima nije vidljiva ušteda
        ImaLiOciscenihMrlja = liulog (L2),
        ispis(ImaLiOciscenihMrlja),
        ociscenomrlja = (koliko L2)/2,
        ispis (ociscenomrlja),
        ukupnomrljaudanu = 16,
        ako (ukupnomrljaudanu != ociscenomrlja)
            vrati Laž
        inače vrati Istina
    }
    '''


def izvrši_primjere(lista_ulaza):
    for ulaz in lista_ulaza:
        global okolina
        okolina = Okolina()
        print('-' * 60)
        print(ulaz)
        prikaz(test := P(ulaz))
        izvrši(test)
        print()


def izvrši(funkcije, *argv):
    print('\nProgram je vratio:', funkcije['Program'].pozovi(argv))


primjeri = [primjer1, primjer2, primjer3]


if __name__ == "__main__":
    izvrši_primjere(primjeri)
