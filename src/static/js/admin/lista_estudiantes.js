$(function () {

    $(window).on("load", function () {
      cargarLista()
      return false;
    });
    $('#Buscar').click(function () {

      var Busqueda = $("#Busqueda").val();
      if (Busqueda == '') {
      } else {
        $.ajax({
          type: "POST",
          url: "/Busqueda_Estudiante",
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
      return false;
    });

    //llenar lista de estudiantes
    function cargarLista(){
      $.ajax({
        type: "POST",
        url: "/TablaEstudiantes",
        data: "json",
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

  });