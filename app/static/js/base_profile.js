$(function () {
    /* プロフィールの画像編集 */
    // 背景画像クリック後、画像選択 
    $('#id_background_img').on('click', function () {
        $('#id_background_img_file').trigger('click');
    });
    // 背景画像にカーソルが当たると矢印から指マークに変わる
    $('#id_background_img').hover(function () {
        $(this).css('cursor', 'pointer');
    });
    //プロフィール画面クリック後、画像選択
    $('#id_profile_img').on('click', function () {
        $('#id_profile_img_file').trigger('click');
    });
    // プロフィール画像にカーソルが当たると矢印から指マークに変わる
    $('#id_profile_img').hover(function () {
        $(this).css('cursor', 'pointer');
    });
    // 選択したプロフィール画像をimgに貼り付ける 
    $('#id_profile_img_file').on('change', function (e) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#id_profile_img').attr('src', e.target.result)
        }
        reader.readAsDataURL(e.target.files[0]);
    })
    // 選択した背景画像をimgに貼り付ける 
    $('#id_background_img_file').on('change', function (e) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#id_background_img').attr('src', e.target.result)
        }
        reader.readAsDataURL(e.target.files[0]);
    })
    /* プロフィールの画像編集 */


    /* 名前の文字カウント */
    $('#id_name_text').on('keyup', countNameLength);

    function countNameLength() {
        var nameAmount = $('#id_name_text').val().length;
        $('#id_name_count').text(nameAmount);
    }
    /* 自己紹介の文字カウント */
    $('#id_introduction_text').on('keyup', countIntroductionLength);

    function countIntroductionLength() {
        var introductionAmount = $('#id_introduction_text').val().length;
        $('#id_introduction_count').text(introductionAmount);
    }
});

//ajax通信と通信成功後の処理をready関数で分離した
$(function () {
    //ログインユーザのプロフィール画像を取得後、プロフィール編集フォームに表示する
    var afterSuccessGetProfile = function (data) {
        var introduction = data['0']['introduction'];
        var name = data['0']['user']['name']
        var profile_image = data['0']['profile_image']
        var background_image = data['0']['background_image']
        $('#id_introduction_count').text(introduction.length);
        $('#id_introduction_text').val(introduction);
        $('#id_name_count').text(name.length);
        $('#id_name_text').val(name);
        $('#id_profile_img').attr('src', profile_image)
        $('#id_background_img').attr('src', background_image)

    }

    //　ログインユーザのプロフィールを取得するためのajax通信
    $('#id_user_profile').on('click', function () {
        $.ajax({
            url: '/api/user_profile/',
            type: 'GET',
            success: afterSuccessGetProfile,
            processData: false,
            contentType: false,
        });
    })
    var afterSuccessUnfollow = function () {
        $('#id_already_follow').hide()
        $('#id_follow').show()
        $('#modal-action-unfollow').modal('hide')
        var numberOfFollower = parseInt($('#id_number-of_follower').text())
        $('#id_number-of_follower').text(numberOfFollower - 1)
    };
    $('#id_unrelate_button').on('click', function () {
        var relationId = $("#id_relation_id_port").val()
        $.ajax({
            url: '/api/relation/' + relationId + '/',
            type: 'DELETE',
            success: afterSuccessUnfollow,
            processData: false,
            contentType: false,
        })
    });
});