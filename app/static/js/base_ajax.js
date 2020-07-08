$(function () {
  var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();
  // httpメソッドがリソースの読み出し->true リソースの編集->false
  function csrfSafeMethod(method) {
    // 下記HTTPメソッドはリソース変更しないため、CSRFTokenをヘッダに埋め込まない
    return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
  }

  // ajax通信の前にリソースを更新するメソッドであればCSRFTOKENをヘッダに埋め込む
  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    },
  });
});
