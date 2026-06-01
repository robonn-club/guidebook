# Global Navigation Satellite Systems (GNSS)

> Absolute positioning anywhere on Earth using satellite signals — understanding both the measurement principle and the error sources that limit accuracy.

---

## Topics

**GNSS Constellations and Signal Structure**
- Constellations: GPS (US), GLONASS (Russia), Galileo (EU), BeiDou (China) — multi-constellation receivers use all four for better geometry and redundancy
- Signal components: carrier wave, ranging code (C/A and P-code), navigation message
- Two measurement types: code pseudorange (metre-level) and carrier phase (millimetre-level, but ambiguous)
- Frequency bands: L1, L2, L5 for GPS; multi-frequency receivers reduce ionospheric error

**Positioning Principle and Satellite Geometry**
- Pseudorange measurement — code correlation gives travel time × speed of light; "pseudo" because receiver clock is unknown; requires 4 satellites to solve for (x, y, z, clock)
- WGS84 — the reference ellipsoid used by GPS; coordinates are in ECEF; convert to geographic (lat, lon, height) or local ENU for navigation
- Dilution of Precision (DOP) — GDOP, PDOP, HDOP, VDOP; measures how satellite geometry amplifies ranging errors; PDOP < 3 is acceptable, > 6 is poor
- Least squares positioning — overdetermined system when >4 satellites; weighted by signal quality

**GNSS Error Sources**
- Ionospheric delay — signal travels slower through the ionosphere; up to 20 m error; mitigated by dual-frequency receivers or models (Klobuchar, NeQuick)
- Tropospheric delay — neutral atmosphere delay; ~2.3 m at zenith; mitigated by models (Saastamoinen, Hopfield)
- Multipath — signal reflects off buildings and terrain before reaching receiver; difficult to model; mitigated by antenna placement and signal processing
- Satellite clock and ephemeris errors — broadcast corrections in navigation message; residual errors ~1 m
- Receiver noise — thermal noise in the correlator; ~0.3 m for pseudorange, ~3 mm for carrier phase

**Differential GNSS and RTK**
- Differential GNSS (DGNSS) — a reference receiver at a known position broadcasts pseudorange corrections; removes common errors; ~0.5 m accuracy
- Single differencing — subtract observations between two receivers; cancels satellite clock errors
- Double differencing — subtract between two receivers AND two satellites; cancels both satellite and receiver clock errors; the standard RTK measurement model
- Integer ambiguity — carrier phase measurement has an unknown integer number of full cycles; must be resolved to achieve centimetre accuracy
- LAMBDA algorithm — Least-squares AMBiguity Decorrelation Adjustment; the standard method for integer ambiguity resolution; produces float solution first, then fixed
- Float solution → fixed solution — float uses real-valued ambiguities (~decimetre); fixed uses resolved integers (~centimetre); fixing requires sufficient observation time and good geometry

**Precise Point Positioning (PPP)**
- No reference station required — uses precise satellite orbit and clock products (IGS)
- Dual-frequency required — to model ionospheric delay
- Long convergence time (15–30 min) compared to RTK — ambiguity convergence is the bottleneck
- PPP-RTK — combines PPP corrections with ambiguity resolution; emerging technique

**GNSS Integrity and Augmentation**
- RAIM — Receiver Autonomous Integrity Monitoring; detects faulty satellites using consistency checks; required for safety-critical applications
- SBAS — Satellite-Based Augmentation Systems (EGNOS in Europe, WAAS in US); geostationary satellites broadcast differential corrections; ~1 m accuracy
- GNSS outages — urban canyons, tunnels, jamming; reason INS/GNSS integration (see topic 9) is mandatory for robust navigation

---

## Videos

- **Lars Klingbeil — GNSS and Navigation lectures** (Universität Bonn) — signal processing, error modeling, and RTK derivations; primary reference for this page
- **ESA Navipedia video series** (navipedia.net) — modular explanations of GNSS signals, error sources, and augmentation systems
- **NovAtel GNSS tutorials** (YouTube @NovAtel) — practical explanations of RTK, PPP, and integration; industry perspective

---

## Book / Article Resources

- **Principles of GNSS, Inertial, and Multisensor Integrated Navigation Systems** — Groves (2nd ed., 2013) — covers GNSS signal processing, error modeling, and all integration architectures; the most complete single reference
- **Understanding GPS/GNSS: Principles and Applications** — Kaplan & Hegarty (3rd ed., 2017) — broader treatment of receiver design and signal processing
- **GPS Satellite Surveying** — Leick, Rapoport, Tatarnikov (4th ed., 2015) — deep treatment of carrier phase processing, double differencing, and ambiguity resolution
- **[ESA Navipedia](https://gssc.esa.int/navipedia/)** — free online encyclopedia; accurate and well-maintained; look up any GNSS concept here first
