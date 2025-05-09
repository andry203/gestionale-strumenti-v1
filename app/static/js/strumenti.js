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

  // 2) prompt per “Richiedi”
  const modal     = document.getElementById('modal-richiesta');
  const form      = document.getElementById('form-richiesta');
  const titoloEl  = document.getElementById('richiestaTitolo');
  const btnChiudi = document.getElementById('btn-chiudi-richiesta');

  document.querySelectorAll('.btn-richiedi').forEach(btn => {
    btn.addEventListener('click', e => {
      e.preventDefault();
      const url  = btn.getAttribute('data-url');
      const nome = btn.getAttribute('data-nome');

      form.setAttribute('action', url);
      titoloEl.textContent = `Richiedi: ${nome}`;
      form.reset();

      modal.style.display = 'flex';
    });
  });

  btnChiudi.addEventListener('click', () => {
    modal.style.display = 'none';
  });

  // chiudi cliccando fuori dal contenuto
  modal.addEventListener('click', e => {
    if (e.target === modal) {
      modal.style.display = 'none';
    }
  });
});
