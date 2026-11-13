css_to_add = """
/* --- Unified Disciplinary Topic Ribbon & Card Styles for 12.7" Tablet --- */
.topic-pill-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  min-height: 48px;
  padding: 10px 18px;
  border-radius: 9999px;
  font-size: 15px;
  font-weight: 700;
  text-decoration: none;
  transition: all .2s ease;
  border: 1.5px solid #b2c9d6;
  background: #ffffff;
  color: #134563;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06);
  touch-action: manipulation;
}
.topic-pill-btn:hover {
  background: #edf6fa;
  border-color: #7fa6bc;
  color: #0b3149;
  transform: translateY(-1px);
}
.topic-pill-btn.active, .topic-pill-btn[aria-current="page"] {
  background: #0284c7;
  color: #ffffff;
  border-color: #0284c7;
  font-weight: 700;
  box-shadow: 0 4px 12px rgba(2,132,199,0.3);
}
.topic-pill-btn .pill-icon { font-size: 18px; line-height: 1; }
.topic-pill-btn .pill-name { letter-spacing: -0.01em; }
.topic-pill-btn .pill-count {
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 12px;
  background: #e0eff6;
  color: #0e5977;
  font-weight: 750;
}
.topic-pill-btn.active .pill-count {
  background: rgba(255,255,255,0.28);
  color: #ffffff;
}
.card {
  background: white;
  border: 1.5px solid #d0dfe9;
  border-radius: 14px;
  padding: 22px 24px;
  margin: 18px 0;
  box-shadow: 0 4px 12px rgba(16,42,67,0.04);
}
.card h2 { font-size: 1.25rem; margin: 0 0 8px; color: #0f172a; font-weight: 800; }
.meta { color: #475569; font-size: 0.92rem; line-height: 1.5; margin: 4px 0 10px; }
.stem { white-space: pre-wrap; margin: 14px 0; font-size: 1.05rem; line-height: 1.6; color: #1e293b; }
.options { margin: 14px 0; display: grid; gap: 9px; }
.options label {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 12px 14px;
  border: 1.5px solid #ccdce6;
  border-radius: 9px;
  min-height: 48px;
  cursor: pointer;
  background: #fafcfe;
  transition: border-color 0.15s, background 0.15s;
}
.options label:hover {
  border-color: #0284c7;
  background: #f0f9ff;
}
.options input { margin-top: 4px; width: 18px; height: 18px; }
.actions { display: flex; flex-wrap: wrap; align-items: center; gap: 10px; margin-top: 14px; }
.actions button {
  min-height: 48px;
  padding: 10px 18px;
  border-radius: 8px;
  border: 1.5px solid #50768c;
  background: white;
  color: #113a55;
  font-weight: 750;
  cursor: pointer;
  touch-action: manipulation;
}
.answer {
  padding: 16px 20px;
  border: 1.5px solid #a6c5cb;
  border-radius: 10px;
  background: #f0faf8;
  white-space: pre-wrap;
  margin-top: 14px;
  line-height: 1.65;
  color: #0f4a47;
}
.figure-warning {
  background: #fff4e5;
  border: 1.5px solid #bc8e54;
  border-radius: 8px;
  padding: 10px 14px;
  color: #7c2d12;
  font-size: 0.92rem;
  margin: 10px 0;
}
.nsejs-topic-ribbon {
  background: #f0fdf4;
  border: 2px solid #86efac;
  border-radius: 14px;
  padding: 18px 22px;
  margin: 18px 0 26px;
  box-shadow: 0 2px 8px rgba(22,101,52,0.05);
}
.ribbon-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 8px;
  font-size: 16px;
  color: #14532d;
  margin-bottom: 14px;
}
.reviewed-ribbon-tag {
  background: #dcfce7;
  color: #15803d;
  border: 1px solid #86efac;
  font-size: 11px;
  font-weight: 800;
  padding: 3px 10px;
  border-radius: 999px;
  letter-spacing: 0.04em;
}
.ribbon-links { display: flex; flex-wrap: wrap; gap: 10px; }
.ribbon-btn {
  display: inline-flex;
  align-items: center;
  min-height: 48px;
  padding: 10px 18px;
  border-radius: 10px;
  background: #16a34a;
  color: #ffffff;
  font-weight: 750;
  font-size: 14px;
  text-decoration: none;
  transition: background .15s, transform .1s;
  box-shadow: 0 2px 6px rgba(22,163,74,0.2);
  touch-action: manipulation;
}
.ribbon-btn:hover { background: #15803d; transform: translateY(-1px); }
"""

with open('css/tablet-12-7.css', 'a', encoding='utf-8') as f:
    f.write(css_to_add)
print('Appended shared topic ribbon styles to css/tablet-12-7.css')
