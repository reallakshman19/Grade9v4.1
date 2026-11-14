# Grade9 v4.1 — Agent 2 PH07–PH12 · Read-only Phase 0 inventory
**Task:** `G9V41-NSEJS-PHYSICS-AGENT2-PH07-PH12-R1`  
**Status:** `INVENTORY_CANDIDATE · AUTHOR_EXPOSED · READ_ONLY · ACADEMIC_HOLD`  
**Date:** 13 November 2026  
**Owner planning baseline:** `82a782f12c57b5d9d25e9b1eb8d2053a56dfabc0`  
**Repository:** https://github.com/reallakshman19/Grade9v4.1  
**Contract candidate:** [Draft PR #2](https://github.com/reallakshman19/Grade9v4.1/pull/2), head `330f9524fe37cff53f20b6f094c85e4739da3a66`, *unmerged*.

> **Authority limit:** This register proposes a curriculum/teaching decomposition, not an authenticated complete official item-by-item syllabus, certified QRT adjudication, scientific acceptance, or permission to publish. No files changed on GitHub.

## A. Basis, source priority and scope convention
Official IAPT 2026 identifies NSEJS Physics, Chemistry and Biology up to CBSE Class 10. HBCSE specifies broadly Class 10-and-below Science/Mathematics and explicitly allows unconventional hard questions within that boundary. Official 2026–27 CBSE IX/X syllabi and governmental lower-class records provide the chapter-level starting point.

| Source ID | Evidence | URL |
|---|---|---|
| IAPT26 | IAPT 2026 NSEJS level/eligibility notice | https://iapt.org.in/ |
| HBCSE | HBCSE Olympiad syllabus boundary | https://olympiads.hbcse.tifr.res.in/syllabus/ |
| CBSE9 | CBSE Class IX Science 2026–27: sound, differential surface heating, scientific inquiry | https://cbseacademic.nic.in/web_material/CurriculumMain27/SecPart1/ScienceSt_SecP1_2026-27.pdf |
| CBSE10 | CBSE Class X Science 2026–27: mirrors, refraction/lenses/eye, circuits, magnetic effects; formative induction/motor/generator | https://cbseacademic.nic.in/web_material/CurriculumMain27/SecPart1/Science_SecP1_2026-27.pdf |
| D7 | Delhi government Class VII 2026–27: heat transfer in nature | https://edustud.nic.in/edu/Syllabus_2026_27/7/7_SCIENCE_SYLLABUS_2026_27_EM.pdf |
| D8 | Delhi government Class VIII 2026–27: baseline electricity/light/material competencies | https://edustud.nic.in/edu/Syllabus_2026_27/8/8_SCIENCE_SYLLABUS_2026_27_EM.pdf |
| NCERT9 | IITK SATHEE reproduction of NCERT Class IX earlier Matter in Our Surroundings: qualitative latent heat, evaporation; historical reference; not claimed verbatim for revised 2026–27 IX | https://sathee.iitk.ac.in/ncert-books/class-09/nb-science-09/sci-09-chapter-1-matter-in-our-surroundings/ |
| CBSE_HIGHER | CBSE senior-secondary Physics 2026–27: explicit comparison demonstrating advanced thermal / electromagnetic theory is not an automatic Class X requirement | https://cbseacademic.nic.in/web_material/CurriculumMain27/SecPart2/Physics_SecP2_2026-27.pdf |

**Scope labels:** `C` = explicitly current Class IX/X curriculum Physics content; `P` = pre-Class IX or prerequisite bridge, requiring exact source mapping; `A` = advanced application of established principles (not automatically a new syllabus topic); `F` = content included in Class X but assessed **formatively** in schools; `E` = enrichment not established as compulsory Class X-and-below NSEJS scope. Treat all proposed QRT bands and source roles as HOLD until reviewed.

**Curriculum nuance:** Class X explicitly names *motor, electromagnetic induction and generator* as formative, not omitted. Class XI explicitly treats detailed calorimetry, thermal expansion, gas laws and thermodynamics. Therefore PH07 high-level calorimetry and PH12 quantitative induction are extension candidates, despite their appearance in coaching and project candidate banks. The IX 2026–27 course differs from the old IX annual content; old NCERT chapters cannot replace exact 2026–27 curriculum mapping.

## B. Reconciled repository state
1. Planning baseline is `82a782f…`; as observed, `main` is `dca026b4f0904d272251d3ef816ce0335af6b18b` — **one commit ahead** (19 files changed). Draft PR #2 has base `82a782f…` and head `330f952…`, with **seven** shared contract files and no topic authoring files. Its two Python CI jobs completed successfully with **351 passed, 1 warning** on Python 3.11 and Python 3.12. This is connector log inspection, not local reproduction.
2. Existing `nsejs/data/core1ab-coverage.v1.json`: **16** historical Physics constructions; three original authored previews and **13** historical constructions without reproducible published builds. Of those 16, **11** are in PH07–PH12: six optics, three circuits and two magnetism; **zero** original heat and sound constructions. The original optics lens-displacement preview is the sole original technical preview in Agent 2 scope. The other originals remain unresolved, even where supplemental skill journeys now exist.
3. `nsejs/data/independent-core1-recovery.v1.json` records **13 supplemental authored Physics recovery journeys**, distinct from restoration of original constructions; this is not 13 qualified textbook modules. The so-called `nsejs-fluids-sound-r1` page is **elevator buoyancy**, belonging to PH06 fluids, not evidence of PH08 sound coverage.
4. `nsejs/core2/question-map.v1.json` records **95** Physics question metadata rows; no qualified exact source mapping (`mapped_exact_qualified: 0`). `nsejs/data/physics-core2-candidates.v1.json` contains a **different 50-record** candidate corpus, divided into 10 OPTICS, 10 CURRENT_ELECTRICITY, 10 MAGNETISM_AND_EMI, 10 ELECTROSTATICS, 10 MECHANICS. Do **not** add these into 145 distinct examination originals or count 10 OPTICS as 10 verified items.
5. Current technical learner pages are problem-centred previews, not chapter-complete Core1A textbook readings. No PH07/PH08 chapter, no PH09–PH12 full chapter package, and no independently qualified D4 examination coverage were established from these inventories.

### Existing coverage by assigned chapter
| Topic | Original technical construction identities | Other candidate resources | Complete textbook? | Exact authenticated Core2? |
|---|---:|---|---|---|
| PH07 Heat | 0 | Crosslinks to material/evaporation and PH11 electrical heating; no original topic Core1 | **No** | **0 confirmed** |
| PH08 Sound | 0 | `fluids-sound` filename is PH06 buoyancy; no sound chapter | **No** | **0 confirmed** |
| PH09 Mirrors | 1 convex-image dynamics (original not published) | `nsejs-optics-r1` supplemental recovery | **No** | **0 confirmed** |
| PH10 Refraction/Lenses/Eye | 5 originals including one lens-displacement authored preview | Multiple prism, lens-mirror, conjugate and screw-lens supplemental recoveries | **No** | **0 confirmed** |
| PH11 Circuits | 3 originals, all historical original builds absent | Cube, ladder and circuit supplemental recovery journeys | **No** | **0 confirmed** |
| PH12 Magnetism | 2 originals, historical original builds absent | Magnetism, terminal-EMF supplemental recovery journeys | **No** | **0 confirmed** |

## C. PH07–PH12 subtopic / scientific model / three-operation D3–D4 planning register
These are **new candidate IDs** for later C01 reconciliation; do not treat them as already approved canonical IDs. Every row lists three *candidate distinct primary operations for three separate tasks*, not three primaries for one question. D3/D4 text denotes authoring opportunity only. Scientific models, representations and boundaries are included at brief Phase 0 granularity; a proper C02 warrant remains required.

### PH07 — Heat and Thermal Physics
| Proposed ID | Scope | Source pointer | Prerequisite pointer | Scientific subtopic / model | Representation, assumptions, misconception or boundary | Three candidate QRT operations | D3/D4 construction opportunity |
|---|:---:|---|---|---|---|---|---|
| PH07-01 | P | D7 | PH00-MEAS (unbound) | Temperature, thermometers, scales and thermal measurement | Thermometer scale and calibration; touch is unreliable | EXPLAIN, REPRESENT, JUSTIFY | D3: infer an unknown reading from a justified, calibrated scale; distinguish systematic error |
| PH07-02 | P | D7 | PH07-01 | Heat versus temperature; direction of energy transfer and equilibrium | Two-object energy-flow diagram; distinguish energy transfer from state temperature | RETRIEVE, EXPLAIN, MODEL | D3: choose the physically correct transfer direction in a multi-body situation |
| PH07-03 | P | D7 | PH07-02 | Conduction; thermal conductors, insulators and contact paths | Material stack / heat-flow paths; no heat transfer without temperature difference | EXPLAIN, MODEL, REPRESENT | D3: compare alternative insulation designs qualitatively with heat leaks |
| PH07-04 | P | D7 | PH07-03 | Convection in fluids and density-driven circulation | Flow arrows, temperature-density relation; distinguish convection from conduction | EXPLAIN, REPRESENT, JUSTIFY | D3: predict circulation reversal when heating and cooling locations change |
| PH07-05 | C | CBSE9 | PH07-03, PH07-04 | Radiation, absorption and differential heating of Earth and air | Radiation-energy diagram and surface comparison; absorptivity and environment matter | EXPLAIN, MODEL, SYNTHESIZE | D3: connect unequal surface heating to observed land/sea breeze phenomena |
| PH07-06 | P | NCERT9 (historical) | PH07-02 | Phase states, melting, boiling, freezing and condensation | Particle model and qualitative heating curve; phase change can occur at steady T | REPRESENT, EXPLAIN, JUSTIFY | D3: reject a false heat-temperature inference across phase transition |
| PH07-07 | P | NCERT9 (historical) | PH07-06 | Evaporation versus boiling, cooling, humidity and wind | Energy-flow map and control-variable comparison; open vs closed, rate vs boiling point | EXPLAIN, MODEL, SYNTHESIZE | D3: select the controlling factors in unfamiliar evaporation/cooling experiments |
| PH07-08 | A | NCERT9 (historical) | PH07-06 | Qualitative heating and cooling curves with multiple stages | Temperature-time graph; label slopes and plateaus without assuming constant power | REPRESENT, MODEL, JUSTIFY | D3: reconstruct what can be inferred and what cannot from a graph |
| PH07-09 | P | D7 | PH07-02 | Thermal expansion and its ordinary consequences | Length/volume sketches; uniform material and constrained expansion assumptions | EXPLAIN, MODEL, JUSTIFY | D3: predict gaps or stress under temperature reversal; quantitative coefficients E |
| PH07-10 | P | D7 | PH07-03 | Experimental thermal comparisons, insulation and fair tests | Apparatus, tables and control variables; distinguish measurements from conclusions | MODEL, REPRESENT, JUSTIFY | D3: diagnose a confounded cooling comparison and redesign the test |
| PH07-11 | E | CBSE_HIGHER (comparison only) | PH07-02, PH04 (unbound) | Specific heat capacity, heat capacity and quantitative calorimetry | Energy balance m c Delta T; isolated-system and no-phase assumptions; XI depth | MODEL, APPLY, SYNTHESIZE | D3/D4 optional: thermal mixing with unequal capacities; EXPLICIT EXTENSION |
| PH07-12 | E | CBSE_HIGHER (comparison only) | PH07-06, PH07-11 | Latent-heat calculations, composite calorimeters and thermal engines | Piecewise energy balance; classify phases first; XI-level quantitative treatment | MODEL, SYNTHESIZE, JUSTIFY | D4 optional: ice-water mixing with changing phases; not compulsory NSEJS core |

### PH08 — Sound and Waves
| Proposed ID | Scope | Source pointer | Prerequisite pointer | Scientific subtopic / model | Representation, assumptions, misconception or boundary | Three candidate QRT operations | D3/D4 construction opportunity |
|---|:---:|---|---|---|---|---|---|
| PH08-01 | C | CBSE9 | PH00-MEAS (unbound) | Vibrating sources: strings, membranes and air columns | Source-time diagram; sound generated by oscillation | EXPLAIN, MODEL, REPRESENT | D3: infer the excitation mechanism from observations, not a memorized instrument name |
| PH08-02 | C | CBSE9 | PH08-01 | Sound as mechanical longitudinal propagation | Compression-rarefaction diagram; particles oscillate locally, energy propagates | EXPLAIN, REPRESENT, JUSTIFY | D3: reconcile a pressure graph with a particle-motion diagram |
| PH08-03 | C | CBSE9 | PH08-02 | Sound needs a material medium; air/liquid/solid comparisons | Travel-path diagram; medium-dependent speed; no sound through vacuum | RETRIEVE, EXPLAIN, MODEL | D3: interpret time delays when a signal uses two media |
| PH08-04 | C | CBSE9 | PH08-02 | Frequency, period and wavelength | Time-series and spatial wave plots; time axis != distance axis | REPRESENT, APPLY, JUSTIFY | D3: extract frequency and wavelength from unlike graph scales |
| PH08-05 | C | CBSE9 | PH08-04 | Sound speed relation v=f lambda and measurement | Space-time propagation; same medium under fixed conditions | APPLY, MODEL, REPRESENT | D3: infer one unknown by correctly combining distinct observations |
| PH08-06 | C | CBSE9 | PH08-04 | Pitch, loudness, amplitude and intensity | Wave plots; pitch tracks frequency, loudness relates to intensity/perception | EXPLAIN, REPRESENT, JUSTIFY | D3: disprove amplitude-frequency confusion using changed wave features |
| PH08-07 | C | CBSE9 | PH08-04 | Sound wave graphs and observational uncertainty | Displacement-time vs pressure-position; axis meaning and phase must be declared | MODEL, REPRESENT, JUSTIFY | D3: translate among graphs without swapping amplitude with wavelength |
| PH08-08 | C | CBSE9 | PH08-05 | Reflection of sound and elementary echo timing | Ray/path diagrams and return-time; round trip rather than one way | MODEL, APPLY, REPRESENT | D3: solve echoes with a nontrivial total path length |
| PH08-09 | C | CBSE9 | PH08-08 | Distinct echo versus reverberation in spaces | Multiple paths and time-delay sketch; hearing thresholds context dependent | EXPLAIN, MODEL, JUSTIFY | D3: classify whether a reflected signal is separately audible in a changed hall |
| PH08-10 | C | CBSE9 | PH08-08 | Echolocation and sonar-style distance inference | Pulse timeline; propagation medium and total travel-time assumptions | APPLY, MODEL, SYNTHESIZE | D3: infer an obstacle location with two pulse recordings |
| PH08-11 | C | CBSE9 | PH08-01, PH08-06 | Sound production by instruments and musical features | Vibrating body, air column and pitch observation; avoid conflating source with medium | EXPLAIN, MODEL, JUSTIFY | D3: explain a modified instrument qualitatively, with controlled assumptions |
| PH08-12 | A | CBSE9 | PH08-08 | Multi-reflector echo pathways and echo sequence reconstruction | Time-of-flight diagrams and reflection order; reflected paths may overlap | REPRESENT, SYNTHESIZE, JUSTIFY | D4 candidate: determine path order from an unfamiliar pulse-arrival trace |
| PH08-13 | E | CBSE_HIGHER (comparison only) | PH08-05 | Doppler effect, quantitative standing waves and resonant modes | Moving-source wavefronts; fixed-medium and boundary assumptions; higher-level theory | MODEL, REPRESENT, SYNTHESIZE | D4 optional only; label EXTENSION and require syllabus warrant |

### PH09 — Reflection and Mirrors
| Proposed ID | Scope | Source pointer | Prerequisite pointer | Scientific subtopic / model | Representation, assumptions, misconception or boundary | Three candidate QRT operations | D3/D4 construction opportunity |
|---|:---:|---|---|---|---|---|---|
| PH09-01 | P | D8 | PH00-MEAS (unbound) | Ray model, rectilinear light and ordinary reflection | Ray arrow, normal, incidence/reflection angles | RETRIEVE, EXPLAIN, REPRESENT | D3: choose valid reflected directions under a rotated surface |
| PH09-02 | P | D8 | PH09-01 | Plane-mirror images, virtuality and apparent position | Backward ray extensions; distinguish image location from physical ray path | EXPLAIN, MODEL, REPRESENT | D3: infer apparent source position from two observer sight lines |
| PH09-03 | P | D8 | PH09-02 | Lateral inversion and object/mirror coordinate conventions | Perspective and image-coordinate drawings; left-right language ambiguous | REPRESENT, JUSTIFY, MODEL | D3: defend a mirror-image orientation in a shifted observer frame |
| PH09-04 | A | CBSE10 | PH09-02, PH01 (unbound) | Object and plane-mirror displacement; relative image motion | Position-line sketches; image shift relative to fixed reference | REPRESENT, APPLY, JUSTIFY | D3: infer image displacement when object and mirror both translate |
| PH09-05 | P | D8 | PH09-02 | Two plane mirrors and repeated reflections | Ray tracing and reflection sequence; geometry and visibility constraints | MODEL, REPRESENT, SYNTHESIZE | D3: check an apparent number of images against allowed ray paths |
| PH09-06 | C | CBSE10 | PH09-01 | Spherical mirror geometry: pole, principal axis, centres, focus | Mirror geometry and normal at point; paraxial approximation | RETRIEVE, REPRESENT, JUSTIFY | D3: decide which ray constructions survive an off-axis arrangement |
| PH09-07 | C | CBSE10 | PH09-06 | Concave mirrors: real/virtual images across object zones | Principal rays with object location; image type and orientation | EXPLAIN, REPRESENT, MODEL | D3: track image behaviour across focus and centre of curvature |
| PH09-08 | C | CBSE10 | PH09-06 | Convex mirrors: virtual image, field of view and motion | Virtual ray extensions; no real screen image for real object | EXPLAIN, MODEL, JUSTIFY | D3: infer changing image distance and distinguish actual from apparent motion |
| PH09-09 | C | CBSE10 | PH09-07, PH09-08 | Mirror formula, sign convention and domain of use | Signed u,v,f; mirror equation and image limits | APPLY, MODEL, REPRESENT | D3: reject an algebraically correct but physically invalid root |
| PH09-10 | C | CBSE10 | PH09-09 | Mirror magnification and experimental focal-length measurement | Image/object height arrows and distant-object experiment | APPLY, REPRESENT, JUSTIFY | D3: infer consistent sign and magnification from partial measurement |
| PH09-11 | E | CBSE_HIGHER (comparison only) | PH09-09, PH10-07 | Multiple curved mirrors and coupled mirror-lens systems | Multi-stage ray-tracing; different local axes and signed positions | MODEL, SYNTHESIZE, JUSTIFY | D4 optional: choose valid branch through a two-element system; extra theory HOLD |
| PH09-12 | A | CBSE10 | PH09-09 | Experimental mirror prediction, error and interpretation | Sketch + measurements; finite apertures and paraxial limits | MODEL, REPRESENT, JUSTIFY | D3: distinguish focal-position uncertainty from incorrect sign convention |

### PH10 — Refraction, Lenses and Human Eye
| Proposed ID | Scope | Source pointer | Prerequisite pointer | Scientific subtopic / model | Representation, assumptions, misconception or boundary | Three candidate QRT operations | D3/D4 construction opportunity |
|---|:---:|---|---|---|---|---|---|
| PH10-01 | C | CBSE10 | PH09-01 | Refraction at a boundary and changing light speed | Incident, refracted ray and normal; transparent materials and angular limits | EXPLAIN, MODEL, REPRESENT | D3: infer deflection direction under reversed material order |
| PH10-02 | C | CBSE10 | PH10-01 | Snell law and refractive index interpretation | Angles to the normal; relative versus absolute refractive index | APPLY, MODEL, JUSTIFY | D3: test a proposed refraction angle for physical admissibility |
| PH10-03 | C | CBSE10 | PH10-02 | Plane-parallel glass slab and lateral displacement | Parallel incident/emergent rays, offset vs angular deviation; slab geometry | REPRESENT, MODEL, JUSTIFY | D3: infer what changes with thickness versus refractive index |
| PH10-04 | A | CBSE10 | PH10-02 | Apparent depth and observer-dependent image position | Back-projected rays; paraxial small-angle approximation, not universal formula | MODEL, REPRESENT, JUSTIFY | D3: determine whether an apparent-depth shortcut is applicable |
| PH10-05 | C | CBSE10 | PH10-01 | Convex/concave thin lenses and principal-ray rules | Optical centre, foci, converging/diverging rays; thin lens approximation | EXPLAIN, REPRESENT, MODEL | D3: distinguish real ray crossing from apparent backward extension |
| PH10-06 | C | CBSE10 | PH10-05 | Lens image zones, orientation and screen visibility | Image-position sketches across focal region | RETRIEVE, REPRESENT, JUSTIFY | D3: classify changed image type across the focus boundary |
| PH10-07 | C | CBSE10 | PH10-06 | Lens formula and consistent sign conventions | Signed object/image distances, 1/f relation and domain | APPLY, MODEL, JUSTIFY | D3: reject a nonphysical solution even with consistent algebra |
| PH10-08 | C | CBSE10 | PH10-07 | Magnification, power of lens and units | Heights, distances, dioptre; signs and convention recorded | APPLY, REPRESENT, JUSTIFY | D3: reconcile magnification sign with an observed screen image |
| PH10-09 | A | CBSE10 | PH10-07, PH10-08 | Lens displacement and two conjugate positions | Object-screen-line and quadratic discriminant; thin-lens/paraxial assumptions | MODEL, SYNTHESIZE, JUSTIFY | D4 candidate: infer physical two-position boundary from inverse measurements |
| PH10-10 | C | CBSE10 | PH10-02 | Refraction through prism and dispersion | Deviation-path diagram; prism orientation and material dependence | EXPLAIN, REPRESENT, MODEL | D3: predict emergent colour ordering after reversing prism orientation |
| PH10-11 | C | CBSE10 | PH10-01 | Scattering and observed colours | Particle interaction schematic; separate scattering from dispersion | EXPLAIN, MODEL, JUSTIFY | D3: choose between scattering and refraction for a new observation |
| PH10-12 | C | CBSE10 | PH10-06 | Human eye: image formation and accommodation | Eye geometry, crystalline lens, retina; finite accommodation | EXPLAIN, MODEL, REPRESENT | D3: infer focusing failure when object distance changes |
| PH10-13 | C | CBSE10 | PH10-12 | Myopia, hypermetropia and their corrections | Ray correction diagrams; diverging vs converging corrective lens | MODEL, REPRESENT, JUSTIFY | D3: derive correct correction from a stated near/far-point limitation |
| PH10-14 | C | CBSE10 | PH10-07 | Focal-length measurement by distant objects and optical investigations | Apparatus and screen measurements; distant object approximation | APPLY, MODEL, JUSTIFY | D3: distinguish a setup error from a physical limit of the lens model |
| PH10-15 | A | CBSE9 (competency C2.3) | PH10-06 | Telescope and microscope qualitative lens combinations | Sequential conceptual ray diagrams; only qualitative role established in IX competency | MODEL, SYNTHESIZE, REPRESENT | D3: explain why objective and eyepiece have different roles |
| PH10-16 | E | CBSE_HIGHER (comparison only) | PH10-09 | Quantitative multi-lens and lens-plus-mirror inverse systems | Compound image transformation, multiple local sign conventions | MODEL, SYNTHESIZE, JUSTIFY | D4 optional; outside explicit X chapter detail unless independently warranted |
| PH10-17 | E | CBSE_HIGHER (comparison only) | PH10-02 | Total internal reflection and quantitative critical-angle optics | Critical-angle interface; higher-syllabus treatment | EXPLAIN, MODEL, JUSTIFY | D4 optional; do not claim Class X listed topic |

### PH11 — Current Electricity
| Proposed ID | Scope | Source pointer | Prerequisite pointer | Scientific subtopic / model | Representation, assumptions, misconception or boundary | Three candidate QRT operations | D3/D4 construction opportunity |
|---|:---:|---|---|---|---|---|---|
| PH11-01 | P | D8 | PH00-MEAS (unbound) | Charge transfer, circuit closure and basic conductor/insulator distinction | Circuit schematic and particle-flow explanation; current not consumed | EXPLAIN, MODEL, REPRESENT | D3: diagnose an open-path or bypass misconception using connections |
| PH11-02 | C | CBSE10 | PH11-01 | Conventional current, potential difference and source/load roles | Directional circuit arrows and potential sketch | RETRIEVE, EXPLAIN, REPRESENT | D3: reconcile current direction with reversed polarity |
| PH11-03 | C | CBSE10 | PH11-02 | Circuit symbols, ammeter and voltmeter connection | Circuit wiring, series vs parallel instrument placement | MODEL, REPRESENT, JUSTIFY | D3: identify why an observed meter reading is physically inconsistent |
| PH11-04 | C | CBSE10 | PH11-03 | Ohm law, V-I plots, ohmic regime | V-I graph and slope; fixed material/temperature assumptions | EXPLAIN, APPLY, JUSTIFY | D3: determine when line-slope resistance inference is justified |
| PH11-05 | C | CBSE10 | PH11-04 | Resistance, resistivity, geometry and material | Length-area ratio, unit and geometry diagram; uniform wire assumption | MODEL, APPLY, REPRESENT | D3: explain resistance change under simultaneous length/area changes |
| PH11-06 | C | CBSE10 | PH11-04 | Series resistor networks and voltage division | Single-current circuit map, sum of potential drops | APPLY, REPRESENT, JUSTIFY | D3: identify a mistaken potential assignment in a modified circuit |
| PH11-07 | C | CBSE10 | PH11-04 | Parallel networks, current division and equivalent resistance | Branch diagrams, equal branch voltages, total current | MODEL, APPLY, REPRESENT | D3: invert a known network to meet a measured total resistance |
| PH11-08 | A | CBSE10 | PH11-06, PH11-07 | Multi-stage mixed series/parallel reductions | Node graph and equivalence mapping; valid reduction topology only | MODEL, REPRESENT, SYNTHESIZE | D3: preserve connection topology while simplifying a less familiar network |
| PH11-09 | C | CBSE10 | PH11-04, PH04 (unbound) | Electric power, energy, ratings and electricity bills | Power/energy unit conversions, load diagrams; rating needs actual supply voltage | APPLY, MODEL, JUSTIFY | D3: distinguish rated power from actual power across altered supply |
| PH11-10 | C | CBSE10 | PH11-09, PH07-02 | Joule heating and safety applications | Electrical-to-thermal energy map; PH07 cross-link, ideal resistive regime | EXPLAIN, APPLY, SYNTHESIZE | D3: compare heat production in two circuits under different conditions |
| PH11-11 | C | CBSE10 | PH11-02, PH11-09 | Household wiring, fuses/MCBs, earthing and short circuits | Live/neutral/earth connection diagram; protective device is not load | EXPLAIN, MODEL, JUSTIFY | D3: diagnose safety issue from a changed installation schematic |
| PH11-12 | C | CBSE10 | PH11-03, PH11-04 | V-I and equivalent resistance experiments with measurement limits | Experimental table and circuit; systematic connection errors | MODEL, REPRESENT, JUSTIFY | D3: infer an experimental fault from apparent nonlinearity |
| PH11-13 | E | CBSE_HIGHER (comparison only) | PH11-08 | Complex cube/tetrahedron/infinite-ladder networks | Graph symmetry and recurrence; advanced topology beyond standard X network | MODEL, SYNTHESIZE, JUSTIFY | D4 optional; existing unqualified practice does not make mandatory |
| PH11-14 | E | CBSE_HIGHER (comparison only) | PH11-04 | Internal resistance, variable EMF and non-ohmic networks | Load-line graphs and source model; extra theory | MODEL, REPRESENT, SYNTHESIZE | D4 optional; scope review before authoring |

### PH12 — Magnetic Effects and Induction
| Proposed ID | Scope | Source pointer | Prerequisite pointer | Scientific subtopic / model | Representation, assumptions, misconception or boundary | Three candidate QRT operations | D3/D4 construction opportunity |
|---|:---:|---|---|---|---|---|---|
| PH12-01 | P | D8 | D8 magnetism prereq (unbound) | Permanent magnets, poles, compass and qualitative magnetic interaction | Compass orientation and magnet field sketch | RETRIEVE, EXPLAIN, REPRESENT | D3: distinguish observation from an unsupported force-line interpretation |
| PH12-02 | C | CBSE10 | PH12-01 | Magnetic field-line direction and qualitative patterns | Field lines, tangent direction and noncrossing rule | EXPLAIN, REPRESENT, JUSTIFY | D3: detect an impossible field map based on direction and geometry |
| PH12-03 | C | CBSE10 | PH12-02, PH11-02 | Field around straight current-carrying conductor | Right-hand thumb rule with current arrows | MODEL, REPRESENT, JUSTIFY | D3: predict field reversal at multiple observation positions |
| PH12-04 | C | CBSE10 | PH12-03 | Field of circular loops and current direction | Loop orientation and field-axis arrows; qualitative superposition | EXPLAIN, REPRESENT, MODEL | D3: distinguish loops with opposite winding directions |
| PH12-05 | C | CBSE10 | PH12-04 | Solenoid field, poles and electromagnet variables | Coil geometry, current and field arrows; qualitative ideal solenoid | MODEL, REPRESENT, JUSTIFY | D3: infer solenoid polarity after specified reconnection |
| PH12-06 | C | CBSE10 | PH12-02, PH11-02 | Force on current-carrying conductor in magnetic field | Three directional vectors; current direction is conventional | MODEL, REPRESENT, JUSTIFY | D3: reject a force-direction claim from inconsistent vector orientation |
| PH12-07 | C | CBSE10 | PH12-06 | Fleming left-hand rule and force reversal | Finger-direction diagram and signed change table | RETRIEVE, REPRESENT, JUSTIFY | D3: track field/current reversals and motor force direction |
| PH12-08 | F | CBSE10 | PH12-06, PH12-07 | Electric motor, force couple and commutator function | Coil-turn stages and contact state; school formative topic | EXPLAIN, MODEL, SYNTHESIZE | D3: explain reversal needed for continued turning |
| PH12-09 | F | CBSE10 | PH12-04, PH11-02 | Qualitative electromagnetic induction: changing flux/linkage | Magnet-coil motion timeline; change matters, static field alone does not | EXPLAIN, MODEL, REPRESENT | D3: diagnose current appearance under different relative motions |
| PH12-10 | F | CBSE10 | PH12-09 | Lenz response and induced direction, when explicitly warranted | Opposing change diagram; do not confuse opposing motion with opposing flux change | MODEL, REPRESENT, JUSTIFY | D3 candidate: decide induced direction from specified change; detailed formula E |
| PH12-11 | F | CBSE10 | PH12-09 | Electric generator, relative motion and AC principle | Coil motion and output direction sequence; formative in X | EXPLAIN, SYNTHESIZE, REPRESENT | D3: distinguish generator action from motor action under reversal |
| PH12-12 | C | CBSE10 | PH12-11, PH11-02 | AC and DC; AC frequency and transmission advantages | Voltage-versus-time waveform; compare frequency and waveform sign | EXPLAIN, REPRESENT, JUSTIFY | D3: infer qualitative output from a changed source |
| PH12-13 | C | CBSE10 | PH11-11 | Domestic circuits: shared boundary with PH11 | Fuse, earthing, live-neutral conductors; owned once in PH11 | MODEL, SYNTHESIZE, JUSTIFY | D3: integrated safety and magnetic-effects task with explicit ownership link |
| PH12-14 | E | CBSE_HIGHER (comparison only) | PH12-09 | Quantitative Faraday flux laws and motional emf | Flux-change and conductor-motion expressions; outside explicit X treatment | MODEL, APPLY, SYNTHESIZE | D4 optional only; cannot infer compulsory scope from past candidate |
| PH12-15 | E | CBSE_HIGHER (comparison only) | PH12-14, PH01 (unbound) | Electromagnetic braking, induced drag and terminal velocity | Multiple energy-flow and force models; advanced cross-topic mechanics | MODEL, SYNTHESIZE, JUSTIFY | D4 optional; flag extension and scientific warrant HOLD |

**Planned denominator:** PH07: 12, PH08: 13, PH09: 12, PH10: 17, PH11: 14, PH12: 15 = **83 proposed subtopics**. Not all are compulsory-syllabus content; enrichment rows are explicitly excluded from the compulsory coverage denominator until separately accepted.

## D. Scientific model, representation and misconception requirements by chapter
| Topic | Scientific minimum to author and review | Representations and critical wrong-route tests |
|---|---|---|
| PH07 | Heat-flow direction; material properties; open/closed environment; phases versus sensible heating; never use `Q=mcΔT` across phase transition without a piecewise model; no isolated calorimeter assumed without warrant. | Heating/phase diagrams, material stacks, cooling experiments; temperature vs heat, conduction vs convection, latent vs sensible; thermal expansion assumptions. |
| PH08 | Medium-dependent wave speed, longitudinal propagation, speed-frequency-wavelength relation, timing including one- versus two-way path, audible perception. | Pressure/particle/time/distance graphs; pressure versus displacement; amplitude versus frequency; echo versus reverberation; multi-path geometry. |
| PH09 | Laws of reflection, ray model, spherical mirrors, real/virtual classification, focal geometry, explicitly signed mirror equation and paraxial limits. | Principal-ray and backward-extension diagrams; image displacement vs object displacement; real versus virtual, convex versus concave, consistent sign reference. |
| PH10 | Snell law, index conventions, slab/prism ray geometry, thin-lens and human eye models, real/virtual image limits, magnification, dioptres; high-order lens constructions need extra warrants. | Incident/refracted/emergent rays; actual vs apparent depth; pupil/retina focus; source/screen geometry; sign conventions, paraxial approximation and physical-root checks. |
| PH11 | Charge conservation/current continuity, Ohm-law applicability, series/parallel invariants, resistivity geometry, energy/power/rating, household safety. | Node-edge circuit topology and V–I plots; current not consumed; voltage not identical in series; resistor nonohmic behaviour, fusing and watt-hour versus watt. |
| PH12 | Field conventions, right-hand rule and force direction, coil/solenoid qualitatives, induction as *change*, generator/motor energy direction, school-formative distinction. | 3D direction arrows, coil sequence, time traces; no induction merely because magnet exists; Fleming L/R distinctions; AC time variation vs sign at an instant. |

## E. Proposed demand construction signatures — priority D3 and selective D4
| Topic | First D3 task signature | Selective D4 task — only if independently supported | Protected learner W |
|---|---|---|---|
| PH07 | Compare thermal-energy transfer explanations in a multi-material or multi-stage setting | Composite heat/phase energy balance **extension-only** | Identify physical exchange regime and choose valid model rather than run a fixed formula |
| PH08 | Infer distances from wave/echo recordings with nontrivial paths | Infer path/order from multiple overlapping echoes; quantitative Doppler **extension-only** | Choose path topology and preserve time-versus-distance representation |
| PH09 | Explain image position/direction under object/mirror changes | Coupled mirror or moving-mirror regime with failed simple-image shortcut **conditional extension** | Defend correct image model and sign reference |
| PH10 | Infer lens positions from object–screen data | Refute an inverse two-image claim at a boundary or mixed optical setup | Choose applicable thin-lens model, identify discriminant/physical root and counterexample |
| PH11 | Simplify unfamiliar but school-scope mixed resistor networks, correctly preserving nodes | Graph-symmetry cube/ladder only as **extension** | Decide which components are actually in series/parallel or equivalent by topology |
| PH12 | Infer field or induced-current direction under changed motion | Coupled mechanical-electric response/terminal motional emf as **extension** | Identify *change* in linked magnetic field and directional consequence, not a memorized arrow |

**Rule:** each task has one *primary* reviewed QRT operation. Other cognitive contributions are secondary. `D3=6–7`, `D4=8–10` are the unchanged five-factor draft rubric and require actual evidence; no mechanical score is an independent academic verdict. D1/D2 Physics common Blueprint remains `SPEC_PENDING`.

## F. Authenticity / Core2 source-ledger and explicit HOLD register
| Finding | PH impact | Required response |
|---|---|---|
| All 95 Physics metadata rows | All | Metadata only; `source_custody:HOLD`, `independent_qrt_review:NOT_RUN`; no verified exam item may populate an admitted cell. |
| 50-record alternate candidate corpus | PH09/10=10 OPTICS; PH11=10 CURRENT_ELECTRICITY; PH12=10 MAGNETISM_AND_EMI; PH07/08=none by category | Reconcile corpus vs 95-map by exact source, never sum candidate counts; zero D4 class claims in 50-record corpus. |
| Source ledger `NSEJS-23-OPT-01`: 2023 Set 51 Q43 official-key B locator recorded | PH09 candidate | Locator/key cross-check recorded in repo; digital text/options/figure fidelity still HOLD; independently compare original paper/key bytes before any admission. |
| Source ledger `NSEJS-24-CIRC-01`: 2024 Set 51 Q42 official-key D locator recorded | PH11 | Original figure required and not held; exact stem/options/figure source custody HOLD. |
| Source ledger `NSEJS-24-MAG-01`: 2024 Set 51 Q44 official-key D locator recorded | PH12 | Original figure required and not held; exact stem/options/figure source custody HOLD. |
| False 2024 optics locators `NSEJS-24-OPT-01` claimed Q1 and `NSEJS-24-OPT-02` claimed Q2 | PH09/10 | Repo ledger states those original numbered positions are Biology topics, not optics; reject these as direct-exam evidence pending authentic remapping. |
| Supplemental authored lens/circuit/magnetism journeys | PH09–PH12 | May be used as `AUTHORED_TRANSFER` after science/task review, NEVER as verified NSEJS exam questions or restored historical originals. |
| PH07 and PH08 source corpus | PH07/08 | No PH07/08 category candidate in the 50-item corpus. Search official full papers as a future source-intake task; inventory does not establish absence from actual exams. |
| Source and redistribution rights | All | Public Git requires independent rights check; original figures/scans/keys stay private pending permission. |

Source evidence file: https://github.com/reallakshman19/Grade9v4.1/blob/82a782f12c57b5d9d25e9b1eb8d2053a56dfabc0/nsejs/data/physics-core2-source-evidence.v1.json  
Corpus: https://github.com/reallakshman19/Grade9v4.1/blob/82a782f12c57b5d9d25e9b1eb8d2053a56dfabc0/nsejs/data/physics-core2-candidates.v1.json  
Map: https://github.com/reallakshman19/Grade9v4.1/blob/82a782f12c57b5d9d25e9b1eb8d2053a56dfabc0/nsejs/core2/question-map.v1.json

## G. Dependencies, Agent 1 ownership and cross-topic joins
| Dependence | PH07–PH12 need | Owner/authority | Phase 0 action |
|---|---|---|---|
| PH00 common measurements | units, graphs, uncertainty, experimental reasoning | Agent 1 / shared | Reference as future pinned prerequisite; no duplicate common file. |
| PH01–PH03 Mechanics | forces, kinematics, energy, relative motion | Agent 1 | Use for moving-reflector tasks, electrical-energy conservation and motor forces via reviewed links. |
| PH04 WPE | energy and power, efficiency, signed work | Agent 1 | PH07 heating, PH11 power and PH12 motors refer to PH04, not copied formulas. |
| PH05 Gravitation / PH06 Fluids | buoyancy, density and flow, pressure and winds | Agent 1 | PH07 convection/thermal expansion cross-link to PH06 only; `fluids-sound` belongs PH06. |
| PH07 + PH11 | electric heating/thermal energy exchange | Agent 2, single primary ownership PH11 Joule heat | Link PH11 law to PH07 model; do not duplicate canonical science record. |
| PH09 + PH10 | reflective ray law vs refractive lens law | Agent 2, mirror ownership PH09, lens PH10 | Avoid two canonical chapters claiming same optical construction. |
| PH11 + PH12 | circuits, DC/AC, safety and electromagnetic energy | Agent 2; domestic circuit primary PH11, magnetism PH12 | Cross-reference without double counting; PH12 induction qualitative formative. |
| Core Contracts C01–C08 | shared versioned package and semantic validation | Agent 1 | Draft PR #2 engineering candidate; accept pin before authoring on an isolated Agent 2 branch. |
| Shared QRT 28 and Physics D3/D4 14 | exact cognitive rule and subject blueprints | Shared/Physics owners | Immutable external/shared pins; no new D4 or D1/D2 scoring method. |
| B1–B7 and release | independent target, signature, teaching, fresh transfer, protected attempt, diagnosis and science/provenance | Independent reviewers + Owner | All HOLD/NOT_RUN until real evidence. |

## H. Exact inspected engineering pins and admissibility
| Dependency | Pin / state |
|---|---|
| Planning commit | `82a782f12c57b5d9d25e9b1eb8d2053a56dfabc0` |
| Observed main | `dca026b4f0904d272251d3ef816ce0335af6b18b`; one commit beyond planning baseline (as observed). |
| Draft PR #2 head | `330f9524fe37cff53f20b6f094c85e4739da3a66`, unmerged; mergeability reported false in metadata at inspection |
| C01–C08 | `1.0.0` `ENGINEERING_CANDIDATE__ACADEMIC_HOLD`; contract registry Git blob SHA `404809faf6989a81ab11b85a7eaf33040962bbae` |
| Shared QRT 28 | Grade9v3.5 commit `574c7fe2`, `Shared/quality/question-demand-templates.v1.json`, recorded Git blob `e2409aef11ae7d98444593bfbe1a38eb00c97cef`, external pin |
| Physics Blueprint | v0.2.0, repository blob `700dafcbe86d76442637bcf214eeb544497cf4ea`, `DRAFT_OWNER_REVIEW`, 14 D3/D4 cells |
| Resolved Physics Blueprint | v0.2.0, blob `b53b970d9ff99e696e84fe6b77805dbf25e0c544`, draft |
| D3 subtile addendum | v0.2.1, blob `b5294b8e510098bef5b3cb3d50658f8748bfda8b`, draft; D3.1 PAUSED |
| WPE historical adapter | `UNSELECTED` — owner-local multiple versions, not in public tree |
| D1/D2 common Physics Blueprint | `SPEC_PENDING` |
| Original upstream Issue #1 | `https://github.com/reallakshman19/Grade9v4.0/issues/1` returned GitHub 404; cannot claim full source-spec review |
| PR #2 CI | GitHub Actions 43460158170: Python 3.11 `351 passed, 1 warning`; Python 3.12 `351 passed, 1 warning` — source PR head mechanical regression, not local execution or academic qualification |

## I. Gap and risk decisions
| Risk ID | Evidence | Disposition | Required next action |
|---|---|---|---|
| P0-01 | Official coverage is Class X and below, not broad coaching topic list | SCOPE_HOLD | Source-match every PH07 E and PH12 E row before compulsory admission. |
| P0-02 | D1/D2 Physics common Blueprint absent | SPEC_PENDING | Foundation may be written pedagogically; no D1/D2 Physics-cell approval claim. |
| P0-03 | Physics Blueprint v0.2.0 draft, D3.1 paused | BLUEPRINT_HOLD | Keep parent pins, use approved gap-note process. |
| P0-04 | PR #2 unmerged, main moved one commit | INTEGRATION_HOLD | Agent 1 owner reviews/adopts base, Agent 2 branch from exact mutually pinned contract head only after acceptance. |
| P0-05 | 2 false optics 2024 item locators | SOURCE_FAIL (for those claimed locators) | Correct exact paper refs/keys privately, do not relabel unexamined items. |
| P0-06 | 2024 circuit/magnetism source figures absent | SOURCE_HOLD | Acquire original rights-cleared figure custody and exact text before source binding. |
| P0-07 | Supplemental recovery modules are not restored originals | LINEAGE_HOLD | Retain original identity/register; map supplements as authored transfer only. |
| P0-08 | Modern PH07 calorimetry/PH12 motional EMF outside explicit school syllabus | SCIENCE_SCOPE_HOLD | Treat as optional E, not required syllabus. |
| P0-09 | A subtopic has three operations but one source question | COVERAGE_HOLD | Require independently fresh three **task signatures** and B3/B4 review; a question cannot supply three primary operations. |
| P0-10 | Current native renderer is exam-first with compressed Core1A | PEDAGOGY_HOLD | Write chapter-first narrative before constructing task-specific cycles; inspect 12.7-inch UX. |
| P0-11 | Original source/figure/key rights unknown | RIGHTS_HOLD | Publish only independently authored noninfringing representations until rights accepted. |
| P0-12 | Human-reviewed academic and learner-state receipts absent | RELEASE_HOLD | B1–B7, seven gates and exact-head HTTP Chromium checks; no merge/deploy without Owner authorization. |

## J. B1–B7 evidence and C04 adapter gap preflight
| Witness | Required later acceptance evidence | Current Phase 0 disposition |
|---|---|---|
| B1 — Target | Exact subtopic, scientific construction and independently traceable target/source | NOT_RUN; this register only proposes identities |
| B2 — Construction signature | Shortest valid route, primary operation, precise protected W and scientific warrant | NOT_RUN; operation triplets here are candidates |
| B3 — Teaching sufficiency | Full prerequisite-to-derivation textbook narrative, diagrams, worked examples, checks, expert reading | NOT_RUN; no six accepted chapters exist |
| B4 — Fresh reconstruction | Independently challenging Core1B tasks distinct in reasoning and values from examples/exam | NOT_RUN; task ideas are proposals, not learner artifacts |
| B5 — Protected first attempt | Real persisted first response, help exposure, refresh, keyboard and disabled-storage fail-closed behavior | NOT_RUN; PR #2 schema checks are not runtime evidence |
| B6 — Diagnosis and transfer | Error discrimination from saved attempts, repair, boundary and unseen changed-condition result | NOT_RUN; misconception themes specified only |
| B7 — Physics and provenance | Correct laws, units, assumptions, source-role and figure/key/rights integrity | HOLD; original examinations and scientific claims not independently accepted |

**Candidate adapter requirements, not proven Blueprint defects:** PH07 needs conditional/piecewise phase and heat-flow states; PH08 needs time-versus-space wave representations plus variable-path delay; PH09/PH10 need per-element sign conventions and actual versus apparent ray extensions; PH11 needs node-edge topology preserving electrical equivalence; PH12 needs consistent three-dimensional field/current/force orientation and school-formative flags. Test these against PR #2 `topic_adapter.cells`, science records and figure contract *after acceptance*. If an instance cannot be represented under an exact pinned contract, return a reproducible gap note to Agent 1; **do not modify C01–C08, Shared QRT, or the Physics Blueprint.**

**No technical execution was performed on this content package**; the only observed CI result is the existing shared-contract PR #2 workflow reported above. This read-only source/inventory analysis does not include local `pytest`, schema validation against drafted PH packages, or Chromium checks, because no PH07–PH12 package was authored.

## K. Next-gate execution order (no action taken)
1. **Owner/Agent 1 contract acceptance:** review PR #2, exact `C01–C08` pins, ownership, schema and any merge/rebase conflict. Preserve current `main` changes; no direct Agent 2 authoring yet.
2. **Inventory reconciliation:** Agent 1 assigns canonical C01 IDs and shared cross-topic prerequisite refs; Agent 2 reconciles all provisional IDs in this report, leaving E/F/P labels explicit.
3. **Choose first PH07–PH12 pilot:** PH10 refraction/lens chapter is technically richest and has an existing unqualified candidate; PH08 sound is clearest verified curricular gap. Use one to prove chapter-first Core1A and 3-operation QRT integration.
4. **Author in isolated Agent 2 branch** against accepted contract base: C01→C02→C03→C04→C05 textbook→C06 fresh attempts→C07 admitted sources only→C08 evidence. Never change Agent 1 files or shared contracts.
5. **Return six separate candidate packages and adapter pins**, native figures and citations, gap notes as needed, and exact QA logs; create draft PRs only; await independent science/QRT and Owner acceptance before merge/deploy.

**Phase 0 conclusion:** 83 proposed inventory subtopics cover PH07–PH12 planning, including explicit source-scope hold rows. No complete Core1A chapter, approved Physics topic adapter, independently admitted exam item, B1–B7 approval or release is established by this read-only inventory.
