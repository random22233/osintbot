import polars as pl


zloy_path = "data/df_zloy.org.parquet"
inattack_part1_members = "data/df_ipb_members_part1.parquet"
inattack_part1_message_text = "data/df_ipb_message_text_part1.parquet"

inattack_part2_members = "data/df_ipb_members_part2.parquet"
inattack_part2_posts= "data/df_ipb_posts_part2.parquet"

inattack_user = "data/df_ipb_members_user.parquet"

carderpro = "data/df_carderpro.parquet"

opensc_ws = "data/df_opensc_ws.parquet"

xakepok_members = "data/df_xakepok_xakepok_user.parquet"
xakepok_posts= "data/df_xakepok_xakepok_post.parquet"

discord_part1 = "data/df_discord_fixed_part1.parquet"
discord_part2 = "data/df_discord_fixed_part2.parquet"

def search_xakepok(target_email):
    print("--search_xakepok")
    members_df = pl.read_parquet(xakepok_members)
    posts_df = pl.read_parquet(xakepok_posts)
    all_result = ""
    members_filtered_df = members_df.filter(members_df[:, 7] == target_email)
    if members_filtered_df.shape[0] > 0:
        user_id=members_filtered_df[:, 0][0]
        username=members_filtered_df[:, 4][0]
        ip = members_filtered_df[:, 40][0]
        register = members_filtered_df[:, 20][0]
        last_post = members_filtered_df[:, 24][0]
        number_of_posts = members_filtered_df[:, 26][0]
        user_data = (  f"search_xakepok:\n"
                        f"Username: {username}\n"
                        f"IP Address: {ip}\n"
                        f"Register: {register}\n"
                        f"Last post: {last_post}\n"
                        f"Number of posts: {number_of_posts}\n\n")
        posts_filtered_df = posts_df.filter(posts_df[:, 4] == user_id)
        for post in posts_filtered_df.iter_rows():
            post_date = post[6]
            post_post = str(post[7]).encode().decode()
            post_ip_address = post[10]
            all_result += (
                            f"Post Date: {post_date}\n"
                           f"Post Text: {post_post}\n"
                           f"Post Ip Address: {post_ip_address}\n\n")
        return user_data, all_result
    else:
        print("Nothing Founded in xakepok db")
        return "Nothing Founded in xakepok db", "" 


def search_opensc_ws(target_email):
    print("--search_opensc_ws")
    members_df = pl.read_parquet(opensc_ws)
    all_result = ""
    print(members_df)
    members_filtered_df = members_df.filter(members_df[:, 7] == target_email)
    if members_filtered_df.shape[0] > 0:
        username=members_filtered_df[:, 4][0] 
        ip = members_filtered_df[:, 34][0] 
        register = members_filtered_df[:, 17][0] 
        last_post = members_filtered_df[:, 21][0]
        number_of_posts = members_filtered_df[:, 22][0]
        all_result = (  f"search_opensc_ws:\n"
                        f"Username: {username}\n"
                        f"IP Address: {ip}\n"
                        f"Register: {register}\n"
                        f"Last post: {last_post}\n"
                        f"Number of posts: {number_of_posts}\n\n"
                        )
        return all_result
    else:
        print("Nothing Founded in opensc_ws db")
        return "Nothing Founded in opensc_ws db"  

def search_carderpro(target_email):
    print("--search_carderpro")
    members_df = pl.read_parquet(carderpro)
    all_result = ""
    members_filtered_df = members_df.filter(members_df[:, 7] == target_email)
    if members_filtered_df.shape[0] > 0:
        username=members_filtered_df[:, 4][0] 
        ip = members_filtered_df[:, 40][0] 
        register = members_filtered_df[:, 6][0] 
        # last_post = members_filtered_df['last_post'][0]
        # number_of_posts = members_filtered_df['posts'][0]
        all_result = (  f"search_carderpro:\n"
                        f"Username: {username}\n"
                        f"IP Address: {ip}\n"
                        f"Register: {register}\n"
                        # f"Last post: {last_post}\n"
                        # f"Number of posts: {number_of_posts}\n\n"
                        )
        return all_result
    else:
        print("Nothing Founded in carderpro db")
        return "Nothing Founded in carderpro db"  

def search_inattack_part2(target_email):
    print("--search_inattack_part2")
    members_df = pl.read_parquet(inattack_part2_members)
    posts_df = pl.read_parquet(inattack_part2_posts)
    all_result = ""
    members_filtered_df = members_df.filter(pl.col('email') == target_email)
    if members_filtered_df.shape[0] > 0:
        user_id=members_filtered_df["id"][0]
        username=members_filtered_df["name"][0]
        ip = members_filtered_df['ip_address'][0]
        register = members_filtered_df['joined'][0]
        last_post = members_filtered_df['last_post'][0]
        number_of_posts = members_filtered_df['posts'][0]
        user_data = (  f"search_inattack_part2:\n"
                        f"Username: {username}\n"
                        f"IP Address: {ip}\n"
                        f"Register: {register}\n"
                        f"Last post: {last_post}\n"
                        f"Number of posts: {number_of_posts}\n\n")
        posts_filtered_df = posts_df.filter(pl.col('author_id') == user_id)
        for post in posts_filtered_df.iter_rows(named=True):
            post_date = post['post_date']
            post_post = str(post['post']).encode().decode()
            post_ip_address = post['ip_address']
            all_result += (f"Post Date: {post_date}\n"
                           f"Post Text: {post_post}\n"
                           f"Post Ip Address: {post_ip_address}\n\n")
        return user_data , all_result
    else:
        print("Nothing Founded in in_attack part2 db")
        return "Nothing Founded in in_attack part2 db", ""

def search_discord_part1(target_email):
    print("--search_discord_part1")
    discord_df = pl.read_parquet(discord_part1)
    discord_filtered_df = discord_df.filter(pl.col('email') == target_email)
    if discord_filtered_df.shape[0] > 0:
        return discord_filtered_df[0].row(0 , named=True)
    else:
        return "Nothing Founded in discord part1 db" 
 
def search_discord_part2(target_email):
    print("--search_discord_part2")
    discord_df = pl.read_parquet(discord_part2)
    discord_filtered_df = discord_df.filter(pl.col('email') == target_email)
    print(discord_filtered_df.head())
    if discord_filtered_df.shape[0] > 0:
        return discord_filtered_df[0].row(0 , named=True)
    else:
        return "Nothing Founded in discord part2 db" 
        
def search_inattack_part1(target_email):
    print("--search_inattack_part1")
    members_df = pl.read_parquet(inattack_part1_members)
    message_df = pl.read_parquet(inattack_part1_message_text)
    all_result = ""
    members_filtered_df = members_df.filter(pl.col('email') == target_email)
    if members_filtered_df.shape[0] > 0:
        user_id=members_filtered_df["id"][0]
        username=members_filtered_df["name"][0]
        ip = members_filtered_df['ip_address'][0]
        register = members_filtered_df['joined'][0]
        last_post = members_filtered_df['last_post'][0]
        number_of_posts = members_filtered_df['posts'][0]
        user = (  f"search_inattack_part1:\n"
                        f"Username: {username}\n"
                        f"IP Address: {ip}\n"
                        f"Register: {register}\n"
                        f"Last post: {last_post}\n"
                        f"Number of posts: {number_of_posts}\n\n")
        messages_filtered_df = message_df.filter(pl.col('msg_author_id') == user_id)
        for message in messages_filtered_df.iter_rows(named=True):
            msg_date = message['msg_date']
            msg_post = str(message['msg_post']).encode().decode()
            msg_ip_address = message['msg_ip_address']
            all_result += (f"Message Date: {msg_date}\n"
                           f"Message Text: {msg_post}\n"
                           f"Message Ip Address: {msg_ip_address}\n\n")
        return user, all_result
    else:
        print("Nothing Founded in in_attack part1 db")
        return "Nothing Founded in in_attack part1 db", ""  
    
def search_inattack_user(target_email):
    print("--search_inattack_user")
    members_df = pl.read_parquet(inattack_user)
    members_filtered_df = members_df.filter(pl.col('email') == target_email)
    if members_filtered_df.shape[0] > 0:
        username=members_filtered_df["name"][0]
        ip = members_filtered_df['ip_address'][0]
        register = members_filtered_df['joined'][0]
        last_post = members_filtered_df['last_post'][0]
        number_of_posts = members_filtered_df['posts'][0]
        user = (  f"search_inattack_user:\n"
                        f"Username: {username}\n"
                        f"IP Address: {ip}\n"
                        f"Register: {register}\n"
                        f"Last post: {last_post}\n"
                        f"Number of posts: {number_of_posts}\n\n")
        return user
    else:
        print("Nothing Founded in in_attack user db")
        return "Nothing Founded in in_attack user db"
    
def search_zloy_db(target_email):
    print("--search_zloy_db")
    df = pl.read_parquet(zloy_path)
    filtered_df = df.filter(pl.col('email') == target_email)
    if filtered_df.shape[0] > 0:
        username=filtered_df["username"][0]
        ip = filtered_df['ipaddress'][0]
        register = filtered_df['joindate'][0]
        last_post = filtered_df['lastpost'][0]
        number_of_posts = filtered_df['posts'][0]

        return(         f"search_zloy_db:\n"
                        f"Username: {username}\n"
                        f"IP Address: {ip}\n"
                        f"Register: {register}\n"
                        f"Last post: {last_post}\n"
                        f"Number of posts: {number_of_posts}\n")
    else:
        print("Nothing Founded in zloy db")
        return "Nothing Founded in zloy db"
#gorokl@yandex.ru , fbixhacker@gmail.com, mafiaboy3@hotmail.com
# print(search_xakepok("dop-big@mail.ru"))