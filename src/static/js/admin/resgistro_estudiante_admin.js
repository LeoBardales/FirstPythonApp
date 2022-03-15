$(function () {
  $(window).on("load", function () {
    $.ajax({
      type: "POST",
      url: "/Tabla_Horas",
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

    $.ajax({
      type: "POST",
      url: "/Total_Horas",
      data: $("form").serialize(),
      cache: false,
      beforeSend: function (html) {
        document.getElementById("insert_Horas").innerHTML = "";
      },
      success: function (html) {
        $("#insert_Horas").show();
        $("#insert_Horas").append(html.data);
      },
    });

    return false;
  });

  $("#FiltrarMes").click(function () {
    $.ajax({
      type: "POST",
      url: "/Tabla_Horas",
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

    $.ajax({
      type: "POST",
      url: "/Total_Horas",
      data: $("form").serialize(),
      cache: false,
      beforeSend: function (html) {
        document.getElementById("insert_Horas").innerHTML = "";
      },
      success: function (html) {
        $("#insert_Horas").show();
        $("#insert_Horas").append(html.data);
      },
    });

    return false;
  });
});
