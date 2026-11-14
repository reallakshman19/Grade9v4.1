"""Generate 4 W3C compliant Biology SVGs with font-size >= 14px and viewBox="0 0 780 440".
Saves to both nsejs/assets/ and nsejs/biology/assets/.
"""
from pathlib import Path

DEST_DIRS = [Path("nsejs/assets"), Path("nsejs/biology/assets")]
for d in DEST_DIRS:
    d.mkdir(parents=True, exist_ok=True)

# 1. Complementary Gene Pathway & Meiotic Stoichiometry
SVG_GENES = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 780 440" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGen" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fdf4ff"/>
      <stop offset="100%" stop-color="#fae8ff"/>
    </linearGradient>
    <filter id="shadowGen" x="-5%" y="-5%" width="110%" height="115%">
      <feDropShadow dx="2" dy="3" stdDeviation="3" flood-opacity="0.12"/>
    </filter>
    <marker id="arrowGen" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
      <path d="M 0 0 L 8 4 L 0 8 Z" fill="#86198f"/>
    </marker>
    <marker id="arrowMeio" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
      <path d="M 0 0 L 8 4 L 0 8 Z" fill="#0369a1"/>
    </marker>
  </defs>

  <rect width="780" height="440" fill="url(#bgGen)" rx="16"/>
  <rect x="16" y="16" width="748" height="408" fill="#ffffff" rx="12" stroke="#e879f9" stroke-width="2" filter="url(#shadowGen)"/>

  <!-- Header -->
  <text x="390" y="44" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="20" font-weight="800" fill="#701a75">Sweet Pea Complementary Gene Pathway (9 : 7 Ratio) &amp; Meiotic Divisions</text>
  <text x="390" y="68" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="600" fill="#86198f">Anthocyanin Biosynthesis Pathway: Both Enzyme C and Enzyme P are Required</text>

  <!-- Metabolic Pathway Diagram -->
  <rect x="40" y="90" width="700" height="135" rx="10" fill="#fdf2f8" stroke="#f472b6" stroke-width="1.5"/>
  <text x="56" y="114" font-family="system-ui, -apple-system, sans-serif" font-size="15" font-weight="800" fill="#9d174d">Biochemical 2-Step Pathway:</text>

  <!-- Step 1 Box -->
  <rect x="56" y="128" width="165" height="58" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="2"/>
  <text x="138" y="152" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="15" font-weight="700" fill="#475569">Colorless Precursor</text>
  <text x="138" y="172" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="600" fill="#64748b">(Substrate 1)</text>

  <!-- Enzyme C Arrow -->
  <line x1="225" y1="157" x2="285" y2="157" stroke="#86198f" stroke-width="3" marker-end="url(#arrowGen)"/>
  <text x="255" y="142" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="800" fill="#701a75">Enzyme C</text>
  <text x="255" y="180" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="600" fill="#9333ea">(Gene C)</text>

  <!-- Intermediate Box -->
  <rect x="290" y="128" width="165" height="58" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="2"/>
  <text x="372" y="152" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="15" font-weight="700" fill="#475569">Colorless Intermediate</text>
  <text x="372" y="172" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="600" fill="#64748b">(Substrate 2)</text>

  <!-- Enzyme P Arrow -->
  <line x1="459" y1="157" x2="519" y2="157" stroke="#86198f" stroke-width="3" marker-end="url(#arrowGen)"/>
  <text x="489" y="142" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="800" fill="#701a75">Enzyme P</text>
  <text x="489" y="180" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="600" fill="#9333ea">(Gene P)</text>

  <!-- Anthocyanin Box -->
  <rect x="525" y="128" width="195" height="58" rx="8" fill="#fae8ff" stroke="#a21caf" stroke-width="2"/>
  <text x="622" y="152" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="16" font-weight="800" fill="#701a75">PURPLE ANTHOCYANIN</text>
  <text x="622" y="174" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="700" fill="#86198f">C_P_ Genotype (9 / 16)</text>

  <text x="390" y="212" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="700" fill="#be185d">White Phenotypes (7 / 16) = 3 C_pp (Enzyme P absent) + 3 ccP_ (Enzyme C absent) + 1 ccpp</text>

  <!-- Meiotic Gametogenesis Stoichiometry -->
  <rect x="40" y="240" width="340" height="165" rx="10" fill="#f0f9ff" stroke="#0284c7" stroke-width="1.5"/>
  <text x="210" y="266" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="16" font-weight="800" fill="#0369a1">Male Gametes (Microsporogenesis)</text>
  <text x="56" y="296" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="700" fill="#0f172a">• 1 Microspore Mother Cell (2n) undergoes meiosis</text>
  <text x="56" y="322" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="700" fill="#0f172a">• Yields 4 viable, functional pollen grains (n)</text>
  <rect x="56" y="338" width="308" height="52" rx="6" fill="#e0f2fe" stroke="#38bdf8" stroke-width="1"/>
  <text x="210" y="360" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="15" font-weight="800" fill="#0369a1">For 1600 Seeds (1600 Pollen Grains):</text>
  <text x="210" y="380" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="15" font-weight="800" fill="#0284c7">1600 / 4 = 400 Meiotic Divisions</text>

  <rect x="400" y="240" width="340" height="165" rx="10" fill="#fef2f2" stroke="#ef4444" stroke-width="1.5"/>
  <text x="570" y="266" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="16" font-weight="800" fill="#b91c1c">Female Gametes (Megasporogenesis)</text>
  <text x="416" y="296" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="700" fill="#0f172a">• 1 Megaspore Mother Cell (2n) undergoes meiosis</text>
  <text x="416" y="322" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="700" fill="#0f172a">• 3 megaspores degenerate; only 1 functional egg</text>
  <rect x="416" y="338" width="308" height="52" rx="6" fill="#fee2e2" stroke="#f87171" stroke-width="1"/>
  <text x="570" y="360" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="15" font-weight="800" fill="#b91c1c">For 1600 Seeds (1600 Functional Eggs):</text>
  <text x="570" y="380" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="15" font-weight="800" fill="#dc2626">1600 / 1 = 1600 Meiotic Divisions</text>

  <!-- Bottom Summary Badge -->
  <rect x="230" y="414" width="320" height="16" fill="transparent"/>
</svg>'''

# 2. Plant Cell Water Potential & van 't Hoff Equilibrium
SVG_POTENTIAL = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 780 440" width="100%" height="100%">
  <defs>
    <linearGradient id="bgWat" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f0fdf4"/>
      <stop offset="100%" stop-color="#dcfce7"/>
    </linearGradient>
    <filter id="shadowWat" x="-5%" y="-5%" width="110%" height="115%">
      <feDropShadow dx="2" dy="3" stdDeviation="3" flood-opacity="0.12"/>
    </filter>
    <marker id="arrowCurve" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
      <path d="M 0 0 L 8 4 L 0 8 Z" fill="#15803d"/>
    </marker>
  </defs>

  <rect width="780" height="440" fill="url(#bgWat)" rx="16"/>
  <rect x="16" y="16" width="748" height="408" fill="#ffffff" rx="12" stroke="#4ade80" stroke-width="2" filter="url(#shadowWat)"/>

  <!-- Header -->
  <text x="390" y="44" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="20" font-weight="800" fill="#14532d">Solanum tuberosum Tuber Tissue Water Potential &amp; Equilibrium</text>
  <text x="390" y="68" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="600" fill="#15803d">Osmotic Incubation in Graded Sucrose Series at T = 293 K (20 °C)</text>

  <!-- Left: Mass Flux Graph -->
  <rect x="36" y="86" width="380" height="318" rx="10" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="226" y="112" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="16" font-weight="800" fill="#0f172a">Tissue Mass Change vs [Sucrose]</text>

  <!-- Graph Axes -->
  <line x1="80" y1="130" x2="80" y2="360" stroke="#475569" stroke-width="2"/>
  <line x1="80" y1="245" x2="390" y2="245" stroke="#475569" stroke-width="2"/> <!-- Baseline 0% -->

  <!-- Axis Labels -->
  <text x="48" y="136" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="700" fill="#16a34a">+Δm%</text>
  <text x="48" y="249" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="800" fill="#334155">0 %</text>
  <text x="48" y="358" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="700" fill="#dc2626">-Δm%</text>

  <!-- Sucrose tick marks -->
  <text x="140" y="265" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="600" fill="#64748b">0.10 M</text>
  <text x="210" y="265" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="600" fill="#64748b">0.20 M</text>
  <text x="250" y="282" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="15" font-weight="800" fill="#15803d">0.25 M</text>
  <text x="320" y="265" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="600" fill="#64748b">0.40 M</text>
  <text x="375" y="265" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="700" fill="#475569">[C]</text>

  <!-- Equilibrium Intersection Marker -->
  <line x1="250" y1="130" x2="250" y2="360" stroke="#16a34a" stroke-width="1.5" stroke-dasharray="4,4"/>
  <circle cx="250" cy="245" r="7" fill="#15803d" stroke="#ffffff" stroke-width="2"/>

  <!-- Curve -->
  <path d="M 90 150 Q 170 190 250 245 T 380 340" fill="none" stroke="#2563eb" stroke-width="3.5"/>

  <rect x="135" y="296" width="230" height="46" rx="6" fill="#ecfdf5" stroke="#10b981" stroke-width="1"/>
  <text x="250" y="316" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="800" fill="#047857">Equilibrium: C = 0.25 M</text>
  <text x="250" y="334" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="700" fill="#059669">Zero Net Water Flux (Δm = 0)</text>

  <!-- Right: Physical Calculations & Turgor Cell Model -->
  <rect x="430" y="86" width="314" height="318" rx="10" fill="#f0fdf4" stroke="#86efac" stroke-width="1.5"/>
  <text x="587" y="112" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="16" font-weight="800" fill="#166534">Van 't Hoff Solute Potential</text>

  <!-- Equation box -->
  <rect x="445" y="126" width="284" height="65" rx="8" fill="#ffffff" stroke="#22c55e" stroke-width="1.5"/>
  <text x="587" y="149" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="16" font-weight="800" fill="#14532d">Ψs = - i · C · R · T</text>
  <text x="587" y="175" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="700" fill="#15803d">= - (1.0)(0.25)(0.0831)(293) = -6.09 bar</text>

  <!-- In Distilled Water State -->
  <rect x="445" y="202" width="284" height="186" rx="8" fill="#ffffff" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="587" y="226" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="15" font-weight="800" fill="#1e40af">Transfer to Pure Water (Ψw = 0 bar)</text>

  <text x="460" y="254" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="700" fill="#0f172a">• Initial State: Ψw(tissue) = Ψs = -6.09 bar</text>
  <text x="460" y="280" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="700" fill="#0f172a">• Endosmosis proceeds until equilibrium:</text>
  <text x="460" y="306" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="800" fill="#2563eb">   Ψw = Ψs + Ψp = 0 bar</text>
  <text x="460" y="332" font-family="system-ui, -apple-system, sans-serif" font-size="15" font-weight="800" fill="#16a34a">   ⇒ Turgor Pressure: Ψp = +6.09 bar</text>
  <text x="460" y="364" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="700" fill="#047857">Rigid cellulose wall prevents osmotic lysis.</text>
</svg>'''

# 3. Nephron Starling Forces & GFR Hemodynamics
SVG_NEPHRON = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 780 440" width="100%" height="100%">
  <defs>
    <linearGradient id="bgNep" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fff7ed"/>
      <stop offset="100%" stop-color="#ffedd5"/>
    </linearGradient>
    <filter id="shadowNep" x="-5%" y="-5%" width="110%" height="115%">
      <feDropShadow dx="2" dy="3" stdDeviation="3" flood-opacity="0.12"/>
    </filter>
    <marker id="arrowFilt" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
      <path d="M 0 0 L 8 4 L 0 8 Z" fill="#ea580c"/>
    </marker>
    <marker id="arrowOpp" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
      <path d="M 0 0 L 8 4 L 0 8 Z" fill="#dc2626"/>
    </marker>
  </defs>

  <rect width="780" height="440" fill="url(#bgNep)" rx="16"/>
  <rect x="16" y="16" width="748" height="408" fill="#ffffff" rx="12" stroke="#fdba74" stroke-width="2" filter="url(#shadowNep)"/>

  <!-- Header -->
  <text x="390" y="44" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="20" font-weight="800" fill="#9a3412">Glomerular Filtration Hemodynamics &amp; Starling Forces</text>
  <text x="390" y="68" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="600" fill="#c2410c">Net Filtration Pressure (NFP), Glomerular Filtration Rate (GFR), and 99.0% Reabsorption</text>

  <!-- Left: Glomerular Capillary Diagram & Starling Forces -->
  <rect x="36" y="86" width="410" height="318" rx="10" fill="#fffbeb" stroke="#fcd34d" stroke-width="1.5"/>
  <text x="241" y="112" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="16" font-weight="800" fill="#b45309">Renal Corpuscle Starling Pressures</text>

  <!-- Afferent and Efferent Arteriole lines -->
  <path d="M 50 160 L 140 180" stroke="#ef4444" stroke-width="7" stroke-linecap="round"/>
  <text x="75" y="150" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="800" fill="#b91c1c">Afferent</text>

  <path d="M 280 180 L 370 160" stroke="#ef4444" stroke-width="4.5" stroke-linecap="round"/>
  <text x="305" y="150" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="800" fill="#b91c1c">Efferent</text>

  <!-- Glomerulus Capillary Tuft Circle -->
  <circle cx="210" cy="205" r="55" fill="#fecaca" stroke="#dc2626" stroke-width="3"/>
  <text x="210" y="196" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="800" fill="#991b1b">Capillary Tuft</text>
  <text x="210" y="216" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="15" font-weight="800" fill="#b91c1c">P_GC = 55 mmHg</text>

  <!-- Bowman's Capsule Contour -->
  <path d="M 120 160 C 110 280, 310 280, 300 160" fill="none" stroke="#f59e0b" stroke-width="3.5"/>
  <text x="210" y="272" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="800" fill="#92400e">Bowman's Space (P_BS = 15 mmHg)</text>

  <!-- Starling Vector Arrows -->
  <line x1="210" y1="225" x2="210" y2="252" stroke="#ea580c" stroke-width="3" marker-end="url(#arrowFilt)"/>
  <text x="220" y="242" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="800" fill="#ea580c">NFP ↓</text>

  <!-- Balance Table -->
  <rect x="52" y="286" width="378" height="106" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="64" y="308" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="700" fill="#15803d">✔ Favors Filtration: Hydrostatic P_GC = + 55.0 mmHg</text>
  <text x="64" y="332" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="700" fill="#dc2626">✖ Opposes Filtration: Hydrostatic P_BS = - 15.0 mmHg</text>
  <text x="64" y="356" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="700" fill="#dc2626">✖ Opposes Filtration: Oncotic Π_GC = - 30.0 mmHg</text>
  <text x="64" y="380" font-family="system-ui, -apple-system, sans-serif" font-size="15" font-weight="800" fill="#0f172a">Net Filtration: NFP = 55.0 - (15.0 + 30.0) = + 10.0 mmHg</text>

  <!-- Right: GFR & Tubular Balance -->
  <rect x="460" y="86" width="284" height="318" rx="10" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5"/>
  <text x="602" y="112" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="16" font-weight="800" fill="#0f172a">GFR &amp; Tubular Output</text>

  <!-- Kf and GFR Box -->
  <rect x="475" y="126" width="254" height="85" rx="8" fill="#ffffff" stroke="#38bdf8" stroke-width="1.5"/>
  <text x="602" y="148" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="800" fill="#0369a1">Filtration Coefficient: Kf = 12.5</text>
  <text x="602" y="172" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="15" font-weight="800" fill="#0284c7">GFR = Kf × NFP = 125.0 mL/min</text>
  <text x="602" y="196" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="15" font-weight="800" fill="#0369a1">Daily GFR = 180.0 Liters/day</text>

  <!-- Tubular Reabsorption Box -->
  <rect x="475" y="222" width="254" height="168" rx="8" fill="#eff6ff" stroke="#60a5fa" stroke-width="1.5"/>
  <text x="602" y="246" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="15" font-weight="800" fill="#1e40af">Tubular Processing (99.0%)</text>

  <text x="490" y="276" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="700" fill="#0f172a">• 99.0% Filtered Volume Reabsorbed</text>
  <text x="490" y="302" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="700" fill="#166534">  Reabsorption = 178.2 L/day</text>
  <text x="490" y="332" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="800" fill="#ea580c">• Daily Urine Excreted (1.0%):</text>
  <text x="602" y="362" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="17" font-weight="800" fill="#c2410c">V_urine = 1.80 Liters/day</text>
</svg>'''

# 4. Trophic Pyramid Energy Flow & Pesticide Biomagnification
SVG_TROPHIC = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 780 440" width="100%" height="100%">
  <defs>
    <linearGradient id="bgTro" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ecfeff"/>
      <stop offset="100%" stop-color="#cffafe"/>
    </linearGradient>
    <filter id="shadowTro" x="-5%" y="-5%" width="110%" height="115%">
      <feDropShadow dx="2" dy="3" stdDeviation="3" flood-opacity="0.12"/>
    </filter>
  </defs>

  <rect width="780" height="440" fill="url(#bgTro)" rx="16"/>
  <rect x="16" y="16" width="748" height="408" fill="#ffffff" rx="12" stroke="#67e8f9" stroke-width="2" filter="url(#shadowTro)"/>

  <!-- Header -->
  <text x="390" y="44" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="20" font-weight="800" fill="#0e7490">Ecological Energy Pyramid &amp; DDT Biological Magnification</text>
  <text x="390" y="68" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="600" fill="#0891b2">Lindeman's 10% Trophic Transfer Law vs 10× Lipophilic Pesticide Bioaccumulation</text>

  <!-- Solar Incident Energy Banner -->
  <rect x="36" y="86" width="708" height="38" rx="8" fill="#fef3c7" stroke="#f59e0b" stroke-width="1.5"/>
  <text x="390" y="110" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="15" font-weight="800" fill="#b45309">Incident Solar Flux = 1.0 × 10⁷ kJ/(m²·yr)  |  Phytoplankton GPP = 1.0% = 100,000 kJ  |  NPP (R = 40%) = 60,000 kJ</text>

  <!-- Left: Energy Pyramid (Lindeman 10% Decay) -->
  <text x="210" y="150" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="16" font-weight="800" fill="#0f766e">Energy Flux (kJ/(m²·yr))</text>

  <!-- T4 Top -->
  <polygon points="175,165 245,165 260,210 160,210" fill="#99f6e4" stroke="#0f766e" stroke-width="1.5"/>
  <text x="210" y="192" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="800" fill="#134e4a">T4: 60.0 kJ</text>

  <!-- T3 -->
  <polygon points="160,210 260,210 285,265 135,265" fill="#5eead4" stroke="#0f766e" stroke-width="1.5"/>
  <text x="210" y="242" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="800" fill="#134e4a">T3: 600 kJ</text>

  <!-- T2 -->
  <polygon points="135,265 285,265 315,325 105,325" fill="#2dd4bf" stroke="#0f766e" stroke-width="1.5"/>
  <text x="210" y="300" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="800" fill="#134e4a">T2: 6,000 kJ</text>

  <!-- T1 Base -->
  <polygon points="105,325 315,325 345,395 75,395" fill="#14b8a6" stroke="#0f766e" stroke-width="1.5"/>
  <text x="210" y="365" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="15" font-weight="800" fill="#042f2e">T1 (Producers NPP): 60,000 kJ</text>

  <!-- Right: Biomagnification Inverted Scale (DDT accumulation) -->
  <text x="560" y="150" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="16" font-weight="800" fill="#b91c1c">DDT Biomagnification (ppm)</text>

  <!-- Level 4 Eagle -->
  <rect x="420" y="165" width="280" height="48" rx="6" fill="#fee2e2" stroke="#dc2626" stroke-width="2"/>
  <text x="435" y="195" font-family="system-ui, -apple-system, sans-serif" font-size="15" font-weight="800" fill="#b91c1c">T4 (Eagles / Apex):</text>
  <text x="685" y="195" text-anchor="end" font-family="system-ui, -apple-system, sans-serif" font-size="16" font-weight="800" fill="#dc2626">40.0 ppm (×10)</text>

  <!-- Level 3 Fish -->
  <rect x="420" y="222" width="280" height="48" rx="6" fill="#fef2f2" stroke="#f87171" stroke-width="1.5"/>
  <text x="435" y="252" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="800" fill="#7f1d1d">T3 (Planktivorous Fish):</text>
  <text x="685" y="252" text-anchor="end" font-family="system-ui, -apple-system, sans-serif" font-size="15" font-weight="800" fill="#b91c1c">4.0 ppm (×10)</text>

  <!-- Level 2 Zooplankton -->
  <rect x="420" y="278" width="280" height="48" rx="6" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="435" y="308" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="700" fill="#334155">T2 (Zooplankton):</text>
  <text x="685" y="308" text-anchor="end" font-family="system-ui, -apple-system, sans-serif" font-size="15" font-weight="800" fill="#475569">0.40 ppm (×10)</text>

  <!-- Level 1 Phytoplankton -->
  <rect x="420" y="334" width="280" height="48" rx="6" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.5"/>
  <text x="435" y="364" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="700" fill="#334155">T1 (Phytoplankton):</text>
  <text x="685" y="364" text-anchor="end" font-family="system-ui, -apple-system, sans-serif" font-size="15" font-weight="800" fill="#334155">0.040 ppm (Initial)</text>

  <!-- Bottom Annotation -->
  <text x="390" y="415" text-anchor="middle" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="700" fill="#475569">Lindeman efficiency 10% loss per step vs non-biodegradable lipid accumulation in food web</text>
</svg>'''

svgs = {
    "fig_bio_complementary_genes.svg": SVG_GENES,
    "fig_bio_water_potential.svg": SVG_POTENTIAL,
    "fig_bio_nephron_filtration.svg": SVG_NEPHRON,
    "fig_bio_trophic_pyramid.svg": SVG_TROPHIC
}

for name, content in svgs.items():
    for d in DEST_DIRS:
        target = d / name
        target.write_text(content.strip(), encoding="utf-8")
        print(f"Wrote {target} ({len(content)} bytes)")
