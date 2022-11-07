#include <iostream>
#include <stdio.h>
#include <string>
#include <time.h>
#include <fstream>
#include <cstring>
#include <vector>
#include <sstream>
#include "TTree.h"
#include "TGraph.h"
#include "TSpline.h"
#include "TGraph2D.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TString.h"
#include "TF1.h"
#include "TF2.h"
#include "TF3.h"
#include "TMultiGraph.h"
#include "TAxis.h"
#include "TPaveText.h"
#include "TText.h"
#include "TPad.h"
#include "Math/Interpolator.h"
#include "Math/GSLMultiRootFinder.h"
#include "Math/WrappedMultiTF1.h"
#include "TH2F.h"
#include "TFile.h"
#include "TVirtualFFT.h"
#include "TRandomGen.h"

// Store histogram with Felix' weights for Pz
void storePz(){
	ifstream myfile("/Users/giovanni/PhD/Simulazioni/BeamTimeMEG/2022_06/PepperPotCheck/g4bl/FelixPzFromThesis.txt");
	double Pz = 0, Counts = 0;

	TH1F* H = new TH1F("H", "H", 45, 23, 32);
	string line;
	getline(myfile, line);
	getline(myfile, line);

	while(!myfile.eof()){
		myfile >> Pz >> Counts;
		H->Fill(Pz, Counts);
	}

	myfile.close();

	TFile* F = TFile::Open("/Users/giovanni/PhD/Simulazioni/BeamTimeMEG/2022_06/PepperPotCheck/g4bl/PepperPotPhaseSpace.root", "UPDATE");
	F->cd();
	H->Write("HPz", TObject::kOverwrite);
	F->Close();
}

// Generates beam based on input from create2D
void generator2Deasy(TString graphName1, TString graphName2, double a, double b, double c, double d, double x0, double xp0, double y0, double yp0, long N, TString fileName = "/Users/giovanni/PhD/Simulazioni/BeamTimeMEG/2022_06/PepperPotCheck/g4bl/PepperPotPhaseSpace.root", TString beamFileName = "/Users/giovanni/PhD/Simulazioni/BeamTimeMEG/2022_06/PepperPotCheck/g4bl/beam/PepperPotPhaseSpace.root"){
	TFile* F = TFile::Open(fileName);
	TGraph2D* Gx = (TGraph2D*) F->Get(graphName1);
	TGraph2D* Gy = (TGraph2D*) F->Get(graphName2);

	// Define evaluation functions
	TF2* fx = new TF2("fx", [&](double *x, double *p){return Gx->Interpolate(x[0], x[1]);}, Gx->GetXmin(), Gx->GetXmax(), Gx->GetYmin(), Gx->GetYmax(), 0);
	fx->SetNpx(1000);
	fx->SetNpy(1000);
	TF2* fy = new TF2("fy", [&](double *x, double *p){return Gy->Interpolate(x[0], x[1]);}, Gy->GetXmin(), Gy->GetXmax(), Gy->GetYmin(), Gy->GetYmax(), 0);
	fy->SetNpx(1000);
	fy->SetNpy(1000);
	
	// Define longitudinal phase space
	TF1* gaus = new TF1("gaus", "gaus(0)", -100, 100);
	// Parameters: [0] = y, [1] = sigma
	TF1* rangeGaus = new TF1("range", "1e5*pow(x[0]/29.79, 3.5)*exp(-pow(x[0] - [0], 2)/2/[1]/[1])", 20, 35);
	// Parameters: [0] = 1st convolution sigma
	//             [1] = window average
	//             [2] = window sigma
	TF1* fI = new TF1("fI", [&](double* x, double* p){
		rangeGaus->SetParameters(x[0], p[0]);
		rangeGaus->SetNpx(100);
		return rangeGaus->Integral(0, 29.79)*TMath::Gaus(x[0], p[1], p[2]);
	}, 20, 35, 3);
	
	// Parameters: [0] = 1st convolution sigma - a
	//             [1] = window average - b
	//             [2] = window sigma - c
	//             [3] = 2nd convolution amplitude (fixed)
	//             [4] = 2nd convolution average (fixed)
	//             [5] = 2nd convolution sigma - d
	TF1Convolution* fconv = new TF1Convolution(fI, gaus);
	TF1* f = new TF1("f", *fconv, 20, 35, fconv->GetNpar());
	f->SetParameters(a, b, c, 1, 0, d);
	f->SetNpx(1000);

	// Define beam TTree
	F->cd();
	float x = 0, y = 0, xp = 0, yp = 0, z = 0, Px = 0, Py = 0, Pz = 0, t = 0, PDGid = 0, EventID = 0, TrackID = 0, ParentID = 0, Weight = 0;
	double X = 0, Y = 0, XP = 0, YP = 0;

	TFile* New = TFile::Open(beamFileName, "RECREATE");
	New->cd();
	TNtuple* tupla = new TNtuple("beam", "beam", "x:y:z:Px:Py:Pz:t:PDGid:EventID:TrackID:ParentID:Weight");
	

	int last = -1;

	TRandomRanlux48* R = new TRandomRanlux48();
	R->SetSeed(299792458);
	for(int i = 0; i < N; i++){
		fx->GetRandom2(X, XP, R);
		fy->GetRandom2(Y, YP, R);
		XP += xp0;
		YP += yp0;
		XP *=1e-3;
		YP *=1e-3;
		double Ptot = f->GetRandom(R);
		Pz = -Ptot/sqrt(1 + pow(XP, 2) + pow(YP, 2)); //fPz->GetRandom(R);
		
		x = X + x0;
		y = Y + y0;
		Px = XP*Pz;
		Py = YP*Pz;
		
		PDGid = -13;
		EventID = 1 + i;
		Weight = 1;

		New->cd();
		tupla->Fill(x, y, z, Px, Py, Pz, t, PDGid, EventID, TrackID, ParentID, Weight);
	}
	New->cd();
	tupla->Write("beam", TObject::kOverwrite);
	New->Close();
	F->Close();
}

void invertBeam(TString fileName = "/Users/giovanni/PhD/Simulazioni/BeamTimeMEG/2022_06/PepperPotCheck/g4bl/beam/USbeamRev.root", TString newFileName = "/Users/giovanni/PhD/Simulazioni/BeamTimeMEG/2022_06/PepperPotCheck/g4bl/beam/USbeam.root"){
	TFile* F = TFile::Open(fileName); 
	F->cd();

	TNtuple* beam = (TNtuple*) F->Get("VirtualDetector/PILL");
	TFile* N = TFile::Open(newFileName, "RECREATE"); 
	N->cd();
	TNtuple* tupla = new TNtuple("beam", "beam", "x:y:z:Px:Py:Pz:t:PDGid:EventID:TrackID:ParentID:Weight");

	float x = 0, y = 0, xp = 0, yp = 0, z = 0, Px = 0, Py = 0, Pz = 0, t = 0, PDGid = 0, EventID = 0, TrackID = 0, ParentID = 0, Weight = 0;
	beam->SetBranchAddress("x", &x);
	beam->SetBranchAddress("y", &y);
	beam->SetBranchAddress("z", &z);
	beam->SetBranchAddress("Px", &Px);
	beam->SetBranchAddress("Py", &Py);
	beam->SetBranchAddress("Pz", &Pz);
	beam->SetBranchAddress("t", &t);
	beam->SetBranchAddress("PDGid", &PDGid);
	beam->SetBranchAddress("EventID", &EventID);
	beam->SetBranchAddress("TrackID", &TrackID);
	beam->SetBranchAddress("ParentID", &ParentID);
	beam->SetBranchAddress("Weight", &Weight);

	for(int i = 0; i < beam->GetEntries(); i++){
		beam->GetEntry(i);
		EventID = i+1;
		x *= -1;
		//Px *= -1;
		Py *= -1;
		Pz *= -1;

		N->cd();
                tupla->Fill(x, y, z, Px, Py, Pz, t, PDGid, EventID, TrackID, ParentID, Weight);
	}

	N->cd();
	tupla->Write("beam", TObject::kOverwrite);
	N->Close();
	F->Close();
}

void genBeam(TString fileName, double a, double b, double c, double d, double x0, double xp0, double y0, double yp0, long nEvents, TString original = "/Users/giovanni/PhD/Simulazioni/BeamTimeMEG/2022_06/PepperPotCheck/g4bl/PepperPotPhaseSpace.root"){
	generator2Deasy("Hpx_2D", "Hpy_2D", a, b, c, d, x0, xp0, y0, yp0, nEvents, original, fileName);
}

void genBeam(TString fileName, TString newFileName){
	invertBeam(fileName, newFileName);
}

void genBeam(){
	genBeam("example.root", 0.0812462, 27.8995, 1.23719, 0.05, 0, 0, 0, 0, 1000000);
}
