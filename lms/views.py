from locale import currency
from unicodedata import category
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from app.models import Categories, Author, Course, Level, Usercourse, Video, Lesson, Payment, Review, Blog
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Sum
import razorpay
from .settings import *
from time import time
from django.views.decorators.csrf import csrf_exempt

client = razorpay.Client(auth=(KEY_ID,KEY_SECRET))

def BASE(request):
    return render(request,'base.html')

def HOME(request):

    course = Course.objects.filter(status="PUBLISH").order_by('-id')[0:8]

    category = Categories.objects.all().order_by('-id')[:8]
    author = Author.objects.all().order_by('-id')[:10]
    blog = Blog.objects.all().order_by('-id')[:3]

    data = {
        'category':category,
        'author':author,
        'course':course,
        'blog':blog,
    }

    return render(request,'Main/home.html',data)

def CONTACT_US(request):
    return render(request,'Main/contact-us.html')

def ABOUT_US(request):
    return render(request,'Main/about-us.html')

def COURSES(request):
    course = Course.objects.filter(status="PUBLISH")
    category = Categories.objects.all().order_by('id') 
    author = Author.objects.all().order_by('id')
    level = Level.objects.all().order_by('id')

    paginator = Paginator(course,9)
    page_no = request.GET.get('page')

    CourseFinal = paginator.get_page(page_no)
    total_page = CourseFinal.paginator.num_pages
    
    data = {
        'course':CourseFinal,
        'total_page':total_page,
        'category':category,
        'author':author,
        'level':level,
    }
    return render(request,'Main/courses.html',data)

def SEARCH(request):
    data = {

    }
    if request.method == "GET":
        search = request.GET.get('query')
        course = Course.objects.filter(title__icontains=search)
        data = {
            'course':course
        }

    return render(request,'search/search.html',data)

def FILLTER_DATA(request):

    category = request.GET.get('category')
    # print(category)
    if category:
        course = Course.objects.filter(category__id__in=category).order_by('-id')[0:8]
    else:
        course = Course.objects.all().order_by('-id')[0:8]

    data  = {
        'course':course
    }
    t = render_to_string('ajax/course.html',data)

    return JsonResponse({'data': t})

def FILLTER_DATA_ALL(request):

    category = request.GET.getlist('category[]')
    author = request.GET.getlist('instructors[]')
    level = request.GET.getlist('level[]')
    price = request.GET.getlist('price[]')

    # print(category)
    if price == ['All']:
        course = Course.objects.all().order_by('id')
    elif price == ['Paid']:
        course = Course.objects.filter(price__gte=1).order_by('-id')
    elif price == ['Free']:
        course = Course.objects.filter(price=0).order_by('-id')
    elif category:
        course = Course.objects.filter(category__id__in=category).order_by('-id')
    elif author:
        course = Course.objects.filter(author__id__in=author).order_by('-id')
    elif level:
        course = Course.objects.filter(level__id__in=level).order_by('-id')
    else:
        course = Course.objects.all().order_by('id')

    data  = {
        'course':course,
    }
    t = render_to_string('ajax/all-course.html',data)

    return JsonResponse({'data': t})

def ERROR(request,slug):
    return render(request,"error/404.html")

def COURSE_DETAIL(request,slug):
    course = Course.objects.filter(slug=slug)
    time_duration = Video.objects.filter(course__slug=slug).aggregate(sum=Sum('time_duration'))
    lessoncount = Lesson.objects.filter(course__slug=slug).all().count()
    courseid = Course.objects.get(slug=slug)
    enrol_student_count = Usercourse.objects.filter(course=courseid).all().count()
    rating_total = Review.objects.filter(course__slug=slug).aggregate(sum=Sum('review_rate'))
    review_total = Review.objects.filter(course__slug=slug).all().count()

    try:
        checkenroll = Usercourse.objects.get(user=request.user,course=courseid)
    except Usercourse.DoesNotExist:
        checkenroll = None
    

    if course.exists():
        data = {
            'course':course.first,
            'checkenroll':checkenroll,
            'time_duration':time_duration,
            'lessoncount':lessoncount,
            'enrol_student_count':enrol_student_count,
            'rating_total':rating_total,
            'review_total':review_total,
        }
        return render(request,"course/detail_course.html",data)
    else:
        return redirect('404')

def MYCOURSE(request):
    course = Usercourse.objects.filter(user=request.user)
    data = {
        'course':course,
    }

    return render(request,"course/mycourse.html",data)

def CHECKOUT(request,slug):
    course = Course.objects.get(slug=slug)
    action = request.GET.get('action')
    order = None

    if course.price == 0:
        course = Usercourse(
            user=request.user,
            course=course,
        )
        course.save()
        messages.success(request,'Course Enroll Successfully !')
        return redirect('mycourse')
    elif action == 'create_payment':
        if request.method == "POST":
            first_name = request.POST.get('billing_first_name')
            last_name = request.POST.get('billing_last_name')
            country = request.POST.get('billing_country')
            add_1 = request.POST.get('billing_address_1')
            add_2 = request.POST.get('billing_address_2')
            city = request.POST.get('billing_city')
            state = request.POST.get('billing_state')
            postcode = request.POST.get('billing_postcode')
            phone = request.POST.get('billing_phone')
            email = request.POST.get('billing_email')
            order_comments = request.POST.get('order_comments')

            dis_price = course.price - (course.price * course.discount / 100)
            amount = int(dis_price) * 100
            currency = "INR"
            notes = {
                "name":f'{first_name} {last_name}',
                "country":country,
                "address":f'{add_1} {add_2}',
                "city":city,
                "state":state,
                "postcode":postcode,
                "phone":phone,
                "email":email,
                "order_comments":order_comments,
            }
            receipt = f"Skola-{int(time())}"

            order = client.order.create({
                'receipt':receipt,
                'notes':notes,
                'amount':amount,
                'currency':currency,
            })
            payment = Payment(
                course=course,
                user=request.user,
                order_id=order.get('id')
            )

            payment.save()

    data = {
        'course':course,
        'order':order,
    }

    return render(request,'checkout/checkout.html',data)

@csrf_exempt
def VERIFY_PAYMENT(request):
    if request.method == "POST":
        data = request.POST
        try:
            client.utility.verify_payment_signature(data)
            razorpay_order_id = data['razorpay_order_id']
            razorpay_payment_id = data['razorpay_payment_id']
            
            payment = Payment.objects.get(order_id = razorpay_order_id)
            payment.payment_id = razorpay_payment_id
            payment.status = True

            usercourse = Usercourse(
                user = payment.user,
                course = payment.course,
            )
            usercourse.save()
            payment.user_course = usercourse
            payment.save()

            context = {
                'data':data,
                'payment':payment,
            }
            return render(request,'verify_payments/success.html',context)

        except:
            return render(request,'verify_payments/fail.html')
    return None

def REVIEW(request,slug):
    if request.method == "POST":
        course = Course.objects.filter(slug=slug)
        blog = Blog.objects.filter(slug=slug)
        user = request.user
        rating = request.POST.get('rating')
        title = request.POST.get('title')
        content = request.POST.get('content')

        if course.exists():
            review = Review(
                user=user,
                course=course.first(),
                review_rate=rating,
                review_title=title,
                review_content=content,
            )
            review.save()
            return redirect('courses')
        elif blog.exists():
            review = Review(
                user=user,
                blog=blog.first(),
                review_rate=rating,
                review_title=title,
                review_content=content,
            )
            review.save()
            return redirect('home')
        else:
            return redirect('home')

    return redirect('courses')

def AUTHOR_PROFILE(request,id):
    author = Author.objects.filter(id=id)
    if author.exists():

        data = {
            'author':author.first,
        }

        return render(request,'author/author.html',data)
    else:
        return redirect('home')
def BLOG_DETAIL(request,slug):
    blog = Blog.objects.filter(slug=slug)
    if blog.exists():
        data = {
            'blog':blog.first,
        }
        return render(request,'blog/blog.html',data)
    
    else:
        return redirect('home')
    