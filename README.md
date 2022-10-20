# PepperPotCheck
This repo contains the studies of the PepperPot measurement performed in June 2022 along the MEG beam line
The strategies reported here are not ordered by importance. The third strategy is somewhat favored for fitting anything, but the first step should be a blunt comparison between Pepper Pot phase space and quadrupole scan phase space.

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

## Third strategy - fit Pz spectrum + phase space assuming scaling factors - HIGH PRIORITY
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

From this fit it could be possible cross check scaling factors as compared to the surface muon energy: the focusing of the quadrupoles depends on the ratio between the gradient and Pz, which means that Pz itself is sensitive to the scaling factor. By imposing the energy of the monochromatic line (which is known by kinematics), it is possible to fit the scaling factors as well.

## Luca's involvement
As the longitudinal fit is probably a bit too convoluted, Luca could try to do the fit to the scale factor. I will prepare a g4bl model and make a first comparison myself between the PILL profiles and the simulation. Could also think of introducing a scale factor on the position scale: if Air MS is non neglible (by current estimate shouldn't introduce any issue), then we would observe a broadening of all the shapes. Assuming that the effect is still small stretching the distributions from the simulation could be enough, otherwise it would be needed to introduce a double deconvolution to the measured beam phase space based on computing the expected brodening for such a column of air, or even fit it through simulation.

# Included Data
Two folders containing 2022 data are included:
<ol>
  <li> Data_2022_Mu3e: contains beam profiles at collimator as a function of QSK43 current </li>
  <li> Data_2022_MEG: contains the PepperPot scan, the MENT scans and the raster scan at COBRA center. Here I'm assuming that FSH41 doesn't affect the phase space </li>
</ol>

# First Simulation check
Start by running Pepper Pot phase space backwards with:
<code> g4bl scripts/MEGconfiguration.g4bl poszPILL=0 beamPositionZ=1250+1117-44 last=1e6 histoFile=/home/developer/Simulazioni/BeamTimeMEG/2022_06/PepperPotCheck/g4bl/beam/USbeamRev.root QSK41cur=-18.1982 QSK42cur=40.7008 QSK43cur=-34.8 SML41cur=10 </code>

# Fit to centroid and to longitudinal phase space
Start fitting the longitudinal phase space and the centroid position. The objective is going to be the log Likelyhood: each data set is going to be interpolated with a spline and used as the likelyhood, to be applied to each particle transmitted in the g4bl model.

For the moment don't consider any misalignment between MEG and Mu3e.

MEG data are inverted in the horizontal direction, as the PILL detector is oriented oppositely than for Mu3e. Just take that into account when weighting every event.

Start by finding a good parametrization for momentum distribution -> found:
<ol>
  <li>Convolute surface muon x^3.5 dependence times theta function between 0 and kinematic edge with a gaussian</li>
  <li>Multiply by gaussian window</li>
  <li>Convolute with gaussian</li>
</ol>

The free parameters are 4:
<ol>
  <li>the three sigmas</li>
  <li>the average of the gaussian window</li>
</ol>

The Ptot parametrization fit to Felix is stored in momentumDistribtion.cpp

On top of these variables, 4 moree free parameters come from the centroids and 2 more from the relative alignment of the pepper-pots (probably the constraint can be very tight on these two).

The complete optimization will run with 10 independent variables and one objective value (log likelihood).

Start with 8: ignore relative alignment for the moment

-- 19.10.2022 --
Current status: now BeamData settings include system dipendent directories and commands. Works on laptop, needs to be tested on the cluster. I will run it on meg first and check how long it takes for it to run 1e5 particles
