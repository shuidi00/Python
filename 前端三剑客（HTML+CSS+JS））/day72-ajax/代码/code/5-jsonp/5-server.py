import json
from aiohttp import web

routes = web.RouteTableDef()


@routes.get("/search")
async def get_js(request):
    # 接受客户端上传过来的请求体数据，并使用json.loads()转换成字典
    username = request.query.get("username")
    func = request.query.get("func", "callback")
    # 假设根据username到数据库中查询数据
    data = {
        "id": 1,
        "username": username,
        "age": 20
    }

    return web.Response(text=f"{func}({json.dumps(data)})", content_type="text/javascript")


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

if __name__ == '__main__':
    web.run_app(Application(routes),host="0.0.0.0",port=8000)
