# PH10 — Lens displacement: conjugate images and limiting geometry

**AUTHOR-EXPOSED CORE1A LEAD DRAFT · NOT COMPLETE CHAPTER · ACADEMIC HOLD**

## Begin with an observation

With an illuminated object and fixed screen, moving a convex lens can produce two separate sharp-image positions.

## Build the physical idea

Place a real object and a screen a fixed distance D apart. A converging thin lens forms a sharp real image only if the object and image distances satisfy its conjugate relation. When we slide the lens, increasing its object distance simultaneously decreases its distance to the screen. This constraint is the key to the two-position effect, not a memorized formula. Let x be the object-to-lens distance, so the lens-to-screen distance is D-x. Substitution into 1/f=1/x+1/(D-x) produces x(D-x)=fD. The left-hand side is a concave quadratic with maximum D²/4 at the midpoint. Thus a real focus exists only if D≥4f. At equality the two locations coincide. When D>4f, two distinct solutions x1 and x2 add to D. One gives a larger inverted image and the other a smaller inverted image. Measuring the distance d between lens positions permits an inverse determination of f, but only with careful definition of D and d and within the thin-lens approximations.

## Derive the model, not a shortcut

1. **Let x denote object-to-lens distance and D-x lens-to-screen distance.** Why valid: The object and screen are fixed, so their lens distances sum to D.

2. **Use 1/f=1/x+1/(D-x) and rearrange to x²-Dx+fD=0.** Why valid: The thin-lens law holds for paraxial real conjugate imaging in the adopted positive-distance convention.

3. **Require a nonnegative discriminant D²-4fD and distinguish equality from two distinct roots.** Why valid: Real positions require nonnegative discriminant; two distinct positions require it to be positive.

4. **Use d=|x2-x1| and x1+x2=D to derive f=(D²-d²)/(4D).** Why valid: Root sum/product identities preserve the two-position geometry and yield the inverse focal-length relation.

## Three worked tiers

### Foundation

**Question:** Object and screen are 90 cm apart and f=20 cm. Find all sharp-image lens positions.

**Reasoning:** Solve x²-90x+1800=0, giving x=30 cm and x=60 cm.

**Independent check:** Both yield 1/20=1/30+1/60; separation d=30 cm.

### Connected

**Question:** The object-screen separation is 80 cm, and the two distinct lens positions are 40 cm apart. Estimate f.

**Reasoning:** f=(80²-40²)/(4*80)=(6400-1600)/320=15 cm.

**Independent check:** D>4f is 80>60, consistent with two positions.

### Advanced

**Question:** A technician fixes D=60 cm for a lens with f=15 cm and expects two distinct image positions.

**Reasoning:** D=4f: only one position at x=D/2=30 cm, a double root.

**Independent check:** The discriminant vanishes; having two equal algebraic roots is not two distinct lens settings.

## Conditions and limitations

- At D=4f there is one double root, not two distinct lens positions
- For D<4f no positive real screen-image lens positions exist in the thin-lens model
- Scattering, aberration or a thick-lens principal-plane shift can invalidate numerical use of a thin-lens approximation

## Diagnose a plausible mistake

**Wrong idea:** The fixed object-screen distance guarantees two sharp-image lens positions for any converging lens.

**Diagnostic:** What happens at D=4f? Do two equal quadratic roots represent separate settings?

**Repair:** Interpret the discriminant and physical position domain; D=4f has one position, D<4f has none.

## Exit question

A converging lens has f=18 cm; a fixed object-screen separation is D=70 cm. Are sharp-image positions possible?

**Answer:** No sharp real image positions under this thin-lens model. 4f=72 cm is greater than D, so the discriminant is negative.

## Visual specification

Original to-scale object–lens–screen track with adjustable x, fixed D, two candidate lens positions, and separate ray sketches for enlarged/reduced inverted images.

## Adjacent chapter syllabus

The other subtopics in PH10 are listed in the sibling 83-subtopic inventory. They are not presented here as taught or qualified. This file covers precisely the authored lead subtopic PH10-09.
