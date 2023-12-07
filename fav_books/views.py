from django.shortcuts import render,redirect
from .models import *
import bcrypt
from django.contrib import messages

def form(request):
    return render(request,"form.html")

def register(request):
    errors = user.objects.validator(request.POST)
    if len(errors) > 0:
        for key,value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        passwd = request.POST['pass']
        hashed_pwd= bcrypt.hashpw(passwd.encode(), bcrypt.gensalt()).decode()
        X =user.create(
            first=request.POST['fname'],
            last=request.POST['lname'],
            email=request.POST['email'],
            birth=request.POST['bdate'],
            pwd=hashed_pwd
        )
        request.session['id'] = X.id
        request.session['username'] = X.first_name
    return redirect("/main")

def login(request):
    check_user = user.objects.filter(email=request.POST['e-mail'])
    if check_user:
        logged_user = check_user[0]
        if bcrypt.checkpw(request.POST['passwd'].encode(),logged_user.password.encode()):
            request.session['id'] = logged_user.id
            request.session['username'] = logged_user.first_name
            return redirect("/main")
        else:
            messages.error(request,"Invalid password")
            return redirect("/")
    else:
        messages.error(request,"Invalid email")
        return redirect("/")

def logout(request):
    request.session.flush()
    return redirect("/")

def main(request):
    if not 'id' in request.session:
        messages.error(request,"No user logged in")
        return redirect("/")
    else:
        context={
            "allbooks":book.show_all(),
            "loggeduser":user.show_logged(request.session['id']),
        }
        return render(request,"main.html",context)

def book_create(request):
    errors2 = book.objects.validator2(request.POST)
    if len(errors2) > 0:
        for key,value in errors2.items():
            messages.error(request, value)
        return redirect("/main")
    else:
        X =book.create(
            request.POST['title'],
            request.POST['desc'],
            request.session['id']
        )
        messages.success(request, "Book successfully created")
        book.fav(
            request.session['id'],
            X.id
        )
        return redirect("/main")

def show_book(request,id):
    if not 'id' in request.session:
        messages.error(request,"No user logged in")
        return redirect("/")
    else:
        owner = book.objects.get(id=id)
        context={
                "onebook":book.show(id),
                "loggeduser":user.show_logged(request.session['id']),
            }
        if owner.uploaded_by.id == request.session['id']:
            return render(request,"book_edit.html",context)
        else:
            return render(request,"book_id.html",context)

def destroy(request,id):
    book.destroy(id)
    return redirect("/main")

def update_book(request): 
    errors = book.objects.validator2(request.POST)
    if len(errors) > 0:
        for key,value in errors.items():
            messages.error(request, value)
        return redirect("/book/"+request.POST['onebook_id'])
    book.update(
        request.POST['onebook_id'],    
        request.POST['title'],
        request.POST['desc'],
    )
    return redirect("/book/"+request.POST['onebook_id'])

def favorite(request,id):
    book.fav(
            request.session['id'],
            id
        )
    return redirect("/book/"+str(id))

def unfavorite(request,id):
    book.unfav(
            request.session['id'],
            id
        )
    return redirect("/book/"+str(id))

def myfav(request):
    fav_book = book.show_fav(request.session['id'])
    context={
        "fav_books": fav_book
    }
    return render(request, "favbook.html",context)