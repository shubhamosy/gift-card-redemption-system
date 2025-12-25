const API_URL = 'http://localhost:8000';

async function issueCard() {
    const amountInput = document.getElementById('issueAmount');
    const amount = amountInput.value;
    const resultDiv = document.getElementById('issueResult');
    const btn = document.querySelector('#issueBtn');
    
    if (!amount || parseFloat(amount) <= 0) {
        showResult(resultDiv, 'error', '❌ Please enter a valid amount greater than 0');
        return;
    }

    setLoading(btn, true);
    
    try {
        const response = await fetch(`${API_URL}/giftcards/issue`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ initial_balance: parseFloat(amount) })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showResult(resultDiv, 'success', `
                <strong>Card Issued Successfully!</strong>
                <div class="code-display">${data.code}</div>
                <div class="balance-info">
                    <span>Initial Balance:</span>
                    <span class="currency">₹${data.initial_balance.toFixed(2)}</span>
                </div>
                <small style="display:block; text-align:center; margin-top:0.5rem; color:var(--text-muted)">
                    ⚠️ Save this code! It won't be shown again.
                </small>
            `);
        } else {
            throw new Error(data.detail || 'Error issuing card');
        }
    } catch (error) {
        showResult(resultDiv, 'error', `❌ ${error.message}`);
    } finally {
        setLoading(btn, false);
    }
}

async function validateCard() {
    const code = document.getElementById('validateCode').value;
    const resultDiv = document.getElementById('validateResult');
    const btn = document.querySelector('#validateBtn');
    
    if (!code || code.length !== 12) {
        showResult(resultDiv, 'error', '❌ Please enter a valid 12-character code');
        return;
    }

    setLoading(btn, true);
    
    try {
        const response = await fetch(`${API_URL}/giftcards/validate/${code}`);
        const data = await response.json();
        
        if (response.ok) {
            const statusClass = data.status === 'ACTIVE' ? 'success-text' : 'error-text';
            showResult(resultDiv, 'success', `
                <strong>Card Details</strong>
                <div style="margin-top: 1rem;">
                    <div class="balance-info">
                        <span>Status:</span>
                        <span style="font-weight:bold;">${data.status}</span>
                    </div>
                    <div class="balance-info">
                        <span>Current Balance:</span>
                        <span class="currency" style="font-size:1.2rem; color:var(--primary-color)">₹${data.current_balance.toFixed(2)}</span>
                    </div>
                    <div class="balance-info" style="color:var(--text-muted)">
                        <span>Initial Balance:</span>
                        <span>₹${data.initial_balance.toFixed(2)}</span>
                    </div>
                </div>
            `);
        } else {
            throw new Error(data.detail || 'Error validating card');
        }
    } catch (error) {
        showResult(resultDiv, 'error', `❌ ${error.message}`);
    } finally {
        setLoading(btn, false);
    }
}

async function redeemCard() {
    const code = document.getElementById('redeemCode').value;
    const amount = document.getElementById('redeemAmount').value;
    const comment = document.getElementById('redeemComment').value;
    const resultDiv = document.getElementById('redeemResult');
    const btn = document.querySelector('#redeemBtn');
    if (!amount || parseFloat(amount) <= 0) {
        showResult(resultDiv, 'error', '❌ Please enter a valid amount greater than 0');
        return;
    }

    
    if (!code || code.length !== 12) {
        showResult(resultDiv, 'error', '❌ Please enter a valid 12-character code');
        return;
    }

    setLoading(btn, true);
    
    // Generate a random idempotency key for this request
    const idempotencyKey = Math.random().toString(36).substring(7);

    try {
        const response = await fetch(`${API_URL}/giftcards/redeem`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                code: code,
                amount: parseFloat(amount),
                comment: comment,
                idempotency_key: idempotencyKey
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showResult(resultDiv, 'success', `
                <strong>Redemption Successful!</strong>
                <div style="margin-top: 1rem;">
                    <div class="balance-info">
                        <span>Redeemed Amount:</span>
                        <span class="currency" style="color:var(--error-text)">-₹${data.amount.toFixed(2)}</span>
                    </div>
                    <div class="balance-info">
                        <span>New Balance:</span>
                        <span class="currency" style="font-size:1.2rem; color:var(--primary-color)">₹${data.new_balance.toFixed(2)}</span>
                    </div>
                    <div style="margin-top:0.5rem; font-size:0.8rem; color:var(--text-muted)">
                        Transaction ID: ${data.id}
                    </div>
                </div>
            `);
        } else {
            throw new Error(data.detail || 'Error redeeming card');
        }
    } catch (error) {
        showResult(resultDiv, 'error', `❌ ${error.message}`);
    } finally {
        setLoading(btn, false);
    }
}

function showResult(element, type, html) {
    element.className = `result ${type}`;
    element.innerHTML = html;
    element.style.display = 'block';
}

function setLoading(btn, isLoading) {
    if (isLoading) {
        btn.dataset.originalText = btn.innerText;
        btn.innerText = 'Processing...';
        btn.disabled = true;
        btn.style.opacity = '0.7';
    } else {
        btn.innerText = btn.dataset.originalText;
        btn.disabled = false;
        btn.style.opacity = '1';
    }
}
