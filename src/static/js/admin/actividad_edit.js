$(function () {
  $(window).on("load", function () {
    var cuenta = $("#Codigo").val();
    datas = "idActividad=" + cuenta;
    if (cuenta == "") {
    } else {
      $.ajax({
        type: "POST",
        url: "/Tabla",
        data: datas,
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

  $("#Actualizar").click(function () {
    $.ajax({
      type: "POST",
      url: "/Actualizar_Registro",
      data: $("form").serialize(),
      cache: false,
      beforeSend: function (html) {
        document.getElementById("msg").innerHTML = "";
      },
      success: function (html) {
        $("#msg").show();
        $("#msg").append(html.data);
      },
    });

    return false;
  });

  $("#agregar").click(function () {
    var cuenta = $("#Cuenta").val();
    if (cuenta == "") {
    } else {
      $.ajax({
        type: "POST",
        url: "/add_cuenta",
        data: $("form").serialize(),
        cache: false,
        beforeSend: function (html) {
          document.getElementById("insert_search").innerHTML = "";
        },
        success: function (html) {
          $("#insert_search").show();
          $("#insert_search").append(html.data);
          // location.reload();
        },
      });
    }
    return false;
  });


});

function ConfirDelete(){

  if(confirm('Estas seguro que quieres eliminar esta cuenta ?')){

    return true;
  }
  else{

    return false;
  }
  
}
