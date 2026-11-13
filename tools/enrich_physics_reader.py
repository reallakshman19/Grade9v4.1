import re

def enrich_physics_reader():
    p = 'nsejs/js/core2-physics-reader.js'
    with open(p, 'r', encoding='utf-8') as f:
        code = f.read()

    ribbon_code = '''
  const TOPIC_RIBBONS = {
    "optics": {
      title: "Ray & Wave Optics",
      links: [
        { label: "▶ Lens Displacement & Transverse Framing (D3 Flagship)", url: "core1/nsejs-optics-displacement-d3-r1/index.html" },
        { label: "▶ Conjugate-Distance Constraints (D3)", url: "core1/recovery/ioqjs-optics-conjugate-d3-r1/index.html" },
        { label: "▶ Lens Image & Plane-Mirror Reflection (D3)", url: "core1/recovery/nsejs-optics-lens-mirror-d3-r1/index.html" },
        { label: "▶ Silvered Prisms Reflection Geometry", url: "core1/recovery/nsejs-optics-prism-d3-r1/index.html" },
        { label: "▶ Convex Mirrors Sign & Limiting Position", url: "core1/recovery/nsejs-optics-r1/index.html" },
        { label: "▶ Lens Magnification & Screw Pitch (D3)", url: "core1/recovery/nsejs-optics-screw-lens-d3-r1/index.html" }
      ]
    },
    "circuits": {
      title: "DC Circuits & Resistor Networks",
      links: [
        { label: "▶ 3D Resistor Cube Symmetry (D3)", url: "core1/recovery/nsejs-circuits-cube-d3-r1/index.html" },
        { label: "▶ Infinite Resistor Ladders (D3)", url: "core1/recovery/nsejs-circuits-ladder-d3-r1/index.html" },
        { label: "▶ Resistor Tetrahedron Symmetry", url: "core1/recovery/nsejs-circuits-r1/index.html" }
      ]
    },
    "electrostatics": {
      title: "Electrostatics & Field Dynamics",
      links: [
        { label: "▶ Transverse Electrostatic Deflection (D3)", url: "core1/recovery/nsejs-electrostatics-deflection-d3-r1/index.html" },
        { label: "▶ Coulomb Force & Quantization Scale", url: "core1/recovery/nsejs-electrostatics-r1/index.html" }
      ]
    },
    "magnetism": {
      title: "Magnetism & Induction",
      links: [
        { label: "▶ Lenz's Law & Induced Flux Change", url: "core1/recovery/nsejs-magnetism-r1/index.html" },
        { label: "▶ Falling Conductive Rod Terminal Damping (D3)", url: "core1/recovery/nsejs-magnetism-terminal-d3-r1/index.html" }
      ]
    },
    "mechanics": {
      title: "Mechanics & Conservation Laws",
      links: [
        { label: "▶ Decoupled Kinematics & Average Speed", url: "core1/recovery/nsejs-mechanics-r1/index.html" },
        { label: "▶ Collision & Friction Interactive Pilot", url: "learn-mechanics.html" }
      ]
    },
    "fluids": {
      title: "Fluids & Sound",
      links: [
        { label: "▶ Droplet Surface Energy & Coalescence (D3)", url: "core1/nsejs-fluids-surface-energy-d3-r1/index.html" },
        { label: "▶ Elevator Buoyancy & Acoustic Doppler", url: "core1/nsejs-fluids-sound-r1/index.html" }
      ]
    }
  };

  function createRibbon(slug) {
    const info = TOPIC_RIBBONS[slug];
    if (!info) return null;
    const box = text("section", "", "nsejs-topic-ribbon");
    box.id = "topic-core1-ribbon";
    const head = text("div", "", "ribbon-head");
    append(head,
      text("strong", "Core 1 Master Learning Journeys for " + info.title),
      text("span", "{Core 1 Available}", "reviewed-ribbon-tag")
    );
    const linksDiv = text("div", "", "ribbon-links");
    info.links.forEach(l => {
      const a = text("a", l.label, "ribbon-btn");
      a.href = l.url;
      linksDiv.appendChild(a);
    });
    append(box, head, linksDiv);
    return box;
  }
'''

    # Insert ribbon_code after TOPICS definition
    code = code.replace('const TOPICS = [', ribbon_code + '\n  const TOPICS = [')

    # In load(): insert ribbon into target before questions
    target_clear = 'status.textContent=topic[2]+": "+questions.length+" candidate records · source and QRT admission HOLD.";'
    ribbon_insert = target_clear + '\n    target.replaceChildren();\n    const ribbon = createRibbon(selectedTopic);\n    if(ribbon) target.append(ribbon);'
    code = code.replace(target_clear, ribbon_insert)

    with open(p, 'w', encoding='utf-8') as f:
        f.write(code)
    print("Added TOPIC_RIBBONS and createRibbon to core2-physics-reader.js")

if __name__ == '__main__':
    enrich_physics_reader()
