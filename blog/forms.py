from django import forms

from .models import Topic,Entry

class TopicForm(forms.ModelForm):
    # 创建表单（让用户输入并提交的页面）
    class Meta:
        #　根据模型创建表单
        # 根据Topic模型创建表单
        model = Topic
        fields = ['text'] # 表单只含字段text
        labels = {'text':''} # 让Django不要为text生成标签
        
class EntryForm(forms.ModelForm):
    class Meta:
        # 表单基于的模型
        model = Entry
        fields = ['text']  # 表单中包含字段类型
        labels = {'text':''}
        # 小部件（widget）是HTML表单元素，如单行文本框，多行文本框和下拉列表
        # widgets属性可以覆盖Django的默认小部件，设置文本框宽度80列（默认40列）
        widgets = {'text':forms.Textarea(attrs={'cols':80})} 