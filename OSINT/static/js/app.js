document.getElementById('checkForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const checkBtn = document.getElementById('checkBtn');
    const btnText = document.getElementById('btnText');
    const btnLoader = document.getElementById('btnLoader');
    const results = document.getElementById('results');
    
    // Show loading state
    checkBtn.disabled = true;
    btnText.style.display = 'none';
    btnLoader.style.display = 'inline-block';
    results.style.display = 'none';
    
    try {
        const response = await fetch('/check', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password })
        });
        
        if (!response.ok) {
            const error = await response.json();
            alert(error.error || 'An error occurred');
            return;
        }
        
        const data = await response.json();
        displayResults(data);
        
    } catch (error) {
        alert('Network error: ' + error.message);
    } finally {
        checkBtn.disabled = false;
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
    }
});

function displayResults(data) {
    const results = document.getElementById('results');
    
    // Email results
    const emailResult = document.getElementById('emailResult');
    const emailSources = document.getElementById('emailSources');
    
    if (data.email.found === true) {
        emailResult.innerHTML = `<div class="status danger">⚠️ ${data.email.message}</div>`;
        
        if (data.email.sources && data.email.sources.length > 0) {
            const sourcesList = data.email.sources.map(s => `<li>• ${s}</li>`).join('');
            emailSources.innerHTML = `<ul>${sourcesList}</ul>`;
        } else {
            emailSources.innerHTML = '';
        }
    } else if (data.email.found === false) {
        emailResult.innerHTML = `<div class="status safe">✅ ${data.email.message}</div>`;
        emailSources.innerHTML = '';
    } else {
        emailResult.innerHTML = `<div class="status warning">⚠️ ${data.email.message}</div>`;
        emailSources.innerHTML = '<p style="margin-top: 10px; font-size: 0.9em; color: #888;">Manual check: <a href="https://haveibeenpwned.com/" target="_blank" style="color: #8b5cf6;">haveibeenpwned.com</a></p>';
    }
    
    // Password results
    const passwordResult = document.getElementById('passwordResult');
    
    if (data.password.count === null) {
        passwordResult.innerHTML = `<div class="status warning">❌ Could not check password exposure</div>`;
    } else if (data.password.count === 0) {
        passwordResult.innerHTML = `<div class="status safe">✅ Password has NOT been found in known breaches</div>`;
    } else {
        passwordResult.innerHTML = `<div class="status danger">⚠️ Password has been seen ${data.password.count.toLocaleString()} times in breaches!</div>`;
    }
    
    // Risk assessment
    const riskLevel = document.getElementById('riskLevel');
    const riskMessage = document.getElementById('riskMessage');
    const recommendation = document.getElementById('recommendation');
    
    riskLevel.className = `risk-badge ${data.risk.level}`;
    riskLevel.textContent = data.risk.level.toUpperCase() + ' RISK';
    riskMessage.textContent = data.risk.message;
    recommendation.innerHTML = `<strong>💡 Recommendation:</strong> ${data.risk.recommendation}`;
    
    // Show results
    results.style.display = 'block';
    results.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}
