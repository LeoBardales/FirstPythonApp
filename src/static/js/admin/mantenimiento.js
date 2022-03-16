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

  function password_show_hide() {
    var x = document.getElementById("password");
    var show_eye = document.getElementById("show_eye");
    var hide_eye = document.getElementById("hide_eye");
    hide_eye.classList.remove("d-none");
    if (x.type === "password") {
      x.type = "text";
      show_eye.style.display = "none";
      hide_eye.style.display = "block";
    } else {
      x.type = "password";
      show_eye.style.display = "block";
      hide_eye.style.display = "none";
    }
  }