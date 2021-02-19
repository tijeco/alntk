import argparse
import sys
from Bio import AlignIO
import pkg.compositionMatrix as cm
import pkg.chi2test as c2


class ParseCommands(object):

    def __init__(self):

        parser = argparse.ArgumentParser(
            description='Pretends to be git',
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
            description="Creates cysteine motif json file")
        parser.add_argument('fasta')
        args = parser.parse_args(sys.argv[2:])

        self.args = args
        print("Running alntk chi2test",self.args.fasta)
        fasta_file = self.args.fasta
        print(fasta_file)

        return(self.args)

    

def run():
	print("hello world")
	alntk_args = ParseCommands().args
	alignment_file = alntk_args.fasta
	alignment = AlignIO.read(open(alignment_file), "fasta")
	compDF = cm.compositionMatrix(alignment)
	compDF.to_csv("compDF.csv")
	print(c2.chi2test(compDF))
	
    
# alignment = AlignIO.read(open("PF09395_seed.sth"), "stockholm")

