from aiohttp import web

async def handle(request):
	name = request.match_info.get('name', "Anonymous")
	text = "Server is up..."
	return web.Response(text=text)

app = web.Application()
app.router.add_get('/', handle)
app.router.add_get('/{name}', handle)
web.run_app(app, host="0.0.0.0", port=3000)
