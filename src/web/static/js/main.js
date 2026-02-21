document.addEventListener('DOMContentLoaded', function() {
    fetchViolations();
    setInterval(fetchViolations, 5000); // Poll every 5 seconds
});

function fetchViolations() {
    fetch('/api/violations')
        .then(response => response.json())
        .then(data => {
            updateRecentList(data);
            updateHistoryTable(data);
        })
        .catch(error => console.error('Error fetching data:', error));
}

function updateRecentList(data) {
    const list = document.getElementById('violation-list');
    list.innerHTML = '';
    
    // Show top 5 recent
    const recent = data.slice(0, 5);
    
    if (recent.length === 0) {
        list.innerHTML = '<li class="list-group-item bg-dark text-white">No violations detected yet.</li>';
        return;
    }

    recent.forEach(v => {
        const item = document.createElement('li');
        item.className = 'list-group-item bg-dark text-white d-flex justify-content-between align-items-center';
        item.innerHTML = `
            <span>${v.timestamp} - <strong>${v.plate_number}</strong></span>
            <span class="badge bg-danger">Alert</span>
        `;
        list.appendChild(item);
    });
}

function updateHistoryTable(data) {
    const tbody = document.getElementById('history-table-body');
    tbody.innerHTML = '';

    data.forEach(v => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${v.id}</td>
            <td>${v.timestamp}</td>
            <td>${v.plate_number}</td>
            <td><span class="badge bg-warning text-dark">${v.status}</span></td>
            <td><a href="#" class="btn btn-sm btn-outline-info">View</a></td>
        `;
        tbody.appendChild(row);
    });
}
