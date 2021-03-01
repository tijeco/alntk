package main

import (
	"bufio"
	"bytes"
	"flag"
	"fmt"
	"io"
	"log"
	"os"
	"strings"
)

var p = fmt.Println
var help bool
var inputFiles = []string{}

type fasta struct {
	id   string
	desc string
	seq  string
}

func init() {

	chi2testCmd := flag.NewFlagSet("chi2test", flag.ExitOnError)
	// chi2testOtherOption := chi2testCmd.Bool("otherOption", false, "otherOption") // add this for other chi2test flag

	flag.BoolVar(&help, "help", false, "print usage")
	flag.BoolVar(&help, "h", false, "print usage (shorthand)")
	flag.Parse()

	if len(os.Args) < 2 {
		fmt.Println("expected chi2test subcommand\nuse -h for help")
		os.Exit(1)
	}

	switch os.Args[1] {
	case "chi2test":
		chi2testCmd.Parse(os.Args[2:])
		inputFiles = chi2testCmd.Args()
	default:
		p("expected chi2test subcommand")
		os.Exit(1)
	}
	for _, file := range inputFiles {
		if fileExists(file) == false {
			log.Fatalln(file, "does not exist")
		}
	}

}

func fileExists(filename string) bool {
	info, err := os.Stat(filename)
	if os.IsNotExist(err) {
		return false
	}
	return !info.IsDir()
}

func buildFasta(header string, seq bytes.Buffer) (record fasta) {
	fields := strings.SplitN(header, " ", 2)

	if len(fields) > 1 {
		record.id = fields[0]
		record.desc = fields[1]
	} else {
		record.id = fields[0]
		record.desc = ""
	}

	record.seq = strings.ToUpper(seq.String())

	return record
}

func parseFasta(fastaFh io.Reader) chan fasta {

	outputChannel := make(chan fasta)

	scanner := bufio.NewScanner(fastaFh)
	// scanner.Split(bufio.ScanLines)
	header := ""
	var seq bytes.Buffer

	go func() {
		// Loop over the letters in inputString
		for scanner.Scan() {
			line := strings.TrimSpace(scanner.Text())
			if len(line) == 0 {
				continue
			}

			// line := scanner.Text()

			if line[0] == '>' {
				// If we stored a previous identifier, get the DNA string and map to the
				// identifier and clear the string
				if header != "" {
					// outputChannel <- buildFasta(header, seq.String())
					outputChannel <- buildFasta(header, seq)
					// fmt.Println(record.id, len(record.seq))
					header = ""
					seq.Reset()
				}

				// Standard FASTA identifiers look like: ">id desc"
				header = line[1:]
			} else {
				// Append here since multi-line DNA strings are possible
				seq.WriteString(line)
			}

		}

		outputChannel <- buildFasta(header, seq)

		// Close the output channel, so anything that loops over it
		// will know that it is finished.
		close(outputChannel)
	}()

	return outputChannel
}

func fastaAlignment(fasta *bufio.Reader) map[string][]rune {
	aln := make(map[string][]rune)
	var alnSize int
	record1 := true
	for record := range parseFasta(fasta) {
		// p(record.id, len(record.seq))
		if record1 {
			// p(1, record.id)
			alnSize = len(record.seq)
			aln[record.id] = make([]rune, alnSize)
			for i, character := range record.seq {
				aln[record.id][i] = character
			}
			record1 = false
		} else if len(record.seq) != alnSize {
			p("ERROR")
			log.Fatalln(record.id, "has a different size\nexpected matrix size:", alnSize)
		} else {
			// p(record.id)
			aln[record.id] = make([]rune, alnSize)
			for i, character := range record.seq {
				aln[record.id][i] = character
			}
		}

		// break
		// p(record.seq)
	}
	return aln
}

func compositionMatrix(aln map[string][]rune) (compMat [][21]int) {
	fixedCharacters := "-ACDEFGHIKLMNPQRSTVWY"
	for header, seq := range aln {
		currentSeqMat := [21]int{}
		for _, aa := range seq {
			characterPos := strings.Index(fixedCharacters, string(aa))
			if characterPos > -1 {
				currentSeqMat[characterPos]++
			} else {
				p("ERROR:", header, "contains character ("+string(aa)+") not in the list:")
			}

		}
		p(header, currentSeqMat)
		compMat = append(compMat, currentSeqMat)
	}
	return
}

func main() {
	p(inputFiles)
	for _, alignmentFileName := range inputFiles {
		alignmentFile, err := os.Open(alignmentFileName)
		if err != nil {
			log.Fatal(err)
		}
		defer alignmentFile.Close()
		alignment := fastaAlignment(bufio.NewReader(alignmentFile))
		p(alignment)
		p(compositionMatrix(alignment))

	}
}
