from django.http.response import Http404
from rest_framework import pagination
from rest_framework import views
from config.settings import SIMPLE_JWT
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Author, Post
from .serializers import AuthorSerializer, LoginSerializer, PostSerializer,RegisterSerializer
from django.contrib.auth.hashers import make_password,check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated,AllowAny
from .tokens import decode_token
from .paginations import PagePaginationCustom
from config import settings
"""
    RegisterView Will take 4 data:
    name:
    email:
    password:
    password1:
    Register the new Author
"""
class RegisterView(APIView):
    permission_classes =[AllowAny]
    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not Author.objects.filter(email= serializer.validated_data['email']).exists():
            password = serializer.validated_data['password']
            password1 = serializer.validated_data['password1']
            if password == password1:
                hash_password = make_password(password,salt=None,hasher='default')
                author = Author(name = serializer.validated_data['name'],email=serializer.validated_data['email'],password =hash_password)
                author.save()
                return Response(serializer.data)
        else:
            return Response({'message':'User already exists'})


"""
    loginView check where the login data is valid or not and give access and refresh token if the author is valid
"""
class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            author = Author.objects.get(email=serializer.validated_data['email'])
            password = serializer.validated_data['password']
            # checking if the author exist or not!
            if author is None:
                raise AuthenticationFailed("Author does not exist!!")
            
            # checking password is correct or not
            if not check_password(password,author.password):
                raise AuthenticationFailed("Password is Incorrect")
            refresh = RefreshToken.for_user(author)
            
            return Response({
                'access':str(refresh.access_token),
                'refresh':str(refresh)
            })
        else:
            raise AuthenticationFailed("Error")











"""
    AuthorListView list the author that have been register in the database
"""
class AuthorListView(APIView,PagePaginationCustom):
    serializer_class = AuthorSerializer
    permission_classes=[IsAuthenticated]
    def get(self,request):
        author = Author.objects.all()
        result = self.paginate_queryset(author,request,view=self)
        serializer = AuthorSerializer(result, many=True)
        return self.get_paginated_response(serializer.data)
   


"""
    PostListView list the post that is in database
    It allow get post http request
    get gives all the data that are available in database
    post take the data from author and store that data
    post take following data:
    title:
    body:
"""
class PostListView(APIView,PagePaginationCustom):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    def get(self,request):
        posts = Post.objects.all()
        result = self.paginate_queryset(posts,request,view=self)
        serializer = PostSerializer(result, many=True)
        # print(serializer.data)
        return self.get_paginated_response(serializer.data)

    
    def post(self,request):
        serializer=PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        payload = decode_token(request)
        # print(payload)

        # getting the user_id from payload
        user_id = payload.get("user_id") 

        # inserting serializers data in post database and creating post instances
        post = Post(title = serializer.validated_data['title'],body = serializer.validated_data['body'],author=Author.objects.get(id=user_id))

        # saving the post instances
        post.save()
        return Response(serializer.data)
    


"""
    PostDetailUpdateDeleteView have get put and delete http methods
    get will get the individual data with the help of primary key
    put will update the data if the author is true or author is the creator of the post
    delete will delete the post if the author is author
    post will take the following data :
    title and body then it will update the data
"""
class PostDetailUpdateDeleteView(APIView):
    # the below function will check where the object with following primary key
    def get_object(self,pk):
        try:
            return Post.objects.get(id=pk)                                       # if there is object it will get that object
        except:
            raise Http404      

    def get(self,request,pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self,request,pk):
        # decode the token
        payload = decode_token(request)
        # extracting the user_id from payload
        user_id = payload.get("user_id")
        post = self.get_object(pk)

        #  checking if the user is owner of post or not
        if user_id == post.author_id:
            serializer=PostSerializer(data=request.data,partial=True)
            serializer.is_valid(raise_exception=True)
            if serializer.is_valid():
                post.title=serializer.validated_data['title']
                post.body=serializer.validated_data['body']
            post.save()
            return Response(serializer.data)
        
    def delete(self,request,pk):
                # decode the token
        payload = decode_token(request)
        # extracting the user_id from payload
        user_id = payload.get("user_id")
        post = self.get_object(pk)
        if user_id == post.author_id:
            post.delete()
            return Response("Post deleted")
        return Response("you are not AUTHOR of the post")
