"""Python script for reducing storage requirements for biological
sequence comparison. Takes one argument i.e. the filename of the
organism whose sequence you are processing. The file must be in FASTA
format."""
import time
import sys

from bisect import insort


def print_minimizers(count):
    """Prints count first minimizers."""
    for minimizer in MINIMIZERS[:count]:
        print(minimizer)

class Minimizer():
    """A class containing the string of a minimizer and all locations it
        was found at (as well as the direction)."""

    def __init__(self, string, loc):
        """String should be k characters long, loc should contain
              only one pair of coordinates i.e. [i, p]."""
        self.string = string
        self.locations = [loc]

    def __lt__(self, other):
        return self.string < other.string

    def __eq__(self, other):
        return self.string == other.string

    def __repr__(self):
        return '({0}, {1})'.format(self.string, self.locations)

    def add_location(self, loc):
        """ Add a pair of coordinates to the minimizer. loc should
              contain two elements [i, p], where p is read number and i
              is offset in that read."""
        if loc not in self.locations:
            self.locations.append(loc)

    def get_locations(self):
        """Returns an array of all location pairs."""
        return self.locations

    def get_number(self):
        """Returns the number of locations on which this minimizer was
              found."""
        return len(self.locations)

    def has_location(self, loc):
        """Returns True if the minimizer exists with location loc."""
        return loc in self.locations

def get_rc(sequence):
    """Returns the reverse complement of sequence. Sequence may only
        contain letters A, C, G, or T."""
    table = ['A', 'C', 'G', 'T']

    sequence = list(sequence)
    for key, value in enumerate(sequence):
        sequence[key] = table[3 - table.index(value)]

    return ''.join(sequence[::-1])

def get_minimizer_string_index(string):
    """Returns the index of a minimizer defined by string if the
         minimizer is present. Returns -1 otherwise."""
    left = 0
    right = len(MINIMIZERS) - 1
    while True:
        if left > right:
            return -1
        index = int((left + right) / 2)
        if MINIMIZERS[index].string < string:
            left = index + 1
        elif MINIMIZERS[index].string > string:
            right = index - 1
        else:
            return index

def get_minimizer_from_window(begin_index, end_index, i, w, k):
    """Returns all minimizers for the window[begin_index:end_index]."""
    current_window = CURRENT_READ[begin_index:end_index]

    minimizer = None
    for p in range(w):
        # making sure we didn't go past the last possible k-mer
        if len(current_window[p:]) >= k:
            temp = Minimizer(''.join(current_window[p:p + k]), [i, p + begin_index])
        else:
            break

        if minimizer is None:
            minimizer = temp
        elif temp.string < minimizer.string:
            minimizer = temp
        elif temp.string == minimizer.string:
            for loc in temp.get_locations():
                minimizer.add_location(loc)

    return minimizer

def get_minimizer_lookalike(minimizer):
    """Returns the minimizer with the same string, None if not found."""
    index = get_minimizer_string_index(minimizer.string)

    return MINIMIZERS[index] if index != -1 else None

def get_end_minimizers(k):
    """Saves left and right k-end-minimizers for the current read."""
    left_minimizer = Minimizer(CURRENT_READ[:k], [READ_NUMBER, 0])
    right_minimizer = Minimizer(CURRENT_READ[-k:], [READ_NUMBER, len(CURRENT_READ) - k])

    if not get_minimizer_lookalike(left_minimizer):
        insort(MINIMIZERS, left_minimizer)
        #MINIMIZERS.append(left_minimizer)
##        temp[left_minimizer.string] = left_minimizer
    if not get_minimizer_lookalike(right_minimizer):
        insort(MINIMIZERS, right_minimizer)
        #MINIMIZERS.append(right_minimizer)
##        temp[right_minimizer.string] = right_minimizer

#@profile
def get_interior_minimizers(w, k):
    """Saves all interior minimizers for the window size = w + k - 1."""
    window_size = w + k - 1
    for i in range(0, len(CURRENT_READ) - window_size + 1):
        minimizer = get_minimizer_from_window(i, i + window_size, READ_NUMBER, w, k)

        lookalike = get_minimizer_lookalike(minimizer)
        # add it if it's the first one with that sting
        if lookalike is None:
            insort(MINIMIZERS, minimizer)
            #MINIMIZERS.append(minimizer)
            #temp[minimizer.string] = minimizer
        # else extend the minimizer that has the same string
        else:
            # if it doesn't have that location, extend it
            for loc in minimizer.get_locations():
                if not lookalike.has_location(loc):
                    lookalike.add_location(loc)
                    break

#@profile
def main():
    """Main method that calls everything else that gets the job done."""
    global READ_NUMBER
    global CURRENT_READ
    global USING_RC

    start = time.time()

    w = 20
    k = 20

    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'ecoli100k.fa'
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if len(line) > 0:
                if line[0] == '>':
                    print(line)
                    print()
                else:
                    USING_RC = False
                    CURRENT_READ = line
                    get_interior_minimizers(w, k)
                    get_end_minimizers(k)

                    USING_RC = True
                    CURRENT_READ = get_rc(line)
                    get_interior_minimizers(w, k)
                    get_end_minimizers(k)

                    if READ_NUMBER % 10 == 0:
                        print('Read ' + str(READ_NUMBER) + '...')

                    READ_NUMBER += 1

    print('%d distinct minimizers in total' % len(MINIMIZERS))
    print_minimizers(20)

    # assuming 1 byte per letter
    memory = k * len(MINIMIZERS)
    for minimizer in MINIMIZERS:
        # assuming 1 byte per index per location
        memory += 2 * len(minimizer.get_locations())
    print('Memory used: %s B' % memory)

    end = time.time()
    total_time = end - start
    print('Total time taken: %.3f seconds (%.3f seconds per read)' % \
          (total_time, total_time / READ_NUMBER))

CURRENT_READ = ''
MINIMIZERS = []
READ_NUMBER = 0
USING_RC = False

if __name__ == '__main__':
    main()
