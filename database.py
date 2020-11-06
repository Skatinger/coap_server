# database interaction helper class
class DBConnector:

    def __init__(self, db):
        self.connector = db

    # fetch all entries of the given table
    async def fetchall(self, model):
        query = "SELECT * FROM `db`.`{}`".format(model)

        async with self.connector.acquire() as conn:
            cur = await conn.cursor()
            await cur.execute(query)
            r = await cur.fetchall()
            # build objects
            ret = []
            num_fields = len(cur.description)
            field_names = [i[0] for i in cur.description]
            for res in r:
                dic = {}
                for i in range(len(field_names)):
                    # replace 1/0 from db to "True/False"
                    if field_names[i] == 'time':
                        dic[field_names[i]] = res[i].strftime("%m-%d-%Y %H:%M:%S")
                    else:
                        dic[field_names[i]] = res[i]
                ret.append(dic)
        return ret

    # run querys without output, e.g. alter, delete, etc.
    async def execute(self, query):
        async with self.connector.acquire() as conn:
            cur = await conn.cursor()
            await cur.execute(query)
            await conn.commit()
            await cur.close()
