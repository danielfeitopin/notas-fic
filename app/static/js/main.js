//Global variables to store charts

let chartComparacion = null;
let chartSuspensos = null;
let chartSexo = []; 

// ============== A) ==============

/**
 * Crea un único gráfico (pie) por cada carrera. Cada porción representa
 * el año académico y la asignatura que tuvo más suspensos en ese año; el
 * tamaño del slice corresponde al número de suspensos.
 */
async function cargarGraficoMasSuspensos() {
    try {
        const response = await fetch('/api/resultados/top-suspensos-por-ano');
        const datos = await response.json();
        const cont = document.getElementById('topSuspensosContainer');
        cont.innerHTML = ''; // borra contenido previo

        // agrupar por carrera
        const byCarrera = datos.reduce((acc, item) => {
            (acc[item.carreira] = acc[item.carreira] || []).push(item);
            return acc;
        }, {});

        Object.entries(byCarrera).forEach(([carreira, items]) => {
            const box = document.createElement('div');
            box.className = 'chart-box';
            box.dataset.carreira = carreira;
            box.innerHTML = `<h3>${carreira}</h3>`;
            cont.appendChild(box);

            // dentro de cada carrera, un pie por año académico
            items.forEach((item, idx) => {
                const sub = document.createElement('div');
                sub.className = 'subchart';
                sub.innerHTML = `
                    <h4>${item.ano}: ${item.asignatura}</h4>
                    <canvas id="pie_${carreira}_${idx}"></canvas>
                `;
                box.appendChild(sub);

                const ctx = sub.querySelector('canvas').getContext('2d');
                new Chart(ctx, {
                    type: 'pie',
                    data: {
                        labels: ['Aprobados', 'Suspensos', 'NP'],
                        datasets: [{
                            data: [item.aprobados, item.suspensos, item.np],
                            backgroundColor: [
                                'rgba(75, 192, 192, 0.7)',
                                'rgba(255, 99, 132, 0.7)',
                                'rgba(255, 206, 86, 0.7)'
                            ],
                            borderColor: [
                                'rgba(75, 192, 192, 1)',
                                'rgba(255, 99, 132, 1)',
                                'rgba(255, 206, 86, 1)'
                            ],
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: { position: 'bottom' },
                            tooltip: {
                                callbacks: {
                                    label: context => {
                                        const idx2 = context.dataIndex;
                                        const val = [item.aprobados, item.suspensos, item.np][idx2];
                                        const label = ['Aprobados','Suspensos','NP'][idx2];
                                        return `${label}: ${val}`;
                                    }
                                }
                            }
                        }
                    }
                });
            });
        });
    } catch (error) {
        console.error('Error al cargar top suspensos:', error);
    }
}


// cuando se desea renderizar solo los pies de una carrera dentro de un
// contenedor específico utilizamos esta función auxiliar
async function cargarGraficoMasSuspensosFor(carrera, container) {
    try {
        const response = await fetch('/api/resultados/top-suspensos-por-ano');
        const datos = await response.json();
        // filtra los registros que pertenecen a la carrera solicitada
        const items = datos.filter(d => d.carreira === carrera);
        container.innerHTML = ''; // limpiar previo contenido
        items.forEach((item, idx) => {
            const sub = document.createElement('div');
            sub.className = 'subchart';
            sub.innerHTML = `
                <h4>${item.ano}: ${item.asignatura}</h4>
                <canvas id="pie_${carrera}_${idx}"></canvas>
            `;
            container.appendChild(sub);

            const ctx = sub.querySelector('canvas').getContext('2d');
            new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: ['Aprobados', 'Suspensos', 'NP'],
                    datasets: [{
                        data: [item.aprobados, item.suspensos, item.np],
                        backgroundColor: [
                            'rgba(75, 192, 192, 0.7)',
                            'rgba(255, 99, 132, 0.7)',
                            'rgba(255, 206, 86, 0.7)'
                        ],
                        borderColor: [
                            'rgba(75, 192, 192, 1)',
                            'rgba(255, 99, 132, 1)',
                            'rgba(255, 206, 86, 1)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { position: 'bottom' },
                        tooltip: {
                            callbacks: {
                                label: context => {
                                    const idx2 = context.dataIndex;
                                    const val = [item.aprobados, item.suspensos, item.np][idx2];
                                    const label = ['Aprobados','Suspensos','NP'][idx2];
                                    return `${label}: ${val}`;
                                }
                            }
                        }
                    }
                }
            });
        });
    } catch (error) {
        console.error('Error al cargar top suspensos for', carrera, error);
    }
}

// cargar listado de asignaturas y desplegar selector dentro de career container
async function cargarAsignaturasCarrera(carrera, container) {
    try {
        const response = await fetch(`/api/asignaturas/${carrera}`);
        const asigns = await response.json();
        // selector
        const select = document.createElement('select');
        select.id = `asigSelect_${carrera}`;
        const optdef = document.createElement('option');
        optdef.value = '';
        optdef.textContent = 'Selecciona asignatura';
        select.appendChild(optdef);
        asigns.forEach(a => {
            const o = document.createElement('option');
            o.value = a.codigo;
            o.textContent = a.nome;
            select.appendChild(o);
        });
        container.appendChild(select);
        // contenedor de evolución (pero sólo se usa en la página dedicada)
        const evoDiv = document.createElement('div');
        evoDiv.className = 'evolucion-container';
        const canv = document.createElement('canvas');
        canv.id = `evol_${carrera}`;
        evoDiv.appendChild(canv);
        container.appendChild(evoDiv);

        select.addEventListener('change', () => {
            const cod = select.value;
            if (cod) {
                // al elegir materia, navegamos a su página dedicada
                window.location.href = `/asignatura/${cod}`;
            }
        });
    } catch (error) {
        console.error('Error al cargar asignaturas de carrera', error);
    }
}

// gráfico de evolución de una asignatura en canvas dado
let chartEvolAsign = null;
function cargarGraficoEvolucionAsignatura(codigo, canvasElem) {
    fetch(`/api/resultados/evolucion/${codigo}`)
        .then(r => r.json())
        .then(datos => {
            const ctx = canvasElem.getContext('2d');
            if (chartEvolAsign) chartEvolAsign.destroy();
            chartEvolAsign = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: datos.map(d => d.ano),
                    datasets: [
                        {
                            label: 'Aprobados',
                            data: datos.map(d => d.aprobados),
                            borderColor: 'rgba(75, 192, 192, 1)',
                            backgroundColor: 'rgba(75, 192, 192, 0.2)',
                            tension: 0.4,
                            fill: true
                        },
                        {
                            label: 'Suspensos',
                            data: datos.map(d => d.suspensos),
                            borderColor: 'rgba(255, 99, 132, 1)',
                            backgroundColor: 'rgba(255, 99, 132, 0.2)',
                            tension: 0.4,
                            fill: true
                        },
                        {
                            label: 'NP',
                            data: datos.map(d => d.np),
                            borderColor: 'rgba(255, 206, 86, 1)',
                            backgroundColor: 'rgba(255, 206, 86, 0.2)',
                            tension: 0.4,
                            fill: true
                        }
                    ]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: { beginAtZero: true }
                    }
                }
            });
        })
        .catch(err => console.error('Error evolución asignatura', err));
}

// Función para cargar y mostrar el gráfico de comparación de carreras
async function cargarGraficoComparacion() {
    try {
        const response = await fetch('/api/resultados/comparacion-carreras');
        const datos = await response.json();

        const ctx = document.getElementById('chartComparacion').getContext('2d');

        if (chartComparacion) {
            chartComparacion.destroy();
        }

        chartComparacion = new Chart(ctx, {
            type: 'radar',
            data: {
                labels: datos.map(d => d.carrera),
                datasets: [
                    {
                        label: 'Aprobados',
                        data: datos.map(d => d.aprobados),
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        pointBackgroundColor: 'rgba(75, 192, 192, 1)'
                    },
                    {
                        label: 'Suspensos',
                        data: datos.map(d => d.suspensos),
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        pointBackgroundColor: 'rgba(255, 99, 132, 1)'
                    }
                ]
            },
            options: {
                responsive: true,
                scales: {
                    r: {
                        beginAtZero: true
                    }
                }
            }
        });

    } catch (error) {
        console.error('Error al cargar datos de comparación:', error);
    }
}

// Función para cargar suspensos de una carrera específica
async function cargarSuspensosCarrera(carrera) {
    try {
        const response = await fetch(`/api/resultados/suspensos/${carrera}`);
        const datos = await response.json();
        
        // Mostrar el contenedor
        document.getElementById('chartSuspensosContainer').style.display = 'block';
        
        actualizarChartSuspensos(datos);
        
    } catch (error) {
        console.error('Error al cargar datos de suspensos:', error);
    }
}

function actualizarChartSuspensos(datos) {
    const ctx = document.getElementById('chartSuspensos').getContext('2d');
    
    if (chartSuspensos) {
        chartSuspensos.destroy();
    }
    
    // Ordenar por suspensos (ya viene ordenado del API, pero por seguridad)
    const datosOrdenados = [...datos].sort((a, b) => b.suspensos - a.suspensos);
    
    chartSuspensos = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: datosOrdenados.map(d => d.asignatura),
            datasets: [
                {
                    label: 'Suspensos',
                    data: datosOrdenados.map(d => d.suspensos),
                    backgroundColor: 'rgba(255, 99, 132, 0.8)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Aprobados',
                    data: datosOrdenados.map(d => d.aprobados),
                    backgroundColor: 'rgba(75, 192, 192, 0.8)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            indexAxis: 'y', // Gráfico horizontal para mejor lectura
            scales: {
                x: {
                    beginAtZero: true,
                    stacked: false
                },
                y: {
                    stacked: false
                }
            }
        }
    });
}

// Función para cargar selector de años académicos dentro de una carrera
async function cargarAnosCarrera(carrera, container) {
    try {
        const response = await fetch('/api/anos');
        const anos = await response.json();
        const select = document.createElement('select');
        select.className = 'year-select';
        select.id = `yearSelect_${carrera}`;
        const optdef = document.createElement('option');
        optdef.value = '';
        optdef.textContent = 'Selecciona año académico';
        select.appendChild(optdef);
        anos.forEach(a => {
            const o = document.createElement('option');
            o.value = a.ano;
            o.textContent = a.ano;
            select.appendChild(o);
        });
        container.appendChild(select);

        select.addEventListener('change', () => {
            const ano = select.value;
            if (ano) {
                // navegar a la página del año dentro de la carrera
                window.location.href = `/carrera/${carrera}/ano/${encodeURIComponent(ano)}`;
            }
        });
    } catch (error) {
        console.error('Error al cargar años académicos', error);
    }
}

// Función para dibujar top‑NP de una carrera y año dados
async function cargarGraficoTopNp(carrera, ano, container) {
    try {
        const response = await fetch('/api/resultados/top-np-por-carreira');
        const data = await response.json();
        const filtrados = data.filter(d => d.carreira === carrera && d.ano === ano);
        container.innerHTML = '';
        const canv = document.createElement('canvas');
        container.appendChild(canv);
        const ctx = canv.getContext('2d');
        const labels = filtrados.map(d => `${d.curso} – ${d.asignatura}`);
        const values = filtrados.map(d => d.porcentaxe_np);
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels,
                datasets: [{
                    label: '% NP',
                    data: values,
                    backgroundColor: 'rgba(153, 102, 255, 0.7)',
                    borderColor: 'rgba(153, 102, 255, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                indexAxis: 'y',
                scales: { x: { beginAtZero: true } }
            }
        });
    } catch (error) {
        console.error('Error top np por carrera/año', error);
    }
}

// similar función que dibuja en un canvas existente (para página del año)
async function cargarGraficoTopNpCanvas(carrera, ano, canvas) {
    try {
        const response = await fetch('/api/resultados/top-np-por-carreira');
        const data = await response.json();
        const filtrados = data.filter(d => d.carreira === carrera && d.ano === ano);
        const ctx = canvas.getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: filtrados.map(d => `${d.curso} – ${d.asignatura}`),
                datasets: [{
                    label: '% NP',
                    data: filtrados.map(d => d.porcentaxe_np),
                    backgroundColor: 'rgba(153, 102, 255, 0.7)',
                    borderColor: 'rgba(153, 102, 255, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                indexAxis: 'y',
                scales: { x: { beginAtZero: true } }
            }
        });
    } catch (error) {
        console.error('Error top np por carrera/año', error);
    }
}

// Función para cargar gráfico de evolución temporal de una carrera
async function cargarGraficoEvolucionCarrera(carrera, container) {
    try {
        const response = await fetch(`/api/resultados/evolucion-carreira/${carrera}`);
        const data = await response.json();
        container.innerHTML = '';
        const canv = document.createElement('canvas');
        canv.id = `evolCarrera_${carrera}`;
        container.appendChild(canv);
        const ctx = canv.getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.map(d => d.ano),
                datasets: [
                    {
                        label: 'Aprobados',
                        data: data.map(d => d.aprobados),
                        borderColor: 'rgba(75, 192, 192, 1)',
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        tension: 0.4,
                        fill: true
                    },
                    {
                        label: 'Suspensos',
                        data: data.map(d => d.suspensos),
                        borderColor: 'rgba(255, 99, 132, 1)',
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        tension: 0.4,
                        fill: true
                    },
                    {
                        label: 'NP',
                        data: data.map(d => d.np),
                        borderColor: 'rgba(255, 206, 86, 1)',
                        backgroundColor: 'rgba(255, 206, 86, 0.2)',
                        tension: 0.4,
                        fill: true
                    }
                ]
            },
            options: {
                responsive: true,
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
    } catch (error) {
        console.error('Error al cargar evolución de carrera', error);
    }
}

// ==============  D) ==============

/**
 * Creates pie charts for each subject showing distribution
 * of women and men. Each pie corresponds to a subject.
 * Shows all careers with data, even if some careers don't have data.
 */
async function cargarGraficoSexo() {
    try {
        const anosResponse = await fetch('/api/anos');
        const anosData = await anosResponse.json();
        
        if (anosData.length === 0) {
            console.warn('No hay años académicos disponibles');
            const wrapper = document.getElementById('sexoChartsWrapper');
            wrapper.innerHTML = '<p class="no-data-message">No hay años académicos disponibles</p>';
            return;
        }
        
        const primerAno = anosData[0].ano;
        
        const response = await fetch(`/api/resultados/porcentaxe-sexo/${encodeURIComponent(primerAno)}`);
        const data = await response.json();
        
        const wrapper = document.getElementById('sexoChartsWrapper');
        wrapper.innerHTML = ''; 
        
        chartSexo.forEach(chart => chart.destroy());
        chartSexo = [];
        
        if (data.length === 0) {
            wrapper.innerHTML = '<p class="no-data-message">No hay datos de sexo disponibles para el año ' + primerAno + '</p>';
            return;
        }
        
        data.forEach((item, index) => {
            // Verificar si hay datos válidos (al menos un valor > 0)
            const hasValidData = (item.mulleres > 0) || (item.homes > 0);
            
            if (!hasValidData) {
                // Si no hay datos válidos, mostrar un mensaje en lugar del gráfico
                const chartItem = document.createElement('div');
                chartItem.className = 'sexo-chart-item';
                chartItem.innerHTML = `<h3>${item.carreira}</h3><p class="no-data-message">Sin datos</p>`;
                wrapper.appendChild(chartItem);
                return;
            }
            
            const chartItem = document.createElement('div');
            chartItem.className = 'sexo-chart-item';
            chartItem.innerHTML = `<h3>${item.carreira}</h3><canvas id="sexoPie_${index}"></canvas>`;
            wrapper.appendChild(chartItem);
            
            const ctx = document.getElementById(`sexoPie_${index}`).getContext('2d');
            
            const chart = new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: ['Mujeres', 'Hombres'],
                    datasets: [{
                        data: [item.mulleres, item.homes],
                        backgroundColor: [
                            'rgba(255, 105, 180, 0.7)',  
                            'rgba(54, 162, 235, 0.7)'   
                        ],
                        borderColor: [
                            'rgba(255, 105, 180, 1)',
                            'rgba(54, 162, 235, 1)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    const label = context.label || '';
                                    const value = context.raw || 0;
                                    const total = item.mulleres + item.homes;
                                    const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : 0;
                                    return `${label}: ${value} (${percentage}%)`;
                                }
                            }
                        }
                    }
                }
            });
            
            chartSexo.push(chart);
        });
        
    } catch (error) {
        console.error('Error al cargar gráfico de sexo:', error);
        const wrapper = document.getElementById('sexoChartsWrapper');
        wrapper.innerHTML = '<p class="error-message">Error al cargar los datos de sexo</p>';
    }
}

// Load all los charts when starting the page
document.addEventListener('DOMContentLoaded', function() {
    cargarGraficoComparacion();
    cargarGraficoSexo(); 

    if (typeof selectedCareer !== 'undefined' && selectedCareer) {
        document.querySelectorAll('.charts-container > .chart-box').forEach(box => {
            box.style.display = 'none';
        });
    }
});
