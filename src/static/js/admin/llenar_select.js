$(function () {
  $(window).on("load", function () {
    datas = "";
    var Beca = $("#Beca").val();
    var Carrera = $("#Carrera").val();
    $.ajax({
      type: "POST",
      url: "/llenar_becas",
      //data: $('form').serialize(),
      data: datas,
      cache: false,
      beforeSend: function (html) {
        document.getElementById("Beca").innerHTML = "";
      },
      success: function (html) {
        $("#Beca").show();
        $("#Beca").append(html.data);
        $('#Beca option[value="'+Beca+'"]').prop('selected', true);
      },
    });
    $.ajax({
      type: "POST",

      url: "/llenar_carreras",
      //data: $('form').serialize(),
      data: datas,
      cache: false,
      beforeSend: function (html) {
        document.getElementById("Carrera").innerHTML = "";
      },
      success: function (html) {
        $("#Carrera").show();
        $("#Carrera").append(html.data);
        $('#Carrera option[value="'+Carrera+'"]').prop('selected', true);
      },
    });

    $.ajax({
      type: "POST",
      url: "/tabla_informes",
      data: $('form').serialize(),
      //data: datas,
      cache: false,
      beforeSend: function (html) {
        document.getElementById("informes").innerHTML = "";
      },
      success: function (html) {
        $("#informes").show();
        $("#informes").append(html.data);
      },
    });

    return false;
  });



  $("#ano1").change(function () {

    $.ajax({
      type: "POST",
      url: "/tabla_informes",
      data: $("form").serialize(),
      cache: false,
      beforeSend: function (html) {
        document.getElementById("informes").innerHTML = "";
      },
      success: function (html) {
        $("#informes").show();
        $("#informes").append(html.data);
      },
    });

    return false;
  });



});

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