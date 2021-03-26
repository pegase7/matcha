import psycopg2 as p

class USERS_MANAGER():
    def get_users(self):
        try:
            with p.connect(host="localhost", database="matchadb", user="ogasnier", password="olivier") as connection:
                with connection.cursor() as cursor:
                    cursor.execute("select * from public.USERS")
                    records = cursor.fetchall()
            return records
        except (Exception, p.DatabaseError) as error:
            print(error)

# if __name__ == '__main__':
#     users = USERS_MANAGER().get_users()
   # print(users)