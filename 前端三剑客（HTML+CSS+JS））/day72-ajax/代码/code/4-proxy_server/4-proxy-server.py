import json

from aiohttp import web, ClientSession

import aiohttp_cors

routes = web.RouteTableDef()

@routes.get("/")
async def get_index(request):
    # 返回json数据
    music = request.query.get("music", None)
    if music is None:
        return web.json_response({"errno": -1, "errmsg": "参数有误！"})
    # 发起请求，搜索音乐
    # http://msearchcdn.kugou.com/api/v3/search/song?keyword=
    url = f"http://msearchcdn.kugou.com/api/v3/search/song?keyword={music}"
    async with ClientSession() as session:
        async with session.get(url) as response:
            print("status:{}".format(response.status))
            if response.status == 200:
                data = await response.text()
                data = json.loads(data)
                print(data)
                return web.json_response(data)
            else:
                return web.json_response({"errno": -1, "errmsg": "搜索失败！"})

class Application(web.Application):
    def __init__(self, routes):
        """
        :param routes: url和服务端处理程序之间的绑定关系, 这种绑定关系，我们一般称之为路由，当然，在服务端开发中，我们也会经常把具有路由功能功能的类/对象，称之为"路由类"或"路由对象"
        """
        print(routes._items) # 路由列表
        # 先让官方的aiohttp的web框架先进行初始化
        super(Application, self).__init__()
        # 注册路由信息到web框架中,routes是一个list列表
        self.add_routes(routes)

        # 这里内部完成了一个for循环，把routes里面每一个路由信息都了遍历，添加一个返回值用于实现跨域资源共享[CORS]。
        cors = aiohttp_cors.setup(self, defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
            )
        })

        # Configure CORS on all routes.
        for route in list(self.router.routes()):
            cors.add(route)


if __name__ == '__main__':
    web.run_app(Application(routes),host="0.0.0.0",port=8000)
