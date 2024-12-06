$('.detail_description').each(function() {
    var $pTag = $(this).find('p');
    if($pTag.text().length > 200){
        var shortText = $pTag.text();
        shortText = shortText.substring(0, 200);
        $pTag.addClass('fullArticle').hide();
        shortText += '<a href="#" class="read-more-link">Show more text ></a>';
        $pTag.append('<a href="#" class="read-less-link">&lt; Show less text</a>');
        $(this).append('<p class="preview">'+shortText+'</p>');
    }
});

$(document).on('click', '.read-more-link', function () {
    $(this).parent().hide().prev().show();
});

$(document).on('click', '.read-less-link', function () {
    $(this).parent().hide().next().show();
});



// const openModalBtn = document.getElementById("openModal");
// const modal = document.getElementById("modal");
// const closeModalBtn = document.getElementById("closeModal");
//
// openModalBtn.addEventListener("click", function(e) {
//   e.preventDefault(); // Предотвращает переход по ссылке
//   modal.style.display = "block";
// });
//
// closeModalBtn.addEventListener("click", function() {
//   modal.style.display = "none";
// });
//
// window.addEventListener("click", function(e) {
//   if (e.target == modal) {
//     modal.style.display = "none";
//   }
// });