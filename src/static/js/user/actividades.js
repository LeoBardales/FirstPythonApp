$(function () {
      
    $(window).on( "load", function() { 
      cargarActividades()
      return false;
    
    });
   /* window.setInterval(function(){
      cargarActividades()
  },1000)*/

    function cargarActividades(){
      $.ajax({
        type: "POST",
        url: "/LlenarActividades",
        data:"json",
        cache: true,
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