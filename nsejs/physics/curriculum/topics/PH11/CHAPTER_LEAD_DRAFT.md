# PH11 — Parallel resistors, branch currents and electrical loading

**AUTHOR-EXPOSED CORE1A LEAD DRAFT · NOT COMPLETE CHAPTER · ACADEMIC HOLD**

## Begin with an observation

Adding a second lamp branch can change the total current drawn from a battery even if each branch receives the same voltage.

## Build the physical idea

In a circuit schematic, two components are in parallel only when both ends are connected to the same two electrical nodes. A drawn branch crossing another wire does not imply a connection without a junction mark. By definition, components sharing the same node pair have the same potential difference. At each junction, conservation of charge requires the currents entering and leaving to balance. For ideal ohmic resistors, I=V/R. Combining these principles gives 1/Req=1/R1+1/R2. Unlike a single path, a parallel network divides the current, not the voltage. A lower equivalent resistance at fixed ideal source voltage means a larger total current. Real cells can sag under load, so the phrase 'fixed voltage' is a model assumption, not an unavoidable physical fact.

## Derive the model, not a shortcut

1. **Label the two nodes and establish equal voltage across each resistor.** Why valid: Potential difference depends only on the node pair, not the shape of the drawing.

2. **Apply I1=V/R1 and I2=V/R2 to the branches.** Why valid: Ohm's law applies here to each ideal resistor at fixed operating conditions.

3. **Use Itotal=I1+I2 and define Req=V/Itotal to derive the reciprocal relation.** Why valid: Charge is conserved at junctions, so total current adds rather than being consumed.

## Three worked tiers

### Foundation

**Question:** Connect 6 ohm and 3 ohm resistors in parallel across an ideal 12 V battery. Find branch currents.

**Reasoning:** I1=2 A and I2=4 A; Itotal=6 A, Req=2 ohm.

**Independent check:** Req is less than the smaller branch resistance and the currents sum to 6 A.

### Connected

**Question:** An ideal 9 V source drives a 9 ohm resistor. Add another 9 ohm parallel branch; compare total current.

**Reasoning:** Total current increases from 1 A to 2 A; equivalent resistance halves to 4.5 ohm.

**Independent check:** Each branch still carries 1 A, assuming ideal fixed source voltage.

### Advanced

**Question:** A 4 ohm and 12 ohm network is drawn with both ends at the same nodes but the lines cross. What is Req?

**Reasoning:** If both components share the two nodes, Req=(4*12)/(4+12)=3 ohm, regardless of the drawn crossing.

**Independent check:** Redraw as two unmistakable parallel branches and check 1/3=1/4+1/12.

## Conditions and limitations

- A parallel pair cannot be treated as a series string
- At a junction charge conservation constrains total current; current is not consumed by components
- A source with significant internal resistance may change terminal voltage when a load is added

## Diagnose a plausible mistake

**Wrong idea:** Current entering a resistor is partly used up, so branch currents must get smaller along the wire.

**Diagnostic:** Where does charge go at a split junction in steady state?

**Repair:** Charge is conserved: the entering current equals the sum of outgoing branch currents.

## Exit question

Two 8-ohm resistors are in parallel across an ideal 8 V source. What is the total current?

**Answer:** 2 A. Each branch draws 1 A; the total is 2 A and equivalent resistance is 4 ohm.

## Visual specification

Original two-node network with marked junctions, two branch resistors, separate I1 and I2 arrows, and an ammeter showing the total current before branching.

## Adjacent chapter syllabus

The other subtopics in PH11 are listed in the sibling 83-subtopic inventory. They are not presented here as taught or qualified. This file covers precisely the authored lead subtopic PH11-07.
