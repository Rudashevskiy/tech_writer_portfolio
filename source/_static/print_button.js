document.addEventListener('DOMContentLoaded', function () {
    const printButton = document.getElementById('print-button');
    printButton.addEventListener('click', function () {
        window.print();
    });
});