$(function () {
    $(window).on("load", function () {
        cargarLista()
        return false;
      });


      function cargarLista(){
        $.ajax({
          type: "POST",
          url: "/TablaUsuarios",
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