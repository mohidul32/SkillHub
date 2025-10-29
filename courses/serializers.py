from rest_framework import serializers
from .models import Course, Lesson, Category
from django.conf import settings
User = settings.AUTH_USER_MODEL  # not used directly here but note

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content', 'video_url', 'order', 'created_at']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description']

class CourseListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    instructor = serializers.StringRelatedField(read_only=True)
    num_students = serializers.IntegerField(read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'slug', 'description', 'price', 'is_published', 'category', 'instructor', 'num_students', 'created_at']


class CourseDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    instructor = serializers.StringRelatedField(read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)
    students = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'slug', 'description', 'price', 'is_published', 'category', 'instructor', 'lessons', 'students', 'created_at']
