$(function () {

    $(window).on("load", function () {

        cargarMiReclamos()

        return false;

    });


    function cargarMiReclamos(){
        $.ajax({
            type: "POST",
            url: "/Llenar_Reclamos",
            data: "json",
            cache: false,
            beforeSend: function (html) {
                document.getElementById("reclamos").innerHTML = '';

            },
            success: function (html) {
                $("#reclamos").show();
                $("#reclamos").append(html.data);
            }
        });
      }




});