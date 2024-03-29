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

-- 24.10.2022 --
Added weight to LL: it is further divided by the number of transmitted perticles to favour high transmission. Now Runs with no particles get a low LL instead of returning a nan.

-- 26.10.2022 --
The fit to centroid only excluding COBRA data is not too bad. Vertical profiles seem reasonable, main issues arise on the horizontal. The SSL magnet might have had different settings for MEG and Mu3e. I'm running on MEG only data both the centroid only fit and the fit to the momentum distribution. A different center in the horizontal might explain the tendency to go to higher momenta: with a lower focusing the distribution becomes broader.

-- 27.10.2022 --
Might have realized the issue: it could be that the mismodeling of the center in the horizontal profiles is due to the lack of a pepperpot point close to the horizontal peak. The idea is to let the parametrization of the slices be part of the BeamData settings and add a method that samples the phase space by adding a slice. Still need to figure out wheather it is worth it or not to create a TGraph2D with python and then sample with the usual sampler or to prefer to sample it at python level again. This would bring 6 more parameters (added slice parametrization).

This is probably the reason why higher momenta are favored by the likelihood: a higher momentum results in lower deviation from the quadrupolar fields and therefore more particles at the horizontal center.

-- 04.11.2022 --
Started testing 2D splines on python3. Seem to have found a reasonable spline with an easy way to add slices. Add 2 slices set to 0 at both sides of space distribution and set to 0 negative values. Can think of includin two more slices on the sides in the fit (+12 params). 

I will go on and see how fast it is to sample the obtained phase space: could integrate in one direction and build a 2D cumulative function. Still need to find a smart way to do so.

For the moment only horizontal space is included. Will do the same for vertical phase space.

-- 07.11.2022 --
Managed to sample the 2d distribution using python3 only in a reasonable amount of time. To build from the slices and sample one phase space 1e6 times the function requires 44-46 seconds, while executing ones the genBeam.C rquires ~90 seconds.

Looks reasonable. Now need to implement it inside BeamData

-- 08.11.2022 --
Start implementation of new sampler. Methods needed:
 - interpolation to evaluate global cumulant
 - cumulant sampler

Still need to add longitudinal momentum function. Done -> less then 2 seconds to sample

-- 09.11.2022 --
2d sampling fixed. Issue with cancellation found out to be an issue with the interpolation class: the issue arises if one samples r and uses inverse cumulant to evaluate Irand:

<code> r = np.random.rand(1000000) </code>

<code> Irand = fi(r) </code>

<code> dxint = f(Irand.astype(int)+1) - f(Irand.astype(int)) </code>

<code> ddx = dx\*(r - f(Irand.astype(int)))/dxint </code>

The last line arises the issue: fixed by changing it to:
<code> ddx = dx\*(f(Irand) - f(Irand.astype(int)))/dxint </code>

So that everything depends on the Irand only.

The standard phase space is built and sampled in 119 seconds

Next step, to test adding a slice in both transverse spaces: done, it's working smoothly. One more slice on x builds and samples in 115 seconds, on y in 116 seconds, on both in 118 seconds. To be compared with 93 seconds of sampling only in include/genBeam.cpp 


Next step: add CMBL model and data. Model added successfully: alerady with beam parameter in final configuration the final focus is quite good.

Next step: check parameter consistency for running optuna trials and test one run. Then can move to the fit

-- 10.11.2022 --
New optuna file added and tested. best.py and plotBest updated as well

Issues to run it on the cluster

-- 11.11.2022 --
Managed to try the optimization, but by chance I left the Bayesian optimizer. I'm now repeting with NSGAII with 50 individuals.

There is still an error in the evaluation of the LL: it happens frequently that the LL gives nan as a result. Need to further explore, not trivial: I'm checking whether fixing the range on LL evaluation is enough

Found issue: run 47 gets to negative values. Current fix: absolute value of PDE. THe values are always small, so it should be fine. In alternative in the future will truncate it.

Testing first run and then launch fit.

-- 12.11.2022 --
Need to check the current LL evaluation, might not be using the right interpolation class for cross profiles: check if it is always dumbly using 0 in data.datasets[run]['profileLL'][]. In that case need to include a check on the length of the profile array -> fixed PlotBests method: wrong indexing to profiles

-> fixed EvaluateLL limits

Need to repeat the fit: the modeling of the tails worsened, might need to add a gaussian BKG to transverse phase spaces or to rerun everything with the root generator once the fit is done.

There was an error in the plotBest method: fixed sign change in MEG data

Fixed aperture of QSK magnets and removed inner collimator from CMBL simulation.

Increased lower limit of addiction slice to 2.8

-- 15.11.2022 --
Performed fit to centroids. Testing same fit with inverted horizontal axis at generation and inverted genbeam.c::Invert

-- 19.11.2022 --
Performed fit to centroids only in QSM focus. Then will propagate beam to HULK center at different HULK fields. 

Still need to implement Chi2.

Might manage to include gaussian tails by using curve_fit

-- 20.11.2022 --
Now gaussian tails are included in prepare2dCumulative.

-- 21.11.2022 --
Fixed sign at COBRA center: there the horizontal axis is consistent with Mu3e.

Added HULK center raster scan: I'll use this to perform the fit to the centroids for Gavin by imploying the Chi2. If it works out I'll include a slice and then the momentum distribution

Started implementation of the Chi2 evaluation method for BeamData.py. Need to test it first on a run

-- 23.11.2022 --
Chi2 method tested on local machine. Will repeat on cluster with 1e6 events and then start the minimization

-- 24.11.2022 --
Added raster scans to PlotBest and fixed 2d interpolation.

Idea: maybe the issue with the tails is due to the precision on the distance between the pepperpot and the detector. I will add a common scaling factor to both x and y divergences and fit that together with the center and the momentu distribution with no slices 

The scaling factor does improve the Chi2. For the moment is not yet clear whether it is only a matter of transmission improvement or if it really matches the beam spot at the center

Need probably to add the horizontal slice or to limit the number of particles that can be transmitted

-- 25.11.2022 --
Increased range of scale in Chi2_CentMOMScale_HULK, to 0.8 5 during optimization (around 2500th job) to check whether it would continue to shrink. At the moment it pushes to the limit (2): what if multiple scattering and hole size are not negligible at all?

The momentum looks good, centering around 27.8, the slice parameter don't seem to be affecting the measurement too much. 

Stopped simulations, now using air in HULK and increased scale range for Slice as well

Reconstruction on the vertical is not bad at all. The horizontal seem to be too wide, maybe because of dispersion. Could be good to add a correlation between x and P together with MS deconvolution. I would do that removing the slice parameters. Let's first see whether using air improves anything in the fit.

!!!! Guess: the scale factor is so high because of how wide the horizontal distribution at HULK center is in lack of correlation. It is a good idea to add correlation between P and x. An wasy way would be to sample (x, xp) and sample a uniform so that it is correlated to x with a certain correlation. Than P is obtained by transforming it through the CDF. It would be good to get a uniformly distributed variable from the (x,xp) pair: after sampling properly x one can use the margin cdf to get a uniformly distributed variable to correlate with the other. Cholesky should be enough for that.

-- 27.11.2022 --
Added correlation between x and Ptot through Iman-Conover method

-- 05.12.2022 --
Now any correlation matrix can be sampled using the relative correlation method. The correlation matrix is 5d.

Started fit including the centroids, the momentum distribution and the 7 correlations (15 parameters). The statistics in the single run has been halved from 1e6 to 5e5 to execute each trial faster. After a few trials needs to be checked.

-- 16.01.2023
COBBRA fitted to:
<ol>
 <li> Corr5d: full correlation matrix sampling + momentum distribution sampling </li>
 <li> CorrMom: x to P correlation only + momentum distribution sampling </li>
 <li> CorrMomSlice: CorrMom + horizontal Slice </li>
</ol>


-- 24.01.2023 --
COBRA fit completely wrong. Need to look into it again. Probably there is an issue with the spline.

-- 06.02.2023 --
Higher statistics and positive field convention is working at HULK center. Still need to understand why the plotBest seems mirrored. Might be due to flip in the meshgrid function. Need to look into that.
The transmission is working and consistent to some extent with what was measured for different magnetic fields. 

COBRA is missing the moderator and windows. Most probable cause of discrepancy. Will implement it and rerun fit. --- Done. Need last checks with Angela

!!! Found issue in EvaluateChi2: the find("HULK") was not used properly and the axis was not mirrored during Chi2 evaluation. Run again while preparing COBRA beamline

-- 09.02.2023 --
Found issue in the fit at COBRA center: the 2d interpolation was restricted to an area too small for a good estimate of the normalization. This might improve fitting COBRA center

-- 18.02.2023 --
Fit at COBRA center biases in a weird way the momentum distribution. Centroid only is not good, trying to fit only the gaussian window on the momentum distribution

-- 24.02.2023 --
Fit to COBRA center not completely fine, might need to check out with scale

Currently running:
<ol>
 <li> CorrMomScale_NoCent: free correlation xP, full momentum fit, scale free, centroid fixed to 0 </li>
 <li> CorrMom_NoCent: free correlation xP, full momentum fit, centroid fixed to 0 </li>
 <li> CorrScale_redCent: free correlation xP, free parameters are only the three sigmas, the momentum window is fixed centered at 27.5 MeV/c, centroid can vary for a smaller range </li>
</ol>
