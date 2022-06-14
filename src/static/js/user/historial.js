$(function () {
    $(window).on("load", function () {
      LlenarTabla()
      
      return false;
    });
  
  
    $("form").on("submit", function (event) {
      var mes = $("#mes").val();
      var ano = $("#ano").val();
  
      if (mes == "0" || ano == "0") {
      } else {
        LlenarTabla()
      }
      return false;
    });
    
  
  
    //Filtrar por dia
    $("#Fecha").change(function () {
      var cuenta = $("#Codigo").val();
  
      $.ajax({
        type: "POST",
        url: "/FiltroActividadesDia",
        data: $("form").serialize(),
        cache: false,
        beforeSend: function (html) {
          document.getElementById("insert_search").innerHTML = "";
        },
        success: function (html) {
          $("#insert_search").show();
          $("#insert_search").append(html.data);
        },
      });
  
      return false;
    });
  
    //Filtrar por ano
    $("#ano1").change(function () {
      var ano = $("#ano1").val();
  
      if(ano == 0){
  
      }else{
        $.ajax({
          type: "POST",
          url: "/FiltroActividadesAno",
          data: $("form").serialize(),
          cache: false,
          beforeSend: function (html) {
            document.getElementById("insert_search").innerHTML = "";
          },
          success: function (html) {
            $("#insert_search").show();
            $("#insert_search").append(html.data);
          },
        });
      }
  
      return false;
    });
  
    
  
     //Llenar Actividades 
     function LlenarTabla(){
      $.ajax({
        type: "POST",
        url: "/FiltroActividades",
        data: $("form").serialize(),
        cache: false,
        beforeSend: function (html) {
          document.getElementById("insert_search").innerHTML = "";
        },
        success: function (html) {
          $("#insert_search").show();
          $("#insert_search").append(html.data);
        },
      });
  
    }
});