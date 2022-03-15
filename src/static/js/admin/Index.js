$(function () {
  $(window).on("load", function () {
    cargarNreclamos()
    cargarreclamos()
    LlenarTabla()
    
    return false;
  });


  $("form").on("submit", function (event) {
    var mes = $("#mes").val();
    var ano = $("#ano").val();

    if (mes == "0" || ano == "0") {
    } else {
      LlenarTabla()
    }
    return false;
  });
  

  $("#Fecha").change(function () {
    var cuenta = $("#Codigo").val();

    $.ajax({
      type: "POST",
      url: "/FiltroActividadesDia",
      data: $("form").serialize(),
      cache: false,
      beforeSend: function (html) {
        document.getElementById("insert_search").innerHTML = "";
      },
      success: function (html) {
        $("#insert_search").show();
        $("#insert_search").append(html.data);
      },
    });

    return false;
  });




  //cargar numero de reclamos
  function cargarNreclamos(){
    $.ajax({
      type: "POST",
      url: "/numero_reclamos",
      data: "json",
      cache: false,
      beforeSend: function (html) {
        document.getElementById("numero").innerHTML = "";
      },
      success: function (html) {
        $("#numero").show();
        $("#numero").append(html.data);
      },
    });


  }
   //cargar  reclamos
   function cargarreclamos(){
    $.ajax({
      type: "POST",
      url: "/bandeja_reclamos",
      data: $("form").serialize(),
      //data:datas,
      cache: false,
      beforeSend: function (html) {
        document.getElementById("bandeja_reclamos").innerHTML = "";
      },
      success: function (html) {
        $("#bandeja_reclamos").show();
        $("#bandeja_reclamos").append(html.data);
      },
    });

  }

   //Llenar Actividades 
   function LlenarTabla(){
    $.ajax({
      type: "POST",
      url: "/FiltroActividades",
      data: $("form").serialize(),
      cache: false,
      beforeSend: function (html) {
        document.getElementById("insert_search").innerHTML = "";
      },
      success: function (html) {
        $("#insert_search").show();
        $("#insert_search").append(html.data);
      },
    });

  }



});

function ConfirDelete(){

  if(confirm('Estas seguro que quieres eliminar actividad ?')){

    return true;
  }
  else{

    return false;
  }
  
}