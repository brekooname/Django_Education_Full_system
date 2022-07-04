from django import template
import math
from django.db.models import Sum
from app.models import Review
from app.models import User_Profile
register = template.Library()

@register.simple_tag
def rating_calculate(rating):
    if rating > 0:
        c = ((100 * int(rating)) / 10) * 2
    return c

@register.simple_tag
def rating_average(rating,review):
    average = str(int(rating) / int(review))
    return average[0:3]

@register.simple_tag
def star_rating_average(rating,review):
    average = int(rating) / int(review)
    if average > 0:
        c = ((100 * int(average)) / 10) * 2
    return c

@register.simple_tag
def Course_page_rating_average(review):
    rating = review.aggregate(sum=Sum('review_rate'))
    total_review = review.count()
    if rating['sum'] != None:
        avg = (int(rating['sum']) / total_review) * 20
        return avg
    else:
        return 0

@register.simple_tag
def author_course_review(course):
    review_count = 0
    for c in course:
        r = Review.objects.filter(course__slug=c.slug).all().count()
        review_count += r
    return review_count

@register.simple_tag
def author_course_avg_rating(course):
    rating = 0
    count = 0
    for c in course:
        r = Review.objects.filter(course__slug=c.slug).aggregate(sum=Sum('review_rate'))
        c = Review.objects.filter(course__slug=c.slug).all().count()
        if r['sum'] != None:
            rating += r['sum']
            count += c

    return str(rating/count)[0:3]

@register.simple_tag
def review_user_profile(user):
    user_profile = User_Profile.objects.filter(user=user)
    if user_profile.exists():
        return user_profile.first().profile_image
    else:
        print(user_profile.first)
        return None
