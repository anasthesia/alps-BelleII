import glob
import re
import numpy as np
from numpy import genfromtxt
import subprocess
import sys

#run python file-with-masses&taus br. Output stored in the output_combined folder

#reads m and tau from input file, runs root macro to get BR and writes (m, tau, BRexp) to a file 
inputfile=sys.argv[1]
print(inputfile)
#br=sys.argv[2]
params = genfromtxt(inputfile,  comments="#", delimiter=',')
print(params)

outputfile=re.sub(".dat","_BR.dat",re.sub("\A([\S]+)/",'output/',inputfile))
# print("output_exp: "+outputfile)

with open(outputfile,'w') as fout:
    fout.write("#m [GeV],  tau [ps], c, BRexp(B+->K+mumu)\n")

for i in range(params.shape[0]):
    # cmd="root -b -l -q -e  \".L getUL.C\" -e \"getUL({mass},{tau},1)\"| awk \'{print $2}\' >> \"{outfile}\"".\
    # format(mass=params[i,0]*10**3,tau=params[i,1],outfile=outputfile)
    mass=params[i,0]*10**3
    tau=params[i,1]
    outfile=outputfile
    cmd=f'root -b -l -q -e  ".L getUL.C" -e "getUL({mass},{tau},1)"| awk \'{{print $2}}\' >> "{outfile}"'
    print("i=",i)
    subprocess.call([cmd],shell=True)

#calculates if BRtheory is allowed and combines together (m, tau, BRtheory, BRexp, allowed/not allowed)

expparams=genfromtxt(outputfile,  comments="#", delimiter='\n') 
print(expparams)

combooutput=re.sub(".dat","_comb.dat",re.sub("\A([\S]+)/",'output_combined/',inputfile))
with open(combooutput,'w') as foutcomb:
    print("output_comb: "+combooutput)
    allparams=[]
    foutcomb.write("#m [GeV],  tau [ps], c, BRtheo(B+->K+mumu), BRexp, allowed/excluded(1/0)\n")
    
    for i in range(params.shape[0]):
        ifallowed=0
        if (float(params[i,3])<float(expparams[i])):
            ifallowed=1
        newparams=np.append(params[i],[expparams[i],ifallowed])
        allparams.append(newparams)
    allparams=np.array(allparams)
    print(allparams)
    np.savetxt(foutcomb, allparams, fmt='%5e', delimiter='\t')

