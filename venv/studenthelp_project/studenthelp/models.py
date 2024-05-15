from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import json
from django import forms

class Post(models.Model):
    OFFER = 'offer'
    DEMAND = 'demande'
    TYPE_CHOICES = (
        (OFFER, 'Offer'),
        (DEMAND, 'Demande'),
    )

    FORM_TYPE_CHOICES = (
        ('stage', 'Stage Form'),
        ('housing', 'Housing Form'),
        ('transportation', 'Transportation Form'),
        ('club_event', 'Club Event Form'),
        ('social_event', 'Social Event Form'),
    )

    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100, null=True, blank=True)
    contact_info = models.CharField(max_length=100, null=True, blank=True)
    post_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=OFFER)
    form_type = models.CharField(max_length=20, choices=FORM_TYPE_CHOICES, default='stage')
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    specific_data = models.JSONField(null=True, blank=True)

    def get_specific_data(self):
        if self.specific_data:
            return json.loads(self.specific_data)
        return {}

    def set_specific_data(self, data):
        self.specific_data = json.dumps(data)

    def get_specific_data_fields(self):
        specific_data = self.get_specific_data()
        fields = {}
        if self.form_type == 'stage':
            fields.update({
                'company': forms.CharField(initial=specific_data.get('company')),
                'duration': forms.CharField(initial=specific_data.get('duration')),
                'subject': forms.CharField(initial=specific_data.get('subject')),
                'stage_type': forms.ChoiceField(
                    choices=Stage.STAGE_TYPE_CHOICES,
                    label='Type de stage',
                    initial=specific_data.get('stage_type'),
                    widget=forms.Select(attrs={'class': 'form-control'})
                )
            })
        elif self.form_type == 'housing':
            fields.update({
                'housing_location': forms.CharField(initial=specific_data.get('housing_location')),
                'housing_description': forms.CharField(initial=specific_data.get('housing_description')),
            })
        elif self.form_type == 'transportation':
            fields.update({
                'departure': forms.CharField(initial=specific_data.get('departure')),
                'destination': forms.CharField(initial=specific_data.get('destination')),
                'departure_time': forms.CharField(initial=specific_data.get('departure_time')),
            })
        elif self.form_type == 'club_event':
            fields.update({
                'club': forms.CharField(initial=specific_data.get('club')),
                'specialization': forms.CharField(initial=specific_data.get('specialization')),
                'seat_capacity': forms.IntegerField(initial=specific_data.get('seat_capacity')),
                'club_contact_info': forms.CharField(initial=specific_data.get('club_contact_info')),
            })
        elif self.form_type == 'social_event':
            fields.update({
                'price': forms.DecimalField(initial=specific_data.get('price')),
                'social_contact_info': forms.CharField(initial=specific_data.get('social_contact_info')),
            })
        return fields

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_list')


class Stage(Post):
    OUVRIER = 'ouvrier'
    TECHNICIEN = 'technicien'
    PFE = 'PFE'

    STAGE_TYPE_CHOICES = (
        (OUVRIER, 'Ouvrier'),
        (TECHNICIEN, 'Technicien'),
        (PFE, 'PFE'),
    )

    company = models.CharField(max_length=100)
    duration = models.CharField(max_length=50)
    subject = models.CharField(max_length=100)
    stage_type = models.CharField(max_length=20, choices=STAGE_TYPE_CHOICES)

    def __str__(self):
        return self.title


class Housing(Post):
    housing_location = models.CharField(max_length=100)
    housing_description = models.TextField()


class Transportation(Post):
    departure = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.CharField(max_length=100)


class ClubEvent(Post):
    club = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    seat_capacity = models.IntegerField()
    club_contact_info = models.CharField(max_length=100)


class SocialEvent(Post):
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    social_contact_info = models.CharField(max_length=100)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def delete_comment(self):
        self.delete()

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"



class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    TYPE_CHOICES = (
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('comment_delete', 'Commentaire supprimé')
    )
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    liker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_notifications', null=True, blank=True)

    def mark_as_read(self):
        self.is_read = True
        self.save()

    def __str__(self):
        if self.type == 'like':
            return f"{self.user.username} a aimé votre publication"
        elif self.type == 'comment':
            return f"{self.comment.user.username} a commenté votre publication"
        elif self.type == 'comment_delete':
            return "Votre commentaire a été supprimé"
        else:
            return "Notification inconnue"
        
