document.addEventListener('DOMContentLoaded', function () {
    const exportButton = document.getElementById('export-pdf');

    exportButton.addEventListener('click', function () {
        // Создаем новый экземпляр jsPDF
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF();

        // Преобразуем HTML-страницу в PDF
        doc.html(document.body, {
            callback: function (doc) {
                doc.save('резюме.pdf');
            },
            x: 10,
            y: 10,
            width: 190, // Ширина контента в PDF
            windowWidthRatio: 1 // Соотношение ширины окна браузера к ширине PDF
        });
    });
});