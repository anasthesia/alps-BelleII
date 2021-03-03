import glob
import re
import numpy as np
from numpy import genfromtxt
import subprocess
import sys

#run python file-with-masses&taus br. Output stored in the output_combined_BR folder

#reads m and tau from input file, runs root macro to get BR and writes (m, tau, BRexp) to a file 
inputfile=sys.argv[1]
print(inputfile)
#br=sys.argv[2]
Rfactor=sys.argv[2]
params = genfromtxt(inputfile,  comments="#", delimiter='\t')
print(params)

outputfile=re.sub(".dat","_exp.dat",re.sub("\A([\S]+)/",'output/',inputfile))
# print("output_exp: "+outputfile)

with open(outputfile,'w') as fout:
    fout.write("#m [GeV],  tau [ps], casb, BRexp(B+->K+mumu)\n")

for i in range(params.shape[0]):
	cmd="root -b -q B2KX_Fig4.C BRmtau.C'({mass},{tau},\"{outfile}\")'".\
            format(mass=params[i,0]*10**3,tau=params[i,1],outfile=outputfile)
	subprocess.call([cmd],shell=True)

#calculates if BRtheory is allowed and combines together (m, tau, BRtheory, BRexp, allowed/not allowed)

expparams=genfromtxt(outputfile,  comments="#", delimiter='\t') 

combooutput=re.sub(".dat","_comb.dat",re.sub("\A([\S]+)/",'output_combined_R{0}/'.format(Rfactor),inputfile))
with open(combooutput,'w') as foutcomb:
    print("output_comb: "+combooutput)
    allparams=[]
    foutcomb.write("#m [GeV],  tau [ps], casb, BRtheo(B+->K+mumu), BRexp, allowed/excluded(1/0)\n")
    
    for i in range(params.shape[0]):
        ifallowed=0
        if (float(params[i,3])<float(expparams[i,2])/float(Rfactor)):
            ifallowed=1
        newparams=np.append(params[i],[expparams[i,2],ifallowed])
        allparams.append(newparams)
    allparams=np.array(allparams)
    print(allparams)
    np.savetxt(foutcomb, allparams, fmt='%5e', delimiter='\t')

