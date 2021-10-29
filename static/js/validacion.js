function validar_formulario() {
    var user = document.formRegistro.user;
    var pwd = document.formRegistro.pwd;
  
    var username_len = user.value.length;
    if (username_len == 0 || username_len < 4) {
      alert("Debes ingresar un username con min. 8 caracteres");
      username.focus();
      return false; //Para la parte dos, que los datos se conserven
    }
  
    var passid_len = pwd.value.length;
    if (passid_len == 0 || passid_len < 4) {
      alert("Debes ingresar una password con mas de 8 caracteres");
      passid.focus();
    }
}
  
  