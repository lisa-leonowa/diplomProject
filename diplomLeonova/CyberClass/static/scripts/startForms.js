function startForms(){
    let change = document.getElementById("clientForm").getElementsByTagName(input); // получение формы с нужным id
    var index; // переменная счетчик
    let btnHidden = document.getElementById("btnHidden");
    for (index = 0; index < change.length; ++index) { // цикл, меняющий значение возможности редактировать
            if (change[index].hasAttribute("readonly")) {
                change[index].removeAttribute("readonly");
                btnHidden.removeAttribute("hidden"); }
            else { change[index].setAttribute("readonly", "readonly");
                    btnHidden.setAttribute("hidden", "hidden"); }
    }
}