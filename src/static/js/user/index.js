$(function () {

    $(window).on("load", function () {

        cargarTotalHoras()
        cargarMisActividades()

        return false;

    });

    $("form").on("submit", function (event) {
        var ano = $("#ano").val();

    if (mes == "0" || ano == "0") {
        } else {
            cargarTotalHoras()
            cargarMisActividades()
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

    function cargarTotalHoras(){
        $.ajax({
            type: "POST",
            url: "/Total_Horas",
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

    function cargarMisActividades(){
        $.ajax({
            type: "POST",
            url: "/Mis_Actividades",
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