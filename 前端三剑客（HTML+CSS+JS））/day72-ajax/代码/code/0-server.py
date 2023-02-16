from aiohttp import web
import aiohttp_cors

# 路由对象
# 路由[router]，是一种用于绑定url地址与服务端应用处理程序[python里面的函数/类方法]之间的映射关系。
# /a1  ---> a函数
# /a2  ---> b函数
# 路由的格式类似hash映射（字典结构）
# {
#     "/a1": a函数,
#     "/a2": b函数,
# }
# 在实际开发中，我们所说的路由，往往也表示在服务端中实现路由关系的类，也叫路由类。

routes = web.RouteTableDef()

@routes.get("/")
async def get_index(request):
    print("hello!, 用户访问进来了！")
    data = [
        {"name": "xiaoming", "age": 17},
        {"name": "xiaoming", "age": 18},
        {"name": "xiaoming", "age": 19},
    ]
    # 返回json数据
    return web.json_response(data)


@routes.post("/")
async def post_index(request):

    # 接受客户端上传过来的请求体数据，并使用json.loads()转换成字典
    data = await request.json()
    print("data=", data)
    # 返回json数据
    return web.json_response(data)


@routes.put("/{name}")  # {name} 变量，当用户通过地址栏使用get请求时，会自动/斜杠后面的内容作为值赋值给name变量
async def num(request):
    # 获取url地址的一部分，这个叫路由参数
    name = request.match_info.get('name', "Anonymous")
    # 返回json数据
    return web.json_response({"name": name, "age": 19})


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
