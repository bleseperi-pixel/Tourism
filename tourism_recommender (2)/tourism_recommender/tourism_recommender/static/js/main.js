/* ─── Chip selection ────────────────────────────────────────────────────── */
document.querySelectorAll('.chip-row').forEach(row => {
  const field = row.dataset.field;
  const hidden = document.getElementById('f_' + field.replace('_preference','').replace('travel_with','travel'));

  row.querySelectorAll('.chip').forEach(chip => {
    chip.addEventListener('click', () => {
      row.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      if (hidden) hidden.value = chip.dataset.value;
    });
  });
});

/* Fix hidden field IDs mapping */
const fieldMap = {
  budget: 'f_budget',
  climate_preference: 'f_climate',
  activity_preference: 'f_activity',
  travel_with: 'f_travel',
};
document.querySelectorAll('.chip-row').forEach(row => {
  const field = row.dataset.field;
  const hiddenId = fieldMap[field];
  if (!hiddenId) return;
  const hidden = document.getElementById(hiddenId);
  row.querySelectorAll('.chip').forEach(chip => {
    chip.addEventListener('click', () => {
      if (hidden) hidden.value = chip.dataset.value;
    });
  });
});

/* ─── Slider ────────────────────────────────────────────────────────────── */
const slider = document.getElementById('f_duration');
const bubble = document.getElementById('sliderBubble');

function updateSlider() {
  const val = slider.value;
  bubble.textContent = val + (val == 1 ? ' day' : ' days');
  const pct = ((val - slider.min) / (slider.max - slider.min)) * 100;
  slider.style.background = `linear-gradient(to right, var(--teal) ${pct}%, rgba(255,255,255,.1) ${pct}%)`;
}
slider.addEventListener('input', updateSlider);
updateSlider();

/* ─── Form submit ───────────────────────────────────────────────────────── */
const btnRecommend = document.getElementById('btnRecommend');
const btnText      = document.getElementById('btnText');
const btnLoader    = document.getElementById('btnLoader');
const resultsSection = document.getElementById('resultsSection');
const resultsGrid  = document.getElementById('resultsGrid');
const btnReset     = document.getElementById('btnReset');

btnRecommend.addEventListener('click', async () => {
  const payload = {
    budget:              document.getElementById('f_budget').value,
    duration_days:       slider.value,
    climate_preference:  document.getElementById('f_climate').value,
    activity_preference: document.getElementById('f_activity').value,
    travel_with:         document.getElementById('f_travel').value,
  };

  // Validate
  if (!payload.budget || !payload.climate_preference || !payload.activity_preference || !payload.travel_with) {
    alert('Please select all preferences before continuing.');
    return;
  }

  // Loading state
  btnText.classList.add('hidden');
  btnLoader.classList.remove('hidden');
  btnRecommend.disabled = true;

  try {
    const res  = await fetch('/recommend', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(payload),
    });
    const data = await res.json();

    if (data.error) { alert('Error: ' + data.error); return; }

    renderResults(data.recommendations);
    resultsSection.classList.remove('hidden');
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
  } catch (err) {
    alert('Could not connect to server. Make sure Flask is running.');
    console.error(err);
  } finally {
    btnText.classList.remove('hidden');
    btnLoader.classList.add('hidden');
    btnRecommend.disabled = false;
  }
});

/* ─── Render results ────────────────────────────────────────────────────── */
const rankLabels = ['🥇 Best Match', '🥈 2nd Pick', '🥉 3rd Pick'];
const rankClasses = ['rank-1', 'rank-2', 'rank-3'];

function renderResults(recs) {
  resultsGrid.innerHTML = '';

  recs.forEach((rec, i) => {
    const card = document.createElement('div');
    card.className = 'result-card';
    card.innerHTML = `
      <div class="card-rank ${rankClasses[i]}">${rankLabels[i]}</div>
      <span class="card-emoji">${rec.emoji}</span>
      <h3 class="card-name">${rec.name}</h3>
      <p class="card-desc">${rec.desc}</p>

      <div class="confidence-bar">
        <div class="conf-label">
          <span>ML Confidence</span>
          <span>${rec.confidence}%</span>
        </div>
        <div class="conf-track">
          <div class="conf-fill" style="width:0%" data-width="${rec.confidence}%"></div>
        </div>
      </div>

      <div class="card-meta">
        ${rec.days ? `<span class="meta-pill">📅 ${rec.days} days</span>` : ''}
        ${rec.best ? `<span class="meta-pill">🌟 Best: ${rec.best}</span>` : ''}
      </div>

      <ul class="card-highlights">
        ${rec.highlights.map(h => `<li>${h}</li>`).join('')}
      </ul>
    `;
    resultsGrid.appendChild(card);

    // Animate confidence bar after render
    setTimeout(() => {
      const fill = card.querySelector('.conf-fill');
      fill.style.width = fill.dataset.width;
    }, 100 + i * 120);
  });
}

/* ─── Reset ─────────────────────────────────────────────────────────────── */
btnReset.addEventListener('click', () => {
  resultsSection.classList.add('hidden');
  document.getElementById('planner').scrollIntoView({ behavior: 'smooth' });
});
