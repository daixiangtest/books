from django.db import models


# Create your models here.
#创建数据表
class Books(models.Model):
    id = models.CharField(primary_key=True, max_length=20, verbose_name="图书编号")
    name = models.CharField(max_length=30, verbose_name='图书名称')
    statua = models.BooleanField(verbose_name='是否出借', default=False)

    class Meta:
        db_table = "book"
        verbose_name = '图书表'

    def __str__(self):
        return self.name


class Record(models.Model):
    book = models.ForeignKey("Books", on_delete=models.CASCADE, verbose_name="书籍名称")
    name = models.CharField(max_length=30, verbose_name='借书人')
    s_time = models.DateTimeField(auto_created=True,auto_now=True, verbose_name='出借时间',blank=True)
    e_time = models.DateTimeField(auto_created=True, auto_now=True, verbose_name='还书时间',blank=True)

    class Meta:
        db_table = "record"
        verbose_name = "借书记录表"
