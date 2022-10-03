# PepperPotCheck
This repo contains the studies of the PepperPot measurement performed in June 2022 along the MEG beam line

## Elements positioning
Based on CMBL 2022 logbook, the PILL was positioned 37 mm away from border of the Mylar window (47 to window attachment, as the ring is 10 mm thick). For phase space reconstruction the distance between QSK43 center and pill position was 1108.5 mm.

Based on MEG 2022 logbook, the PILL was positioned 45.5 mm away from border of the Mylar window (55.5 to window attachment). Thus the distance between the PILL and QSK43 center was 8.5 mm longer than for Mu3e, namely 1117 mm.

For the Pepper Pot analysis, L = 44 was used. L is the distance along the beam drifts after being stopped by the grid. As the Pepper Pot is 3 mm thick, this is consistent aith assuming the drift as the distance between the PILL and the center of the grid, that is to say 1.5 mm DS to the ring of the Mylar window: 45.5 - 1.5 mm = 44 mm.

Thus, the beam reconstructed with the Pepper Pot has to be positioned 1117 mm - 44 mm = 1073 mm DS to the center of QSK43.

## First strategy -  assume Pz spectrum and infer scaling factors
<ol>
  <li>Generate beam with Pz = -28. The phase space than can be sampled as usual. By multiplying Pz times the transverse divergences the obtained Pt is going to have opposite sign as expected by requiring backpropagation. The quadrupole are modeled by using genericQuad with round aperture for killing particles (maybe in the future could use the right pole tip aperture to check on transmission. The field is the one coming from the usual qsk fieldmap.</li>
  <li>Generating a beam with Pz distribution analogous to the one used in GEM. The rest is analogous to first point 1</li>
  <li>Generating a beam with Pz distribution equal to the one obtained by running Felix' simulation. That could be skipped.</li>
</ol>

The aim is producing a beam file upstream to QSK41 to then apply the current changes and compare beam profiles measured during quad scan. A fit to the scaling factor could be performed to check whether the current factors make sense.
Centroids could be included as well in the fit to help a bit.

Plan on writing a python script that can run on the cluster.

## Second strategy - fit Pz spectrum assuming scaling factors
<ol>
  <li>Could define a Pz distribution as the convolution of a triangle with a theta function and a gaussian. Could then minimize chi2 to measured profiles to determine Pz spectrum. Even if the emittance is big probably QSK non linearities are not high enough to allow for a sensitive estimate. None the less, including the measurements at COBRA center (with full beamline) would give better sensitivity on longitudinal dynamics</li>
 </ol>

That being said, for such a method to be effective I have to go through the setpoint files, the TRANSPORT files and the specs as provided by Peter-R. by the magnet group, to evaluate myself the scaling factor and compare with the one we've being using so far. Maybe Luca cannot really help with this.

COBRA and BTS could as well constrain the centroids.

## Third strategy - fit Pz spectrum + phase space assuming scaling factors
Fit full phase space with asymmetric guass with exponential tail using both quad scan and pepper-pot measurements. To do:
<ol>
  <li> Check parametrization as function of u in transverse phase space from PepperPot 2022.</li>
  <li> Create generator for phase space. </li>
</ol>

Parameters to fit:
<ol>
  <li> x phase space parametrization (include centerline)</li>
  <li> y phase space parametrization (include centerline)</li>
  <li> Pz distribution (for the future beamline, would maybe be good to include up to QSF41 to take into account different Sextupole settings between 2021 and 2022)</li>
  <li> Pepper pot position on the transverse plane (x, y), of the two plates.</li>
</ol>

Minimize on combined Chi2.

At each iteration need to:
<ol>
  <li> sample phase space: for Pepper Por simulations sample only in front of the holes to gain in statistics. Try to have always enough statistics in simulation to neglect stocastic errors.</li>
  <li> run one simulation per each beam quadrupole setting, one per COBRA center settings, one per each PepperPot plate (maybe include flange)</li>
  <li> evaluate chi2 on beam profiles </li> 
</ol>

## Luca's involvement
As the longitudinal fit is probably a bit too convoluted, Luca could try to do the fit to the scale factor. I will prepare a g4bl model and make a first comparison myself between the PILL profiles and the simulation. Could also think of introducing a scale factor on the position scale: if Air MS is non neglible (by current estimate shouldn't introduce any issue), then we would observe a broadening of all the shapes. Assuming that the effect is still small stretching the distributions from the simulation could be enough, otherwise it would be needed to introduce a double deconvolution to the measured beam phase space based on computing the expected brodening for such a column of air, or even fit it through simulation.

# Included Data
Two folders containing 2022 data are included:
<ol>
  <li> Data_2022_Mu3e: contains beam profiles at collimator as a function of QSK43 current </li>
  <li> Data_2022_MEG: contains the PepperPot scan, the MENT scans and the raster scan at COBRA center </li>
</ol>

