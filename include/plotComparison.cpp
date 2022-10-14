#include "TF1.h"
#include "TSpline.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TGraph.h"
#include "TGraph2D.h"
#include "TFile.h"
#include "TTree.h"
#include "TCanvas.h"
#include "TPad.h"
#include <iostream>
#include <fstream>
#include <string>

// The data file is always a txt file
// for the moment the format is assumed to be always that in PILL format

// MEG data has opposite sign on horizontal axis, as the monitor is put on the opposite side w.r.t. Mu3e configuration
// For the moment I'm fixing it mydelf offline
void plotComparison(TString dataName, TString runName, int cross = 1){
	std::ifstream myfile(dataName);
	double x = 0, y = 0, proton = 0, ch0 = 0, ch0n = 0, ch2 = 0, ch2n = 0, ch3 = 0, ch3n = 0;
	std::string line; //First line must be dumped
	getline(myfile, line);

	// Define TGraphs
	TGraph* Gx = new TGraph();
	TGraph* Gy = new TGraph();
	TGraph2D* G = new TGraph2D();

	// Cross scan
	if(cross){
		double tempCoord = -999, tempCoord2 = -999;
		double temp = 0;
		int flagX = 0; // Flag for horizontal and vertical profile: 0 for vertical
		// Store first point
		myfile >> x >> y >> proton >> ch0 >> ch0n >> ch2 >> ch2n >> ch3 >> ch3n;
		tempCoord = x;
		tempCoord2 = y;
		temp = ch0n;
		// Check whether first values are vertical or horizontal
		myfile >> x >> y >> proton >> ch0 >> ch0n >> ch2 >> ch2n >> ch3 >> ch3n;
		if(tempCoord == x){
			Gy->SetPoint(Gy->GetN(), tempCoord2, temp);
			Gy->SetPoint(Gy->GetN(), y, ch0n);
		}
		else if(tempCoord == y){
			Gx->SetPoint(Gx->GetN(), tempCoord2, temp);
			Gx->SetPoint(Gx->GetN(), x, ch0n);
			flagX = 1;
		}

		while(!myfile.eof()){
			myfile >> x >> y >> proton >> ch0 >> ch0n >> ch2 >> ch2n >> ch3 >> ch3n;
			if(flagX){
				// Check whether point is still on the horizontal
				if( y == tempCoord){
					if(tempCoord2 != x && temp != ch0n){
						Gx->SetPoint(Gx->GetN(), x, ch0n);
						temp = ch0n;
						tempCoord2 = x;
					}
				}
				else{
					flagX = 0;
					Gy->SetPoint(Gy->GetN(), y, ch0n);
					tempCoord = x;
				}
			}
			else if(!flagX){
				// Check whether point is still on the vertical
				if( x == tempCoord ){
					if(tempCoord2 != y && temp != ch0n){
						Gy->SetPoint(Gy->GetN(), y, ch0n);
						temp = ch0n;
                                                tempCoord2 = y;
					}
				}
				else{
					flagX = 1;
					Gx->SetPoint(Gx->GetN(), x, ch0n);
					tempCoord = y;
				}
			}
		}
	}
	// Raster scan
	else{
		while(!myfile.eof()){
			myfile >> x >> y >> proton >> ch0 >> ch0n >> ch2 >> ch2n >> ch3 >> ch3n;
			G->SetPoint(G->GetN(), x, y, ch0n);
		}
	}

	// Close data file
	myfile.close();

	// ------------------------
	
	// Open simulation file
	TFile* F = TFile::Open(runName, "UPDATE");
	F->cd();

	TTree* T = (TTree*) F->Get("VirtualDetector/PILL");

	TH1F* Hx = new TH1F("Hx", "Hx", 250, -250, 250);
	TH1F* Hy = new TH1F("Hy", "Hy", 250, -250, 250);
	TH2F* H  = new TH2F("H" , "H" , 250, -250, 250, 250, -250, 250);
	
	if(cross){
		T->Draw("x>>Hx", "abs(y) < 1", "goff");
		T->Draw("y>>Hy", "abs(x) < 1", "goff");
	}
	else{
		T->Draw("y:x>>H", "", "goff");
	}
	
	// ------------------------
	
	// Plot
	TCanvas* can = 0;

	if(cross){
		can = new TCanvas("can", "can", 1920, 960);
		can->Divide(2, 1);
		can->cd(1);
		gPad->SetGrid();
		gPad->SetMargin(0.15, 0.1, 0.15, 0.1);
		
		TSpline3* Sx = new TSpline3("Sx", Gx, "b1 e1", (Gx->GetY()[1] - Gx->GetY()[0])/(Gx->GetX()[1] - Gx->GetX()[0]), (Gx->GetY()[Gx->GetN() - 1] - Gx->GetY()[Gx->GetN() - 2])/(Gx->GetX()[Gx->GetN() - 1] - Gx->GetX()[Gx->GetN() - 2]));
		Sx->SetNpx(10000);
		//TF1* fx = new TF1("fx", [&](double *x, double *p){return Gx->Eval(x[0], Sx);}, Gx->GetX()[0], Gx->GetX()[Gx->GetN()-1], 0);
		TF1* fx = new TF1("fx", [&](double *x, double *p){return Sx->Eval(x[0] - p[0]);}, Gx->GetX()[0], Gx->GetX()[Gx->GetN()-1], 1);
		fx->SetParameter(0, 0);
		TF1* fxMean = new TF1("fxMean", [&](double *x, double *p){return x[0]*Sx->Eval(x[0]);}, Gx->GetX()[0], Gx->GetX()[Gx->GetN()-1], 0);
		double xMean = fxMean->Integral(Gx->GetX()[0], Gx->GetX()[Gx->GetN()-1])/fx->Integral(Gx->GetX()[0], Gx->GetX()[Gx->GetN()-1]);
		xMean = 0;
		fx->SetParameter(0, Hx->GetMean() - xMean);
		//TF1* fx = new TF1("fx", [&](double *x, double *p){return Gx->Eval(x[0]);}, Gx->GetX()[0], Gx->GetX()[Gx->GetN()-1], 0);

		Hx->Scale(fx->Integral(Gx->GetX()[0], Gx->GetX()[Gx->GetN()-1])/Hx->GetSum()/Hx->GetBinWidth(1));

		Sx->SetLineWidth(3);
		Sx->SetLineColor(64);

		Gx->SetMarkerStyle(20);
		Gx->SetMarkerColor(64);
		Gx->SetLineColor(64);

		Hx->SetLineWidth(3);
		Hx->SetLineColor(94);
		Hx->SetFillColorAlpha(94, 0.4);

		Hx->SetTitle("Horizontal profile; x [mm]; Counts [a.u.]");

		Hx->Draw("hist");
		Hx->SetMaximum(Hx->GetMaximum()*1.35);
		Hx->GetXaxis()->SetRangeUser(Gx->GetX()[0], Gx->GetX()[Gx->GetN()-1]);
		Gx->Draw("same lp");
		Sx->Draw("same");

		can->cd(2);
		gPad->SetGrid();
		gPad->SetMargin(0.15, 0.1, 0.15, 0.1);
		
		TSpline3* Sy = new TSpline3("Sy", Gy, "b1 e1", (Gy->GetY()[1] - Gy->GetY()[0])/(Gy->GetX()[1] - Gy->GetX()[0]), (Gy->GetY()[Gy->GetN() - 1] - Gy->GetY()[Gy->GetN() - 2])/(Gy->GetX()[Gy->GetN() - 1] - Gy->GetX()[Gy->GetN() - 2]));
		TF1* fy = new TF1("fy", [&](double *x, double *p){return Sy->Eval(x[0] - p[0]);}, Gy->GetX()[0], Gy->GetX()[Gy->GetN()-1], 1);
                fy->SetParameter(0, 0);
                TF1* fyMean = new TF1("fyMean", [&](double *x, double *p){return x[0]*Sy->Eval(x[0]);}, Gy->GetX()[0], Gy->GetX()[Gy->GetN()-1], 0);
                double yMean = fyMean->Integral(Gy->GetX()[0], Gy->GetX()[Gy->GetN()-1])/fy->Integral(Gy->GetX()[0], Gy->GetX()[Gy->GetN()-1]);
		yMean = 0;
                fy->SetParameter(0, Hy->GetMean() - yMean);

		Hy->Scale(fy->Integral(Gy->GetX()[0], Gy->GetX()[Gy->GetN()-1])/Hy->GetSum()/Hy->GetBinWidth(1));

		Sy->SetLineWidth(3);
		Sy->SetLineColor(64);

		Gy->SetMarkerStyle(20);
		Gy->SetMarkerColor(64);
		Gy->SetLineColor(64);

		Hy->SetLineWidth(3);
		Hy->SetLineColor(94);
		Hy->SetFillColor(94);
		Hy->SetFillStyle(1001);
		Hy->SetFillColorAlpha(94, 0.4);

		Hy->SetTitle("Vertical profile; y [mm]; Counts [a.u.]");

		Hy->Draw("hist");
		Hy->SetMaximum(Hy->GetMaximum()*1.35);
		Hy->GetXaxis()->SetRangeUser(Gy->GetX()[0], Gy->GetX()[Gy->GetN()-1]);
		Gy->Draw("same lp");
		Sy->Draw("same");
	}

	// Store plot in simulation file
	F->cd();
	can->Write("Comparison", TObject::kOverwrite);
	can->Print((runName.Copy()).Remove(runName.Copy().Index(".root")) + ".png");
	F->Close();
}

int main(int argc, char** argv){
	std::cout << argv[0] << std::endl;
	plotComparison("../Data_2022_Mu3e/Collimator/QSK43_348A_180kV_fastScan.txt", "../g4bl/scores/Mu3e_run00031.root", 1);

	return 0;
}
