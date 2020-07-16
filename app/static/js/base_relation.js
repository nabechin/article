$(function () {

    $('.relation-profile-image').hover(function () {
        $(this).css('cursor', 'pointer');
        $(this).css('opacity', '0.7');
    });

    /* 記事に付随するプロフィール画像にカーソルから外れると
    　　　写真の明るさがデフォルトに戻る　*/
    $('.relation-profile-image').mouseout(function () {
        $(this).css('opacity', '1');
    });

    /* フォローのリクエストをajax通信でpostした後の処理
          「フォローする」-> 「フォロー中」にボタンを変更
        　後にフォロー解除ができるように、relationIdを埋め込む */
    var afterSuccessFollow = function ($unfollowButtonElement, target) {
        return function (data) {
            $unfollowButtonElement.text('フォロー中')
            $unfollowButtonElement.removeClass('un-follow').addClass('already-follow')
            $unfollowButtonElement.removeClass('btn-outline-primary').addClass('bg-gradient-primary')
            relationId = data['id']
            if (relationId) {
                $('#' + target).val(data['id']);
            }
        }
    };

    /* フォロー解除をdeleteメソッドでリクエストをした後の処理
       「フォロー中」-> 「フォローする」にボタンを変更 */
    var afterSuccessUnfollow = function ($alreadyfollowButtonElement, target) {
        $alreadyfollowButtonElement.text('フォローする')
        $alreadyfollowButtonElement.removeClass('already-follow').addClass('un-follow')
        $alreadyfollowButtonElement.removeClass('bg-gradient-primary').addClass('btn-outline-primary')
    };

    /* 「フォローする」ボタンを押した後の処理
        フォローのリクエストをajax通信でpostする処理 */
    $('body').on('click', '.un-follow', function (e) {
        e.stopPropagation();
        var $unfollowButtonElement = $(this)
        var target = $unfollowButtonElement.next().attr('id');
        var data = new FormData();
        data.append('target', target);
        $.ajax({
            url: '/api/relation/',
            type: 'POST',
            dataType: 'json',
            data: data,
            success: afterSuccessFollow($unfollowButtonElement, target),
            processData: false,
            contentType: false,
        })
    });

    /* 「フォロー」タンを押した後の処理
       フォロー解除をdeleteメソッドでリクエストする */
    $('body').on('click', '.already-follow', function (e) {
        e.stopPropagation();
        var $alreadyfollowButtonElement = $(this)
        var target = $alreadyfollowButtonElement.next().val();
        $.ajax({
            url: '/api/relation/' + target + '/',
            type: 'DELETE',
            success: afterSuccessUnfollow($alreadyfollowButtonElement),
            processData: false,
            contentType: false,
        })
    });


});