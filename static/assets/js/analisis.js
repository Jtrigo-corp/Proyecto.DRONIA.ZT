let dataTable;
let dataTableIsInitialized = false;

const dataTableAction = {
    columnDefs: [
        {className:'centered', targets:[0,1,2,3,4,5,6,7]},
        {orderable: false, targets: [5,6]},
        {searchable: false, targets: [1,2,3,4,5,6]},
    ],
    pageLength: 4,
    destroy: true
}
const initDataTable = async () => {
    if (dataTableIsInitialized) {
        dataTable.destroy();
    }

    await listVuelos();
    dataTable = $('#datatable-analisis').DataTable(dataTableAction);
    dataTableIsInitialized = true;
};

const listVuelos = async () => {
    try {
        const response = await fetch('http://127.0.0.1:8000/list_vuelos/');
        const data = await response.json();
        console.log(data);
        let content ='';
        data.vuelos.forEach((vuelo, carga) => {
            content += `
                <tr>
                    <td>${carga+1}</td>
                    <td>${vuelo.norte}</td>
                    <td>${vuelo.este}</td>
                    <td>Higo01</td>
                    <td>Higuera</td>
                    <td>Predicción</td>
                    <td>84%</td>
                    <td>${vuelo.update_at}</td>
                    <td>
                        <button class='btn btn-sm btn-info'><i class='fa-solid fa-check'></i>Cargar</button>
                    </td>
                </tr>
                `;
        });
        tableBody_analisis.innerHTML = content;

    } catch (e) {
        
    }
};

window.addEventListener('load', async () => {
    await initDataTable();
});