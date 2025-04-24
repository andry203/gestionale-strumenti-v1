// strumenti.js

document.addEventListener('DOMContentLoaded', () => {
    // 1) filtro client‐side
    const searchInput = document.getElementById('search');
    if (searchInput) {
      searchInput.addEventListener('keyup', function() {
        const filter = this.value.toLowerCase();
        document.querySelectorAll('#strumenti-table tbody tr')
          .forEach(row => {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(filter) ? '' : 'none';
          });
      });
    }
  
    // 2) prompt note per “Richiedi”
    document.querySelectorAll('.btn-richiedi').forEach(btn => {
      btn.addEventListener('click', function() {
        const form = this.closest('.richiedi-form');
        const nome = form.dataset.nome;
        const note = prompt(
          `Stai richiedendo lo strumento:\n\n  ${nome}\n\nVuoi aggiungere eventuali note?`, ''
        );
        if (note !== null) {
          form.querySelector('input[name="note"]').value = note.trim();
          form.submit();
        }
      });
    });
  });
  