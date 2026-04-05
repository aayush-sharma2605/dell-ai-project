<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email Intel | Premium Outreach Intelligence</title>
    <link rel="stylesheet" href="styles.css">
    <!-- Font Awesome for SaaS Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <meta name="description"
        content="Production-ready AI for cold email success prediction and linguistic optimization.">
</head>

<body>

    <!-- Premium Sticky Header -->
    <header>
        <div class="logo-group">
            <h1>Email</h1>
            <p>Intelligence Platform</p>
        </div>
        <div class="status-indicator">
            <div class="dot active" id="api-dot"></div>
            <span id="api-text">API ACTIVE</span>
        </div>
    </header>

    <main class="dashboard-grid">

        <!-- Left Column: Input & Composer -->
        <section class="input-section">
            <div class="card">
                <h2>Draft Outreach</h2>
                <div class="composer-wrapper">
                    <textarea id="email-input"
                        placeholder="Hi [Name], I'm reaching out because I saw your recent work on..."></textarea>
                </div>
                <button id="analyze-btn" class="analyze-btn">
                    <i class="fas fa-microchip"></i>
                    Analyze Success Rate
                </button>
                <div id="error-container" class="hidden"
                    style="margin-top: 1rem; color: var(--danger); font-size: 0.85rem; font-weight: 600; text-align: center;">
                    <i class="fas fa-exclamation-triangle"></i> <span id="error-text"></span>
                </div>
            </div>
        </section>

        <!-- Right Column: Results & Intelligence -->
        <section class="results-section">
            <h2 id="result-header">Intelligence Reports</h2>

            <!-- Result Placeholder / Skeleton -->
            <div id="skeleton-ui" class="hidden">
                <div class="card" style="padding: 3rem;">
                    <div class="skeleton-circle skeleton"></div>
                    <div class="skeleton-bar skeleton" style="width: 60%; margin: 0 auto 3rem;"></div>
                    <div class="skeleton-text skeleton"></div>
                    <div class="skeleton-text skeleton" style="width: 60%;"></div>
                    <div class="skeleton-text skeleton" style="width: 40%;"></div>
                </div>
            </div>

            <!-- Empty State -->
            <div id="empty-state">
                <div class="card" style="text-align: center; padding: 5rem 2rem; color: var(--text-muted);">
                    <i class="fas fa-search-nodes" style="font-size: 3.5rem; margin-bottom: 2rem; opacity: 0.3;"></i>
                    <p style="font-weight: 500; font-size: 1.1rem;">Awaiting input...</p>
                    <p style="font-size: 0.9rem; opacity: 0.7;">Compose an email and click analyze to generate
                        intelligence reports.</p>
                </div>
            </div>

            <!-- Analysis Results (Hidden initially) -->
            <div id="analysis-results" class="hidden">

                <!-- Score Card -->
                <div class="card score-card fade-in">
                    <div class="circular-progress-container">
                        <svg class="progress-ring" width="180" height="180">
                            <circle class="progress-ring__background" cx="90" cy="90" r="70"></circle>
                            <circle id="score-circle" class="progress-ring__circle" cx="90" cy="90" r="70"></circle>
                        </svg>
                        <div class="score-text">
                            <span id="score-val" class="number">0</span>
                            <span class="unit">%</span>
                        </div>
                    </div>
                    <div id="score-label" class="badge-label label-average">AVERAGE EMAIL</div>
                    <p style="margin-top: 1rem; font-size: 0.8rem; color: var(--text-muted); font-weight: 600;">
                        CONFIDENCE: <span id="confidence-val">0.0</span>
                    </p>
                </div>

                <!-- Breakdown Metrics -->
                <div class="card metrics-card fade-in" style="animation-delay: 0.1s; margin-top: 2rem;">
                    <h3
                        style="font-size: 0.9rem; font-weight: 800; color: var(--text-muted); text-transform: uppercase; margin-bottom: 2rem; letter-spacing: 1px;">
                        Metrics Breakdown</h3>
                    <div class="metrics-container" id="metrics-list">
                        <!-- Dynamic metrics injected here -->
                    </div>
                </div>

                <!-- Suggestions -->
                <div class="card suggestions-card fade-in" style="animation-delay: 0.2s; margin-top: 2rem;">
                    <h3
                        style="font-size: 0.9rem; font-weight: 800; color: var(--text-muted); text-transform: uppercase; margin-bottom: 2rem; letter-spacing: 1px;">
                        Strategic Suggestions</h3>
                    <div class="suggestion-list" id="suggestions-list">
                        <!-- Dynamic suggestions injected here -->
                    </div>
                </div>

            </div>
        </section>
    </main>

    <script>
        const API_URL = 'http://localhost:10000';

        const emailInput = document.getElementById('email-input');
        const analyzeBtn = document.getElementById('analyze-btn');
        const emptyState = document.getElementById('empty-state');
        const skeletonUi = document.getElementById('skeleton-ui');
        const resultsContainer = document.getElementById('analysis-results');
        const errorContainer = document.getElementById('error-container');
        const errorText = document.getElementById('error-text');

        // Initial Health Check
        async function checkApiHealth() {
            try {
                const res = await fetch(`${API_URL}/health`);
                if (res.ok) {
                    document.getElementById('api-dot').classList.add('active');
                    document.getElementById('api-text').innerText = 'API ACTIVE';
                    document.getElementById('api-text').style.color = 'var(--success)';
                } else { throw new Error(); }
            } catch (e) {
                document.getElementById('api-dot').classList.remove('active');
                document.getElementById('api-text').innerText = 'API OFFLINE';
                document.getElementById('api-text').style.color = 'var(--danger)';
            }
        }

        async function analyzeEmail() {
            const text = emailInput.value.trim();
            if (!text) return;

            // State: Analyzing
            analyzeBtn.disabled = true;
            analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
            errorContainer.classList.add('hidden');
            emptyState.classList.add('hidden');
            resultsContainer.classList.add('hidden');
            skeletonUi.classList.remove('hidden');

            try {
                const response = await fetch(`${API_URL}/predict`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email: text })
                });

                if (!response.ok) {
                    const errData = await response.json();
                    throw new Error(errData.detail || 'Prediction failed');
                }

                const data = await response.json();
                renderResults(data);

            } catch (err) {
                errorText.innerText = err.message;
                errorContainer.classList.remove('hidden');
                emptyState.classList.remove('hidden');
            } finally {
                analyzeBtn.disabled = false;
                analyzeBtn.innerHTML = '<i class="fas fa-microchip"></i> Analyze Success Rate';
                skeletonUi.classList.add('hidden');
            }
        }

        function renderResults(data) {
            // 1. Update Score & Circle
            document.getElementById('score-val').innerText = data.score;
            document.getElementById('confidence-val').innerText = data.confidence;

            const circle = document.getElementById('score-circle');
            const score = data.score;
            const offset = 440 - (440 * score / 100);
            circle.style.strokeDashoffset = offset;

            // Set Color based on score
            let color = 'var(--danger)';
            let labelClass = 'label-weak';
            if (score >= 70) {
                color = 'var(--success)';
                labelClass = 'label-strong';
            } else if (score >= 40) {
                color = 'var(--warning)';
                labelClass = 'label-average';
            }
            circle.style.stroke = color;

            const label = document.getElementById('score-label');
            label.innerText = data.label;
            label.className = `badge-label ${labelClass}`;

            // 2. Render Metrics
            const metricsList = document.getElementById('metrics-list');
            metricsList.innerHTML = '';

            const icons = {
                personalization: 'fa-user-check',
                clarity: 'fa-wand-magic-sparkles',
                relevance: 'fa-bullseye',
                tone: 'fa-comments',
                length: 'fa-ruler-horizontal'
            };

            Object.entries(data.breakdown).forEach(([key, val]) => {
                const item = document.createElement('div');
                item.className = 'metric-item';
                item.innerHTML = `
                    <div class="metric-label">
                        <span><i class="fas ${icons[key] || 'fa-chart-bar'}"></i> ${key.toUpperCase()}</span>
                        <span>${val}%</span>
                    </div>
                    <div class="bar-bg">
                        <div class="bar-fill" style="width: ${val}%"></div>
                    </div>
                `;
                metricsList.appendChild(item);
            });

            // 3. Render Suggestions
            const suggestionsList = document.getElementById('suggestions-list');
            suggestionsList.innerHTML = '';

            data.suggestions.forEach(sug => {
                const card = document.createElement('div');
                card.className = 'suggestion-card';
                card.innerHTML = `
                    <div class="suggestion-icon"><i class="fas fa-lightbulb"></i></div>
                    <div class="suggestion-text">${sug}</div>
                `;
                suggestionsList.appendChild(card);
            });

            resultsContainer.classList.remove('hidden');
        }

        analyzeBtn.addEventListener('click', analyzeEmail);

        // Initial Health Check
        checkApiHealth();
        setInterval(checkApiHealth, 30000);

        // Optional: LocalStorage persistence
        emailInput.value = localStorage.getItem('email_draft') || '';
        emailInput.addEventListener('input', () => {
            localStorage.setItem('email_draft', emailInput.value);
        });
    </script>
</body>

</html>