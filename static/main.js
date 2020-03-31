const inputFile = document.querySelector('input');

inputFile.addEventListener('change', changeLabelText);

function changeLabelText(e) {
    document.getElementById('fileText').textContent = e.target.files[0].name;
}
