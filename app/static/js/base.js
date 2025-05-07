// base.js

// for flash messages

document.addEventListener('DOMContentLoaded', function() {
    const flashContainer = document.getElementById('flashes');
    if (!flashContainer) return;
    // Dopo 3 secondi fai scomparire gradualmente
    setTimeout(() => {
      // puoi fare direttamente display:none oppure una dissolvenza via JS/CSS
      flashContainer.style.transition = 'opacity 0.5s ease';
      flashContainer.style.opacity = '0';
      // dopo la dissolvenza, rimuovi il contenitore per non occupare spazio
      setTimeout(() => flashContainer.remove(), 500);
    }, 3000);
  });


// for the recovery password process

document.addEventListener('DOMContentLoaded', function() {
    const btn = document.getElementById('btn-pass-recover');
    if (!btn) return;
  
    btn.addEventListener('click', async function(e) {
      e.preventDefault();
  
      const url = btn.dataset.recoveryUrl;  
      // Step 1: chiedi l'email
      const email = prompt("Inserisci la tua email:");
      if (!email) return;
  
      try {
        // Step 2: richiedi la domanda
        let res = await fetch(url, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email })
        });
        const data1 = await res.json();
        if (!res.ok) throw data1;
        
        // Step 3: chiedi la risposta alla domanda
        const answer = prompt(data1.question);
        if (answer === null) return;
  
        res = await fetch(url, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, answer })
        });
        const data2 = await res.json();
        if (!res.ok) throw data2;
  
        // Step 4: chiedi la nuova password
        if (data2.request_new_password) {
          const newPwd = prompt("Risposta corretta! Inserisci la nuova password:");
          if (!newPwd) return;
  
          res = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, answer, new_password: newPwd })
          });
          const data3 = await res.json();
          if (!res.ok) throw data3;
        }
  
        alert("Password aggiornata con successo!");
        window.location.href = btn.dataset.loginUrl || "/login";
  
      } catch(err) {
        console.error("Recovery Error:", err);
        alert(err.error || "Si è verificato un errore, riprova.");
      }
    });
  });