#include <fstream>
using namespace std;

void BRmtau(double mphi, double tau, char *outputfile){
  
  //extracting branching ratios
  gROOT->ProcessLine(".L getUL.C");
  gROOT->ProcessLine(".L test.C");
  // TH2D *hul = getULHisto();
  // cout<< mphi<<"\t"<< tau << endl;
  // int b = hul->FindBin(mphi,tau); 
  double br = gROOT->ProcessLine("getUL(500,10,1)");

  //appending result to the outputfile
  ofstream outfile;
  outfile.open(outputfile, std::ios_base::app);
  //myfile << "m [GeV]  tau [ps] BR(B+->K+mumu)\n";
  outfile << mphi/1000 << "\t" << tau << "\t" << br <<"\n";
  outfile.close();
}
