let dataTable;
let dataTableIsInitialized = false;

const dataTableAction = {
    columnDefs: [
        { className: 'centered', targets: [0, 1, 2, 3, 4] },  // Ajusta según sea necesario
        { orderable: false, targets: [] },  // Desactiva la ordenación para ciertas columnas si es necesario
        { searchable: false, targets: [] },  // Desactiva la búsqueda para ciertas columnas si es necesario
    ],
    pageLength: 4,
    destroy: true
}

const initDataTable = async () => {
    if (dataTableIsInitialized) {
        dataTable.destroy();
    }

    // Elimina la siguiente línea si ya no necesitas listMuestreo
    // await listMuestreo();

    dataTable = $('#datatables').DataTable(dataTableAction);
    dataTableIsInitialized = true;
};

$(document).ready(async function () {
    await initDataTable();

    // Resto de tu código...
});

window.addEventListener('load', async () => {
    await initDataTable();
});

$(document).ready(function () {
    // Cuando se abre el modal, hacer una solicitud AJAX para obtener la información detallada del vuelo
    $('.modal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget); // Botón que activó el modal
        var id_vuelo = button.data('vuelo'); // Extraer el ID del vuelo del atributo data-vuelo del botón
        var modal = $(this); // Referencia al modal

        // Hacer la solicitud AJAX
        $.ajax({
            url: '/detalle_vuelo/' + id_vuelo + '/',
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                var modalBody = $('#modalBody');
                modalBody.empty(); // Limpiar el contenido anterior del modal
                modal.find('.modal-title').text('Detalles del Vuelo :' + id_vuelo); // Cambiar el título del modal
                modal.find('#vueloId').text(id_vuelo);
                modal.find('#cantidadImagenes').text('Aquí va la cantidad de imágenes');
            }
        });
    });
});

$(document).ready(function () {
    // Cuando se hace clic en el botón "Validar"
    $('#validateButton').click(function () {
        var id_vuelo = $('#vueloId').text(); // Obtener el ID del vuelo del primer modal

        // Hacer la solicitud AJAX
        $.ajax({
            url: '/predecir_imagenes/' + id_vuelo + '/',
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                // Aquí se mostrarán los resultados de la predicción
                var resultsList = $('<ul>');
                data.results.forEach(function (result) {
                    result.predictions.forEach(function (prediction) {
                        resultsList.append($('<li>').text(prediction.tagName + ': ' + prediction.probability));
                    });
                });
                $('#imagesModal' + id_vuelo).find('.modal-body').append(resultsList);
            }
        });
    });
});
