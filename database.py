class DBConnector:

    def __init__(self, db):
        self.connector = db


    async def fetchall(self, model):
        query = "SELECT * FROM `db`.`{}`".format(model)

        async with self.connector.acquire() as conn:
            cur = await conn.cursor()
            await cur.execute(query)
            r = await cur.fetchall()
            print("QUERY:")
            print(query)
            print("RESULT")
            print(r)
            # build objects
            ret = []
            num_fields = len(cur.description)
            field_names = [i[0] for i in cur.description]
            # print(field_names)
            for res in r:
                dic = {}
                for i in range(len(field_names)):
                    # replace 1/0 from db to "True/False"
                    if field_names[i] == 'time':
                        dic[field_names[i]] = res[i].strftime("%m-%d-%Y %H:%M:%S")
                    else:
                        dic[field_names[i]] = res[i]
                ret.append(dic)
            # await cur.close()
        return ret
    #
    # async def fetchall2(self, model):
    #     query = "SELECT * FROM `db`.`{}`".format(model)
    #     async with self.connector.acquire() as conn:
    #         async with conn.cursor as cur:
    #             print("EXECUTING QUERY:")
    #             print(cur)
    #             await cur.execute(query)
    #             print("executed")
    #             r = await cur.fetchall()
    #             print("result:")
    #             print(r)
    #             # build objects
    #             ret = []
    #             num_fields = len(cur.description)
    #             field_names = [i[0] for i in cur.description]
    #             # print(field_names)
    #             for res in r:
    #                 dic = {}
    #                 for i in range(len(field_names)):
    #                     # replace 1/0 from db to "True/False"
    #                     if field_names[i] == 'time':
    #                         dic[field_names[i]] = res[i].strftime("%m-%d-%Y %H:%M:%S")
    #                     else:
    #                         dic[field_names[i]] = res[i]
    #                 ret.append(dic)
    #             # await cur.close()
    #     return ret

    #
    async def execute(self, query):
        async with self.connector.acquire() as conn:
            cur = await conn.cursor()
            await cur.execute(query)
            await conn.commit()
            await cur.close()

        # conn = await self.connector.acquire()
        # cur = await conn.cursor()
        # await cur.execute(query)
        # await conn.commit()
        # await cur.close()
