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
void generator2Deasy(TString graphName1, TString graphName2, TString histName, long N, TString fileName = "/Users/giovanni/PhD/Simulazioni/BeamTimeMEG/2022_06/PepperPotCheck/g4bl/PepperPotPhaseSpace.root", TString beamFileName = "/Users/giovanni/PhD/Simulazioni/BeamTimeMEG/2022_06/PepperPotCheck/g4bl/beam/PepperPotPhaseSpace.root"){
	TFile* F = TFile::Open(fileName);
	TGraph2D* Gx = (TGraph2D*) F->Get(graphName1);
	TGraph2D* Gy = (TGraph2D*) F->Get(graphName2);
	TH1F* H = (TH1F*) F->Get(histName);

	// Define evaluation functions
	TF2* fx = new TF2("fx", [&](double *x, double *p){return Gx->Interpolate(x[0], x[1]);}, Gx->GetXmin(), Gx->GetXmax(), Gx->GetYmin(), Gx->GetYmax(), 0);
	fx->SetNpx(1000);
	fx->SetNpy(1000);
	TF2* fy = new TF2("fy", [&](double *x, double *p){return Gy->Interpolate(x[0], x[1]);}, Gy->GetXmin(), Gy->GetXmax(), Gy->GetYmin(), Gy->GetYmax(), 0);
	fy->SetNpx(1000);
	fy->SetNpy(1000);
	
	// Use MEG truncated gaussian
	TF1* fPz = new TF1("fPz", "gaus(0)", 0, 30.6);
	fPz->SetNpx(1e5);
	fPz->SetParameters(1, 27.9, 0.9);
	
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
		XP *=1e-3;
		YP *=1e-3;

		Pz = -H->GetRandom(R)/sqrt(1 + pow(XP, 2) + pow(YP, 2)); //fPz->GetRandom(R);
		
		x = X;
		y = Y;
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

void generator(){
	generator2Deasy("Hpx_2D", "Hpy_2D", "HPz", 1000000);
}


