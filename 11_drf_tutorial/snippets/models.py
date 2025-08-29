from django.db import models

# 这是一个语法分析的lib
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

# 都是和语法高亮相关的内容
LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


# 一个普通的Model
# 一个model是一个数据库表的映射（自动关联）
class Snippet(models.Model):
    # 这里没有显式定义主键
    # 实际上主键是必须的（有且仅有一个）
    # 没有的话，DRF会自动添加一个主键字段
    # id = models.BigAutoField(primary_key=True)

    # 关于关系型数据库的表的主键（Primary Key, pk）
    #

    # 创建字段的方式
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default="")
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    # 多选字段
    language = models.CharField(
        choices=LANGUAGE_CHOICES, default="python", max_length=100
    )
    style = models.CharField(choices=STYLE_CHOICES, default="friendly", max_length=100)

    # 后续添加，和认证相关的部分
    # 一对多关系
    # 这里涉及到了多个表之间的连接，需要复习一下几种连接关系（如：一对一、一对多、多对多）
    owner = models.ForeignKey(
        "auth.User", related_name="snippets", on_delete=models.CASCADE
    )
    highlighted = models.TextField()

    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code snippet.
        """
        # 自己做一些对代码的处理
        lexer = get_lexer_by_name(self.language)
        linenos = "table" if self.linenos else False
        options = {"title": self.title} if self.title else {}
        formatter = HtmlFormatter(
            style=self.style, linenos=linenos, full=True, **options
        )
        self.highlighted = highlight(self.code, lexer, formatter)
        # 记得调用父类的save方法
        super().save(*args, **kwargs)

    # 元数据
    # 用于指定和模型的行为相关的选项
    class Meta:
        ordering = ["created"]


# 构建数据库
# python manage.py makemigrations snippets
# python manage.py migrate
