function isValidText (text) {
    if(text && text.trim && text.trim().length > 0){
        return true;
    }
    return false;
}

function isValidDateTime (date) {
    if(isValidText(date)){
        return dayjs(date).isValid();
    }
    return false;
}

function validateEmail(mail) {
    if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{1,3})+$/.test(mail)){
        return (true)
    }
    console.log(mail)
    return (false)
}

function isValidoAccount (event){
   console.log(document.getElementById("ruolo"))
    const account = {
        nome : document.getElementById("nome").value,
        cognome : document.getElementById("cognome").value,
        email : document.getElementById("email").value,
        ruolo : document.getElementById("ruolo").value,
        password1 : document.getElementById("password1").value,
        password2 : document.getElementById("password2").value,
    };
    if(!account){
        event.preventDefault();
        document.getElementById("message").innerHTML = "Compila il formulario";
        return;
    }
    if(!isValidText(account.cognome)){
        event.preventDefault()
        document.getElementById("message").innerHTML = "Inserisci il cognome";
        return;
    }
    if(!isValidText(account.nome)){
        event.preventDefault()
        document.getElementById("message").innerHTML = "Inserisci il nome";
    }
    if(!isValidText(account.ruolo)){
        event.preventDefault()
        document.getElementById("message").innerHTML = "Selecziona il ruolo";
        return;
    }
    if(!isValidText(account.email) || !validateEmail(account.email)){
        event.preventDefault()
        document.getElementById("message").innerHTML = "Inserisci email";
        return;
    }
    if(!isValidText(account.password1)){
        event.preventDefault()
        document.getElementById("message").innerHTML = "Inserisci password";
        return;
    }
    if(!isValidText(account.password2)){
        event.preventDefault()
        document.getElementById("message").innerHTML = "Manca confermare la password";
        return;
    }
    if(account.password1 != account.password2){
        event.preventDefault()
        document.getElementById("message").innerHTML = "Le password sono diverse";
        return;
    }
}

function isValidoCredential (event){
    const credential = {
        email : document.getElementById("email").value,
        password : document.getElementById("password").value,
    };
    if(!credential){
        event.preventDefault();
        document.getElementById("message").innerHTML = "Compila il formulario";
        return;
    }
    if(!isValidText(credential.email) || !validateEmail(credential.email)){
        event.preventDefault()
        document.getElementById("message").innerHTML = "Inserisci l email";
        return;
    }
    if(!isValidText(credential.password)){
        event.preventDefault()
        document.getElementById("message").innerHTML = "Inserisci la password";
        return;
    }
}

function getValutatione (voto){
    if(voto == 1){
       return
    }
}

function search(event, corsi){
    console.log(corsi)
    let value = document.getElementById("search").value;

}

function isValidoCorso (event){
    const corso = {
        titolo : document.getElementById("titolo").value,
        descrizione : document.getElementById("descrizione").value,
        istruttore : document.getElementById("istruttore").value,
        startTime : document.getElementById("startTime").value,
        endTime : document.getElementById("endTime").value,
    };
    if(!corso){
        event.preventDefault();
        document.getElementById("message").innerHTML = "Compila il formulario";
        return;
    }
    if(!isValidText(corso.titolo)){
        event.preventDefault()
        document.getElementById("message").innerHTML = "Inserisci il titolo";
        return;
    }
    if(!isValidText(corso.descrizione)){
        event.preventDefault()
        document.getElementById("message").innerHTML = "Inserisci la descrizione";
        return;
    }
    if(!isValidText(corso.istruttore)){
        event.preventDefault()
        document.getElementById("message").innerHTML = "Inserisci  l istruttore";
        return;
    }
    if(!isValidDateTime(corso.startTime)){
        event.preventDefault()
        document.getElementById("message").innerHTML = "Inserisci la data di inizio";
        return;
    }
    if(!isValidDateTime(corso.endTime)){
        event.preventDefault()
        document.getElementById("message").innerHTML = "Inserisci la data di fine";
        return;
    }
}
