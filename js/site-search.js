/**
 * Grade9 v4.0 Unified & Customizable Site Search Runtime
 *
 * Capabilities:
 * - Multi-depth relative URL resolution (works from root, /nsejs/, /physics/, /nsejs/physics/core1/... etc.)
 * - Scope Customization: All, NSEJS Only, Physics, Chemistry, Biology, Mathematics
 * - Dynamic Scope Filter Chips inside the search dialog
 * - Query prefix syntax: 'nsejs: optics', 'phy:', 'chem:', 'bio:', 'd3:', 'd2:'
 * - Synonym expansion from keyword-synonyms thesaurus
 * - Multi-token boolean matching + stemming + intelligent relevance ranking
 * - Live dynamic facet counts on category tabs
 * - Deep-linking directly to questions in Question Banks with query pre-fill
 * - Global Ctrl/Cmd + K shortcut and keyboard navigation
 */

(function () {
  'use strict';

  // Prevent multiple initializations
  if (window.Grade9Search && window.Grade9Search.initialized) {
    return;
  }

  const script = document.currentScript;

  // Compute relative root to site root based on script src or location
  function computeSiteRoot() {
    if (script && script.dataset && script.dataset.siteRoot) {
      return script.dataset.siteRoot;
    }
    if (script && script.src) {
      try {
        const u = new URL(script.src, window.location.href);
        const idx = u.pathname.lastIndexOf('/js/');
        if (idx !== -1) {
          const rootPath = u.pathname.slice(0, idx + 1);
          // Return relative path from current page to that root
          const curPath = window.location.pathname;
          const curParts = curPath.split('/').filter(Boolean);
          const rootParts = rootPath.split('/').filter(Boolean);
          let depth = 0;
          if (curParts.length > rootParts.length) {
            depth = curParts.length - rootParts.length;
          }
          if (depth > 0) {
            return '../'.repeat(depth);
          }
          return './';
        }
      } catch (e) {}
    }

    // Heuristic based on current pathname
    const p = window.location.pathname.toLowerCase();
    if (p.includes('/core1/recovery/') || p.includes('/physics/core1/recovery/')) {
      return '../../../../';
    }
    if (p.includes('/physics/core1/') || p.includes('/chemistry/core1/') || p.includes('/biology/core1/')) {
      return '../../../';
    }
    if (p.includes('/nsejs/physics/') || p.includes('/nsejs/chemistry/') || p.includes('/nsejs/biology/') || p.includes('/preview/batches/')) {
      return '../../';
    }
    if (p.includes('/nsejs/') || p.includes('/physics/') || p.includes('/chemistry/') || p.includes('/mathematics/') || p.includes('/preview/') || p.includes('/architecture/')) {
      return '../';
    }
    return './';
  }

  const siteRoot = computeSiteRoot();

  // Determine page context default scope
  const isNSEJSPage = window.location.pathname.toLowerCase().includes('/nsejs/');
  let currentScope = isNSEJSPage ? 'nsejs' : 'all';
  let activeCategory = 'all';

  // Data cache
  let searchData = null;
  let synonymsData = [];
  let fetchPromise = null;

  // Search candidate URLs
  function getCandidateDataUrls(fileName) {
    return [
      siteRoot + 'data/' + fileName,
      siteRoot + 'nsejs/data/' + fileName,
      'data/' + fileName,
      '../data/' + fileName,
      '../../data/' + fileName,
      '../../../data/' + fileName,
      '/data/' + fileName,
      '/Grade9v4.0/data/' + fileName
    ];
  }

  async function loadData() {
    if (fetchPromise) return fetchPromise;

    fetchPromise = (async () => {
      // 1. Fetch search index
      const indexCandidates = getCandidateDataUrls('learner-search-index.v1.json');
      let loadedIndex = null;
      for (const u of indexCandidates) {
        try {
          const res = await fetch(u);
          if (res.ok) {
            const data = await res.json();
            if (Array.isArray(data) && data.length > 0) {
              loadedIndex = data;
              break;
            }
          }
        } catch (e) {}
      }

      // 2. Fetch synonyms (optional enhancement)
      const synCandidates = getCandidateDataUrls('keyword-synonyms.v1.json');
      for (const u of synCandidates) {
        try {
          const res = await fetch(u);
          if (res.ok) {
            const data = await res.json();
            if (data && Array.isArray(data.synonyms)) {
              synonymsData = data.synonyms;
              break;
            }
          }
        } catch (e) {}
      }

      if (!loadedIndex) {
        console.warn('[Grade9Search] Could not fetch search index from candidate URLs.');
        return [];
      }

      searchData = loadedIndex;
      return searchData;
    })();

    return fetchPromise;
  }

  // Pre-load data in background
  if ('requestIdleCallback' in window) {
    window.requestIdleCallback(() => loadData());
  } else {
    setTimeout(loadData, 100);
  }

  // Build UI Elements
  const dialog = document.createElement('dialog');
  dialog.className = 'g9-search-dialog';
  dialog.setAttribute('aria-labelledby', 'g9SearchTitle');
  dialog.setAttribute('role', 'dialog');
  dialog.setAttribute('aria-modal', 'true');

  const wrap = document.createElement('div');
  wrap.className = 'g9-search-wrap';

  // Top Title Bar
  const topBar = document.createElement('div');
  topBar.className = 'g9-search-top';

  const titleWrap = document.createElement('div');
  titleWrap.className = 'g9-search-title-wrap';

  const titleIcon = document.createElement('span');
  titleIcon.className = 'g9-search-title-icon';
  titleIcon.textContent = '⚡';

  const title = document.createElement('strong');
  title.id = 'g9SearchTitle';
  title.textContent = isNSEJSPage ? 'Search NSEJS Junior Science' : 'Search Grade9 v4.0';

  const scopeIndicator = document.createElement('span');
  scopeIndicator.className = 'g9-search-scope-indicator' + (currentScope === 'nsejs' ? ' scope-nsejs' : '');
  scopeIndicator.textContent = currentScope === 'nsejs' ? '⭐ NSEJS' : 'ALL PORTALS';

  titleWrap.append(titleIcon, title, scopeIndicator);

  const closeBtn = document.createElement('button');
  closeBtn.type = 'button';
  closeBtn.className = 'g9-search-close-btn';
  closeBtn.setAttribute('aria-label', 'Close search dialog');
  closeBtn.textContent = '×';
  closeBtn.addEventListener('click', () => dialog.close());

  topBar.append(titleWrap, closeBtn);

  // Search Input Box
  const inputBox = document.createElement('div');
  inputBox.className = 'g9-search-input-box';

  const inputIcon = document.createElement('span');
  inputIcon.className = 'g9-search-input-icon';
  inputIcon.textContent = '🔍';

  const input = document.createElement('input');
  input.type = 'search';
  input.placeholder = 'Search pages, concepts, questions, or topics…';
  input.autocomplete = 'off';
  input.spellcheck = false;
  input.setAttribute('aria-label', 'Search query');

  inputBox.append(inputIcon, input);

  // Scope Filter Bar (Customizability)
  const scopeBar = document.createElement('div');
  scopeBar.className = 'g9-search-scope-bar';

  const scopeLabel = document.createElement('span');
  scopeLabel.className = 'g9-search-scope-label';
  scopeLabel.textContent = 'Scope:';
  scopeBar.appendChild(scopeLabel);

  const scopes = [
    { id: 'all', label: '🌐 All Portals' },
    { id: 'nsejs', label: '⭐ NSEJS Only', isNsejs: true },
    { id: 'physics', label: '⚛️ Physics' },
    { id: 'chemistry', label: '🧪 Chemistry' },
    { id: 'biology', label: '🧬 Biology' }
  ];

  const scopeButtons = {};

  scopes.forEach(sc => {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'g9-search-scope-btn' + (sc.isNsejs ? ' btn-nsejs' : '') + (currentScope === sc.id ? ' active' : '');
    btn.textContent = sc.label;
    btn.addEventListener('click', () => {
      setScope(sc.id);
      renderSearch();
    });
    scopeBar.appendChild(btn);
    scopeButtons[sc.id] = btn;
  });

  // Category Tabs Container
  const tabsContainer = document.createElement('div');
  tabsContainer.className = 'g9-search-tabs';
  tabsContainer.setAttribute('role', 'tablist');
  tabsContainer.hidden = true;

  // Search Hint
  const hint = document.createElement('div');
  hint.className = 'g9-search-hint';

  const hintLeft = document.createElement('span');
  hintLeft.innerHTML = 'Tip: press <kbd class="g9-search-hint-kbd">Ctrl</kbd> + <kbd class="g9-search-hint-kbd">K</kbd> anywhere. Type <kbd class="g9-search-hint-kbd">nsejs:</kbd> to filter.';

  const hintRight = document.createElement('span');
  hintRight.innerHTML = '<kbd class="g9-search-hint-kbd">Esc</kbd> to close';

  hint.append(hintLeft, hintRight);

  // Results Container
  const results = document.createElement('div');
  results.className = 'g9-search-results';
  results.setAttribute('aria-live', 'polite');

  wrap.append(topBar, inputBox, scopeBar, tabsContainer, hint, results);
  dialog.appendChild(wrap);

  // Mount dialog on DOM
  function mountDialog() {
    if (!document.body.contains(dialog)) {
      document.body.appendChild(dialog);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mountDialog);
  } else {
    mountDialog();
  }

  // Helper: Normalize string
  function normalize(v) {
    return String(v || '').toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();
  }

  // Set Scope with UI update
  function setScope(scopeId) {
    currentScope = scopeId;
    Object.keys(scopeButtons).forEach(id => {
      scopeButtons[id].classList.toggle('active', id === scopeId);
    });

    if (scopeIndicator) {
      scopeIndicator.className = 'g9-search-scope-indicator' + (currentScope === 'nsejs' ? ' scope-nsejs' : '');
      scopeIndicator.textContent = currentScope === 'nsejs' ? '⭐ NSEJS' : (currentScope === 'all' ? 'ALL PORTALS' : currentScope.toUpperCase());
    }

    if (title) {
      title.textContent = currentScope === 'nsejs' ? 'Search NSEJS Junior Science' : 'Search Grade9 v4.0';
    }
  }

  // Find synonyms for query tokens
  function expandTokensWithSynonyms(tokens) {
    const expanded = new Set(tokens);
    if (!synonymsData || synonymsData.length === 0) return Array.from(expanded);

    tokens.forEach(tok => {
      if (tok.length < 3) return;
      synonymsData.forEach(syn => {
        const slug = syn.slug || '';
        const canon = syn.canonical_term || '';
        const aliases = syn.aliases || [];
        if (slug.includes(tok) || canon.includes(tok) || aliases.some(a => a.toLowerCase().includes(tok))) {
          aliases.slice(0, 5).forEach(a => {
            a.toLowerCase().split(/\s+/).forEach(t => {
              if (t.length >= 3) expanded.add(t);
            });
          });
        }
      });
    });

    return Array.from(expanded);
  }

  // Scoring function
  function scoreItem(item, tokens, rawTerm) {
    let score = 1000;
    const titleNorm = normalize(item.title);
    const idNorm = normalize(item.original_id || item.id);
    const textNorm = normalize(item.search_text);

    // Exact ID Match (e.g. NSEJS-2023-P-Q01)
    if (idNorm === rawTerm || item.original_id === rawTerm || item.id === rawTerm || idNorm === 'q ' + rawTerm) {
      score += 30000;
    } else if (idNorm.includes(rawTerm)) {
      score += 8000;
    }

    // Active Scope Match
    if (currentScope === 'nsejs' && item.is_nsejs) {
      score += 5000;
    } else if (currentScope !== 'all' && (item.subject || '').toLowerCase() === currentScope) {
      score += 5000;
    }

    // Title Matches
    if (titleNorm === rawTerm) {
      score += 15000;
    } else if (titleNorm.startsWith(rawTerm)) {
      score += 7000;
    } else if (tokens.every(tok => titleNorm.includes(tok))) {
      score += 3500;
    } else if (tokens.some(tok => titleNorm.includes(tok))) {
      score += 1200;
    }

    // Topic & Cognitive Demand Match
    const topicNorm = normalize(item.topic);
    if (topicNorm.includes(rawTerm)) score += 2500;

    const bandNorm = normalize(item.band);
    if (rawTerm === bandNorm || tokens.includes(bandNorm)) score += 2000;

    // Full text vector match
    if (tokens.every(tok => textNorm.includes(tok))) score += 800;
    if (textNorm.includes(rawTerm)) score += 400;

    return score;
  }

  // Filter item by current active scope
  function itemMatchesScope(item, scope) {
    if (scope === 'all') return true;
    if (scope === 'nsejs') return Boolean(item.is_nsejs);
    const subj = (item.subject || '').toLowerCase();
    return subj === scope;
  }

  // Render Result Card Element
  function createResultCard(item, rawTerm) {
    const a = document.createElement('a');
    a.className = 'g9-search-result';

    let resolvedUrl = item.url || '#';
    if (!resolvedUrl.startsWith('http') && !resolvedUrl.startsWith('/')) {
      resolvedUrl = siteRoot + resolvedUrl;
    }
    a.href = resolvedUrl;

    // Title
    const main = document.createElement('span');
    main.className = 'g9-search-result-main';
    main.textContent = item.title || item.original_id || item.id;

    // Breadcrumb
    const breadcrumb = document.createElement('span');
    breadcrumb.className = 'g9-search-breadcrumb';
    breadcrumb.textContent = item.breadcrumb || `${item.subject || 'Portal'} · ${item.category}`;

    // Snippet
    const sub = document.createElement('span');
    sub.className = 'g9-search-result-sub';
    if (item.stem && item.stem !== item.title) {
      sub.textContent = item.stem.slice(0, 140) + '…';
    } else if (item.search_text) {
      sub.textContent = item.search_text.slice(0, 120) + '…';
    } else {
      sub.textContent = item.original_id || item.id;
    }

    // Badge Pill
    const badge = document.createElement('span');
    badge.className = 'g9-search-result-kind';
    const rawBadge = item.badge || item.type || 'ITEM';
    badge.textContent = rawBadge;

    const bNorm = rawBadge.toLowerCase();
    if (bNorm.includes('core 1a')) badge.classList.add('g9-badge-core1a');
    else if (bNorm.includes('core 1b')) badge.classList.add('g9-badge-core1b');
    else if (bNorm.includes('core 2')) badge.classList.add('g9-badge-core2');
    else if (bNorm.includes('nsejs')) badge.classList.add('g9-badge-nsejs');
    else if (bNorm.includes('topic')) badge.classList.add('g9-badge-topic');
    else if (bNorm.includes('reviewed')) badge.classList.add('g9-badge-reviewed');

    a.append(main, breadcrumb, sub, badge);

    a.addEventListener('click', () => {
      dialog.close();
    });

    return a;
  }

  // Render Question Bank Bridge
  function createQbBridge(count, queryTerm) {
    const bridge = document.createElement('a');
    bridge.className = 'g9-search-qb-bridge';

    let qbUrl = siteRoot + 'nsejs/physics/question-bank.html';
    if (currentScope === 'chemistry') {
      qbUrl = siteRoot + 'nsejs/chemistry/question-bank.html';
    } else if (currentScope === 'biology') {
      qbUrl = siteRoot + 'nsejs/biology/question-bank.html';
    }

    bridge.href = qbUrl + '?q=' + encodeURIComponent(queryTerm);

    const left = document.createElement('span');
    left.textContent = `🎯 Open Question Bank with all ${count} matching questions`;

    const arrow = document.createElement('span');
    arrow.textContent = '›';

    bridge.append(left, arrow);
    bridge.addEventListener('click', () => dialog.close());

    return bridge;
  }

  // Main Render Logic
  async function renderSearch() {
    let rawInput = input.value.trim();
    results.replaceChildren();

    // Check for inline scope prefix, e.g. "nsejs: optics" or "chem: atom"
    let effectiveScope = currentScope;
    const prefixMatch = rawInput.match(/^(nsejs|physics|phy|chemistry|chem|biology|bio|math|mathematics):\s*(.*)$/i);
    if (prefixMatch) {
      const scopeKey = prefixMatch[1].toLowerCase();
      if (scopeKey === 'nsejs') effectiveScope = 'nsejs';
      else if (scopeKey === 'phy' || scopeKey === 'physics') effectiveScope = 'physics';
      else if (scopeKey === 'chem' || scopeKey === 'chemistry') effectiveScope = 'chemistry';
      else if (scopeKey === 'bio' || scopeKey === 'biology') effectiveScope = 'biology';
      else if (scopeKey === 'math' || scopeKey === 'mathematics') effectiveScope = 'mathematics';
      rawInput = prefixMatch[2].trim();
      setScope(effectiveScope);
    }

    const term = normalize(rawInput);

    if (!term) {
      tabsContainer.hidden = true;
      const empty = document.createElement('div');
      empty.className = 'g9-search-empty';

      const icon = document.createElement('div');
      icon.className = 'g9-search-empty-icon';
      icon.textContent = currentScope === 'nsejs' ? '🏆' : '🔍';

      const text = document.createElement('div');
      text.textContent = currentScope === 'nsejs'
        ? 'Search 288+ authentic NSEJS questions, 27 Core 1 lessons, and Junior Science topics.'
        : 'Type to search across Physics, Chemistry, Biology, Mathematics, and NSEJS Junior Science.';

      empty.append(icon, text);
      results.appendChild(empty);
      return;
    }

    const data = await loadData();
    if (!data || data.length === 0) {
      tabsContainer.hidden = true;
      const p = document.createElement('div');
      p.className = 'g9-search-empty';
      p.textContent = 'Loading search index... Please wait a moment.';
      results.appendChild(p);
      return;
    }

    // Token extraction
    const rawTokens = term.split(/\s+/).filter(Boolean);
    const searchTokens = expandTokensWithSynonyms(rawTokens);

    // Filter by Scope & Tokens
    const matched = data.filter(item => {
      if (!itemMatchesScope(item, effectiveScope)) {
        return false;
      }
      const hay = normalize([
        item.title,
        item.original_id,
        item.id,
        item.search_text,
        item.topic,
        item.band,
        item.op,
        item.subject
      ].join(' '));

      // Each query token must match directly or via stem/synonym
      return rawTokens.every(tok => {
        if (hay.includes(tok)) return true;
        if (tok.length >= 4) {
          const stem = tok.slice(0, 4);
          if (hay.includes(stem)) return true;
        }
        // Check expanded synonym tokens
        return searchTokens.some(st => st.length >= 3 && hay.includes(st) && (st.includes(tok) || tok.includes(st)));
      });
    });

    if (matched.length === 0) {
      tabsContainer.hidden = true;
      const empty = document.createElement('div');
      empty.className = 'g9-search-empty';

      const icon = document.createElement('div');
      icon.className = 'g9-search-empty-icon';
      icon.textContent = '🔍';

      const msg = document.createElement('div');
      msg.textContent = `No matching results for "${input.value.trim()}" in ${effectiveScope.toUpperCase()} scope.`;

      if (effectiveScope !== 'all') {
        const resetBtn = document.createElement('button');
        resetBtn.type = 'button';
        resetBtn.className = 'g9-search-scope-reset-btn';
        resetBtn.textContent = 'Search across All Portals instead';
        resetBtn.addEventListener('click', () => {
          setScope('all');
          renderSearch();
        });
        empty.append(icon, msg, resetBtn);
      } else {
        empty.append(icon, msg);
      }

      results.appendChild(empty);
      return;
    }

    // Sort by smart relevance score
    matched.sort((a, b) => scoreItem(b, rawTokens, term) - scoreItem(a, rawTokens, term));

    // Dynamic facet counts
    const countAll = matched.length;
    const countQuestions = matched.filter(m => m.category === 'question').length;
    const countTablets = matched.filter(m => m.category === 'tablet').length;
    const countCurriculum = matched.filter(m => m.category === 'curriculum').length;
    const countPages = matched.filter(m => m.category === 'page').length;

    // Reset tab if current tab has 0
    if (activeCategory === 'question' && countQuestions === 0) activeCategory = 'all';
    if (activeCategory === 'tablet' && countTablets === 0) activeCategory = 'all';
    if (activeCategory === 'curriculum' && countCurriculum === 0) activeCategory = 'all';
    if (activeCategory === 'page' && countPages === 0) activeCategory = 'all';

    // Render Facet Tabs
    tabsContainer.hidden = false;
    tabsContainer.replaceChildren();

    const tabDefs = [
      { id: 'all', label: 'All', count: countAll },
      { id: 'question', label: 'Questions', count: countQuestions },
      { id: 'tablet', label: 'Tablets & Lessons', count: countTablets },
      { id: 'curriculum', label: 'Topics', count: countCurriculum },
      { id: 'page', label: 'Portals', count: countPages }
    ].filter(t => t.count > 0 || t.id === 'all');

    tabDefs.forEach(def => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'g9-search-tab' + (activeCategory === def.id ? ' active' : '');
      btn.setAttribute('role', 'tab');
      btn.setAttribute('aria-selected', String(activeCategory === def.id));

      const lbl = document.createElement('span');
      lbl.textContent = def.label;

      const cnt = document.createElement('span');
      cnt.className = 'g9-search-tab-count';
      cnt.textContent = String(def.count);

      btn.append(lbl, cnt);
      btn.addEventListener('click', () => {
        activeCategory = def.id;
        renderSearch();
      });

      tabsContainer.appendChild(btn);
    });

    // Render Items
    if (activeCategory === 'all') {
      const tablets = matched.filter(m => m.category === 'tablet');
      const curriculum = matched.filter(m => m.category === 'curriculum');
      const questions = matched.filter(m => m.category === 'question');
      const pages = matched.filter(m => m.category === 'page');

      // 1. Tablets / Master Lessons
      if (tablets.length > 0) {
        const sec = document.createElement('div');
        sec.className = 'g9-search-section-header';
        sec.textContent = `📑 Core 1A & 2 Interactive Lessons (${tablets.length})`;
        results.appendChild(sec);
        tablets.slice(0, 5).forEach(item => results.appendChild(createResultCard(item, term)));
      }

      // 2. Curriculum Topics
      if (curriculum.length > 0) {
        const sec = document.createElement('div');
        sec.className = 'g9-search-section-header';
        sec.textContent = `📚 Curriculum Topics (${curriculum.length})`;
        results.appendChild(sec);
        curriculum.slice(0, 4).forEach(item => results.appendChild(createResultCard(item, term)));
      }

      // 3. Question Bank Items
      if (questions.length > 0) {
        const sec = document.createElement('div');
        sec.className = 'g9-search-section-header';
        sec.textContent = `🎯 Questions in Question Bank (${questions.length})`;
        results.appendChild(sec);
        results.appendChild(createQbBridge(questions.length, input.value.trim()));
        questions.slice(0, 8).forEach(item => results.appendChild(createResultCard(item, term)));
      }

      // 4. Portal Pages
      if (pages.length > 0) {
        const sec = document.createElement('div');
        sec.className = 'g9-search-section-header';
        sec.textContent = `🧭 Portal & Verification Hubs (${pages.length})`;
        results.appendChild(sec);
        pages.slice(0, 3).forEach(item => results.appendChild(createResultCard(item, term)));
      }
    } else {
      // Specific Category Tab Active
      const filtered = matched.filter(m => m.category === activeCategory);
      if (activeCategory === 'question' && filtered.length > 0) {
        results.appendChild(createQbBridge(filtered.length, input.value.trim()));
      }
      filtered.slice(0, 30).forEach(item => results.appendChild(createResultCard(item, term)));
    }
  }

  // Debounced input handler
  let searchTimer = null;
  input.addEventListener('input', () => {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(renderSearch, 50);
  });

  // Open Search Dialog
  function openSearch(options) {
    mountDialog();
    if (options && options.scope) {
      setScope(options.scope);
    }
    if (options && options.query) {
      input.value = options.query;
    }
    if (options && options.category) {
      activeCategory = options.category;
    }

    if (typeof dialog.showModal === 'function') {
      if (!dialog.open) {
        dialog.showModal();
      }
    } else {
      dialog.setAttribute('open', '');
    }

    input.focus();
    input.select();
    renderSearch();
  }

  // Keyboard navigation & Shortcuts
  document.addEventListener('keydown', e => {
    // Ctrl + K or Cmd + K
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      openSearch();
      return;
    }

    if (e.key === 'Escape') {
      if (dialog.open) {
        dialog.close();
      }
    }
  });

  // Universal button binder
  function bindTriggers() {
    mountDialog();
    document.querySelectorAll('[data-g9-action="search"], .g9-search-trigger, .g9-search-btn').forEach(btn => {
      btn.onclick = e => {
        e.preventDefault();
        const customScope = btn.dataset.searchScope || (isNSEJSPage ? 'nsejs' : 'all');
        const customQuery = btn.dataset.searchQuery || '';
        openSearch({ scope: customScope, query: customQuery });
      };
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bindTriggers);
  } else {
    bindTriggers();
  }

  // Public API
  window.Grade9Search = {
    initialized: true,
    open: openSearch,
    close: () => dialog.close(),
    setScope: setScope,
    loadData: loadData,
    query: (term, options) => {
      openSearch(Object.assign({ query: term }, options));
    }
  };

  // Backwards compatibility with Grade9Header
  window.Grade9Header = window.Grade9Header || {};
  window.Grade9Header.openSearch = openSearch;
  window.Grade9Header.closeSearch = () => dialog.close();
})();
