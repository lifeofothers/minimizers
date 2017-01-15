def print_miniz(count):
    for m in miniz[:count]:
        print(m)
##        print(m.s, m.getNumber())

class Triple():
    def __init__(self, s=0, i=-1, p=-1):
        global unused_triples
        self.s = s
        self.i = i
        self.p = p
        #print([iii])
        unused_triples += 1
    def __lt__(self, other):
        return self.s < other.s

    def __repr__(self):
        return '({0}, {1}, {2})'.format(self.s, self.i, self.p)

class Minimizer():
    locations = []
    def __init__(self, s=0, loc=[]):
        self.s = s
        self.locations = [loc]

    def __lt__(self, other):
        return self.s < other.s

    def __repr__(self):
        return '({0}, {1})'.format(self.s, self.locations)

    def get_locations(self):
        return self.locations

    def extend(self, loc=[]):
        if not loc in self.locations:
            self.locations.append(loc)

    def add_locations(self, locs=[[]]):
        for L in locs:
            if not L in self.locations:
                self.locations.append(L)

    def get_number(self):
        return len(self.locations)

def get_RC(sequence):
    table = ['A', 'C', 'G', 'T']
    sequence = list(sequence)
    for i in range(len(sequence)):
        sequence[i] = table[3 - table.index(sequence[i])]
    return ''.join(sequence[::-1])

# returns smallest of the kmers from the list
def get_minimizer(kmers):
    kmers = sorted(kmers)

    result = Minimizer(kmers[0].s, [kmers[0].i, kmers[0].p])
    #print(result)
    for k in kmers[1:]:
        if k.s == result.s:
            result.extend([k.i, k.p])
            #print(result)
        else:
            break

    return result

def get_triples(begin, end, i, w, k):
    # returns a list of (s, i, p) triples (any) using window w
    global strings

    if begin >= 0 and end > 0: # prefix or substring
        T = strings[0][begin:end]
    elif begin == -1 and end > 0: # suffix
        T = strings[0][-end+1::1]

    #print(T)
    result = []
    L = w + k - 1 # how many it will process to find 1 k-mer
    #print(get_triples(T[1:], i, window, k))
    for p in range(w):
        # left end minimizer
        if begin != -1:
            # making sure we didn't go go past last possible k-mer
            if len(T[p:]) >= k:
                #print(T[p:])
                triple = Triple(''.join(T[p:p + k]), i, p + begin)
                #print(triple)
                result.append(triple)                                                         # p + i ??
            else:
                break
        # right end minimizer
        else:
            # FIX THIS TO TAKE THE RIGHT RIGHT END MINIMIZER
            #print(T[-end:])
            #triple = Triple(''.join(T[p:p + k]), i, len(T) - end)
            #print(end)
            #print()
            if len(T[p:]) >= k:
                triple = Triple(''.join(T[p:p+k]), i, len(T) - k)
                #                                                   ^ hack
                #print(triple)
                result.append(triple)
    return result

def get_interior_minimizers(read_number, w, k):
    global strings
    global miniz
    global unused_triples

    L = w + k - 1
    T = strings[0]
    #print('Interior minimizers:')
    for i in range(0, len(T) - L + 1):
        kmers = get_triples(i, i+L, read_number, w, k)
        #print(kmers)
        #[print(km) for km in kmers]
        miniCands = get_minimizer(kmers)

        exists = False
        # check if the minimizer exists
        for m in miniz:
            # not in list
            if m.s > miniCands.s:
                exists = False
                break
            if m.s == miniCands.s:
                #print(m.s + ' exists')
                exists = True
                break
##        print(skip)

        # add it if it's the first one of the kind
        if not exists:
            #print('inserting ' + str(miniCand))
            #minimizers.append(miniCand)
            locs = miniCands.get_locations()
            temp = Minimizer(miniCands.s, [locs[0][0], locs[0][1]])
            temp.add_locations(locs)
            unused_triples -= 1
            #miniz.append(temp)
            insort(miniz, temp)
            #print(temp)
        # extend the minimizer with the same string
        else:
            for m in miniz:
                # when we find a match
                if miniCands.s == m.s:
                    #print(m.s)
                    # if it doesn't have that location, extend it
                    locs = miniCands.get_locations()
                    m.add_locations(locs)
                    break

##    for m in minimizers:
##        print(m)

def get_end_minimizers(read_number, k, left=True):
    global strings
    global miniz
    global unused_triples

    T = strings[0]

    max_u = len(T) - k + 1
    for u in range(1, max_u + 1):
        L = u + k - 1
        #print('End minimizers:')
        for i in range(0, len(T) - L + 1):
            if left:
                kmers = get_triples(0, u + k, read_number, u, k)
            else:
                kmers = get_triples(-1, u + k, read_number, u, k)
            #[print(km) for km in kmers]
            miniCands = get_minimizer(kmers)

            exists = False
            # check if the minimizer exists
            for m in miniz:
                if m.s == miniCands.s:
                    #print(m.s + ' exists')
                    exists = True
                    break
    ##        print(skip)

            # add it if it's the first one of the kind
            if not exists:
                #print('inserting ' + str(miniCand))
                #minimizers.append(miniCand)
                locs = miniCands.get_locations()
                temp = Minimizer(miniCands.s, [locs[0][0], locs[0][1]])
                temp.add_locations(locs)
                unused_triples -= 1
                insort(miniz, temp)
##                miniz.append(temp)
                #print(temp)
            # extend the minimizer with the same string
            else:
                for m in miniz:
                    # when we find a match
                    if miniCands.s == m.s:
                        # if it doesn't have that location, extend it
                        locs = miniCands.get_locations()
                        m.add_locations(locs)
                        break
    return

from bisect import insort, bisect_left

#@profile
def main():
    import time
    import sys
##    from bisect import insort, bisect_left

    start = time.time()

    global read_n

    with open('ecoli10k.fa', 'r') as f:
        for line in f:
            line = line.strip()
            if len(line) > 0: # not empty line?
                if line[0] == '>': # comment?
                    print(line)
                    print()
                else: # sequence
                    # for k = 20 and L = 60, max w is 41
                    # L = k + w - 1
                    w = 20
                    k = 20
                    
                    usingRC = False
                    strings[0] = line#'GGGTACGTCCACGT'#'2310321012331011'
                    #print(line)
                    get_interior_minimizers(read_n, w, k)
##                    get_end_minimizers(read_n, k, True)
##                    get_end_minimizers(read_n, k, False)
##                    print('ORG:')
##                    print_miniz(20)
##                    miniz = []

                    usingRC = True
                    strings[0] = get_RC(line)#get_RC('GGGTACGTCCACGT')#'2310321012331011'
##                    #print(line)
                    get_interior_minimizers(read_n, w, k)
##                    get_end_minimizers(read_n, k, True)
##                    get_end_minimizers(read_n, k, False)
##                    print('RC:')
##                    print_miniz(20)
##                    miniz = []

                    #break
                    if read_n % 10 == 0:
                        print('Read ' + str(read_n) + '...')
                    read_n += 1
        #minimizers = sorted(minimizers)

    print('%d distinct miniz in total' % len(miniz))
    print_miniz(20)

    end = time.time()
    print('Time taken: %s seconds' % (end-start))
    # assuming 1 byte per letter
    memory = k * len(miniz)
    for m in miniz:
        # assuming 1 byte per index per location
        memory += 2 * len(m.get_locations())
    print('Memory used: %s B' % memory)

strings = ['']
miniz = []
read_n = 0
unused_triples = 0

if __name__ == '__main__':
    main()
##    print(str(unused_triples) + ' triples needlessly created')
          
