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
        

class RelationDto:
    def __init__(self,relation_profile,is_follow,relation):
        self.relation_profile = relation_profile
        self.is_follow = is_follow
        self.relation = relation