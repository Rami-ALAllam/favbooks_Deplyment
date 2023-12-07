from django.db import models
import datetime
from datetime import datetime
import re

class userManager(models.Manager):
    def validator(self,postData):
        errors={}
        if len(postData['fname']) < 2:
            errors["fname"] = "first name should be at least 2 characters"
        if len(postData['lname']) < 2:
            errors["lname"] = "last name should be at least 2 characters"

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Invalid email Address"
        if len(user.objects.filter(email = postData['email'])) > 0:
            errors["email"] = "Email address must be unique"

        if postData['bdate'] == "":
            errors["bdate"] = "Birth date is mandatory"
        else:
            bdate = datetime.strptime(postData['bdate'],'%Y-%m-%d')
            date_num1 = datetime.today().year
            date_num2 = bdate.year
            if datetime.today() < bdate:
                errors["bdate"] = "Birth date should be in the past"
            elif (date_num1 - date_num2) < 13:
                errors["bdate"] = "Age should be 13 years old at least"

        if len(postData['pass']) < 8:
            errors["password"] = "password should be at least 8 charcters"
        if postData["con-pass"] != postData['pass']:
            errors["password"] = "Password should be the same"
        return errors

class bookManager(models.Manager):
        def validator2(self,postData):
            errors2={}
            if postData['title'] == "":
                errors2["title"] = "Book title is required"
            if len(book.objects.filter(title= postData['title'])):
                errors2["title"] = "Book title must be unique"
            if len(postData['desc']) < 5:
                errors2["desc"] = "Show description should be at least 5 characters"
            return errors2

class user(models.Model):
    first_name=models.CharField(max_length=45)
    last_name=models.CharField(max_length=45)
    email=models.CharField(max_length=45)
    birth_date=models.DateField()
    password=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=userManager()

    def create(first,last,email,birth,pwd):
        return user.objects.create(
        first_name=first,
        last_name=last,
        email=email,
        birth_date=birth,
        password=pwd
        )
    
    def show_logged(id):
        return user.objects.get(id=id)

class book(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    users_who_like = models.ManyToManyField(user,related_name="liked_books")
    uploaded_by = models.ForeignKey(user, related_name= "uploaded_books", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=bookManager()

    def show_all():
        return book.objects.all()

    def create(title,desc,uploaded_by):
        return book.objects.create(
        title = title,
        desc = desc,
        uploaded_by = user.objects.get(id=uploaded_by)
        )

    def show(id):
        return book.objects.get(id=id)

    def destroy(id):
        b1=book.objects.get(id=id)
        b1.delete()

    def update(editbook_id, title, desc):
        book_update=book.objects.get(id=int(editbook_id))
        book_update.title=title
        book_update.desc=desc
        book_update.save()

    def fav(usr_id,bk_id):
        bk = book.objects.get(id=int(bk_id))
        usr = user.objects.get(id=int(usr_id))
        bk.users_who_like.add(usr)

    def unfav(usr_id,bk_id):
        bk = book.objects.get(id=int(bk_id))
        usr = user.objects.get(id=int(usr_id))
        bk.users_who_like.remove(usr)

    def show_fav(usr_id):
        logged_user = user.objects.get(id=usr_id)
        return logged_user.liked_books.all()