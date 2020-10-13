class DBConnector:

    def __init__(self, db):
        self.connector = db

    async def fetchall(self, model):
        query = "SELECT * FROM `db`.`{}`".format(model)
        cur = await self.connector.cursor()
        await cur.execute(query)
        r = await cur.fetchall()
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

        await cur.close()
        return ret


    async def execute(self, query):
        cur = await self.connector.cursor()
        await cur.execute(query)
        await self.connector.commit()
        await cur.close()
