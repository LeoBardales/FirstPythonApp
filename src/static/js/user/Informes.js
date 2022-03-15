$(function () {
    $(window).on("load", function () {
        llenarTabla()
      return false;
    });

    $("form").on("submit", function (event) {
        var ano = $("#ano").val();
        
        if (ano == "0") {
        } else {
            llenarTabla()
        }
        return false;
      });

    function llenarTabla()
    {
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
    }
  });