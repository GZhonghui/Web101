from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from snippets.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import action

# 一般来说，常用的方法就GET和POST吧？
# POST可以包含数据，所以理论上，所有的请求都能做成POST的形式

# ===== 最基础的写法，基于函数，在urls.py中绑定 =====

# # we want to be able to POST to this view from clients that won't have a CSRF token
# # 不是正式做法，调试时可以使用
# @csrf_exempt
# # 这个函数应该对应（绑定）某个url（我们把这个url叫做一个view？）
# # 函数内部再细分请求方法
# def snippet_list(request):
#     """
#     List all code snippets, or create a new snippet.
#     """
#     if request.method == 'GET':
#         snippets = Snippet.objects.all() # 从数据库中获取所有
#         serializer = SnippetSerializer(snippets, many=True)
#         return JsonResponse(serializer.data, safe=False)

#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         # 创建新的Snippet实例
#         # 没有many=True，应该只能创建1个
#         serializer = SnippetSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)

# @csrf_exempt
# # pk是动态路由参数
# def snippet_detail(request, pk):
#     """
#     Retrieve, update or delete a code snippet.
#     """
#     try:
#         snippet = Snippet.objects.get(pk=pk) # 从数据库中获取实例
#     except Snippet.DoesNotExist:
#         return HttpResponse(status=404)

#     if request.method == 'GET':
#         serializer = SnippetSerializer(snippet)
#         return JsonResponse(serializer.data)

#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         # 注意这种写法，从snippet和data两个对象创建了一个序列化器
#         # 这不是创建新的实例，而是更新现有实例
#         serializer = SnippetSerializer(snippet, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)

#     elif request.method == 'DELETE':
#         # 这是从数据库中删除实例
#         snippet.delete()
#         return HttpResponse(status=204)

# ===== 还是基于函数的写法，稍微标准了一些 =====

# # 稍微简洁了一点
# @api_view(['GET', 'POST'])
# # 【自动内容协商】
# # 我们加了一个format参数，表示客户端的请求格式
# # 比如客户端可以GET x.com/a x.com/a.json x.com/a.yaml
# # 或者在HTTP请求头中指定 Accept: application/json等
# # 如果只是返回一个dict，那么我们什么都不用处理，DRF会自动处理
# # 如果需要根据不同的类型返回不同的内容，可以在这里进行处理（if format=="xxx"）
# # 总之，加上这个参数比较好，即使用不到，也不会影响其他功能
# # 另外，可以直接返回HTML形式，非常方便
# def snippet_list(request, format=None):
#     """
#     List all code snippets, or create a new snippet.
#     """
#     if request.method == 'GET':
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         # 这个Response就是返回的请求
#         # 里面什么都可以放吗？
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         # request.data 是一个字典，包含了请求的内容（HTTP body）
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# def snippet_detail(request, pk, format=None):
#     """
#     Retrieve, update or delete a code snippet.
#     """
#     try:
#         snippet = Snippet.objects.get(pk=pk)
#     except Snippet.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = SnippetSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# ===== 基于类的写法 =====

# # 要继承自APIView这个类
# class SnippetList(APIView):
#     """
#     List all snippets, or create a new snippet.
#     """
#     # 每个请求方法对应一个处理函数
#     # 其他的地方，好像差别也不太大
#     def get(self, request, format=None):
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class SnippetDetail(APIView):
#     """
#     Retrieve, update or delete a snippet instance.
#     """
#     def get_object(self, pk):
#         try:
#             return Snippet.objects.get(pk=pk)
#         except Snippet.DoesNotExist:
#             # 可以直接404啊
#             raise Http404

#     def get(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data)

#     def put(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# ===== 使用混入 =====

# # 好家伙，已经看不太懂了
# # Mixin 是一种设计模式，用来提供可重用的功能片段
# # 可以理解为"功能积木块"，你可以把不同的积木组合起来构建完整的功能
# # ListModelMixin 提供 list() 方法（获取列表）
# # CreateModelMixin 提供 create() 方法（创建对象）
# # 最后的GenericAPIView是必须的基类
# class SnippetList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     # 这两个要提前指定好
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer

#     # 全部参数都传进去，啥也不管
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

# class SnippetDetail(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

# ===== 更加简洁，通用类视图 =====

# 基类就是支持List和Create的通用视图
# class SnippetList(generics.ListCreateAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#     # 用这样的方式来描述「权限验证方式」
#     # 只允许认证用户创建，其他人只能读取
#     # 「创建」默认指的是POST请求
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]

#     # 这是一个create之前的钩子方法
#     def perform_create(self, serializer):
#         # 一定要执行这句保存，加上一些额外的数据
#         serializer.save(owner=self.request.user)


# class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#     # permission_classes 是 AND 关系 - 全部权限类都必须通过
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

# ===== 用户相关的视图 =====

# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# ===== API入口 =====


@api_view(["GET"])
def api_root(request, format=None):
    return Response(
        {
            # reverse：根据url名称（是的，每个url都可以设置一个名称），反向解析url
            # 最后返回的结果就是入口的url
            "users": reverse("user-list", request=request, format=format),
            "snippets": reverse("snippet-list", request=request, format=format),
        }
    )


# ===== 代码高亮 =====

# GenericAPIView相比APIView多了很多通用功能
# 但仍需手动实现 HTTP 方法
# class SnippetHighlight(generics.GenericAPIView):
#     # 比如GenericAPIView可以这样定义一些属性
#     # queryset = Snippet.objects.all()          # 数据查询集
#     # serializer_class = SnippetSerializer      # 序列化器类
#     # lookup_field = 'pk'                       # 查找字段（默认）
#     # permission_classes = [...]                # 权限类
#     # pagination_class = [...]                  # 分页类

#     queryset = Snippet.objects.all()
#     # 这里要用到一点HTML渲染了（服务器渲染的内容）
#     renderer_classes = [renderers.StaticHTMLRenderer]

#     def get(self, request, *args, **kwargs):
#         snippet = self.get_object() # 使用内置方法获取对象
#         return Response(snippet.highlighted)


# ===== ViewSets重构 =====
# 基类ReadOnlyModelViewSet/ModelViewSet
# 相当于把多个「操作同一种数据的View」合并到一起？
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer


class SnippetViewSet(viewsets.ModelViewSet):
    """
    This ViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """

    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    # create/update/delete以外的，自定义方法
    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# 请看定义
# class ModelViewSet(mixins.CreateModelMixin,
#                    mixins.RetrieveModelMixin,
#                    mixins.UpdateModelMixin,
#                    mixins.DestroyModelMixin,
#                    mixins.ListModelMixin,
#                    GenericViewSet):
#     """
#     A viewset that provides default `create()`, `retrieve()`, `update()`,
#     `partial_update()`, `destroy()` and `list()` actions.
#     """
#     pass
