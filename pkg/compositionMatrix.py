import pandas as pd
def compositionMatrix(aln):
	compDict = {}
	fixedCharacters = ["-","A","C","D","E","F","G","H","I","K","L","M","N","P","Q","R","S","T","V","W","Y"]
	for record in aln:
		header = record.id
		seq = record.seq
		currentSeqMat = [0]*21
		for i in range(len(seq)):
			aa = seq[i]
			try:
				characterPos = fixedCharacters.index(aa)
				currentSeqMat[characterPos]+= 1
			except:
				print("ERROR:", header, "contains character ("+aa+") not in the list:",fixedCharacters)
		compDict[header] = currentSeqMat
	compDF = pd.DataFrame.from_dict(compDict, orient='index',
                       columns=fixedCharacters)
	return compDF
