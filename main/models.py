from django.contrib.auth.models import AbstractUser
from django.db import models



class MedicalInstitution(models.Model):
    Codeokpo = models.IntegerField(null=True)
    Addokpo = models.IntegerField(null=True)
    Coderjn = models.BigIntegerField(null=True)
    codved = models.IntegerField(null=True)
    Nokpo = models.CharField(max_length=254, null=True)
    LeverOrg = models.IntegerField(null=True)
    prHosp = models.IntegerField(null=True)
    Address = models.CharField(max_length=254, null=True)
    unp = models.IntegerField(null=True)


class User(AbstractUser):
    user_code = models.CharField(max_length=254, null=True)
    is_role = models.IntegerField(null=True)
    medical_institution = models.ForeignKey(MedicalInstitution, on_delete=models.SET_NULL, null=True, blank=True)



class Child(models.Model):
    child_code = models.CharField(max_length=254, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    child_birthday_date = models.DateField()
    child_gender = models.CharField(max_length=254, null=True)
    medical_institution = models.ForeignKey(MedicalInstitution, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)



class Test(models.Model):
    test_identifier = models.CharField(max_length=254)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_tests')
    child = models.ForeignKey(Child, on_delete=models.SET_NULL, null=True, blank=True, related_name='child_tests')
    medical_institution = models.ForeignKey(MedicalInstitution, on_delete=models.SET_NULL, null=True, blank=True, related_name='medical_institution_tests')
    test_code = models.CharField(max_length=254, null=True)
    child_birthday = models.DateField(null=True, blank=True)
    test_date = models.DateTimeField(auto_now_add=True)
    result_test = models.TextField(null=True, blank=True)







