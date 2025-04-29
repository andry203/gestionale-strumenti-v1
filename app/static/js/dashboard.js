// dashboard.js

// Open form for adding new instrument

const btnApri = document.getElementById('btn-apri-aggiungi');
const modal   = document.getElementById('modal-aggiungi');
const btnChiudi = document.getElementById('btn-chiudi-aggiungi');

btnApri?.addEventListener('click', () => {
modal.style.display = 'flex';
});

btnChiudi?.addEventListener('click', () => {
modal.style.display = 'none';
});

// chiudi cliccando fuori dal contenuto
modal.addEventListener('click', e => {
if (e.target === modal) {
    modal.style.display = 'none';
}
});


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
    };
});

// --- MODALE DI MODIFICA ---
const modalMod = document.getElementById('modal-modifica');
const formMod = document.getElementById('form-modifica');
const btnChiudiMod = document.getElementById('btn-chiudi-modifica');

// Apri e popola
document.querySelectorAll('.btn-modifica').forEach(link => {
  link.addEventListener('click', e => {
    e.preventDefault();
    // Leggi i campi dal data-*
    const d = link.dataset;
    formMod.action = link.href;               // assegna URL POST
    formMod.tipo.value             = d.tipo;
    formMod.marca.value            = d.marca;
    formMod.modello.value          = d.modello;
    formMod.serial_number.value    = d.serial;
    formMod.caratteristiche.value  = d.caratteristiche || '';
    formMod.data_calibrazione.value= d.dataCalib || '';
    formMod.note.value             = d.note || '';
    // mostra il modal
    modalMod.style.display = 'flex';
  });
});

// Chiudi il modal
btnChiudiMod.addEventListener('click', () => {
  modalMod.style.display = 'none';
});
modalMod.addEventListener('click', e => {
  if (e.target === modalMod) modalMod.style.display = 'none';
});


// --- ELIMINA CON CONFIRM ---
document.querySelectorAll('.btn-elimina').forEach(link => {
  link.addEventListener('click', e => {
    e.preventDefault();
    const nome = link.dataset.nome;
    if (confirm(`Sei sicuro di voler eliminare lo strumento "${nome}"?`)) {
      // creiamo un form POST “al volo” perché <a> non invia metodi POST
      const f = document.createElement('form');
      f.method = 'post';
      f.action = link.href;
      document.body.appendChild(f);
      f.submit();
    }
  });
});


document.addEventListener('DOMContentLoaded', () => {
    // 1) Riordino righe: “in attesa” in cima, poi per data decrescente
    const table = document.getElementById('richieste-table');
    const tbody = table.querySelector('tbody');
    const rows  = Array.from(tbody.querySelectorAll('tr'));
  
    rows.sort((a, b) => {
      const statusA = a.cells[5].textContent.trim();
      const statusB = b.cells[5].textContent.trim();
      if (statusA === 'in attesa' && statusB !== 'in attesa') return -1;
      if (statusA !== 'in attesa' && statusB === 'in attesa') return 1;
      // ordino per data (colonna 4) decrescente
      const parseDate = txt => {
        const [d,m,y] = txt.split('/');
        return new Date(`${y}-${m}-${d}`);
      };
      const dateA = parseDate(a.cells[4].textContent.trim());
      const dateB = parseDate(b.cells[4].textContent.trim());
      return dateB - dateA;
    });
    rows.forEach(r => tbody.appendChild(r));
  
    // 2) Apertura modal “Modifica Stato”
    const modal    = document.getElementById('modal-stato');
    const form     = document.getElementById('form-stato');
    const infoP    = document.getElementById('info-richiesta');
    const btnClose = document.getElementById('btn-close-stato');
  
    document.querySelectorAll('.btn-cambia-stato').forEach(btn => {
      btn.addEventListener('click', () => {
        // imposto action del form
        form.action = btn.dataset.url;
        infoP.textContent = `Richiesta #${btn.dataset.id} → ${btn.dataset.strumento}`;
        form.status.value = '';
        modal.style.display = 'flex';
      });
    });
  
    // 3) Chiusura modal
    btnClose.addEventListener('click', () => modal.style.display = 'none');
    modal.addEventListener('click', e => {
      if (e.target === modal) modal.style.display = 'none';
    });
  });
  

document.getElementById('email-search')
  .addEventListener('input', function() {
    const filtro = this.value.toLowerCase();
    const sel = document.getElementById('email-utente');
    Array.from(sel.options).forEach(opt => {
      opt.style.display = opt.value.toLowerCase().includes(filtro)
                        ? '' : 'none';
    });
});