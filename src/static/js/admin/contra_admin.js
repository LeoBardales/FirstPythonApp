function CambiarContra(){
    const  NC = document.getElementById('NC');
    const  RNC = document.getElementById('RNC');
    
    
    if(NC.value == RNC.value){
      return true;
    }
    else{
      alert('Las Contraseñas no coindiden')
      return false;
    }
    
  }
