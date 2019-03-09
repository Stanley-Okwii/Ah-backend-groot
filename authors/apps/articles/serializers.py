from rest_framework import serializers
from .models import Category, Article
from ..profiles.models import Profile
from ..profiles.serializers import ProfileSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'name',
            'slug',
            'id')
        read_only_fields = ('id', 'slug',)


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    likes = serializers.SerializerMethodField()
    dislikes = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = (
            'id',
            'slug',
            'title',
            'body',
            'description',
            'category',
            'created_at',
            'updated_at',
            'author',
            'likes',
            'dislikes'
        )
        read_only_fields = ('id', 'slug', 'author_id')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = ProfileSerializer(
            Profile.objects.get(user=instance.author),
            read_only=True).data
        representation['category'] = CategorySerializer(instance.category,
                                                        read_only=True).data
        return representation

    # Gets all the articles likes
    def get_likes(self, instance):
        return instance.votes.likes().count()

    # # Gets all the articles dislikes
    def get_dislikes(self, instance):
        return instance.votes.dislikes().count()
