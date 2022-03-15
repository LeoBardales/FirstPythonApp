$(function () {
      
    $( window ).on( "load", function() { 
      acceso=$("#Acceso").val();

      if(acceso=='NO'){}
      else{
        $.ajax({
          type: "POST",
          url: "/Comprobar",
          data: $('form').serialize(),
          //data:datas,
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
    
  });