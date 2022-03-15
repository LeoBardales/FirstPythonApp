$(function () {

    $(window).on("load", function () {

        cargarTotalHoras()
        cargarMisActividades()

        return false;

    });

    $("form").on("submit", function (event) {
        var mes = $("#mes").val();
    
        if (mes == "0") {
        } else {
            cargarTotalHoras()
            cargarMisActividades()
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








});