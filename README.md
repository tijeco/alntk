# alntk
A toolkit for various summarizations of multiple sequence alignments


# Library dependencies

Libraries and versions required are specified in ```alntk_conda.yml```

To build this environment (you must have conda installed), issue the following command:
```
bash build_conda.sh
```

# Installation

To install simply run
```
python setup.py install
```

# Chi-square analysis

To run a chi-square analysis on a protein multiple sequence alignment, run

```
aln chi2test <alignment.fasta> -out <chi2results.txt>
```

## background
For a general chi-square analysis for an alignment it is calulated
chi2 = sum[i from 1 to k] (O_i - E_i)^2 / E_i

where k is the size of the alphabet (e.g. 4 for DNA, 20 for amino acids) and the values 1 to k correspond uniquely to one of the nucleotides or amino acids.
O_i is the nucleotide or amino acid frequency in the sequence tested.
E_i is the nucleotide or amino acid frequency expected from the ‘master’ distribution (e.g. the overall frequencies - depends on what one is using).

Whether the nucleotide (or amino acid) composition deviates significantly for the ‘master’ distribution is done by testing the chi2 value using the chi2-distribution with k-1 degrees of freedom (df=3 for DNA or df=19 for amino acids).