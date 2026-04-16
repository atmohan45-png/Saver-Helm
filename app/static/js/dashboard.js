document.addEventListener('DOMContentLoaded', function () {
    const helmetContainer = document.getElementById('helmet-container');
    const gasAlert = document.getElementById('gas-alert');
    const alertMessage = document.getElementById('alert-message');

    function fetchLatestData() {
        fetch('/api/latest-data')
            .then(response => response.json())
            .then(data => {
                const loadingSpinner = document.getElementById('loading-spinner');
                if (loadingSpinner) loadingSpinner.remove();

                if (data.length === 0) {
                    helmetContainer.innerHTML = `
                        <div class="col-span-full bg-white p-12 rounded-3xl text-center border-2 border-dashed border-gray-200">
                            <i class="fas fa-plus-circle text-4xl text-gray-300 mb-4"></i>
                            <p class="text-gray-500">No helmets registered. <a href="/manage-helmets" class="text-blue-600 font-bold">Add one now</a></p>
                        </div>
                    `;
                    return;
                }

                let html = '';
                let dangerousGas = false;
                let dangerousHelmets = [];

                data.forEach(helmet => {
                    const statusColor = helmet.status === 'danger' ? 'red' : 'green';
                    if (helmet.status === 'danger') {
                        dangerousGas = true;
                        dangerousHelmets.push(helmet.helmet_name);
                    }

                    html += `
                        <div class="glass-card bg-white p-6 rounded-3xl shadow-sm hover:shadow-xl transition-all duration-300 border-t-4 border-${statusColor}-500 transform hover:-translate-y-1">
                            <div class="flex justify-between items-start mb-4">
                                <div>
                                    <h3 class="text-xl font-bold text-gray-800">${helmet.helmet_name}</h3>
                                    <p class="text-sm text-gray-500 flex items-center gap-1">
                                        <i class="fas fa-user text-xs"></i> ${helmet.worker_name}
                                    </p>
                                </div>
                                <div class="px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider bg-${statusColor}-100 text-${statusColor}-600">
                                    ${helmet.status}
                                </div>
                            </div>

                            <div class="grid grid-cols-2 gap-4 mb-6">
                                <div class="bg-slate-50 p-4 rounded-2xl border border-gray-100">
                                    <p class="text-xs text-gray-400 mb-1">Temperature</p>
                                    <p class="text-2xl font-bold text-gray-700">${helmet.temperature}°C</p>
                                </div>
                                <div class="bg-slate-50 p-4 rounded-2xl border border-gray-100">
                                    <p class="text-xs text-gray-400 mb-1">Gas Level</p>
                                    <p class="text-2xl font-bold ${helmet.status === 'danger' ? 'text-red-500' : 'text-gray-700'}">${helmet.gas} <span class="text-xs font-normal opacity-50">ppm</span></p>
                                </div>
                            </div>

                            <div class="flex justify-between items-center text-xs text-gray-400 border-t border-gray-50 pt-4 mt-2">
                                <div class="flex gap-3">
                                    ${helmet.is_admin ? `
                                    <a href="/edit-helmet/${helmet.helmet_id}" class="text-gray-400 hover:text-blue-600 transition-colors" title="Edit Helmet">
                                        <i class="fas fa-edit"></i>
                                    </a>
                                    <button onclick="confirmDelete('/delete-helmet/${helmet.helmet_id}', 'Remove Helmet?', 'Are you sure you want to unregister this worker helmet? All history will be lost.')" 
                                            class="text-gray-400 hover:text-red-600 transition-colors" title="Delete Helmet">
                                        <i class="fas fa-trash-alt"></i>
                                    </button>
                                    ` : ''}
                                </div>
                                <div class="flex items-center gap-3">
                                    <span><i class="fas fa-clock mr-1"></i> ${helmet.last_updated}</span>
                                    <a href="/helmet/${helmet.helmet_id}" class="text-blue-500 hover:text-blue-700 font-bold uppercase transition-colors">Details <i class="fas fa-chevron-right ml-1"></i></a>
                                </div>
                            </div>
                        </div>
                    `;
                });

                helmetContainer.innerHTML = html;

                if (dangerousGas) {
                    gasAlert.classList.remove('translate-y-32');
                    alertMessage.innerText = `Danger detected in: ${dangerousHelmets.join(', ')}`;
                } else {
                    gasAlert.classList.add('translate-y-32');
                }
            })
            .catch(error => console.error('Error fetching helmet data:', error));
    }

    fetchLatestData();
    setInterval(fetchLatestData, 5000);
});
