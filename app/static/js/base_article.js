$(function () {
    /* 記事に付随するプロフィール画像にカーソルが当たると矢印から指マークに変わる
    　　　写真の明るさが暗くなる　*/
    $('.article-profile-image').hover(function () {
        $(this).css('cursor', 'pointer');
        $(this).css('opacity', '0.7');
    });

    /* 記事に付随するプロフィール画像にカーソルから外れると
    　　　写真の明るさがデフォルトに戻る　*/
    $('.article-profile-image').mouseout(function () {
        $(this).css('opacity', '1');
    });

    /* 記事ににカーソルが当たると矢印から指マークに変わる
    記事の背景色がグレーに変わる */
    $('.article').hover(function () {
        $(this).css('cursor', 'pointer');
    });

    // 記事にマウスが乗ると、背景色がグレーに変わる
    $('.article').on('mouseover', function () {
        $(this).css('background-color', '#f4f4f5');
    });

    // 記事からマウスが離れると、背景色が元のカラーに変わる
    $('.article').on('mouseout', function () {
        $(this).css('background-color', '');
    });

});