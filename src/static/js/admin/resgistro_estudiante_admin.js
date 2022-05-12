$(function () {
  $(window).on("load", function () {
    $.ajax({
      type: "POST",
      url: "/Tabla_Horas",
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

    $.ajax({
      type: "POST",
      url: "/Total_Horas",
      data: $("form").serialize(),
      cache: false,
      beforeSend: function (html) {
        document.getElementById("insert_Horas").innerHTML = "";
      },
      success: function (html) {
        $("#insert_Horas").show();
        $("#insert_Horas").append(html.data);
      },
    });

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

  $("#ano1").change(function () {
    var ano = $("#ano1").val();

    if(ano == 0){

    }else{
      Filtrarano()
      cargarTotalHorasAno()
    }

    return false;
  });

  function LlenarTabla(){
    $.ajax({
      type: "POST",
      url: "/Tabla_Horas",
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

    $.ajax({
      type: "POST",
      url: "/Total_Horas",
      data: $("form").serialize(),
      cache: false,
      beforeSend: function (html) {
        document.getElementById("insert_Horas").innerHTML = "";
      },
      success: function (html) {
        $("#insert_Horas").show();
        $("#insert_Horas").append(html.data);
      },
    });

  }

//Filtrar ano
function Filtrarano(){
  $.ajax({
      type: "POST",
      url: "/FiltroAno",
      data: $('form').serialize(),
      cache: false,
      beforeSend: function (html) {
          document.getElementById("insert_search").innerHTML = '';

      },
      success: function (html) {
          $("#insert_search").show();
          $("#insert_search").append(html.data);
      }
  });
}

//filtrar horas ano
function cargarTotalHorasAno(){
  $.ajax({
      type: "POST",
      url: "/Total_Horas_Ano",
      data: $('form').serialize(),
      cache: false,
      beforeSend: function (html) {
          document.getElementById("insert_Horas").innerHTML = '';

      },
      success: function (html) {
          $("#insert_Horas").show();
          $("#insert_Horas").append(html.data);
      }
  });

}





});
