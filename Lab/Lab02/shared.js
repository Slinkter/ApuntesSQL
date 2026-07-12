document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.btn-reveal').forEach(function(btn) {
        btn.addEventListener('click', function() {
            var answer = this.nextElementSibling;
            if (answer && answer.classList.contains('answer')) {
                answer.classList.toggle('visible');
                this.textContent = answer.classList.contains('visible') ? 'Ocultar respuesta' : 'Ver respuesta';
            }
        });
    });
    if (typeof hljs !== 'undefined') hljs.highlightAll();
});
