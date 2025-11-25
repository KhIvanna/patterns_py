const API_BASE = '/api';

document.addEventListener('DOMContentLoaded', () => {
    loadAllData();
    setupEventListeners();
});

function setupEventListeners() {
    document.getElementById('refresh-btn').addEventListener('click', refreshPlan);
    
    document.getElementById('edit-preferences-btn').addEventListener('click', openPreferencesModal);
    
    document.querySelector('.close').addEventListener('click', closePreferencesModal);
    
    document.getElementById('preferences-form').addEventListener('submit', savePreferences);
    
    window.addEventListener('click', (e) => {
        const modal = document.getElementById('preferences-modal');
        if (e.target === modal) {
            closePreferencesModal();
        }
    });
}

async function loadAllData() {
    await Promise.all([
        loadWeather(),
        loadPlan(),
        loadPreferences(),
        loadHistory()
    ]);
}

async function loadWeather() {
    const weatherContent = document.getElementById('weather-content');
    
    try {
        const response = await fetch(`${API_BASE}/weather/current`);
        const data = await response.json();
        
        if (data.success && data.weather) {
            displayWeather(data.weather);
        } else {
            weatherContent.innerHTML = '<p class="error-message">No weather data available. Click Refresh Plan to fetch weather.</p>';
        }
    } catch (error) {
        console.error('Error loading weather:', error);
        weatherContent.innerHTML = '<p class="error-message">Failed to load weather data.</p>';
    }
}

function displayWeather(weather) {
    const weatherContent = document.getElementById('weather-content');
    
    const weatherIcons = {
        'Sunny': 'Sunny',
        'Rainy': 'Rainy',
        'Cloudy': 'Cloudy',
        'Snowy': 'Snowy'
    };
    
    const icon = weatherIcons[weather.condition] || 'Cloudy';
    
    weatherContent.innerHTML = `
        <div class="weather-info">
            <div class="weather-icon">${icon}</div>
            <div class="weather-details">
                <h3>${weather.city}</h3>
                <p class="temperature">${weather.temperature}°C</p>
                <p>${weather.condition} - ${weather.description}</p>
                <p>Feels like: ${weather.feels_like}°C | Humidity: ${weather.humidity}%</p>
            </div>
        </div>
    `;
}

async function loadPlan() {
    const planContent = document.getElementById('plan-content');
    
    try {
        const response = await fetch(`${API_BASE}/plan/current`);
        const data = await response.json();
        
        if (data.success && data.plan) {
            displayPlan(data.plan);
        } else {
            planContent.innerHTML = '<p class="error-message">No plan available. Click Refresh Plan to generate.</p>';
        }
    } catch (error) {
        console.error('Error loading plan:', error);
        planContent.innerHTML = '<p class="error-message">Failed to load plan.</p>';
    }
}

function displayPlan(plan) {
    const planContent = document.getElementById('plan-content');
    
    if (!plan.activities || plan.activities.length === 0) {
        planContent.innerHTML = '<p>No activities planned for today.</p>';
        return;
    }
    
    const activitiesHtml = plan.activities.map(activity => `
        <li class="activity-item">
            <div class="activity-name">${activity.name}</div>
            <div class="activity-meta">
                <span class="activity-type">${activity.type}</span>
                <span class="activity-priority">Priority: ${activity.priority}</span>
            </div>
        </li>
    `).join('');
    
    planContent.innerHTML = `
        <div class="plan-info">
            <p><strong>Date:</strong> ${plan.date}</p>
            <p><strong>Generated:</strong> ${plan.time_generated}</p>
            <p><strong>Weather:</strong> ${plan.weather.condition}, ${plan.weather.temperature}°C</p>
        </div>
        <ul class="activity-list">
            ${activitiesHtml}
        </ul>
    `;
}

async function loadPreferences() {
    const preferencesContent = document.getElementById('preferences-content');
    const editBtn = document.getElementById('edit-preferences-btn');
    
    try {
        const response = await fetch(`${API_BASE}/preferences`);
        const data = await response.json();
        
        if (data.success && data.preferences) {
            displayPreferences(data.preferences);
            editBtn.style.display = 'block';
        } else {
            preferencesContent.innerHTML = '<p class="error-message">Failed to load preferences.</p>';
        }
    } catch (error) {
        console.error('Error loading preferences:', error);
        preferencesContent.innerHTML = '<p class="error-message">Failed to load preferences.</p>';
    }
}

function displayPreferences(userData) {
    const preferencesContent = document.getElementById('preferences-content');
    const prefs = userData.preferences;
    
    preferencesContent.innerHTML = `
        <div class="preferences-display">
            <div class="pref-item">
                <span class="pref-label"Location:</span>
                <span class="pref-value">${userData.location}</span>
            </div>
            <div class="pref-item">
                <span class="pref-label">Preferred Types:</span>
                <span class="pref-value">${prefs.preferred_types.join(', ')}</span>
            </div>
            <div class="pref-item">
                <span class="pref-label">Avoid Types:</span>
                <span class="pref-value">${prefs.avoid_types.join(', ')}</span>
            </div>
            <div class="pref-item">
                <span class="pref-label">Working Hours:</span>
                <span class="pref-value">${prefs.working_hours.start}:00 - ${prefs.working_hours.end}:00</span>
            </div>
            <div class="pref-item">
                <span class="pref-label">Weekend Mode:</span>
                <span class="pref-value">${prefs.weekend_mode}</span>
            </div>
        </div>
    `;
}

async function loadHistory() {
    const historyContent = document.getElementById('history-content');
    
    try {
        const response = await fetch(`${API_BASE}/plans/history`);
        const data = await response.json();
        
        if (data.success && data.history) {
            displayHistory(data.history);
        } else {
            historyContent.innerHTML = '<p>No history available yet.</p>';
        }
    } catch (error) {
        console.error('Error loading history:', error);
        historyContent.innerHTML = '<p class="error-message">Failed to load history.</p>';
    }
}

function displayHistory(history) {
    const historyContent = document.getElementById('history-content');
    
    if (history.length === 0) {
        historyContent.innerHTML = '<p>No history available yet.</p>';
        return;
    }
    
    const historyHtml = history.reverse().map(plan => `
        <div class="history-item">
            <div class="history-date">${plan.date} - ${plan.location}</div>
            <div class="history-weather">${plan.weather.condition}, ${plan.weather.temperature}°C</div>
            <div>${plan.activities.length} activities planned</div>
        </div>
    `).join('');
    
    historyContent.innerHTML = `<div class="history-list">${historyHtml}</div>`;
}

async function refreshPlan() {
    const btn = document.getElementById('refresh-btn');
    btn.disabled = true;
    btn.textContent = 'Refreshing...';
    
    try {
        const response = await fetch(`${API_BASE}/weather/update`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            await loadAllData();
            showNotification('Plan refreshed successfully!', 'success');
        } else {
            showNotification('Failed to refresh plan.', 'error');
        }
    } catch (error) {
        console.error('Error refreshing plan:', error);
        showNotification('Error refreshing plan.', 'error');
    } finally {
        btn.disabled = false;
        btn.textContent = 'Refresh Plan';
    }
}

function openPreferencesModal() {
    const modal = document.getElementById('preferences-modal');
    
    fetch(`${API_BASE}/preferences`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                populatePreferencesForm(data.preferences.preferences);
                modal.style.display = 'block';
            }
        });
}

function populatePreferencesForm(prefs) {
    document.querySelectorAll('input[name="preferred"]').forEach(checkbox => {
        checkbox.checked = prefs.preferred_types.includes(checkbox.value);
    });
    
    document.querySelectorAll('input[name="avoid"]').forEach(checkbox => {
        checkbox.checked = prefs.avoid_types.includes(checkbox.value);
    });
    
    document.getElementById('work-start').value = prefs.working_hours.start;
    document.getElementById('work-end').value = prefs.working_hours.end;
    
    document.getElementById('weekend-mode').value = prefs.weekend_mode;
}

function closePreferencesModal() {
    const modal = document.getElementById('preferences-modal');
    modal.style.display = 'none';
}

async function savePreferences(e) {
    e.preventDefault();
    
    const preferredTypes = Array.from(document.querySelectorAll('input[name="preferred"]:checked'))
        .map(cb => cb.value);
    
    const avoidTypes = Array.from(document.querySelectorAll('input[name="avoid"]:checked'))
        .map(cb => cb.value);
    
    const workStart = parseInt(document.getElementById('work-start').value);
    const workEnd = parseInt(document.getElementById('work-end').value);
    const weekendMode = document.getElementById('weekend-mode').value;
    
    const preferences = {
        preferred_types: preferredTypes,
        avoid_types: avoidTypes,
        working_hours: { start: workStart, end: workEnd },
        weekend_mode: weekendMode
    };
    
    try {
        const response = await fetch(`${API_BASE}/preferences`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(preferences)
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification('Preferences updated successfully!', 'success');
            closePreferencesModal();
            await loadAllData();
        } else {
            showNotification('Failed to update preferences.', 'error');
        }
    } catch (error) {
        console.error('Error saving preferences:', error);
        showNotification('Error saving preferences.', 'error');
    }
}

function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = type === 'success' ? 'success-message' : 'error-message';
    notification.textContent = message;
    notification.style.position = 'fixed';
    notification.style.top = '20px';
    notification.style.right = '20px';
    notification.style.zIndex = '9999';
    notification.style.padding = '15px 25px';
    notification.style.borderRadius = '8px';
    notification.style.boxShadow = '0 4px 8px rgba(0,0,0,0.2)';
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}