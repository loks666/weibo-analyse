import pandas as pd
from sqlalchemy import create_engine

from spiderComments import start as commentsStart
from spiderContent import start as contentStart

engine = create_engine('mysql+pymysql://root:root@127.0.0.1/weiboarticle?charset=utf8mb4')


def save_to_sql():
    try:
        articleOldPd = pd.read_sql('select * from article', engine)
        articleNewPd = pd.read_csv('./articleData.csv')
        concatPd = pd.concat([articleNewPd, articleOldPd], join='inner')
        concatPd = concatPd.drop_duplicates(subset='id', keep='last')
        concatPd.to_sql('article', con=engine, if_exists='replace', index=False)

        commentOldPd = pd.read_sql('select * from comments', engine)
        commentNewPd = pd.read_csv('./commentsData.csv')
        concatCommentPd = pd.concat([commentNewPd, commentOldPd], join='inner')
        concatCommentPd = concatCommentPd.drop_duplicates(subset='content', keep='last')
        concatCommentPd.to_sql('comments', con=engine, if_exists='append', index=False)
        # concatCommentPd.to_sql('comments', con=engine, if_exists='replace', index=False)



    except:
        articleNewPd = pd.read_csv('./articleData.csv')
        commentNewPd = pd.read_csv('./commentsData.csv')
        articleNewPd.to_sql('article', con=engine, if_exists='replace', index=False)
        commentNewPd.to_sql('comments', con=engine, if_exists='append', index=False)
        # commentNewPd.to_sql('comments', con=engine, if_exists='replace', index=False)

    # os.remove('./articleData.csv')
    # os.remove('./commentsData.csv')
    print('数据存储完成！')


def main():
    print('正在爬取文章内容...')
    contentStart(10, 10)  # 爬取的标签及页数

    print('正在爬取评论内容...')
    commentsStart()
    print('爬取完毕正在存储中...')
    save_to_sql()


if __name__ == '__main__':
    main()
