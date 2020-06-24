/* 記事データのinsert */
insert into 
article_article(content,user_id)
values
('content1',1),
('content2',1),
('content3',1),
('content4',2),
('content5',2),
('content6',2),
('content7',6),
('content7',6),
('content7',6);


/* コメントデータのinsert */
insert into 
article_comment(content,article_id)
values
('comment1',1),
('comment2',1),
('comment3',1),
('comment4',2),
('comment5',2),
('comment6',2);
('comment7',6),
('comment8',6),
('comment9',6),
('comment10',2),
('comment11',2),
('comment12',2);


/* コメントデータのinsert */
insert into 
article_comment(content,article_id,user_id)
values('user47のコメント',12,47)
,('user48のコメント',12,48);

/* フォロー、アンフォロー関係データinsert */
insert into account_relation(follower_id,target_id)values(47,49);