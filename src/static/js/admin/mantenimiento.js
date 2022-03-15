$(function () {
    $(window).on("load", function () {
        llenarcarreras()
        llenarbecas()
      return false;
    });

    function llenarcarreras(){
        $.ajax({
            type: "POST",
      
            url: "/llenar_carreras",
            data: "json",
            cache: false,
            beforeSend: function (html) {
              document.getElementById("Carrera").innerHTML = "";
            },
            success: function (html) {
              $("#Carrera").show();
              $("#Carrera").append(html.data);
            },
          });
    }

    function llenarbecas(){
        $.ajax({
            type: "POST",
            url: "/llenar_becas",
            data: "json",
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
    }


  });