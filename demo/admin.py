from django.contrib import admin
from django.db.models import Sum
from .models import *

# Register your models here.

admin.site.register(Contact_Me_info)
admin.site.register(AddBlogs)
admin.site.register(Department)
admin.site.register(StudentId)
admin.site.register(Student)
admin.site.register(Subject)

class StudentReportCardAdmin(admin.ModelAdmin):
    list_display = ['student','total_marks','student_rank','date_of_report_card']

admin.site.register(StudentReportCard,StudentReportCardAdmin)


class StudentMarksAdmin(admin.ModelAdmin):
    list_display = ['student','subject','marks']

admin.site.register(StudentMarks,StudentMarksAdmin)