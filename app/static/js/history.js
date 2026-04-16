document.addEventListener('DOMContentLoaded', function () {
    const historyTableBody = document.querySelector('tbody');
    const helmetId = window.location.pathname.split('/').pop();

    function updateHistory() {
        if (!helmetId) return;

        fetch(`/api/history/${helmetId}`)
            .then(response => response.json())
            .then(data => {
                if (data.length === 0) return;

                let html = '';
                data.forEach(reading => {
                    const statusClass = reading.gas > 650 ? 'text-red-500' : 'text-gray-700';
                    const statusBadge = reading.gas > 650
                        ? '<span class="px-2 py-1 rounded-full bg-red-100 text-red-600 text-[10px] font-bold uppercase">Danger</span>'
                        : '<span class="px-2 py-1 rounded-full bg-green-100 text-green-600 text-[10px] font-bold uppercase">Safe</span>';

                    html += `
                        <tr class="hover:bg-slate-50 transition-colors animate-fade-in">
                            <td class="px-6 py-4 text-sm text-gray-600">${reading.timestamp}</td>
                            <td class="px-6 py-4 font-bold text-gray-700">${reading.temperature}°C</td>
                            <td class="px-6 py-4 font-bold ${statusClass}">${reading.gas} ppm</td>
                            <td class="px-6 py-4">${statusBadge}</td>
                        </tr>
                    `;
                });
                historyTableBody.innerHTML = html;
            })
            .catch(err => console.error("Error updating history:", err));
    }

    setInterval(updateHistory, 5000);
});
