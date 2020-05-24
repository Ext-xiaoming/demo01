
# python .\manage.py inspectdb
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Course(models.Model):
    course_id = models.IntegerField(primary_key=True)
    course_name = models.CharField(max_length=255)
    teacher = models.ForeignKey('Teacher', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'course'


class PicServer(models.Model):
    picture_id = models.IntegerField(primary_key=True)
    pic = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pic_server'


class PostCheckIn(models.Model):
    post_id = models.CharField(primary_key=True, max_length=11)
    teacher_id = models.IntegerField(blank=True, null=True)
    post_date = models.CharField(max_length=255, blank=True, null=True)
    post_num = models.IntegerField(blank=True, null=True)
    course_id = models.IntegerField(blank=True, null=True)
    post_type = models.IntegerField(blank=True, null=True)
    post_longitude = models.CharField(max_length=255, blank=True, null=True)
    post_latitude = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'post_check_in'


class ResPic(models.Model):
    res_id = models.IntegerField(primary_key=True)
    res_pic_1 = models.CharField(max_length=255, blank=True, null=True)
    res_pic_2 = models.CharField(max_length=255, blank=True, null=True)
    res_pic_3 = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'res_pic'


class SignIn(models.Model):
    sign_id = models.IntegerField(primary_key=True)
    student_id = models.IntegerField(blank=True, null=True)
    post_type = models.IntegerField(blank=True, null=True)
    post_num = models.IntegerField(blank=True, null=True)
    post_id = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sign_in'


class StuPic(models.Model):
    stu_id = models.IntegerField(primary_key=True)
    stu_picture = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stu_pic'


class Student(models.Model):
    student_id = models.IntegerField(primary_key=True)
    stu_index = models.IntegerField()
    student_name = models.CharField(max_length=255)
    student_password = models.CharField(max_length=255, blank=True, null=True)
    student_phone = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'student'


class StudentCourse(models.Model):
    stu_course_id = models.IntegerField(primary_key=True)
    course = models.ForeignKey(Course, models.DO_NOTHING, blank=True, null=True)
    student = models.ForeignKey(Student, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'student_course'


class Teacher(models.Model):
    teacher_id = models.IntegerField(primary_key=True)
    tea_index = models.CharField(max_length=255)
    teacher_name = models.CharField(max_length=255, blank=True, null=True)
    teacher_password = models.CharField(max_length=255, blank=True, null=True)
    teacher_phone = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'teacher'


class TeacherPostPic(models.Model):
    teacher_post_pic_id = models.IntegerField(blank=True, null=True)
    teacher_pic = models.TextField(blank=True, null=True)
    course_id = models.IntegerField(blank=True, null=True)
    post_num = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'teacher_post_pic'
