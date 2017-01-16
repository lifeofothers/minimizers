##
#TEMA: MINIMIZATORI
#Programski kod koji generira minimizatore iz ulazne datoteke.
#Datoteka, kao i velicina miniimzatora(k), broj minimizatora koji se provjeravaju u svakom koraku(w), te velicina podnizova ulaznog niza na kojem zelimo naci minimizatore
#       zadaju se preko komandne linije. Primjer poziva programa uz k = 20, w = 15, te velicina podniza 60 nad datotekom e_coli.fa: >python minimizer_python_2.py e_coli.fa 20 15 60 
#Program nakon izvrsavanja ispisuje broj pronadenih minimizatora, kao i vrijeme izvodenja na konzolu, a pronadene minimizatore zapisuje u datoteku minimizers.txt
#
#Sven Srebot
##
import sys
import time
from collections import defaultdict
from memory_profiler import profile


#
#Klasa fifio sluzi za ostvarenje pomicnog prozora odredene velicine. Velicina prozora ovisna je o parametrima s kojima se pokrece program (k + w - 1), te
#kada se popunjenom prozoru dodaje simbol, on izbacuje simbol na krajnjoj lijevoj poziciji, te dodaje novi simbol na krajnju desnu poziciju.
#
class fifo():
    def __init__(self, w, k):
        self.list = []
        self.w = w
        self.k = k
        self.size = self.w + self.k - 1
    def add(self, val):
        if len(self.list) == self.size:
            self.list = self.list[1:]
        self.list.append(val)
    def last_k_1(self):
        return self.list[w:]

#
#Klasa minimizer() u kojuj su ostvarene sve funkcije koje sudjeluju u stvaranju minimizatora
#

class minimizer():
    def __init__(self, w, k, file_name, sub_size):
        self.w = w
        self.k = k
        self.num = 0
        self.input = []
        self.size = self.w + self.k - 1
        self.window = fifo(w, k)
        self.sub_size = sub_size
        self.br = 0
        self.minimized_dict = defaultdict(list)
        self.file = open(str(file_name), "r")
        self.lessA = ["C"]
        self.lessT_U = ["C", "A"]
        self.lessG = ["C", "A", "T", "U"]
        self.all = ["C", "A", "T", "U", "G"]
        self.lessT1 = ["G"]
        self.lessA1 = ["G", "T"]
        self.lessC1 = ["G", "T", "A"]
        self.i = 0
        
    def read_n(self, n):
        for a in range(0, n):
            new = self.file.read(1)
            if new == "\n":
                break
            else:
                self.window.add(new)
        return (a + 1)

    #
    #Funkcija reverse_compl() se poziva nakon sto je zavrseno stvaranje minimizatora nad ulaznim nizom, te je zaduzena za stvaranje reverznog komlementa ulaznog niza
    #

    def reverse_compl(self):
        #print self.input
        rev1 = reversed(self.input)
        rev = []
        self.input = []
        for a in rev1:
            rev.append(a)
        for a in rev:
            if a == "A":
                self.input.append("T")
            elif a == "C":
                self.input.append("G")
            elif a == "G":
                self.input.append("C")
            elif a == "T" or a == "U":
                self.input.append("A")
        return
            
    #
    #Funkcija compare() usporeduje minimizator koji je pronaden u trenutnom prozoru sa novim potencijalnim minimizatorom
    #Pri usporedivanju ne usporeduje nizove abecedno, nego: za parne pozicije minimizera (0, 2, 4, 6, ...) najmanju tezinu ima slovo C, zatim A, zatim T pa G
    #                                                       za neparne pozicije minimizera(1, 3, 5, 7, ...) najmanju tezinu ima slovo G, zatim T, pa A, pa C    
    #Sukladno navedenom najmanji moguci niz duzine 3 je 'CGC', a najveci 'GCG'
    #
    def compare(self, i):
        pos = i + self.k
        last_position = 0
        same = 0
        for j in range(0, self.k):
            i_j = i + j
            if j%2 == 0:
                if self.best[j] == self.window.list[i_j]:
                    if same == 0:
                        last_position = (self.p + i)
                    same = same + 1
                    if same == self.k and self.last_position != last_position:
                        self.best = self.window.list[i:pos]
                        self.position = i
                        break
                    continue
                elif j == 0 or same >= j:
                    if self.best[j] not in self.all and self.window.list[i_j] in self.all:
                        self.best = self.window.list[i:pos]
                        self.position = i
                        break
                    elif self.best[j] == "C":
                        break
                    elif self.best[j] == "A":
                        if self.window.list[i_j] in self.lessA:
                            self.best = self.window.list[i:pos]
                            self.position = i
                            break
                    elif self.best[j] == "T" or self.best == "U":
                        if self.window.list[i_j] in self.lessT_U:
                            self.best = self.window.list[i:pos]
                            self.position = i
                            break
                    elif self.best[j] == "G":
                        if self.window.list[i_j] in self.lessG:
                            self.best = self.window.list[i:pos]
                            self.position = i
                            break
                    else:
                        break
                else:
                    break
            else:
                if self.best[j] == self.window.list[i_j]:
                    if same == 0:
                        last_position = (self.p + i)
                    same = same + 1
                    if same == self.k and self.last_position != last_position:
                        self.best = self.window.list[i:pos]
                        self.position = i
                        break
                    continue
                elif j == 0 or same >= j:
                    if self.best[j] not in self.all and self.window.list[i_j] in self.all:
                        self.best = self.window.list[i:pos]
                        self.position = i
                        break
                    elif self.best[j] == "G":
                        break
                    elif self.best[j] == "T" or self.best[j] == "U":
                        if self.window.list[i_j] in self.lessT1:
                            self.best = self.window.list[i:pos]
                            self.position = i
                            break
                    elif self.best[j] == "A":
                        if self.window.list[i_j] in self.lessA1:
                            self.best = self.window.list[i:pos]
                            self.position = i
                            break
                    elif self.best[j] == "C":
                        if self.window.list[i_j] in self.lessC1:
                            self.best = self.window.list[i:pos]
                            self.position = i
                            break
                    else:
                        break
                else:
                    break

    #
    #Funkcija check_all() trazi najbolju k-torku cijelog prozora visestruko pozivajuci funkciju compare(). Poziva se kada minimizator ispadne iz prozora ili na pocetku izvodenja algoritma
    #
    
    def check_all(self):
        self.best = self.window.list[0:self.k]
        best = []
        best = self.best
        for i in range(1, self.w):
            self.compare(i)
        if best != self.best:
            pass
        else:
            self.position = 0
        return
    #
    #Funkcija check() provjerava da li je zadnja k-torka u prozoru bolja od zadnjeg dodanog minimizatora, te ako je postaje novi minimizator.
    #
        
    def check(self):
        i = self.size - self.k
        self.compare(i)
        return

    #
    #check_pos_substring() provjerava da li je prozor dosao do kraja podniza koji provjeravamo, ako je vraca 1, inace 0
    #

    def check_pos_substring(self):
        if (self.pos_substring % (self.sub_size)) == 0 and self.pos_substring != 0:
            return 1
        else:
            return 0

    #
    #Funkcija minimize() poziva funkciju za obradivanje podniza za svaki podniz ulazne datoteke
    #

    def minimize(self, checker, inverz):
        self.inverz = inverz
        self.i = self.i + 1
        self.last_position = -1
        self.pos_substring = 0
        self.no_substring = 0
        result, checker = self.process_substring(checker)
        while result == 1 and checker == 0:
            self.no_substring = self.no_substring + 1
            self.best = []
            self.last_position = -1
            self.pos_substring = 0
            self.window.list = []
            result, checker = self.process_substring(checker)
        self.file.close()
        return result, checker
    #
    #Funkcija end() stvara krajnji minimizator
    #
    
    def end(self):
        l = len(self.window.list)
        k_end = self.window.list[(l - self.k):]
        if k_end != self.best:
            self.best = k_end
            self.b = ""
            for a in k_end:
                self.b = self.b + str(a)
            self.minimized_dict[self.b].append((self.no_substring, self.pos_substring - self.k, self.inverz))
            self.num = self.num + 1

    #
    #Funkcija process_substring() ucitava nove simbole dok ne dode do kraja podniza, dok ucitava znakove, pomice prozor i na njima trazi minimizatore
    #
    
    def process_substring(self, checker):
        max_size = 0
        k_end = []
        if checker == 1:
            new = ">"
        else:
            new = self.file.read(1)
        if new == "\n" or new == " " or new == "":
            new = self.file.read(1)
            if new == "\n" or new == " " or new == "":
                return 1, 1
        br = 0
        self.p = 1
        if new == ">":
            self.com = self.file.readline()
            new = self.file.read(1)
        self.window.add(new)
        self.input.append(new)
        self.br = self.br + 1
        self.pos_substring = self.pos_substring + 1
        max_size = self.check_pos_substring()
        best = 0
        case = 0
        e = 0;
        lp = -1
        while new in self.all:
            new = self.file.read(1)
            before = self.window.list
            if new == "\n" or new == " " or new == "":
                new = self.file.read(1)
                if new == "\n" or new == " " or new == "":
                    return 1, 1
            if new == ">":
                return 2, 1
            if new in self.all:
                self.window.add(new)
                self.p = self.p + 1
            else:
                return 1, 1
            if self.inverz == 0:
                self.input.append(new)
            self.br = self.br + 1
            self.pos_substring = self.pos_substring + 1
            max_size = self.check_pos_substring()
            if (len(self.window.list) == self.k and e == 0):
                self.position = 0
                k_start = self.window.list[0:self.k]
                self.best = k_start
                self.b = ""
                for a in self.best:
                    self.b = self.b + str(a)
                self.minimized_dict[self.b].append((self.no_substring, 0, self.inverz))
                self.num = self.num + 1
                self.best = k_start
                best = self.best
                e = 1
            if len(self.window.list) == self.size:
                lp = self.last_position
                self.check_all()
                if ((best == 0) or (best != self.best) or (best == self.best and lp != self.last_position)):
                    self.b = ""
                    for a in self.best:
                        self.b = self.b + str(a)
                    self.minimized_dict[self.b].append((self.no_substring, self.pos_substring - self.size + self.position, self.inverz))
                    self.num = self.num + 1
                    self.last_position = self.pos_substring - self.size + self.position
                pos = self.position
                case = 0
                if max_size == 0:
                    for check in range(0, pos):
                        new = self.file.read(1)
                        if new == "\n" or new == " " or new == "":
                            new = self.file.read(1)
                            if new == "\n" or new == " " or new == "":
                                return 1, 1
                        if new == ">":
                            return 2, 1
                        if new in self.all:
                            if self.inverz == 0:
                                self.input.append(new)
                            self.br = self.br + 1
                            self.window.add(new)
                            self.pos_substring = self.pos_substring + 1
                            max_size = self.check_pos_substring()
                            self.p = self.p + 1
                            best = self.best
                            lp = self.last_position
                            self.check()
                            if (best != self.best) or (best == self.best and lp != self.last_position):
                                self.b = ""
                                for a in self.best:
                                    self.b = self.b + str(a)
                                self.minimized_dict[self.b].append((self.no_substring, self.pos_substring - self.size + self.position, self.inverz))
                                self.num = self.num + 1
                                self.last_position = self.pos_substring - self.size + self.position
                                case = 1
                        if max_size == 1:
                            self.end()
                            max_size = 0
                            return 1, 0
                else:
                    self.end()
                    max_size = 0
                    return 1, 0
                best = self.best
                lp = self.last_position
            if max_size == 1:
                self.end()
                max_size = 0
                return 1, 0
        if new == ">":
            return 2, 1
        return 1, 0
    #
    #Funkcija print_dict() u file zapisuje sve minimizatore koji su pronadeni
    #
    
    def print_dict(self, output):
        for key in self.minimized_dict:
            output.write( key + ": " + "\n")
            for value in self.minimized_dict[key]:
                for a in range(0, self.k):
                    output.write(" ")
                output.write("(" + str(value[0]) + ", " + str(value[1]) + ", " + str(value[2]) + ")" + "\n")
#
#Funkcija main() poziva funkciju minimaze() prvo za ulazni niz podataka, a nakon toga za inverzni komplement ulaznog niza, te nakon toga ispisuje minimizatore u datoteku
#   te racuna vrijeme izvodenja.
#
@profile
def main(argv):
    start = time.time()
    file_name = str(sys.argv[1])
    k = int(sys.argv[2])
    w = int(sys.argv[3])
    sub_size = int(sys.argv[4])
    checker = 0
    out = "minimizers.txt"
    output = open(out, "w+")
    minimizer1 = minimizer(w, k, file_name, sub_size)
    result, checker = minimizer1.minimize(0, 0)
    minimizer1.window.list = []
    while result == 2:
        result, checker = minimizer1.minimize(checker, 0)
        output.write(str(minimizer1.com) + "\n")
        minimizer1.minimized = []
        minimizer1.window.list = []
        if result != 2:
            new = minimizer1.file.read(1)
    minimizer1.reverse_compl()
    minimizer1.window.list = []
    complement = "complement.txt"
    compl = open(complement, "w+")
    compl.write(">" + str(minimizer1.com))
    for element in minimizer1.input:
        compl.write(str(element))
    compl.close()
    minimizer1.file = open("complement.txt", "r")
    result, checker = minimizer1.minimize(0, 1)
    minimizer1.minimized = []
    minimizer1.window.list = []
    while result == 2:
        result, checker = minimizer1.minimize(checker, 1)
        minimizer1.minimized = []
        minimizer1.window.list = []
        if result != 2:
            new = minimizer1.file.read(1)
    end = time.time()
    print "Number of minimizers(total): ", minimizer1.num
    print "Time:  " + str((round(end - start, 5))) + " s"
    minimizer1.print_dict(output)
    return

if __name__ == "__main__":
   main(sys.argv[1:])
























                        






                            
