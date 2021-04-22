

function hello() {
    eel.hello()
}

function getPojazdy() {
    resetProgress()
    setProgress(50)
    eel.getPojazdy()
}

eel.expose(updatePojazdy)
function updatePojazdy(data) {
    setProgress(100)
    Notify("Odświeżono Pojazdy!")
    document.getElementById("auta_lista_1").innerHTML = data
}


eel.expose(updatePojazdy2)
function updatePojazdy2(data) {
    setProgress(100)
    Notify("Wczytano Paczkę!")
    document.getElementById("auta_lista_1").innerHTML = data
    init_CarList()
}



function loadPack() {
    resetProgress()
    setProgress(50)
    eel.loadPack()
}

function init_CarList() {
    var close = document.querySelectorAll('[id=remove_car_button]');
    var i;
    for (i = 0; i < close.length; i++) {
        close[i].onclick = function() {
            var div = this.parentElement;
            var div = div.parentElement;
            confirmDialog()
            eel.delCar(this.value)
            div.style.display = "none";
        }
    }
}


function confirmDialog() {

}


function test() {
    console.log(this.parentElement)
}

async function addCar() {
    loadPack()
    resetProgress()
    var cars = await eel.getNewCars()();
    var dialog = document.querySelector('dialog');
    dialog.showModal();
    document.getElementById('dialog_select_car').innerHTML = cars;
}

function killDialog() {
    var dialog = document.querySelector('dialog');
    dialog.close();
}

function confirmSelection() {
    loadPack()
    var dialog = document.querySelector('dialog');
    dialog.close();
    var value = document.getElementById('dialog_select_car').value;
    eel.addCarToPack(value)
    loadPack()
}

function main_open_folder() {
    eel.open_folder('/pakowanko/input')
}

function edit_open_folder() {
    eel.open_folder('/pakowanko/pack_to_modify')
}

function input_edit_open_folder() {
    eel.open_folder('/pakowanko/modify_input')
}


function startPacking() {
    Notify("Rozpoczęto Pakowanie")
    resetProgress()
    eel.startPacking()
}

eel.expose(zamknij_program)
function zamknij_program() {
    window.close()
    console.log("exiting")
    eel.close()
}

function main_ui() {
    document.location.href = 'index.html';
}

function settings_ui() {
    document.location.href = 'settings_ui.html';
}

eel.expose(setProgress)
function setProgress(val) {
    var elem = document.getElementById("myBar");
    var curr_width = String(elem.style.width)
    curr_width = curr_width.slice(0, -1);
    curr_width = Number(curr_width)
    var width = curr_width;
    var i = val
    var id = setInterval(frame, 10);
    function frame() {
        if (width >= i) {
          clearInterval(id);
          i = 0;
        } else {
          width++;
          elem.style.width = width + "%";
        }
      }
}

eel.expose(Notify)
function Notify(text) {
    var notification = document.querySelector('.mdl-js-snackbar');
    var data = {
    message: text,
    timeout: 1000
    };
    notification.MaterialSnackbar.showSnackbar(data);
}

eel.expose(resetProgress)
function resetProgress() {
    var elem = document.getElementById("myBar");
    elem.style.width = 1 + "%";
}

window.setInterval(function() {
    var elem = document.getElementById('consoleOutput');
    elem.scrollBy({ 
        top: 50, // could be negative value
        left: 0, 
        behavior: 'smooth' 
    })
}, 100);

eel.expose(addToLog)
function addToLog(text) {
    var logBox = document.getElementById('consoleOutput');
    logBox.innerHTML += "<p>"+text+"</p>"
}