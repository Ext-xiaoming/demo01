import json

import os
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db.models import Max, Q
from django.http import HttpResponse
from django.shortcuts import render
from app1 import models
from django.core import serializers
from django.utils import timezone #引入timezone模块


# Create your views here.
from demo01 import settings


def index(request):
    return  render(request,'hello.html')

#教师端点击上传照片 开始发布新的人脸识别签到
def postIfaceCheck(request):

    # 算法接口##############################################################################################################
    # tree_path = './'
    # addStudent(fpath, fname文件名，index学生的)
    # studentList : index
    # addClass([index, ...], class_index)
    # studentNum, studentIndex = backends.processing(path=file_path教师上传, name=file_name, class_index=name)
    # ToDO pic = visualize(xxxxx)
    # ToDO classAddNewStud
    # index[1,2....]-->studentId[1800301038,...]
    # 算法接口##############################################################################################################

    postId = request.POST.get('postId')
    postData = request.POST.get('postData')
    teacherId = request.POST.get('teacherId')

    file_save_path_InServer= request.POST.get('file_save_path_InServer')#至指定到文件夹
    file_name_InSFolder= request.POST.get('file_name_InSFolder')#文件在指定文件夹中的名字
    class_index= request.POST.get('class_index')#班级索引 就是班级的课程码(一个四位数 courseId)


    # 保存照片到指定文件夹下
    try:
        image=request.FILES.get('file')

        #方案一
        # if image.size>1000 and image.size<20480000:
        #     path=default_storage.save(file_save_path_InServer+image.name,ContentFile(image.read()))
        #     destination =os.path.join(settings.MEDIA_ROOT,path)
        # else:
        #     print("no")

        #方案二
        #destination = open(os.path.join("E:\\upload", myFile.name), 'wb+')  # 打开特定的文件进行二进制的写操作

        destination = open(os.path.join(file_save_path_InServer, file_name_InSFolder), 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in image.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()

    except:
        return HttpResponse("no!")

    #打印
    print(postId)
    print(teacherId)
    print(file_save_path_InServer)
    print(file_name_InSFolder)
    print(class_index)

    #通过course_id 查找post_num
    res0 = models.PostCheckIn.objects.filter(course_id=class_index)
    postNum = int(res0.aggregate(Max('post_num')).get('post_num__max')) + 1




    #获取班级成员的index
    res = models.StudentCourse.objects.filter(course_id=class_index)
    student_index=[]#学生的index 列表[1,2,3,4,6,...]-->[180003...]
    for p in res:
        student_index.append(p.sign_id)
    # ToDO addClass(student_index, class_index)
    # ToDO studentNum, res_StudentIndex = backends.processing(path=file_path教师上传, name=file_name, class_index=name)

    res_StudentIndex = []#算法处理后得到

    #将student_index[] 还原回学号
    studentId=[]#studentId[]为学生的学号
    len_student_index=len(res_StudentIndex)
    j=0
    while j < len_student_index:
        q_stu_id=models.Student.objects.filter(stu_index=res_StudentIndex[j])
        for s in q_stu_id:
            studentId.append(s.student_id)
        j += 1

    #在post_check_in 里面插入发布的签到  type=1 人脸签到
    opreateAdd = models.PostCheckIn(post_id=postId, teacher_id=teacherId, post_date=postData,
                                    post_num=postNum, course_id=class_index,post_type=1,post_longitude=0,post_latitude=0)
    opreateAdd.save()

    #将结果存入数据库表中--在sign_in 中插入签到记录
    #查询出当前的singId
    sql='select * from sign_in order by sign_id desc'
    res = models.Student.objects.raw(sql)  #RawQuerySet 集合对象 【只支持基础操作，比如循环】

    #获取最大的那个sign_in
    for p in res:
        print(p.sign_id)
        sign_id=p.sign_id;
        break

    #插入学生签到记录
    for i in studentId:
        sign_id =sign_id+1
        opreateAdd =models.SignIn(sign_id=sign_id,student_id=i,post_type=1,post_num=postNum,post_id=postId)
        opreateAdd.save()
    #返回的结果集


    return HttpResponse("ok")

#学生端上传个人照片
def savePictures(request):
    fpath = request.POST.get('file_save_path_InServer')  # 至指定到文件夹
    fname = request.POST.get('file_name_InSFolder')  # 文件在指定文件夹中的名字
    studentId = request.POST.get('studentId')  #识别时哪一个学生
     # 保存照片到指定文件夹下
    print(11111)
    try:
        image=request.FILES.get('file')

        #方案一
        # if image.size>1000 and image.size<20480000:
        #     path=default_storage.save(file_save_path_InServer+image.name,ContentFile(image.read()))
        #     destination =os.path.join(settings.MEDIA_ROOT,path)
        # else:
        #     print("no")

        #方案二
        #destination = open(os.path.join("E:\\upload", myFile.name), 'wb+')  # 打开特定的文件进行二进制的写操作

        destination = open(os.path.join(fpath, fname), 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in image.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
    except:
        data = {"RESULT": -1}
        return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")

    #查询获取学生的index
    studentIndex=-1
    res = models.Student.objects.filter(student_id=studentId)
    for s in res:
        studentIndex=s.student_id

    print(studentIndex)
    #上传成功后进行 班级树的重新构建
    #TODO addStudent(fpath, fname, studentIndex)

    data = {"RESULT": 1}
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")

#注册账号
def signUp(request):
    id = request.POST.get('id')
    user = request.POST.get('user')
    password = request.POST.get('password')
    phone = request.POST.get('phone')
    flag = request.POST.get('flag')


    if flag=='true':                             #教师，先查询index，插入注册信息
        #查询获取做大的index
        res0=models.Teacher.objects.all()
        index=int(res0.aggregate(Max('tea_index')).get('tea_index__max'))+1

        #插入
        opreateAdd = models.Teacher(teacher_id=id, tea_index=index, teacher_name=user, teacher_password=password,
                                   teacher_phone=phone)
        opreateAdd.save()

        print("over!")
    else:                                        #学生，先查询index，插入注册信息
        # 查询获取做大的index
        res1 = models.Student.objects.all()
        print(res1.aggregate(Max('stu_index')) )
        index = int(res1.aggregate(Max('stu_index')).get('stu_index__max'))+1


        print(index)
        # 插入
        opreateAdd = models.Student(student_id=id, stu_index=index, student_name=user, student_password=password,
                                    student_phone=phone)
        opreateAdd.save()
        print("over!")
    return HttpResponse("ok")


#登陆
def login(request):
    #获取传递的账号密码 - 查询判定是教师 or 学生 - 返回user身份标志 RESULT=1 为教师 (-1 为账号或密码错误)

    userId = request.POST.get('userId')
    userPassword = request.POST.get('password')
    print(userId)
    print(userPassword)

    #判断是否是教师
    user = models.Teacher.objects.filter(teacher_id=userId)   # 如果使用get（）当查询结果不存在时会出现异常
    if user.exists():
        for res in user:
            passeord =res.teacher_password
            userName =res.teacher_name
        if passeord==userPassword:
            print("the teacher  password  is true")
            data = {"RESULT": 1,"userName":userName}
            return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")
    else:
        print("sorry, the count is not from  teacher")

        # 判断是否是学生
        user = models.Student.objects.filter(student_id=userId)
        if user.exists():
            for res in user:
                passeord = res.student_password
                userName = res.student_name
            if passeord == userPassword:
                print("the Student  password  is true")
                data = {"RESULT":0,'userName':userName}
                return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")
        else:
            print("sorry, the count is not from  teacher")

    data={"RESULT":-1,'userName':"no"}
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")

#修改密码
def changePassward(request):
    #RESULT = 1#返回结果的标志


    userId = request.POST.get('userId')
    new_password = request.POST.get('new_password')
    flag = request.POST.get('flag')
    print(flag)
    print(new_password)


    if flag=="T":                                 #教师
        #修改教师的密码

        #修改数据库方法一
        #models.Teacher.objects.filter(teacher_id=userId).update(teacher_password=new_password)
        #修改数据库方法二
        res2=models.Teacher.objects.get(teacher_id=userId)
        res2.teacher_password=new_password
        res2.save()
        data={"RESULT": 1}
        print("over!")
        return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")

    else:
        # 修改学生的密码
        res2 = models.Student.objects.get(student_id=userId)
        res2.student_password = new_password
        res2.save()
        data = {"RESULT": 1}
        print("over!")
        return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")


    data = {"RESULT": 0 } # 1表示完成功能没有错误
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")

#加载教师端课程列表
def lodeTeaCourseList(request):
    teacherId = request.POST.get('teacherId')

    #查询教师姓名
    teacher=models.Teacher.objects.filter(teacher_id=teacherId)
    for t in teacher:
        teacher_name=t.teacher_name
    print(teacher_name)

    course_id=[]
    course_name=[]
    i=0
    course = models.Course.objects.filter(teacher_id=teacherId)
    print(type(course),course)
    for c in course:
        course_id.append(c.course_id)
        course_name.append(c.course_name)

    len_id = len(course_id)
    data=[]
    j = 0
    while j < len_id:
        data.append({"course_name":course_name[j],"course_id":course_id[j],"teacher_name":teacher_name})
        j+=1


    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")

#加载学生端课程列表
def lodeStuCourseList(request):
    studentId = request.POST.get('studentId')

    print(studentId)
    course_id=[]
    course_name = []
    teacher_id = []
    teacher_name = []

    #查询所选课程的所有id
    res0 = models.StudentCourse.objects.filter(student_id=studentId)
    for r in res0:
        course_id.append(r.course_id)


    #根据id 获取老师名称和课程名
    for i in course_id:
        res1 = models.Course.objects.filter(course_id=i)
        for c in res1:
            course_name.append(c.course_name)
            teacher_id.append(c.teacher_id)

    #根据teacher_id 查询teacher_name
    for t in teacher_id:
        res1 = models.Teacher.objects.filter(teacher_id=t)
        for l in res1:
            teacher_name.append(l.teacher_name)


    len_c=len(course_id)
    data = []
    j=0
    while j<len_c:
        data.append( {"course_id": course_id[j], "course_name": course_name[j], "teacher_name": teacher_name[j]})
        j+=1

    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")

# 验证是否已经签到
def verIsCheck(request):
    courseId = request.POST.get('courseId')
    studentId = request.POST.get('studentId')
    qiandaoNum = request.POST.get('qiandaoNum')

    print(courseId)#加课码
    print(studentId)#学生id
    print(qiandaoNum)#签到码

    #查询：post_id是已知的（输入的签到码），student_id已知 只需要查 sign_in是否有 有 就已经签到了不用再签了
    sign=models.SignIn.objects.filter(Q(post_id=qiandaoNum) & Q(student_id=studentId))
    if sign.exists():
        #如果结果不为空则表明已经签到了 RESULT=-1为已经签到了
        data = {"RESULT": -1,"post_longitude":-1,"post_latitude":-1,"post_num":-1,"post_date":-1,"post_id":-1}
        return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")
    else:
        #结果为空表明没有签到，则需要获取一些列信息  !!!!由于一直报错  Raw query must include the primary key 放弃
        # sql = "select * from  post_check_in  where  post_num in( select max(post_num) from post_check_in where post_id = " + qiandaoNum + ")"
        # print(sql)
        # res = models.Student.objects.raw(sql)

        #先查询 获取最大的post_num
        res_post_num = models.PostCheckIn.objects.filter(post_id=qiandaoNum)
        # 这里必须注意添加.get('post_num__max'))  否则  错误 int() argument must be a string, a bytes-like object or a number, not 'dict'
        max = int(res_post_num.aggregate(Max('post_num')).get('post_num__max'))
        #根据post_num和post_id查询
        res4 = models.PostCheckIn.objects.filter(Q(post_num=max) & Q(post_id=qiandaoNum))

        if res4.exists():
            for r in res4:
                post_id=r.post_id
                post_date=r.post_date
                post_num=r.post_num
                post_longitude=r.post_longitude
                post_latitude=r.post_latitude
                data = {"RESULT": 1, "post_longitude": post_longitude, "post_latitude": post_latitude, "post_num": post_num, "post_date": post_date,
                        "post_id": post_id}
                return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")
        else:
            #此时结果为空表明postID不正确
            data = {"RESULT": 0, "post_longitude": -1, "post_latitude": -1, "post_num": -1, "post_date": -1, "post_id": -1}
            return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")

    data = {"RESULT": 0, "post_longitude": -1, "post_latitude": -1, "post_num": -1, "post_date": -1, "post_id": -1}
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")

#学生端进行数字签到
def numQiandaoS(request):
    post_id = request.POST.get('post_id')
    post_num = request.POST.get('post_num')
    post_type = request.POST.get('post_type')
    student_id = request.POST.get('student_id')

    print(post_id)
    print(post_num)
    print(post_type)
    print(student_id)

    # 查询获取做大的sign_id
    res = models.SignIn.objects.all()
    if res.exists():
        sign_id = int(res.aggregate(Max('sign_id')).get('sign_id__max')) + 1
    else:
        sign_id=1
    # 插入
    opreateAdd = models.SignIn(sign_id=sign_id, student_id=student_id, post_type=post_type, post_num=post_num,
                               post_id=post_id)
    opreateAdd.save()

    data = {"RESULT": 1}
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")

#学生考勤的签到列表，显示学生哪一次签到哪一次没有
def stuKaoQinList(request):
    courseId = request.POST.get('courseId')

    post_id = []
    post_num = []
    post_date = []
    IsCheck = []

    # 查询course_id 对应的所有签到记录 按照post_num排序
    res0 = models.PostCheckIn.objects.filter(course_id=courseId).order_by("-post_num")
    for r in res0:
        post_id.append(r.post_id)
        post_num.append(r.post_num)
        post_date.append(r.post_date)

    # 根据post_id 判断是否签到了
    for i in post_id:
        res1 = models.SignIn.objects.filter(post_id=i)
        if res1.exists():
            IsCheck.append("出勤")
        else:
            IsCheck.append("缺勤")

    len_c = len(post_id)
    data = []
    j = 0
    while j < len_c:
        data.append({"post_num": post_num[j], "post_date": post_date[j], "IsCheck": IsCheck[j]})
        j += 1

    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")

#这个课号所有的签到发布情况
def teaCourseFabu(request):
    courseId = request.POST.get('courseId')

    post_id = []
    post_num = []
    post_date = []
    num = []

    # 查询course_id 对应的所有签到记录 按照post_num排序
    res0 = models.PostCheckIn.objects.filter(course_id=courseId).order_by("-post_num")
    for r in res0:
        post_id.append(r.post_id)
        post_num.append(r.post_num)
        post_date.append(r.post_date)

    # 根据post_id 判断是否签到了
    for i in post_id:
        res1 = models.SignIn.objects.filter(post_id=i)
        if res1.exists():
            # 如果存在就遍历统计人数
            num.append(res1.count())
        else:
            num.append(0)

    len_c = len(post_id)
    data = []
    j = 0
    while j < len_c:
        data.append({"post_num": post_num[j], "post_date": post_date[j], "num": num[j], "post_id": post_id[j]})
        j += 1

    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")

#该次签到中谁签了
def whoQiandao(request):
    courseId = request.POST.get('courseId')
    postId = request.POST.get('postId')

    student_id = []
    student_name = []
    CheckStatu = []
    num = []

    # 通过course_id 在SC表中找到该课程所有的学生（student_id）
    res0 = models.StudentCourse.objects.filter(course_id=courseId)
    for r0 in res0:
        student_id.append(r0.student_id)

    # 由student_id 在 student 中找到姓名
    for si in student_id:
        res1 = models.Student.objects.filter(student_id=si)
        for r1 in res1:
            student_name.append(r1.student_name)

    # 由post_id、 student_id 在 sign_in 中查询有则出勤否则反之
    len_c = len(student_id)  # 班级选课总人数
    i = 0
    while i < len_c:  # 进行n 次查询
        res2 = models.SignIn.objects.filter(Q(student_id=student_id[i]) & Q(post_id=postId))
        if res2.exists():
            CheckStatu.append("出勤")
        else:
            CheckStatu.append("缺勤")
        i += 1

    data = []
    j = 0
    while j < len_c:
        data.append({"student_id": student_id[j], "student_name": student_name[j], "CheckStatu": CheckStatu[j]})
        j += 1

    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")

#教师发布课程
def teaPostCourse(request):
    courseId = request.POST.get('courseId')
    courseName = request.POST.get('courseName')
    teacherId = request.POST.get('teacherId')

    # 检验courseId是否存在 存在返回0 不存在则插入成功返回1
    res0 = models.Course.objects.filter(course_id=courseId)
    if res0.exists():
        data = {"RESULT": 0}
        return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")
    else:
        opreateAdd = models.Course(teacher_id=teacherId, course_id=courseId, course_name=courseName)
        opreateAdd.save()
        print("over!")
        data = {"RESULT": 1}
        return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")

    data = {"RESULT": -1}
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")


#学生添加课程
def stuAddCourse(request):
    courseId = request.POST.get('courseId')
    studentId = request.POST.get('studentId')

    # 检验courseId是否存在 存在返回0 不存在则插入成功返回1
    res0 = models.StudentCourse.objects.filter(course_id=courseId)
    if res0.exists():
        data = {"RESULT": 0}
        return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")
    else:
        # 查询最大的stu_course_id 以及
        res1 = models.StudentCourse.objects.all()
        if res1.exists():
            stu_course_id = int(res1.aggregate(Max('stu_course_id')).get('stu_course_id__max')) + 1
        else:
            stu_course_id = 1

        # 查询学号对应的index
        res2 = models.Student.objects.filter(student_id=studentId)
        if res2.exists():
            for r in res2:
                stu_index = r.stu_index
            #插入操作
            opreateAdd = models.StudentCourse(stu_course_id=stu_course_id, course_id=courseId, student_id=studentId,
                                              stu_index=stu_index)
            opreateAdd.save()
            data = {"RESULT": 1}
            return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")
        else:
            data = {"RESULT": -1}
            return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")

    data = {"RESULT": -1}
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")

#教师发布数字签到
def teaPostNumCheck(request):
    post_id = request.POST.get('post_id')
    post_date = request.POST.get('post_date')
    course_id = request.POST.get('course_id')
    post_longitude = request.POST.get('post_longitude')
    post_latitude = request.POST.get('post_latitude')


    #查询是否已经存在该条记录
    res2 = models.PostCheckIn.objects.filter(post_id=post_id)
    if res2.exists():
        data = {"RESULT": 0}
        return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")

    # 由course_id 查询 post_num
    res1 = models.PostCheckIn.objects.filter(course_id=course_id)
    if res1.exists():
        post_num = int(res1.aggregate(Max('post_num')).get('post_num__max')) + 1
    else:
        post_num = 1

    # 有course_id 查询teacher_id
    res0 = models.Course.objects.filter(course_id=course_id)
    if res0.exists():
        for r in res0:
            teacher_id = r.teacher_id
        opreateAdd = models.PostCheckIn(post_id=post_id, post_date=post_date, course_id=course_id, post_num=post_num,
                                    teacher_id=teacher_id, post_longitude=post_longitude, post_latitude=post_latitude)
        opreateAdd.save()
        print("over!")
        data = {"RESULT": 1}
        return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")

    data = {"RESULT": -1}
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")

def demotest(request):
    postId="123"
    sql = "select post_id , post_date, post_num , post_longitude , post_latitude " \
          "from  post_check_in  where  post_num in( select max(post_num) from post_check_in where post_id = " + postId +")"
    print(sql)

    fpath = request.POST.get('file_save_path_InServer')  # 至指定到文件夹
    fname = request.POST.get('file_name_InSFolder')  # 文件在指定文件夹中的名字
    studentId = request.POST.get('studentId')  # 识别时哪一个学生
    # 保存照片到指定文件夹下
    try:
        image = request.FILES.get('file')

        # 方案一
        # if image.size>1000 and image.size<20480000:
        #     path=default_storage.save(file_save_path_InServer+image.name,ContentFile(image.read()))
        #     destination =os.path.join(settings.MEDIA_ROOT,path)
        # else:
        #     print("no")

        # 方案二
        # destination = open(os.path.join("E:\\upload", myFile.name), 'wb+')  # 打开特定的文件进行二进制的写操作

        destination = open(os.path.join(fpath, fname), 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in image.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
    except:
        data = {"RESULT": -1}
        return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")

    # 查询获取学生的index
    studentIndex = -1
    res = models.Student.objects.filter(student_id=studentId)
    for s in res:
        studentIndex = s.student_id

    print(studentIndex)
    # 上传成功后进行 班级树的重新构建
    # TODO addStudent(fpath, fname, studentIndex)

    data = {"RESULT": 1}
    return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")




    # studentId = request.GET.get('studentId')
    #
    # print(studentId)
    # course_id = []
    # course_name = []
    # teacher_id = []
    # teacher_name = []
    #
    # # 查询所选课程的所有id
    # res0 = models.StudentCourse.objects.filter(student_id=studentId)
    # for r in res0:
    #     course_id.append(r.course_id)
    #
    # # 根据id 获取老师名称和课程名
    # for i in course_id:
    #     res1 = models.Course.objects.filter(course_id=i)
    #     for c in res1:
    #         course_name.append(c.course_name)
    #         teacher_id.append(c.teacher_id)
    #
    # # 根据teacher_id 查询teacher_name
    # for t in teacher_id:
    #     res1 = models.Teacher.objects.filter(teacher_id=t)
    #     for l in res1:
    #         teacher_name.append(l.teacher_name)
    #
    # len_c = len(course_id)
    # data = []
    # j = 0
    # while j < len_c:
    #     data.append({"course_id": course_id[j], "course_name": course_name[j], "teacher_name": teacher_name[j]})
    #     j += 1
    #
    # return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")


    #     res1 = models.StudentCourse.objects.all()
    #     if res1.exists():
    #         stu_course_id = int(res1.aggregate(Max('stu_course_id')).get('stu_course_id__max')) + 1
    #     else:
    #         stu_course_id =1
    #
    #     #查询学号对应的index
    #     res2 = models.Student.objects.filter(student_id=studentId)
    #     if res2.exists():
    #         for r in res2:
    #             stu_index=r.stu_index
    #         opreateAdd = models.StudentCourse(stu_course_id=stu_course_id, course_id=courseId, student_id=studentId,stu_index=stu_index)
    #         opreateAdd.save()
    #
    #     else:
    #         data = {"RESULT": -1}
    #         return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")
    #
    # data = {"RESULT": -1}
    # return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")


    # student_id = []
    # student_name=[]
    # CheckStatu = []
    # num = []
    #
    # #通过course_id 在SC表中找到该课程所有的学生（student_id）
    # res0 = models.StudentCourse.objects.filter(course_id=courseId)
    # for r0 in res0:
    #     student_id.append(r0.student_id)
    #
    # #由student_id 在 student 中找到姓名
    # for si in student_id:
    #     res1 = models.Student.objects.filter(student_id=si)
    #     for r1 in res1:
    #         student_name.append(r1.student_name)
    #
    # #由post_id、 student_id 在 sign_in 中查询有则出勤否则反之
    # len_c=len(student_id)#班级选课总人数
    # i=0
    # while i<len_c:      #进行n 次查询
    #     res2 = models.SignIn.objects.filter(Q(student_id=student_id[i]) & Q(post_id=postId))
    #     if res2.exists():
    #         CheckStatu.append("出勤")
    #     else:
    #         CheckStatu.append("缺勤")
    #     i+=1
    #
    #
    # data = []
    # j=0
    # while j<len_c:
    #     data.append( {"student_id": student_id[j], "student_name": student_name[j], "CheckStatu": CheckStatu[j]})
    #     j+=1
    #
    # return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json,charset=utf-8")

    # # 查询教师姓名
    # teacher = models.Teacher.objects.filter(teacher_id=studentId)
    # for t in teacher:
    #     teacher_name = t.teacher_name
    # print(teacher_name)
    #
    # course_id = []
    # course_name = []
    # i = 0
    # course = models.Course.objects.filter(teacher_id=studentId)
    # print(type(course), course)
    # for c in course:
    #     course_id.append(c.course_id)
    #     course_name.append(c.course_name)
    #
    # len_id = len(course_id)
    # data = []
    # j = 0
    # while j < len_id:
    #     data.append({"course_name": course_name[j], "course_id": course_id[j], "teacher_name": teacher_name})
    #     j += 1

    # return HttpResponse("ok")

































