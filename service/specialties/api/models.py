from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True


class University(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, db_index=True)
    region = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class Specialty(BaseModel):
    form_of_education = models.CharField(max_length=255)
    educational_degree = models.CharField(max_length=255)
    branch = models.CharField(max_length=255)
    number_of_spec = models.PositiveIntegerField(default=0)
    name_of_spec = models.CharField(max_length=255)
    faculty = models.CharField(max_length=255)
    educational_program = models.TextField()
    offer_type = models.CharField(max_length=150)
    license_scope = models.PositiveIntegerField(default=0)
    contract = models.PositiveIntegerField(default=0)
    budget = models.PositiveIntegerField(default=0)
    average_contract_mark = models.FloatField()
    average_budget_mark = models.FloatField()
    university = models.ForeignKey(University, on_delete=models.CASCADE,
                                   related_name='specialty_list')
    time_of_study = models.PositiveIntegerField()
    examination_coefficients = models.JSONField(blank=True)
    slug = models.SlugField(db_index=True, null=True)
    characteristic = models.TextField()
    future = models.TextField()

    class Meta:
        ordering = ('-average_budget_mark',)

    def __str__(self):
        return f"{self.name_of_spec}({self.number_of_spec}) - {self.slug}"


class Comment(BaseModel):
    author = models.CharField(max_length=20)
    content = models.TextField(max_length=400)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    specialty = models.ForeignKey(
        Specialty, on_delete=models.CASCADE, related_name='comments', null=True)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return f"{self.author}({self.created_at})"
