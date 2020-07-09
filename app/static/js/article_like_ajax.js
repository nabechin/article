/* 記事に乗っているいいねを押した時のajax通信
ajax通信が成功した際の処理を定義 */
$(function () {
  var afterSuccessLike = function ($notLikeElement, articleId) {
    return function (data) {
      $("#id_like_article_" + articleId).val(data["id"]);
      $notLikeElement.removeClass("not-like").addClass("already-like");
      $notLikeElement.children().css("color", "indianred");
      var nowLikeCount = $("#id_like_count_" + articleId).text();
      if (!nowLikeCount) {
        nowLikeCount = "0";
      }
      nowLikeCount = parseInt(nowLikeCount);
      afterLikeCount = nowLikeCount + 1;
      $("#id_like_count_" + articleId).text(afterLikeCount);
    };
  };

  /* 特定の記事のいいねを解除してajax通信した後の処理
      　　いいねボタンがグレー色に変わり、いいねカウントが１減算される */
  var afterSuccessNotLike = function ($alreadyLikeElement, articleId) {
    $alreadyLikeElement.children().css("color", "");
    $alreadyLikeElement.removeClass("already-like").addClass("not-like");
    var nowLikeCount = $("#id_like_count_" + articleId).text();
    nowLikeCount = parseInt(nowLikeCount);
    var afterLikeCount = nowLikeCount - 1;
    if (afterLikeCount == 0) {
      afterLikeCount = "";
    }
    $("#id_like_count_" + articleId).text(afterLikeCount);
  };

  /* 特定の記事にいいねをつけた時のアクション
      記事に対するいいねをajax通信でpostする */
  $(document).on("click", ".not-like", function (e) {
    e.stopPropagation();
    $(".article").off("click");
    var $notLikeElement = $(this);
    var articleId = $notLikeElement
      .next()
      .attr("id")
      .replace("id_like_article_", "");
    var data = new FormData();
    data.append("article", articleId);
    $.ajax({
      url: "http://localhost/api/favoriteArticle/",
      type: "POST",
      dataType: "json",
      data: data,
      success: afterSuccessLike($notLikeElement, articleId),
      processData: false,
      contentType: false,
    });
  });

  /* 記事いいねを解除した時のアクション
         記事に対するいいねをajax通信でdeleteする */
  $(document).on("click", ".already-like", function (e) {
    e.stopPropagation();
    var $alreadyLikeElement = $(this);
    var likeId = $alreadyLikeElement.next().val();
    var articleId = $alreadyLikeElement
      .next()
      .attr("id")
      .replace("id_like_article_", "");
    $.ajax({
      url: "http://localhost/api/favoriteArticle/" + likeId + "/",
      type: "DELETE",
      dataType: "json",
      success: afterSuccessNotLike($alreadyLikeElement, articleId),
      processData: false,
      contentType: false,
    });
  });
});
