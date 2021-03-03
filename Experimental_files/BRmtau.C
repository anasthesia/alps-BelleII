#include <fstream>
using namespace std;

void BRmtau(double mphi, double tau, char *outputfile){
  
  //extracting branching ratios
  gROOT->ProcessLine(".L B2KX_Fig4.C");
  TH2D *hul = getULHisto();
  cout<< mphi<<"\t"<< tau << endl;
  int b = hul->FindBin(mphi,tau); 
  double br = hul->GetBinContent(b);

  //appending result to the outputfile
  ofstream outfile;
  outfile.open(outputfile, std::ios_base::app);
  //myfile << "m [GeV]  tau [ps] BR(B+->K+mumu)\n";
  outfile << mphi/1000 << "\t" << tau << "\t" << br <<"\n";
  outfile.close();
}
