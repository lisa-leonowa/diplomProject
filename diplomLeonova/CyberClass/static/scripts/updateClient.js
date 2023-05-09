function changeClick(my_id, updateButton, BtnHidden){

    let change = document.getElementById(my_id).getElementsByTagName("input"); // получение формы с нужным id
    let btn = document.getElementById(updateButton); // получение кнопки с нужным id

    var index; // переменная счетчик
    let btnHidden = document.getElementById(BtnHidden);

    for (index = 0; index < 5; ++index) { // цикл, меняющий значение возможности редактировать
        if (change[index].hasAttribute("readonly")) {
            change[index].removeAttribute("readonly");
            btnHidden.removeAttribute("hidden"); }
        else { change[index].setAttribute("readonly", "readonly");
               btnHidden.setAttribute("hidden", "hidden"); }
    }
}