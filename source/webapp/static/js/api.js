var text = document.querySelector('.text');
var created_at = document.querySelector('created_at');
var rating = document.querySelector('.rating');

fetch(document)
    .then(response => response.json())
    .then(data => {
        var textValue = data['text'];
        var created_atValue = data['created_at'];
        var ratingValue = data['rating'];

        text.innerHTML = textValue;
        created_at.innerHTML = "Added: "+created_atValue;
        rating.innerHTML = ratingValue;
    })