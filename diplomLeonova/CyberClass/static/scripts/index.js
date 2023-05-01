document.querySelectorAll('.trigger').forEach((element) => {
    element.addEventListener("click", (e) => {
        const parent = e.target.parentNode.parentNode;
        const content = parent.querySelector('.content');

        content.classList.toggle('contentActive');
    });
 });