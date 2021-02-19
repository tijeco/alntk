from scipy import stats
import numpy as np
import pandas as pd 

def chi2test(compDF):
	seqTotals = compDF.sum(axis=1)
	gaps = compDF["-"]
	gapsPerSeq = gaps/seqTotals
	# print(gaps/characterTotals)
	# print(gaps.shape,.shape)
	
	nonGap = compDF.loc[:, 'A':'Y']
	nonGapTotals = nonGap.sum().to_frame()
	nonGapSeqTotals = nonGap.sum(axis=1).to_frame()
	numCharacters = nonGapTotals.sum()
	expectedFreq = nonGapTotals / numCharacters

	expectedCountArray = np.dot(nonGapSeqTotals,expectedFreq.transpose())
	expectedCountDF = pd.DataFrame(expectedCountArray,columns =nonGap.columns, index =nonGap.index.values )
	chi2DF = ((expectedCountDF - nonGap)**2)/expectedCountDF
	chi2Sum = chi2DF.sum(axis=1)

	pValueDf = 1 - stats.chi2.cdf(chi2Sum, 19)

	print(pd.DataFrame({"Gap/Ambiguity":gapsPerSeq,"p-value":pValueDf}))

	

