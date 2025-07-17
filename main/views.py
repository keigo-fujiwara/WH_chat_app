from django.contrib import auth
from django.shortcuts import  get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from .models import Talk, User

from .forms import (
    LoginForm, 
    SignUpForm, 
    TalkForm, 
    UsernameChangeForm,
    EmailChangeForm
)

def index(request):
    return render(request, "main/index.html")


def signup(request):
    if request.method == "GET":
        form = SignUpForm()
    elif request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]

            user = auth.authenticate(username=username, password=password)

            if user:
                auth.login(request, user)

            return redirect("index")

    context = {"form": form}
    return render(request, "main/signup.html", context)


@csrf_exempt
def login_view(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "main/login.html", {"form": form})
    elif request.method == "POST":
        form = LoginForm(request.POST)
        print(f"POST data: {request.POST}")  # デバッグ用
        print(f"Form is valid: {form.is_valid()}")  # デバッグ用
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            print(f"Username: {username}")  # デバッグ用
            user = auth.authenticate(username=username, password=password)
            print(f"User authenticated: {user}")  # デバッグ用
            if user:
                auth.login(request, user)
                print("Login successful, redirecting to friends")  # デバッグ用
                return redirect("friends")
            else:
                form.add_error(None, "ユーザー名とパスワードが一致しません。")
        else:
            # フォームが無効な場合のエラーメッセージを追加
            print(f"Form errors: {form.errors}")  # デバッグ用
            print(f"Form non_field_errors: {form.non_field_errors()}")  # デバッグ用
            print(f"Form field errors: {form.field_errors}")  # デバッグ用
            # フォームが無効な場合は、エラーメッセージを直接テンプレートに渡す
            context = {"form": form, "error_message": "フォームの入力に問題があります。"}
            return render(request, "main/login.html", context)
        return render(request, "main/login.html", {"form": form})

@login_required
def friends(request):
    friends = User.objects.exclude(id=request.user.id)
    context = {"friends": friends}
    print(friends)
    return render(request, "main/friends.html", context)


@login_required
def talk_room(request, user_id):
    friend = get_object_or_404(User, id=user_id)
    
    talks = Talk.objects.filter(
        Q(sender=request.user, receiver=friend)
        | Q(sender=friend, receiver=request.user)
    ).order_by("time")

    if request.method == "GET":
        form = TalkForm()
    elif request.method == "POST":
        form = TalkForm(request.POST)
        if form.is_valid():
            new_talk = form.save(commit=False)
            new_talk.sender = request.user
            new_talk.receiver = friend
            new_talk.save()
            return redirect("talk_room", user_id)

    context = {
        "form": form,
        "friend": friend,
        "talks": talks,
    }
    return render(request, "main/talk_room.html", context)


@login_required
def settings(request):
    return render(request, "main/settings.html")

@login_required
def username_change(request):
    if request.method == "GET":
        # instance を指定することで、指定したインスタンスのデータにアクセスできます
        form = UsernameChangeForm(instance=request.user)
    elif request.method == "POST":
        form = UsernameChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            # 保存後、完了ページに遷移します
            return redirect("username_change_done")

    context = {"form": form}
    return render(request, "main/username_change.html", context)


@login_required
def username_change_done(request):
    return render(request, "main/username_change_done.html")

@login_required
def email_change(request):
    if request.method == "GET":
        form = EmailChangeForm(instance=request.user)
    elif request.method == "POST":
        form = EmailChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("email_change_done")

    context = {"form": form}
    return render(request, "main/email_change.html", context)


@login_required
def email_change_done(request):
    return render(request, "main/email_change_done.html")

class PasswordChangeView(auth_views.PasswordChangeView):
    """Django 組み込みパスワード変更ビュー

    template_name : 表示するテンプレート
    success_url : 処理が成功した時のリダイレクト先
    """

    template_name = "main/password_change.html"
    success_url = reverse_lazy("password_change_done")


class PasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    """Django 標準パスワード変更ビュー"""

    template_name = "main/password_change_done.html"

@csrf_exempt
def logout_view(request):
    auth.logout(request)
    return redirect("index")