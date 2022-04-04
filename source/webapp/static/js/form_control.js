async function formSubmit(e) {
    e.preventDefault();
    const form = document.getElementById('quote_create_form');
    console.log(form);
}

function initForm() {
    const form = document.getElementById('quote_create_form');
    form.addEventListener('submit', formSubmit)
}


window.addEventListener('load', function() {
    initForm();
});