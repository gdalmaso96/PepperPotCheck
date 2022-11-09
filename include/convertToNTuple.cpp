void convertToNTuple(TString fileName, TString treeName = "beam"){
	TFile* F = TFile::Open(fileName, "UPDATE");
	TTree* T = (TTree*) F->Get(treeName);
	
	float x = 0, y = 0, z = 0, Px = 0, Py = 0, Pz = 0, t = 0, PDGid = 0, EventID = 0, TrackID = 0, ParentID = 0, Weight = 0;
	F->cd();
	TNtuple* Tnew = new TNtuple("beam", "beam", "x:y:z:Px:Py:Pz:t:PDGid:EventID:TrackID:ParentID:Weight");

	long nEvents = T->GetEntries();
	T->SetBranchAddress("x", &x);
        T->SetBranchAddress("y", &y);
        T->SetBranchAddress("z", &z);
        T->SetBranchAddress("Px", &Px);
        T->SetBranchAddress("Py", &Py);
        T->SetBranchAddress("Pz", &Pz);
        T->SetBranchAddress("t", &t);
        T->SetBranchAddress("PDGid", &PDGid);
        T->SetBranchAddress("EventID", &EventID);
        T->SetBranchAddress("TrackID", &TrackID);
        T->SetBranchAddress("ParentID", &ParentID);
        T->SetBranchAddress("Weight", &Weight);
	for(long i = 0; i < nEvents; i++){
		T->GetEntry(i);
		Tnew->Fill(x, y, z, Px, Py, Pz, t, PDGid, EventID, TrackID, ParentID, Weight);
        }
	
	F->cd();
	Tnew->Write("beam", TObject::kOverwrite);
	F->Close();
}
