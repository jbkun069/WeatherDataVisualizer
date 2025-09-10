// JavaScript to load states, months, analysis, and charts
const stateSelect = document.getElementById('stateSelect');
const monthSelect = document.getElementById('monthSelect');
const stateName = document.getElementById('stateName');
const analysisSection = document.getElementById('analysisSection');
const chartsSection = document.getElementById('chartsSection');
const statsGrid = document.querySelector('.stats-grid');

// Load states
function loadStates() {
    fetch('/states')
        .then(response => response.json())
        .then(states => {
            stateSelect.innerHTML = '<option value="">-- Select a State --</option>';
            states.forEach(state => {
                const option = document.createElement('option');
                option.value = state;
                option.textContent = state;
                stateSelect.appendChild(option);
            });
        })
        .catch(error => console.error('Error loading states:', error));
}

// Create stat card element
function createStatCard(title, value, context = '') {
    const card = document.createElement('div');
    card.className = 'stat-card';
    card.innerHTML = `
        <p class="stat-card-title">${title}</p>
        <p class="stat-card-value">${value}</p>
        ${context ? `<p class="stat-card-context">${context}</p>` : ''}
    `;
    return card;
}

// Load analysis for selected state
function loadAnalysis(state) {
    fetch(`/analysis/${encodeURIComponent(state)}`)
        .then(response => response.json())
        .then(data => {
            stateName.textContent = state;
            statsGrid.innerHTML = ''; // Clear previous stats

            if (data.error) {
                statsGrid.innerHTML = `<p>${data.error}</p>`;
                analysisSection.style.display = 'block';
                return;
            }

            // Populate stats cards
            if (data.temperature_extremes) {
                statsGrid.appendChild(createStatCard('Hottest Week', `${data.temperature_extremes.hottest.temp}°C`, `on ${data.temperature_extremes.hottest.week}`));
                statsGrid.appendChild(createStatCard('Coldest Week', `${data.temperature_extremes.coldest.temp}°C`, `on ${data.temperature_extremes.coldest.week}`));
            }
            if (data.other_extremes) {
                statsGrid.appendChild(createStatCard('Most Humid Week', `${data.other_extremes.most_humid.value}%`, `on ${data.other_extremes.most_humid.week}`));
                statsGrid.appendChild(createStatCard('Windiest Week', `${data.other_extremes.windiest.value} km/h`, `on ${data.other_extremes.windiest.week}`));
            }
            if(data.record_count) {
                statsGrid.appendChild(createStatCard('Total Weeks Recorded', data.record_count));
            }

            analysisSection.style.display = 'block';
        })
        .catch(error => console.error('Error loading analysis:', error));
}

// Load months for selected state
function loadMonths(state) {
    monthSelect.disabled = false;
    fetch(`/months/${encodeURIComponent(state)}`)
        .then(response => response.json())
        .then(months => {
            monthSelect.innerHTML = '';
            months.forEach(month => {
                const option = document.createElement('option');
                option.value = month;
                option.textContent = month;
                monthSelect.appendChild(option);
            });
            monthSelect.dispatchEvent(new Event('change')); // Trigger chart load for the first month
        })
        .catch(error => console.error('Error loading months:', error));
}

// Load charts for selected state and month
function loadCharts(state, month) {
    chartsSection.style.display = 'block';
    document.getElementById('temperatureChart').src = '';
    document.getElementById('humidityChart').src = '';
    document.getElementById('windChart').src = '';

    fetch(`/charts/${encodeURIComponent(state)}/${encodeURIComponent(month)}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('temperatureChart').src = `data:image/png;base64,${data.temp_chart}`;
            document.getElementById('humidityChart').src = `data:image/png;base64,${data.humidity_chart}`;
            document.getElementById('windChart').src = `data:image/png;base64,${data.wind_chart}`;
        })
        .catch(error => console.error('Error loading charts:', error));
}

// Event Listeners
function setupEventListeners() {
    // On state change, load months and analysis
    stateSelect.addEventListener('change', () => {
        const state = stateSelect.value;
        if (state) {
            loadMonths(state);
            loadAnalysis(state);
        } else {
            monthSelect.disabled = true;
            monthSelect.innerHTML = '<option>Select a state first</option>';
            analysisSection.style.display = 'none';
            chartsSection.style.display = 'none';
        }
    });

    // On month change, load charts
    monthSelect.addEventListener('change', () => {
        const state = stateSelect.value;
        const month = monthSelect.value;
        if (state && month) {
            loadCharts(state, month);
        }
    });
}

// Initialize the dashboard when DOM content is loaded
document.addEventListener('DOMContentLoaded', function() {
    loadStates();
    setupEventListeners();
});
