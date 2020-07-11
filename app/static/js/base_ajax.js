$(function () {
  function getCookieArray() {
    var arr = new Array();
    if (document.cookie != '') {
      var tmp = document.cookie.split('; ');
      for (var i = 0; i < tmp.length; i++) {
        var data = tmp[i].split('=');
        arr[data[0]] = decodeURIComponent(data[1]);
      }
    }
    return arr;
  }
  // ajax通信の前にリソースを更新するメソッドであればCSRFTOKENをヘッダに埋め込む
  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
      var arr = getCookieArray()
      var token = arr["token"];
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
      xhr.setRequestHeader("Authorization", "Token " + token);
    },
  });
});