from django.shortcuts import render, HttpResponse, redirect
from app import models
import os
from PIL import Image
import shutil, errno

def keep_number(string):
    result = ''
    for i in string:
        if ('0' <= i <= '9') or i == '.':
            result += i
        else:
            break
    return result

def rename_folder(root_path, id, file_list):
    new_key = []
    new_value = []
    for key in file_list.keys():
        new_dir = []
        for value in file_list[key]:
            os.rename("app/static/md/"+root_path+'/'+key+'/'+value, "app/static/md/"+root_path+'/'+key+'/'+keep_number(value))
            new_dir.append(keep_number(value))
        new_value.append(new_dir)
        os.rename("app/static/md/"+root_path+'/'+key, "app/static/md/"+root_path+'/'+keep_number(key))
        new_key.append(keep_number(key))
    os.rename('app/static/md/'+root_path, "app/static/md/"+str(id))
    return new_key, new_value

def title_to_path(id, new_key, new_value):
    result = []
    for key in new_key:
        dir = []
        for value in new_value:
            dir.append(str(id)+'/'+key+'/'+value)
        result.append(dir)
    return result

def copyanything(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        if exc.errno in (errno.ENOTDIR, errno.EINVAL):
            shutil.copy(src, dst)
        else: raise

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
    tutorial = models.Tutorial.objects.all()
    if len(tutorial) > 3:
        tutorial = tutorial[:3]
    masterpiece = models.Masterpiece.objects.all()
    if len(masterpiece) > 3:
        masterpiece = masterpiece[:3]
    return render(request, "index.html", {"tutorial": tutorial, "masterpiece": masterpiece, **get_status(request)})

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
    cookie = request.session.get("info")
    #user = models.User.objects.filter(user_name=cookie["user_name"])

    with open("masterpiece/" + url, 'wb') as f:
        for chunk in upload_img.chunks():
            f.write(chunk)
    models.Masterpiece.objects.create(author=author, description=description, url=url, user_name_id=cookie["user_name"])
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
    cookie = request.session.get("info")
    #user = models.User.objects.filter(user_name=cookie["user_name"])

    with open("masterpiece/" + url, 'wb') as f:
        for chunk in upload_img.chunks():
            f.write(chunk)
    models.Masterpiece.objects.create(author=author, description=description, url=url, user_name_id=cookie["user_name"])
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
    id = request.GET.get("id")
    info = models.Tutorial.objects.filter(id=id).first()
    print(info)
    
    title = info.title
    root_path = info.url
    first_dir = []
    index = []
    for f in os.listdir("tutorial/"+root_path):
        if not f.startswith('.'):
            first_dir.append(f)
    first_dir.sort()

    second_dir = {}
    show_dir = {}
    for value in first_dir:
        dir = []
        title_dir = []
        address_dir = []
        for f in os.listdir("tutorial/"+root_path+"/"+value):
            if not f.startswith('.'):
                dir.append(f)
                title_dir.append(f.replace('.md', ''))
                address_dir.append(str(id)+'/'+keep_number(value)+'/'+keep_number(f))
        dir.sort()
        title_dir.sort()
        address_dir.sort()
        s_dir = []
        for i in range(len(title_dir)):
            s_dir.append({"title": title_dir[i], "address": address_dir[i]})
        second_dir[value] = dir
        show_dir[value] = s_dir

    if not os.path.exists("app/static/md/"+str(id)):
        copyanything("tutorial/"+root_path, "app/static/md/"+root_path)
        new_key, new_value = rename_folder(root_path, id, second_dir)
    else:
        new_key, new_value = [], []
        for key in second_dir.keys():
            new_key.append(keep_number(key))
            dir = []
            for value in second_dir[key]:
                dir.append(keep_number(value))
            new_value.append(dir)

    if not request.GET.get("address"):
        path = str(id) + "/" + new_key[0] + "/" + new_value[0][0]
    else:
        path = request.GET.get("address")

    return render(request, "tutorial-detail.html", {"id": id, "title": title, "path": path, "second_dir": show_dir, **get_status(request)})

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
    md_url = str(len(md_info)) + "_" + md.name.split('.')[0]
    cookie = request.session.get("info")
    #user = models.User.objects.filter(user_name=cookie["user_name"])
    
    with open("tutorial/"+ img_url, "wb") as f:
        for chunk in img.chunks():
            f.write(chunk)
    with open("tutorial/" + md.name, "wb") as f:
        for chunk in md.chunks():
            f.write(chunk)
    import tarfile
    with tarfile.open("tutorial/" + md.name) as f:
        f.extractall('tutorial/')

    os.rename("tutorial/"+md.name.split('.')[0], "tutorial/"+md_url)
    models.Tutorial.objects.create(title=title, author=author, img_url=img_url, url=md_url, user_name_id=cookie["user_name"])
    return redirect("tutorial.html")

def person(request):
    cookie = request.session.get("info")
    user_name_id = cookie["user_name"]
    tutorial = models.Tutorial.objects.filter(user_name_id=user_name_id).all()
    masterpiece = models.Masterpiece.objects.filter(user_name_id=user_name_id).all()

    return render(request, "person.html", {"tutorial": tutorial, "masterpiece": masterpiece, **get_status(request)})  