document.addEventListener('DOMContentLoaded', function() {
    let sortSelect = document.getElementById('id_form_sorted');
    if (sortSelect) {
        sortSelect.addEventListener('change', function() {
            document.getElementById('sortForm').submit();
        });
    }
});