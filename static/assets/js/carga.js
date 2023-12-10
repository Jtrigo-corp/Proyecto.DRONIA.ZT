let dataTable;
        let dataTableIsInitialized = false;
    
        const dataTableAction = {
            columnDefs: [
                {className:'centered', targets:[0,1,2,3,4]},  // Ajusta según sea necesario
                {orderable: false, targets: []},  // Desactiva la ordenación para ciertas columnas si es necesario
                {searchable: false, targets: []},  // Desactiva la búsqueda para ciertas columnas si es necesario
            ],
            pageLength: 4,
            destroy: true
        }
    
        const initDataTable = async () => {
            if (dataTableIsInitialized) {
                dataTable.destroy();
            }
    
            await listMuestreo();
            dataTable = $('#datatables').DataTable(dataTableAction);
            dataTableIsInitialized = true;
        };
    
        window.addEventListener('load', async () => {
            await initDataTable();
        });