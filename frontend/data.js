const API_URL = 'http://localhost:8000';

async function fetchData() {
    try {
        const response = await fetch(`${API_URL}/admin/data`);
        if (!response.ok) {
            throw new Error('Failed to fetch data');
        }
        const data = await response.json();
        renderTables(data);
    } catch (error) {
        console.error('Error:', error);
        document.querySelectorAll('[id$="-table-container"]').forEach(el => {
            el.innerHTML = `<div class="error">Error loading data: ${error.message}</div>`;
        });
    }
}

function renderTables(data) {
    renderTable('giftcards-table-container', data.gift_cards, ['id', 'code_hash', 'initial_balance', 'current_balance', 'status', 'created_at']);
    renderTable('redemptions-table-container', data.redemptions, ['id', 'gift_card_id', 'amount', 'comment', 'created_at']);
    renderTable('redis-table-container', data.redis_data, ['key', 'value']);
}

function renderTable(containerId, data, columns) {
    const container = document.getElementById(containerId);
    if (!data || data.length === 0) {
        container.innerHTML = '<div class="empty-state">No data available</div>';
        return;
    }

    let html = '<table><thead><tr>';
    columns.forEach(col => {
        html += `<th>${col.replace(/_/g, ' ').toUpperCase()}</th>`;
    });
    html += '</tr></thead><tbody>';

    data.forEach(row => {
        html += '<tr>';
        columns.forEach(col => {
            let val = row[col];
            if (typeof val === 'object' && val !== null) {
                val = JSON.stringify(val); // Handle objects/arrays if any
            }
            // Truncate long hashes for display
            if (typeof val === 'string' && val.length > 20 && !val.includes(' ')) {
                val = `<span title="${val}">${val.substring(0, 10)}...${val.substring(val.length - 5)}</span>`;
            }
            html += `<td>${val}</td>`;
        });
        html += '</tr>';
    });
    html += '</tbody></table>';
    container.innerHTML = html;
}

document.addEventListener('DOMContentLoaded', fetchData);
