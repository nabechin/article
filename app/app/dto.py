class CustomComment:
    def __init__(self,comment):
        self.comment = comment
    
    def is_login_user_like_comment(self,login_user_id):
        self.is_login_user_like_comment = False
        for favorite_comment in self.comment.favorite_comment.all():
            if favorite_comment.user.id == login_user_id:
                self.is_login_user_like_comment = True
                self.login_user_favorite_comment_id = favorite_comment.id
                break


class CustomArticle:
    def __init__(self,article):
        self.article = article

    def is_login_user_like(self,login_user_id):
        self.is_login_user_like = False
        for favorite_article in self.article.favorite_article.all():
            if favorite_article.user.id == login_user_id:
                self.is_login_user_like = True
                self.login_user_favorite_article_id = favorite_article.id
                break

    def is_login_user_like_comment(self,login_user_id):
        comment_list = []
        for comment in self.article.comment.all():
            custom_comment = CustomComment(comment)
            custom_comment.is_login_user_like_comment(login_user_id)
            comment_list.append(custom_comment)
        self.comment_list = comment_list


class RelationDto:
    def __init__(self,relation_profile,is_follow,relation):
        self.relation_profile = relation_profile
        self.is_follow = is_follow
        self.relation = relation