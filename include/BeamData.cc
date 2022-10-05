#include "BeamData.hh"

BeamData::BeamData() : fFileName(""), fPILLposition(0), fFileFormat(0), fGraph2D(nullptr){}

BeamData::~BeamData(){}

void BeamData::SetFileName(TString fileName){
	fFileName = fileName;
}

const BeamData& BeamData::operator=(const BeamData &right){
        fFileName = right.fFileName;
        fMagnetCurrents = right.fMagnetCurrents;
        fMagnetPosition = right.fMagnetPosition;
        fMagnetLength = right.fMagnetLength;
        fPILLposition = right.fPILLposition;

        fFileFormat = right.fFileFormat;
        fGraph2D = right.fGraph2D;
	return* this;
}

TString BeamData::GetFileName(){ return fFileName;}

void BeamData::ReadFile(TGraph2D* value){ // The data are stored inside a 2d graph
	if(fFileFormat == 0){
		std::ifstream myfile(fFileName);
		double x = 0, y = 0, proton = 0, ch0 = 0, ch0n = 0, ch2 = 0, ch2n = 0, ch3 = 0, ch3n = 0;
		std::string line; //First line must be dumped
		getline(myfile, line);
		while(!myfile.eof()){
			myfile >> x >> y >> proton >> ch0 >> ch0n >> ch2 >> ch2n >> ch3 >> ch3n;
			value->SetPoint(value->GetN(), x, y, ch0n);
		}
		myfile.close();
		return;
	}
	else{
		std::cout << "Yet to be defined" << std::endl;
		return;
	}
}

TGraph2D* BeamData::GetGraph2D(){
	if(fGraph2D == 0){
		fGraph2D = new TGraph2D();
		ReadFile(fGraph2D);
	}
	return fGraph2D;
}

double BeamData::GetPILLposition(){
	return fPILLposition;
}

void BeamData::SetPILLposition(TString Magnet, double z){
	fPILLposition = z + fMagnetPosition[Magnet];
}

void BeamData::SetFileFormat(int value){ fFileFormat = value;}

int BeamData::GetFileFormat(){ return fFileFormat;}

void BeamData::AddElement(TString Magnet, double current, double position, double length){
	fMagnetCurrents.insert(std::pair <TString, double>(Magnet, current));
	fMagnetPosition.insert(std::pair <TString, double>(Magnet, position));
	fMagnetLength.insert(std::pair <TString, double>(Magnet, length));
}

double BeamData::GetCurrent(TString Magnet){return fMagnetCurrents[Magnet];}

double BeamData::GetPosition(TString Magnet){return fMagnetPosition[Magnet];}

double BeamData::GetLength(TString Magnet){return fMagnetLength[Magnet];}
