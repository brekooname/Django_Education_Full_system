from django.contrib import admin

from app.models import Categories, Author, Course, Level, Language, Requirement, What_you_learn, Lesson, Video, Usercourse, Payment, Review, User_Profile, Blog


class What_you_learn_tublar(admin.TabularInline):
    model = What_you_learn

class Requirement_tublar(admin.TabularInline):
    model = Requirement

class Lesson_tublar(admin.TabularInline):
    model = Lesson

class Video_tublar(admin.TabularInline):
    model = Video

class course_admin(admin.ModelAdmin):
    inlines = (What_you_learn_tublar,Requirement_tublar,Lesson_tublar,Video_tublar)

# Register your models here.
admin.site.register(Categories)
admin.site.register(Author)
admin.site.register(Course,course_admin)
admin.site.register(Level)
admin.site.register(Language)
admin.site.register(Requirement)
admin.site.register(What_you_learn)
admin.site.register(Lesson)
admin.site.register(Usercourse)
admin.site.register(Payment)
admin.site.register(Review)
admin.site.register(User_Profile)
admin.site.register(Blog)
