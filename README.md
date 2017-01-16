# Minimizers
This is a program written in Python3 for reducing storage requirements for biological sequence comparison which consist of one script file:
* main.py

Currently, this script works with FASTA files and supports only creation of DNA sequences (letters A, C, T, and G). By not using every k-mer from the input sequence, but choosing them using this algorithm, we get a significant improvement in memory requirements.

For more information about the algorithm please check out the [original paper](http://yorke.umd.edu/papers/genome_papers/minimizerpaper.pdf).

## Run prerequisites

The script works on Unix-based and Windows platforms and it's written for Python3, so the machine needs to have that installed in order for it to work.

# Usage

To get the minimizers from a sequence, simply run the script and, as an argument in the terminal type the name of the input file.

## main.py

main.py performs a reading of the input file in FASTA format containing a DNA sequence. As an input it takes a single FASTA file and stores the output to a `*.txt` file, containing all minimizers found from the given sequence.

### Command line
The script is run from the terminal (command prompt):

    main.py [w k filename]

The parameters `w k filename` are not mandatory, and if not used will cause the script to use the test file ecoli100k.fa from the current directory of the script and find all minimizers where `k` and `w` parameters will be set to 20 and then print the first 20 minimizers in ascending order (alphabetically) to standard output (nothing will be saved to a file). Parameter `k` represents the k-mer size, and parameter `w` window size (this is explained in detail in the paper linked above).

If, on the other hand, the parameters are entered, it will them as well as the file to find all minimizers that will then be saved to a file called the same as the input file, with a string `_res.txt` appended to it. The recommended values for `w` and `k` are both 20.

### Example

Load file `ecoli100k.fa` and use w = 10, k = 15 when finding minimizers. The output file name will then be `ecoli100k.fa_res.txt`.

    main.py 10 15 ecoli100k.fa
    
