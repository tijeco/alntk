import argparse
import sys
from Bio import AlignIO

import pkg.compositionMatrix as cm
import pkg.chi2test as c2


class ParseCommands(object):

	def __init__(self):

		parser = argparse.ArgumentParser(
			description='multiple sequence alignment toolkit',
			usage='''alntk <command> [<args>]
			The most commonly used alntk commands are:
				chi2test''')
		parser.add_argument("command", help="Subcommand to run")
		
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
		args = parser.parse_args(sys.argv[1:2])
		if not hasattr(self, args.command):
			print("Unrecognized command")
			parser.print_help()
			exit(1)
		self.args = parser.parse_args(sys.argv[1:2])
        # use dispatch pattern to invoke method with same name
		getattr(self, args.command)()

	def chi2test(self):
		parser = argparse.ArgumentParser(
			description="Runs chi-square composition analysis on multiple sequence alignment")
		parser.add_argument('fasta')
		parser.add_argument('-out',type = str,default = "chi2results.txt")
		parser.add_argument('-format',
                    choices=["clustal",
							"emboss",
							"fasta",
							"fasta-m10",
							"ig",
							"maf",
							"mauve",
							"msf",
							"nexus",
							"phylip",
							"phylip-sequential",
							"phylip-relaxed",
							"stockholm"],
					default="fasta",
                    help='Special testing value')
		
		
		args = parser.parse_args(sys.argv[2:])

		self.args = args
		print("Running alntk chi2test",self.args.fasta)
		fasta_file = self.args.fasta
		return(self.args)

    

def run():
	alntk_args = ParseCommands().args
	alignment_file = alntk_args.fasta
	alignment = AlignIO.read(open(alignment_file), alntk_args.format)
	compDF = cm.compositionMatrix(alignment)
	# print(compDF)
	
	compDFchi2 = c2.chi2test(compDF)
	compDFchi2["passed"] = compDFchi2["p-value"] > 0.05
	
	compDFchi2.to_csv(alntk_args.out,sep="\t")
	
	
    


