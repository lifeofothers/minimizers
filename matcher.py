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
    result = Minimizer(kmers[0].s, [kmers[0].i, kmers[0].p])
    #print(result)
    for k in kmers[1:]:
        if k.s == result.s:
            result.extend([k.i, k.p])
            #print(result)
        else:
            break

    return result

def get_triples(begin_index, end_index, i, w, k):
    # returns a list of (s, i, p) triples (any) using window w
    global current_read
    global get_triples_time
    global wcount

    start = time.time()

    current_window = current_read[begin_index:end_index]

    #print(T)
    result = []
    #L = w + k - 1 # how many it will process to find 1 k-mer
    #print(get_triples(T[1:], i, window, k))
    for p in range(w):
        # making sure we didn't go go past last possible k-mer
        if len(current_window[p:]) >= k:
            #print(T[p:])
            wcount += 1
            temp = Triple(''.join(current_window[p:p + k]), i, p + begin_index)# p + i ??
            
            #print(triple)
        else:
            break
        
        if len(result) == 0:
            result.append(temp)
        elif temp.s < result[0].s:
            result = [temp]
        elif temp.s == result[0].s:
            result.append(temp)
        #insort(result, temp)
    get_triples_time += (time.time() - start)
##    for r in result:
##        print(r)
##    print()
    
    return result

def minimizer_exists(minimizer):
    global minimizer_exists_time

    start = time.time()
    
    # check if the minimizer exists
    for m in miniz:
        # not in list
        if m.s > minimizer.s:
            minimizer_exists_time += (time.time() - start)
            return False
        if m.s == minimizer.s:
##            print(m.s + ' exists')
            minimizer_exists_time += (time.time() - start)
            return True

def get_end_minimizers(read_number, k):
    global unused_triples
    global current_read
    global total_ender_time

    start = time.time()

    left_minimizer = Minimizer(current_read[:k], [read_number, 0])
    right_minimizer = Minimizer(current_read[-k:], [read_number, len(current_read) - k])
        
    if not minimizer_exists(left_minimizer):
        insort(miniz, left_minimizer)
        unused_triples -= 1
    if not minimizer_exists(right_minimizer):
        insort(miniz, right_minimizer)
        unused_triples -= 1

    total_ender_time += (time.time() - start)

wcount = 0
##@profile
def get_interior_minimizers(read_number, w, k):
    global miniz
    global unused_triples

    global total_inter_time

    start = time.time()

    L = w + k - 1
    #print('Interior minimizers:')
    for i in range(0, len(current_read) - L + 1):
        kmers = get_triples(i, i + L, read_number, w, k)
        #print(kmers)
        #[print(km) for km in kmers]
        if len(kmers) > 1:
            print(kmers)
        miniCands = get_minimizer(kmers)

        # add it if it's the first one of the kind
        if not minimizer_exists(miniCands):
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
    total_inter_time += (time.time() - start)
    
##@profile
from bisect import insort, bisect_left
import time

#@profile
def main():
##    import time
##    from bisect import insort, bisect_left


    global read_n
    global current_read
    global miniz
    global using_RC
    global wcount

    # for k = 20 and L = 60, max w is 41
    # L = k + w - 1
    w = 20
    k = 20
    
    with open('ecoli10k.fa', 'r') as f:
        for line in f:
            line = line.strip()
            if len(line) > 0: # not empty line?
                if line[0] == '>': # comment?
                    print(line)
                    print()
                else: # sequence

                    wcount = 0

                    using_RC = False
                    current_read= line
                    get_interior_minimizers(read_n, w, k)
                    get_end_minimizers(read_n, k)

                    using_RC = True
                    current_read = get_RC(line)
                    get_interior_minimizers(read_n, w, k)
                    get_end_minimizers(read_n, k)

##                    break

                    if read_n % 10 == 0:
                        print('Read ' + str(read_n) + '...')

                    read_n += 1
                    
    print('%d distinct miniz in total' % len(miniz))
    print_miniz(20)

    # assuming 1 byte per letter
    global memory
    memory = k * len(miniz)
    for m in miniz:
        # assuming 1 byte per index per location
        memory += 2 * len(m.get_locations())
    print('Memory used: %s B' % memory)

current_read = ''
miniz = []
read_n = 0
using_RC = False
unused_triples = 0
memory = 0

total_inter_time = 0
total_ender_time = 0
get_triples_time = 0
minimizer_exists_time = 0

if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    total_time = end - start
    print('Total time taken: %.3f seconds (%.3f seconds per read)' % (total_time, total_time / read_n))
    print('    get_interior_minimizers: %.3f seconds' % total_inter_time)
    print('    get_end_minimizers: %.3f seconds' % total_ender_time)
    print('        get_triples: %.3f seconds' % get_triples_time)
    print('        minimizer_exists: %.3f seconds' % minimizer_exists_time)
    print('Unused triples: %d' % unused_triples)
##    print(str(unused_triples) + ' triples needlessly created')
          
