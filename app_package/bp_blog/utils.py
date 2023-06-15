# import pandas as pd
import os
from flask import current_app
from dd07_models import sess_users, Users, BlogPosts

def create_blog_posts_list(number_of_posts_to_return=False):
    #Blog
    blog_posts = sess_users.query(BlogPosts).all()

    blog_posts_list =[]
    for post in blog_posts:
        if post.date_published in ["", None]:
            post_date = post.time_stamp_utc.strftime("%Y-%m-%d")
        else:
            post_date = post.date_published.strftime("%Y-%m-%d")
        post_title = post.title
        post_description = post.description
        post_string_id = post.post_id_name_string
        
        blog_posts_list.append((post_date,post_title,post_description,post_string_id))
    

    blog_posts_list.sort(key=lambda tuple_element: tuple_element[0], reverse=True)
    if number_of_posts_to_return:
        blog_posts_list = blog_posts_list[:number_of_posts_to_return]

    # print("- blog_posts_list -")
    # print(blog_post_list_most_recent)

    return blog_posts_list