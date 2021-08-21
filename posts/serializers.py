from rest_framework import serializers

class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)
    password1 = serializers.CharField(max_length=100)

class AuthorSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    email = serializers.EmailField()
    name = serializers.CharField(max_length=100)

class PostSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    title = serializers.CharField(max_length=100)
    body = serializers.CharField(max_length=1000)
    author_id = serializers.IntegerField(read_only=True)
    posted_on = serializers.ReadOnlyField()

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()