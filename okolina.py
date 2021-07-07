from random import randint
import collections
from time import sleep


class Okolina:

    def __init__(self):
        self.robot, self.mrlja, self.prepreka = 'R*x'
        self.pod = [['0']*10 for _ in range(10)]
        self.pod[0][0] = self.robot
        self.baterija = self.max_kapacitet = 300  # pun kapacitet baterije
        self.spremnik = 0  # spremnik koji se puni usisavanjem mrlje, max = 100
        self.max_vrijeme_punjenja = 30  # 30 sekundi za puni kapacitet
        self.inicijalno_stanje = True
        self.stavi_prepreke()
        self.stavi_mrlju()

    def pokaži_pod(self):
        for line in self.pod:
            print(*line)
        print("-"*20)

    def pronađi_robota(self):
        for i, y in enumerate(self.pod):
            for j, z in enumerate(y):
                if self.robot in self.pod[i][j]:
                    return i, j

    def pronađi_mrlju(self):
        for i, y in enumerate(self.pod):
            for j, z in enumerate(y):
                if self.mrlja in self.pod[i][j]:
                    return i, j
        print("Nema mrlje!")
        return -1, -1

    def stanje_baterije(self):
        return self.baterija

    def stanje_spremnika(self):
        return self.spremnik

    def stavi_prepreke(self):  # poziva se samo jednom, inicijalno
        for _ in range(10):  # 10 prepreka na podu
            while(True):
                mjestox, mjestoy = randint(0, 9), randint(0, 9)
                if self.pod[mjestox][mjestoy] not in {self.robot, self.mrlja}:
                    self.pod[mjestox][mjestoy] = self.prepreka
                    break

    def stavi_mrlju(self):
        if self.inicijalno_stanje:
            while(True):
                mjestox, mjestoy = randint(0, 9), randint(0, 9)
                if self.pod[mjestox][mjestoy] not in {self.robot, self.prepreka}:
                    self.pod[mjestox][mjestoy] = self.mrlja
                    self.inicijalno_stanje = False
                    break
        else:
            print(
                "Čekam mrlju...po mojim izračunima trebala bi se pojaviti unutar jedne minute.")
            sleep(randint(1, 60))  # mrlja dolazi nekad unutar minute
            while(True):
                mjestox, mjestoy = randint(0, 9), randint(0, 9)
                if self.pod[mjestox][mjestoy] not in {self.robot, self.prepreka}:
                    self.pod[mjestox][mjestoy] = self.mrlja
                    print("Nastala je nova mrlja.")
                    break

    def počisti(self):
        if self.pronađi_robota() == self.pronađi_mrlju():
            if self.stanje_baterije() >= 10 and self.stanje_spremnika() <= 90:
                print("Čistim mrlju...")
                self.makni_mrlju()
                sleep(3)
                self.spremnik += 10
                self.baterija -= 10
                self.pokaži_pod()
            else:
                if self.stanje_baterije() < 10:
                    print("Moram napuniti bateriju!")
                    self.napuni_bateriju()
                    self.počisti()
                else:
                    print("Moram isprazniti spremnik!")
                    self.isprazni_spremnik()
                    self.počisti()
        else:
            print("Tu gdje se nalazim nema mrlje!")

    def pomakni(self, x, y):
        if (x, y) != self.pronađi_mrlju():
            print("Tamo nije mrlja, a ja ne trošim bateriju bespotrebno!")
        else:
            if self.pronađi_mrlju() == self.pronađi_robota():
                return
            else:
                path = self.bfs(self.pod, self.pronađi_robota())
                if path == None:  # postoje barikade
                    print(
                        "Okružen sam preprekama! Ne mogu se pomaknuti na željenu poziciju...")
                    return 0
                else:  # postoji najkraći put
                    path.pop(0)  # makni poziciju na kojoj se nalazi robot
                    duljina = len(path)
                    print("Duljina puta: ", duljina)
                    print("Koordinate puta: ", path)
                    if duljina <= 10:
                        for pozicija in path:  # pomiče se polje po polje
                            i, j = pozicija
                            self.jedan_pomak(i, j, 5)
                            duljina -= 1
                            self.pokaži_pod()
                        return 1
                    else:  # inače je utrošak baterije veći od 10*5=50 pa je efikasnije odletjeti, čiji je utrošak 50
                        print("Više mi se isplati odletjeti...letim!")
                        self.odleti(x, y)

    def jedan_pomak(self, x, y, utrošak):
        if self.stanje_baterije() >= utrošak:  # ima dovoljno energije
            robotx, roboty = self.pronađi_robota()
            if self.pod[robotx][roboty] == self.robot:
                self.pod[robotx][roboty] = '0'
                if self.pod[x][y] == self.mrlja:
                    self.pod[x][y] += self.robot
                else:
                    self.pod[x][y] = self.robot
                self.baterija -= utrošak
                sleep(1)
            else:  # inače je bio na mrlji
                self.pod[robotx][roboty] = self.pod[robotx][roboty].replace(
                    self.robot, '')  # obriši R iz stringa
                if self.pod[x][y] == self.mrlja:
                    self.pod[x][y] += self.robot
                else:
                    self.pod[x][y] = self.robot
                self.baterija -= utrošak
                sleep(1)
        else:
            print("Moram prvo napuniti bateriju!")
            self.napuni_bateriju()
            self.jedan_pomak(x, y, utrošak)

    def odleti(self, x, y):
        if (x, y) != self.pronađi_mrlju():
            print("Tamo nije mrlja, a ja ne trošim bateriju bespotrebno!")
            return 0
        else:
            self.jedan_pomak(x, y, 50)
            self.pokaži_pod()
            return 1

    def makni_mrlju(self):
        mrljax, mrljay = self.pronađi_mrlju()
        self.pod[mrljax][mrljay] = self.pod[mrljax][mrljay].replace(
            self.mrlja, '')

    def napuni_bateriju(self):
        trenutno = self.stanje_baterije()
        za_napuniti = self.max_kapacitet - trenutno
        postotak = za_napuniti/self.max_kapacitet
        print("Punim bateriju! Ovo može potrajati neko vrijeme...")
        sleep(postotak*self.max_vrijeme_punjenja)
        self.baterija = self.max_kapacitet
        print("Baterija puna!")

    def isprazni_spremnik(self):
        sleep(1)
        self.spremnik = 0

    def bfs(self, grid, start):  # algoritam pretraživanja u širinu za pronalazak najkraćeg puta
        queue = collections.deque([[start]])
        seen = set([start])
        while queue:
            path = queue.popleft()
            x, y = path[-1]
            if grid[x][y] == self.mrlja:
                return path
            for x2, y2 in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                if 0 <= x2 < 10 and 0 <= y2 < 10 and grid[x2][y2] != self.prepreka and (x2, y2) not in seen:
                    queue.append(path + [(x2, y2)])
                    seen.add((x2, y2))


"""
if __name__ == "__main__":
    okolina = Okolina()
    okolina.pokaži_pod()
    # ovo je primjer kad je robot okružen preprekama
    okolina.pod[0][1] = okolina.prepreka
    okolina.pod[1][0] = okolina.prepreka
    okolina.pokaži_pod()
    print('-' * 20)
    x, y = okolina.pronađi_mrlju()
    a = okolina.pomakni(x, y)
    if not a:
        okolina.odleti(x, y)
    okolina.počisti()
"""
