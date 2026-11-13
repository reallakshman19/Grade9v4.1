# PH11 — Current Electricity
## Continuous Core1A textbook manuscript · R2 author candidate

**Status:** AUTHOR_EXPOSED_DRAFT · SCIENCE_REVIEW_HOLD · NOT A PUBLISHED TEXTBOOK.  
**Curriculum boundary:** CBSE Class X electrical circuits, resistance, potential difference, current, power/heating and household safety. Infinite networks, cube reductions and nonideal-source load lines remain **EXTENSION**, not compulsory NSEJS assumptions.

### 1. What makes a circuit operate?

A lamp lights when an electrical source, the lamp and connecting conductors form a closed conducting path through which charge can flow. A diagram that looks circular may nevertheless contain a broken switch, loose connection or bypass wire. Decide connectivity before doing any calculation.

Electric current is the rate of flow of charge across a selected cross-section: \(I=\Delta Q/\Delta t\) for average current during a finite interval. The unit ampere is coulomb per second. In a steady circuit the current in and out of a small junction balances because charge cannot accumulate there indefinitely. This is conservation of charge, not a convention about how artists draw wires.

**Diagnostic:** If 2 A enters an ideal junction and two wires carry 0.7 A and 1.3 A away, charge balances. A claim that “some current is used up by the lamp” confuses energy transfer with charge conservation.

### 2. Conventional current, electron drift and direction

The conventional direction of current in an external circuit is from higher electrical potential toward lower potential through passive resistive elements. In ordinary metal wires, mobile electrons drift on average in the opposite direction. Both statements can be true because conventional current is defined in terms of positive charge flow.

Reversing a battery swaps polarity and reverses the conventional current in a simple passive DC circuit. The direction arrows must be changed consistently. The wires and the charge do not need to be “consumed” for the lamp to receive energy; the electric field can transfer energy to the circuit's loads.

**Check:** A student's electron-arrow diagram disagrees with a conventional current arrow. Is either automatically wrong? No; first identify what the arrow labels describe.

### 3. Potential difference is measured between two points

The potential difference between nodes A and B is \(V_{AB}=V_A-V_B\). A voltmeter must be connected across the relevant two nodes, because its job is to compare potentials, not to carry the whole lamp current. An ammeter is normally placed in series in the branch whose current is to be measured. Ideal meters illustrate the distinction: a voltmeter has extremely high resistance; an ammeter extremely low resistance.

Connecting an ammeter directly across a battery may create a hazardous low-resistance path. Classroom experiments should use proper protected supplies and teacher-approved setups; never instruct a learner to test a real household mains circuit.

**Worked reasoning:** A diagram places a voltmeter in series with one resistor. Under the ideal-voltmeter model it would greatly reduce current, making the measurement arrangement inappropriate. The wrong result is not corrected by changing the resistor's numerical value.

### 4. Ohm's law is conditional

For an ideal ohmic resistor at approximately constant temperature, \(V=IR\) relates voltage, current and resistance. The slope of a \(V\)-versus-\(I\) graph is \(R\); the slope of an \(I\)-versus-\(V\) graph is \(1/R\). State the axis order before reporting a slope.

Real filaments can heat as current increases, changing resistance and producing a curved characteristic. Their nonlinear response does not mean charge conservation has failed; it means the constant-\(R\) approximation is no longer appropriate.

**Worked anchor:** A resistor has measured values \(V=2,4,6\) V at \(I=0.5,1.0,1.5\) A under controlled thermal conditions. Each ratio \(V/I\) equals 4 Ω. A plot with voltage vertical would have gradient 4 Ω. Reversing the axes changes the reported numerical slope but not the underlying observations.

### 5. Why wire geometry matters

A long uniform wire has more resistance than a shorter wire of the same material and cross-sectional area, all else equal. Its resistance is modeled by \(R=\rho L/A\), where \(\rho\) is material resistivity. The equation assumes a uniform wire and a suitable approximately constant resistivity over the measurement range.

Double a wire's length while preserving area and material and resistance doubles. Double the cross-sectional area at fixed length and resistance halves. But “stretch the wire to double its length” may also reduce its cross-sectional area if volume is nearly conserved; then treating area as fixed is not physically justified.

**Transfer:** A wire of length L and area A is stretched uniformly to length 2L while volume stays fixed. The new area is A/2. With unchanged resistivity, \(R'=\rho(2L)/(A/2)=4R\), not 2R. This is a model with explicit assumptions, not a generic rule for all material deformation.

### 6. Series circuits have one steady branch current

In a simple series connection, every resistor lies on the same current path, so the steady current is the same through each. Under ideal wire assumptions the total voltage drop across the string is the sum of individual drops. Thus \(R_{\rm eq}=R_1+R_2\) for two ohmic resistors.

Voltage is divided, but not necessarily equally; for the same current \(V_1:V_2=R_1:R_2\). An open component in a simple one-path series string can interrupt current throughout the string.

**Worked anchor:** A 3 Ω and a 6 Ω resistor are connected in series to an ideal 9 V source. Total resistance 9 Ω, current 1 A, drops 3 V and 6 V. The sum agrees with source voltage.

### 7. Parallel networks share node-to-node voltage

Resistors in parallel connect between the same two nodes. The shape of a circuit drawing cannot tell us whether two components are parallel unless their electrical endpoints are identified. Two lines crossing without a junction marker are not necessarily electrically connected.

For two parallel ideal resistors, \(I_{\rm total}=I_1+I_2\) and \(1/R_{\rm eq}=1/R_1+1/R_2\). The same potential difference acts across both branches, while currents depend on the separate resistances.

**Worked anchor:** A 6 Ω and a 3 Ω resistor in parallel across 12 V draw 2 A and 4 A. Total 6 A and \(R_{\rm eq}=2\) Ω. The equivalent resistance is smaller than either branch resistance, as it must be for positive resistors in parallel.

### 8. A mixed network is a graph, not a picture puzzle

For a circuit with more components, mark nodes, then identify actual series chains and parallel branches before reducing the network. A resistor pair sharing one common node is **not** automatically in series if a third conductor branches from that node. Likewise, visually side-by-side resistors can fail to share both endpoints.

The valid order of reductions can matter for keeping track of intermediate potentials, although equivalent resistance between the same terminals must be invariant. After reduction, reconstruct individual branch currents rather than assuming they equal the total current.

**Connected example:** A 2 Ω resistor in series with a parallel pair 3 Ω and 6 Ω has \(R_\parallel=2\) Ω and total resistance 4 Ω. On an ideal 12 V supply, total current 3 A. The parallel pair receives 6 V; its branch currents are 2 A and 1 A, summing to 3 A. This provides both a numerical and conservation-law check.

### 9. Electric power differs from energy

A load's electrical power at a particular operating point is \(P=VI\). For an ohmic resistor the same power can be written \(P=I^2R=V^2/R\), but the chosen identity must use the correct actual current or voltage. Power is measured in watts, while energy is power multiplied by time and can be measured in joules or kilowatt-hours.

An appliance rated “100 W at 220 V” is not guaranteed to consume 100 W when connected to a different voltage. For an ideal fixed resistance, its operating power changes approximately as the square of voltage.

**Worked anchor:** A steady 60 W lamp operates for 3 hours. Ideal electrical energy \(E=60\times3=180\) Wh = 0.18 kWh. Do not call the energy “180 watts.”

### 10. Why a resistor gets warm

Electrical energy can become thermal energy in a resistor. For a constant ohmic resistor over time \(t\), the transferred energy is \(E=I^2Rt\), and in the ideal Joule-heating setting becomes thermal energy. The formula is a consequence of \(E=Pt\) and \(P=I^2R\); it is not a separate conservation rule.

Comparisons require knowing what is held fixed. At fixed current, increasing resistance increases \(I^2R\). At fixed voltage, increasing resistance decreases \(V^2/R\). Therefore the statement “a larger resistance always heats more” is false without specifying the operating conditions.

The resulting temperature rise also depends on thermal losses and heat capacity, which cross-link to PH07. Electrical heating power does not uniquely predict final temperature without a thermal model.

### 11. Household wiring uses protection, not shortcut experiments

Domestic circuits are arranged with live, neutral and protective earth conductors in prescribed roles. Appliances are generally connected in parallel to receive the intended supply voltage. Protective earth provides a fault-current path when properly connected to the protection system, and fuses or circuit breakers interrupt abnormal currents under their rated conditions.

A fuse should not be treated as a normal load, and protective devices are not interchangeable. Correct protection depends on installation details and local electrical rules. For a junior-science textbook, use schematic safety reasoning; never propose hands-on tests with household mains power.

**Diagnostic:** Why is a simple “parallel means safe” assertion inadequate? An unintended low-resistance short-circuit path can draw dangerous current even in a circuit with parallel loads.

### 12. Measure carefully: circuit experiments are models too

A standard school experiment records V–I pairs for a resistor at controlled temperature, chooses appropriate instrument ranges and plots the measurements. If an ammeter has nonzero internal resistance or a voltmeter loads a high-resistance circuit, readings can differ from ideal predictions. Scientific reporting must distinguish measurement uncertainty and a change in the physical model.

An observed curve in a real filament experiment may represent heating rather than a defective instrument. Conversely, a negative resistance inferred from a student's mislabeled axes may reflect a representation error. The experiment should capture the actual wiring and graph axes before assigning a physical explanation.

### 13. Advanced resistor topologies: extension gate

Cube, tetrahedron, infinite-ladder and graph-symmetry networks can be intellectually valuable D4 practice but are **EXTENSION/HOLD** under the school-level syllabus register until separately accepted. An exact source claim requires the original examination item, figure, answer-key and task-specific QRT review. The existence of a recovery page does not establish that the original construction is published or qualified.

If such tasks are taught, lead with node equivalence and conservation, not with memorized reductions. A symmetric network becomes simple only when the stated voltage boundary conditions truly force some nodes to the same potential.

### 14. Non-ohmic source models: another boundary

Real cells have internal resistance; terminal voltage can change under load. Diodes and lamps can display nonlinear V–I behavior. These are legitimate scientific examples of model limitations, but elaborate load-line and nonohmic network calculations are not automatically part of the compulsory Class X syllabus.

The reasoning habit is general: declare the ideal source or real source assumption and decide whether Ohm's law with constant R applies to the component at that operating point.

### 15. Chapter synthesis and fresh cognitive targets

The core progression is closed paths → conservation of charge → potential difference → instruments → Ohm's law applicability → series/parallel topology → energy and power → safe measurement. The conceptual difficulty increases when the diagram hides node identity, when operating conditions change, or when power and energy are confused.

The chapter's representative D3 targets are MODEL (identify the correct circuit topology), REPRESENT (translate a node list to a wiring graph while preserving connections), and APPLY/SYNTHESIZE (compute branch currents and power using charge conservation and valid reductions). D4 remains **unadmitted** until a specific unseen task warrants the higher five-factor total.

**Independent exit investigations:** Redraw a crossing-wire network without changing connectivity; reject a false series claim at a branching node; compare \(P=I^2R\) under fixed current against \(P=V^2/R\) under fixed voltage; and explain why an ammeter cannot replace a voltmeter. Only PH11-07 currently has the native lead's protected Core1B candidate cycle; other subtopics require authoring and reviewer assessment.
