from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
from django.contrib.auth.models import User

# 一个普通的序列化器
# 一个序列化器同时负责「序列化」和「反序列化」
# 这个普通的序列化器和Model没有强制绑定关系
# class SnippetSerializer(serializers.Serializer):
#     # 你会发现，字段和Model的字段不是完全对应的
#     # 理解：序列化器只关心会被传输的数据，有些数据是服务器生成的，但是不会发送，所以没必要序列化
#     # 而且，一个model可以有多个序列化器，每个序列化可能只是对应某种类型的请求
#     # 每个字段都有一些描述，这些都是用于验证数据合法性的
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(required=False, allow_blank=True, max_length=100)
#     code = serializers.CharField(style={'base_template': 'textarea.html'})
#     linenos = serializers.BooleanField(required=False)
#     language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
#     style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

#     # 根据json等创建一个对象，并且是自动同步到数据库的
#     def create(self, validated_data):
#         """
#         Create and return a new `Snippet` instance, given the validated data.
#         """
#         # 这一步会调用save，也就是保存到数据库的一步
#         return Snippet.objects.create(**validated_data)

#     # 根据一个json等更新一个对象（instance）
#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Snippet` instance, given the validated data.
#         """
#         instance.title = validated_data.get('title', instance.title)
#         instance.code = validated_data.get('code', instance.code)
#         instance.linenos = validated_data.get('linenos', instance.linenos)
#         instance.language = validated_data.get('language', instance.language)
#         instance.style = validated_data.get('style', instance.style)
#         # 因为这里已经有了instance，所以不是创建，而是更新
#         instance.save()
#         return instance

# 手动创建一个模型实例
# snippet = Snippet(code='foo = "bar"\n')
# save会把这个对象保存到数据库
# snippet.save()

# ===== 序列化（数据->文本） =====

# 基于这个model实例，创建序列化器，序列化为json
# serializer = SnippetSerializer(snippet)
# 输出json（或者类json的文本流）
# serializer.data

# 同时序列化多个model实例，使用many=True
# serializer = SnippetSerializer(Snippet.objects.all(), many=True)
# serializer.data

# ===== 反序列化（文本->数据） =====

# 基于json创建一个模型实例
# stream = io.BytesIO(content)
# data = JSONParser().parse(stream)
# 创建了一个model实例（基于json）
# serializer = SnippetSerializer(data=data)
# serializer.is_valid()
# True
# serializer.validated_data
# {'title': '', 'code': 'print("hello, world")', 'linenos': False, 'language': 'python', 'style': 'friendly'}
# 保存到数据库
# serializer.save()
# <Snippet: Snippet object>


# 更简便的方式：使用ModelSerializer
# 重要的是要记住，ModelSerializer 类并没有什么特别神奇的，它们只是创建序列化器类的快捷方式
class SnippetSerializer(serializers.ModelSerializer):
    # 只读字段，表示该字段只用于序列化，不用于反序列化（不会从json中得到）
    # 不会更新model数据，所以服务端手动添加了
    # 虽然是只读，但是也要在Meta中声明
    # source是读取这个数据的路径？它是一个属性访问路径
    # 这个owner没有类型？没有固定的数据类型，它是一个通用字段
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Snippet
        fields = ["id", "title", "code", "linenos", "language", "style", "owner"]


# ===== 用户相关的序列化器 =====
class UserSerializer(serializers.ModelSerializer):
    # 一对多关系
    snippets = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Snippet.objects.all()
    )

    class Meta:
        model = User
        fields = ["id", "username", "snippets"]


# ===== Hyperlinked序列化器 =====

# 超链接，是用于表示实体之间关系的一种方式
# It does not include the id field by default
# It includes a url field, using HyperlinkedIdentityField
# Relationships use HyperlinkedRelatedField, instead of PrimaryKeyRelatedField

# User -> Snippet（一对多）
# Snippet -> Highlight（一对一）


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    # 链接关系使用HyperlinkedIdentityField，设置view_name和format
    highlight = serializers.HyperlinkedIdentityField(
        view_name="snippet-highlight", format="html"
    )

    class Meta:
        model = Snippet
        fields = [
            "url",
            "id",
            "highlight",
            "owner",
            "title",
            "code",
            "linenos",
            "language",
            "style",
        ]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    # 链接关系使用HyperlinkedRelatedField
    snippets = serializers.HyperlinkedRelatedField(
        many=True, view_name="snippet-detail", read_only=True
    )

    class Meta:
        model = User
        fields = ["url", "id", "username", "snippets"]
