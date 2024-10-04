from django.shortcuts import render, HttpResponse, redirect
from app import models
import os
from PIL import Image
import shutil

def get_status(request):
    cookie = request.session.get("info")
    if "level" not in cookie:
        show = False
        user_name = None
    else:
        show = cookie["level"]
        user_name = cookie["user_name"]
    output = {"show": show, "user_name": user_name}
    #print(output)
    return output

# Create your views here.
def index(request):
    #return HttpResponse("Hello World!")
    return render(request, "index.html", {**get_status(request)})

def about(request):
    return render(request, "about.html", {**get_status(request)})

def login(request):
    request.session["info"] = {}
    if request.method == "GET":
        return render(request, "login.html", {"notice": "", **get_status(request)})
    user_name = request.POST.get("user")
    password = request.POST.get("password")
    result = models.User.objects.filter(user_name=user_name, password=password).first()
    if not result:
        return render(request, "login.html", {"notice": "登陆失败！", **get_status(request)})
    else:
        request.session["info"] = {"level": result.admin, "user_name": user_name}
        return render(request, "index.html", {**get_status(request)})

def masterpiece_detail(request):
    id = request.GET.get("id")
    image_info = models.Masterpiece.objects.all()
    info = models.Masterpiece.objects.filter(id=id).first()
    if not os.path.exists("app/static/img/" + info.url):
        shutil.copy("masterpiece/" + info.url, "app/static/img/" + info.url)
    if request.method == "GET":
        return render(request, "masterpiece-detail.html", {"info": info, **get_status(request)})

    author = request.POST.get("author")
    description = request.POST.get("description")
    upload_img = request.FILES.get("masterpiece-file")
    url = str(len(image_info)) + "_" + upload_img.name

    with open("masterpiece/" + url, 'wb') as f:
        for chunk in upload_img.chunks():
            f.write(chunk)
    models.Masterpiece.objects.create(author=author, description=description, url=url)
    return redirect(f"masterpiece-detail.html?id={id}")

def masterpiece(request):
    image_info = models.Masterpiece.objects.all()
    info_1, info_2, info_3 = [], [], []
    for item in image_info:
        if not os.path.exists("app/static/img/small_" + item.url):
            img = Image.open("masterpiece/" + item.url)
            width = 400
            w, h = img.size
            img = img.resize([width, int(h / w * width)])
            img.save("app/static/img/small_" + item.url)

        if item.id % 3 == 0:
            info_1.append(item)
        elif item.id % 3 == 1:
            info_2.append(item)
        else:
            info_3.append(item)
                
    if request.method == "GET":
        return render(request, "masterpiece.html", {'info_1': info_1, 'info_2': info_2, 'info_3': info_3, **get_status(request)})
    
    author = request.POST.get("author")
    description = request.POST.get("description")
    upload_img = request.FILES.get("masterpiece-file")
    url = str(len(image_info)) + "_" + upload_img.name

    with open("masterpiece/" + url, 'wb') as f:
        for chunk in upload_img.chunks():
            f.write(chunk)
    models.Masterpiece.objects.create(author=author, description=description, url=url)
    #new_info = models.Masterpiece.objects.filter(url=url).first()

    '''
    if new_info.id % 3 == 0:
        info_1.append(new_info)
    elif new_info.id % 3 == 1:
        info_2.append(new_info)
    else:
        info_3.append(new_info)
        '''
    return redirect("masterpiece.html")

def member(request):
    if request.method == "GET":
        queryset = models.NewContact.objects.all()
        return render(request, "member.html", {'queryset': queryset, **get_status(request)})
    search_text = request.POST.get("name_department")
    name_queryset = models.NewContact.objects.filter(name__startswith=search_text)
    department_queryset = models.NewContact.objects.filter(department__startswith=search_text)
    queryset = [*name_queryset, *department_queryset]
    return render(request, "member.html", {'queryset': queryset, **get_status(request)})

def register_quiz(request):
    if request.method == "GET":
        return render(request, "register-quiz.html", {**get_status(request)})
    cookie = request.session.get("info")
    q_num = 2
    answers = ['B', 'D']
    flag = True
    for i in range(1, q_num+1):
        answer = request.POST.get("quiz_"+str(i))
        if answer != answers[i-1]:
            flag = False
            break
    if flag:
        models.User.objects.create(user_name=cookie["user_name"], password=cookie["password"])
        request.session["info"] = {"status": 1}
        return redirect("register.html")
    else:
        request.session["info"] = {"status": 0}
        return redirect("register.html")

def register(request):
    cookie = request.session.get("info")
    if request.method == "GET":
        if 'status' not in cookie:
            return render(request, "register.html", {"notice": "", **get_status(request)})
        elif cookie['status'] == 1:
            return render(request, "register.html", {"notice": "注册成功！", **get_status(request)})
        elif cookie['status'] == 0:
            return render(request, "register.html", {"notice": "答题错误，注册失败！", **get_status(request)})

    user_name = request.POST.get("user")
    password = request.POST.get("password")
    re_password = request.POST.get("re-password")

    if len(user_name) >= 20:
        return render(request, "register.html", {"notice": "用户名大于20位！", **get_status(request)})
    elif len(user_name) == 0:
        return render(request, "register.html", {"notice": "用户名不能为空！", **get_status(request)})
    
    if len(password) >= 25:
        return render(request, "register.html", {"notice": "密码大于25位！", **get_status(request)})
    elif len(password) == 0:
        return render(request, "register.html", {"notice": "密码不能为空！", **get_status(request)})

    if password != re_password:
        return render(request, "register.html", {"notice": "两次密码输入不同！", **get_status(request)})
    
    exist = models.User.objects.filter(user_name=user_name).first()
    if exist:
        return render(request, "register.html", {"notice": "用户已存在", **get_status(request)})
    cookie = {'user_name': user_name, 'password': password}
    request.session["info"] = cookie
    return redirect("register-quiz.html", {**get_status(request)})

def tutorial_detail(request):
    return render(request, "tutorial-detail.html", {**get_status(request)})

def tutorial(request):
    md_info = models.Tutorial.objects.all()
    for item in md_info:
        if not os.path.exists("app/static/img/" + item.img_url):
            img = Image.open("tutorial/" + item.img_url)
            width = 400
            w, h = img.size
            img = img.resize([width, int(h / w * width)])
            img.save("app/static/img/" + item.img_url)

    if request.method == "GET":
        return render(request, "tutorial.html", {"md_info": md_info, **get_status(request)})
    title = request.POST.get("title")
    author = request.POST.get("author")
    img = request.FILES.get("tutorial-img")
    img_url = "img_" + str(len(md_info)) + "_" + img.name
    md = request.FILES.get("tutorial-md")
    md_url = str(len(md_info)) + "_" + md.name
    
    with open("tutorial/"+ img_url, "wb") as f:
        for chunk in img.chunks():
            f.write(chunk)
    with open("tutorial/" + md_url, "wb") as f:
        for chunk in md.chunks():
            f.write(chunk)
    import tarfile
    with tarfile.open("tutorial/" + md_url) as f:
        f.extractall("tutorial/" + md_url.split('.')[0])

    md_url = md_url.split('.')[0]
    models.Tutorial.objects.create(title=title, author=author, img_url=img_url, url=md_url)
    return redirect("tutorial.html")

def person(request):
    return render(request, "person.html", {**get_status(request)})  