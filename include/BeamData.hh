// This class defines an object to fast recover settings and file names.

// This class hold a fileName, quadrupole settings and can be used to store data points inside TGraph
#ifndef BeamData_h
#define BeamData_h 1

#include "TString.h"
#include "TGraph2D.h"
#include <map>
#include <iostream>
#include <fstream>
#include <string>


class BeamData {
	public:
		BeamData();
		virtual ~BeamData();
		
		const BeamData& operator=(const BeamData &right);

		void SetFileName(TString fileName); //{ fFileName = fileName;}
		
		TString GetFileName();
		
		void ReadFile(TGraph2D*); // The data are stored inside a 2d graph
		TGraph2D* GetGraph2D();

		double GetPILLposition();
		void SetPILLposition(TString Magnet, double position);

		void SetFileFormat(int fileFormat);
		int GetFileFormat();
		
		void AddElement(TString Magnet, double current, double position, double length);
		double GetCurrent(TString Magnet);
		double GetPosition(TString Magnet);
		double GetLength(TString Magnet);

	private:
		TString fFileName;
		std::map <TString, double> fMagnetCurrents;
		std::map <TString, double> fMagnetPosition;
		std::map <TString, double> fMagnetLength;
		double fPILLposition; // PILL position w.r.t. last magnet center

		int fFileFormat; // if 0 data is formatted PILL style, if 1 is formatted ODB style
		
		TGraph2D* fGraph2D;
};

#endif
