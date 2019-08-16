from django.shortcuts import render
from django.http import HttpResponseRedirect,Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Topic,Entry
from .forms import TopicForm,EntryForm

# Create your views here.
def index(request):
    #学习笔记的主页
    return render(request,'blog/index.html')
    
# 限制访问，只有登录用户可以访问
@login_required    
def topics(request):
    # 显示所有主题
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics':topics}
    return render(request,'blog/topics.html',context)

@login_required 
def topic(request,topic_id):
    # 显示单个主题及其条目
    topic = Topic.objects.get(id=topic_id)
    # 确认请求的主题属于当前用户
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic':topic,'entries':entries}
    return render(request,'blog/topic.html',context)

@login_required    
def new_topic(request):
    # 添加新主题
    if request.method != 'POST': # 确定请求方法
        # 未提交数据：创建一个新表单
        form = TopicForm()
    else:
        # POST 提交的数据，对数据进行处理
        form = TopicForm(request.POST)
        if form.is_valid(): # 检查表单是否有效
            new_topic = form.save(commit=False) # 先修改新主题，所以设置False，不提交
            new_topic.owner = request.user
            new_topic.save() # 将新主题表单数据写入数据库
            # HttpResponseRedirect类，用户提交主题后，将用户重定向到网页topics
            # reverse()根据指定的URL模型确定URL，Django将在页面请求时生成url，获取topics的url
            return HttpResponseRedirect(reverse('blog:topics'))
            
    context = {'form':form}
    return render(request,'blog/new_topic.html',context)

@login_required    
def new_entry(request,topic_id):
    # 在特定主题中添加新条目
    topic = Topic.objects.get(id=topic_id) # 根据topic_id获取正确主题
    if request.method != 'POST': # 检查请求方法
        # 获取一个新表单
        form = EntryForm()
    else:
        # POST 提交数据，对数据进行处理
        form = EntryForm(data=request.POST) # 创建实例并使用POST数据填充
        if form.is_valid(): # 判断表单是否有效
            new_entry = form.save(commit=False) # 让Django创建一个新的条目对象，并将其存储到new_entry，但不保存到数据库中
            new_entry.topic = topic # 设置条目对象属性，从数据库获取的主题
            new_entry.save() # 将条目保存到数据库，并将其与正确的主题相关联
            # reverse根据参数生成URL的URL模式的名称
            # HttpResponseRedirect将用户重定向到显示新增条目所属主题的页面，用户将在该页面的条目列表中看到新添加的条目
            return HttpResponseRedirect(reverse('blog:topic',args=[topic.id]))
            
    context = {'topic':topic,'form':form}
    return render(request,'blog/new_entry.html',context)

@login_required
def edit_entry(request,entry_id):
    # 编辑既有条目
    # 获取条目
    entry = Entry.objects.get(id=entry_id)
    # 获取条目的主题
    topic = entry.topic
    
    # 确认请求的主题属于当前用户
    if topic.owner != request.user:
        raise Http404
    
    if request.method != 'POST':
        # 初次请求，使用已有条目填充表单
        form = EntryForm(instance=entry)
    else:
        # POST提交的数据，对数据进行处理
        form = EntryForm(instance=entry,data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('blog:topic',args=[topic.id]))
    context = {'entry':entry,'topic':topic,'form':form}
    return render(request,'blog/edit_entry.html',context)