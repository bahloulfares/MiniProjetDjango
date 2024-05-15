from django import forms
from .models import Stage, Housing, Transportation, ClubEvent, SocialEvent, Post, Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class PostTypeForm(forms.Form):
    TYPE_CHOICES = (
        ('stage', 'Stage'),
        ('housing', 'Logement'),
        ('transportation', 'Transport'),
        ('club_event', 'Événement de club'),
        ('social_event', 'Événement social'),
    )
    type = forms.ChoiceField(choices=TYPE_CHOICES, label='Type de publication', widget=forms.Select(attrs={'class': 'form-control'}))

class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

class StageForm(BaseForm):
    class Meta:
        model = Stage
        fields = ['image', 'title', 'description', 'location', 'contact_info', 'post_type', 'company', 'duration', 'subject', 'stage_type']
    
    def __init__(self, *args, **kwargs):
        super(StageForm, self).__init__(*args, **kwargs)
        self.fields['stage_type'].widget.attrs.update({'class': 'form-control'})
        


class HousingForm(BaseForm):
    class Meta:
        model = Housing
        fields = ['image', 'title', 'description', 'location', 'contact_info', 'post_type', 'housing_location', 'housing_description']


class TransportationForm(BaseForm):
    class Meta:
        model = Transportation
        fields = ['image', 'title', 'description', 'location', 'contact_info', 'post_type', 'departure', 'destination', 'departure_time']

class ClubEventForm(BaseForm):
    class Meta:
        model = ClubEvent
        fields = ['image', 'title', 'description', 'location', 'contact_info', 'post_type', 'club', 'specialization', 'seat_capacity', 'club_contact_info']

class SocialEventForm(BaseForm):
    class Meta:
        model = SocialEvent
        fields = ['image', 'title', 'description', 'location', 'contact_info', 'post_type', 'price', 'social_contact_info']

# class PostForm(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields = ['title', 'description', 'location', 'contact_info', 'image', 'post_type']
#         widgets = {
#             'title': forms.TextInput(attrs={'class': 'form-control'}),
#             'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
#             'location': forms.TextInput(attrs={'class': 'form-control'}),
#             'contact_info': forms.TextInput(attrs={'class': 'form-control'}),
#             'image': forms.FileInput(attrs={'class': 'form-control-file'}),
#             'post_type': forms.Select(attrs={'class': 'form-control'}),
#         }
#     def __init__(self, *args, **kwargs):
#         instance = kwargs.get('instance')
#         super(PostForm, self).__init__(*args, **kwargs)

#         if instance:
#             self.fields['title'].required = False
#             self.fields['description'].required = False
#             self.fields['location'].required = False
#             self.fields['contact_info'].required = False
#             self.fields['image'].required = False

#             specific_data_fields = instance.get_specific_data_fields()
#             self.fields.update(specific_data_fields)

#             # Précharger les valeurs des champs spécifiques
#             for field, widget in specific_data_fields.items():
#                 self.initial[field] = instance.get_specific_data().get(field)

#     def save(self, commit=True):
#         post = super().save(commit=False)
#         post_type = post.post_type

#         if post_type == "stage":
#             post.stage.company = self.cleaned_data.get("company")
#             post.stage.duration = self.cleaned_data.get("duration")
#             post.stage.subject = self.cleaned_data.get("subject")
#             post.stage.stage_type = self.cleaned_data.get("stage_type")
#             post.stage.save()
#         elif post_type == "housing":
#             post.housing.housing_location = self.cleaned_data.get("housing_location")
#             post.housing.housing_description = self.cleaned_data.get("housing_description")
#             post.housing.save()
#         elif post_type == "transportation":
#             post.transportation.departure = self.cleaned_data.get("departure")
#             post.transportation.destination = self.cleaned_data.get("destination")
#             post.transportation.departure_time = self.cleaned_data.get("departure_time")
#             post.transportation.save()
#         elif post_type == "club_event":
#             post.clubevent.club = self.cleaned_data.get("club")
#             post.clubevent.specialization = self.cleaned_data.get("specialization")
#             post.clubevent.seat_capacity = self.cleaned_data.get("seat_capacity")
#             post.clubevent.club_contact_info = self.cleaned_data.get("club_contact_info")
#             post.clubevent.save()
#         elif post_type == "social_event":
#             post.socialevent.price = self.cleaned_data.get("price")
#             post.socialevent.social_contact_info = self.cleaned_data.get("social_contact_info")
#             post.socialevent.save()

#         post.save()
#         return post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'location', 'contact_info', 'image', 'post_type']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_info': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
            'post_type': forms.Select(attrs={'class': 'form-control'}),
            # Ajoutez vos champs spécifiques avec les classes Bootstrap correspondantes ici
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'stage_type': forms.Select(attrs={'class': 'form-control'}),
            'housing_location': forms.TextInput(attrs={'class': 'form-control'}),
            'housing_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'departure': forms.TextInput(attrs={'class': 'form-control'}),
            'destination': forms.TextInput(attrs={'class': 'form-control'}),
            'departure_time': forms.TextInput(attrs={'class': 'form-control'}),
            'club': forms.TextInput(attrs={'class': 'form-control'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control'}),
            'seat_capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'club_contact_info': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'social_contact_info': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super(PostForm, self).__init__(*args, **kwargs)

        if instance:
            self.fields['title'].required = False
            self.fields['description'].required = False
            self.fields['location'].required = False
            self.fields['contact_info'].required = False
            self.fields['image'].required = False

            specific_data_fields = instance.get_specific_data_fields()
            self.fields.update(specific_data_fields)

            for field, widget in specific_data_fields.items():
                if widget == forms.TextInput:
                    self.fields[field].widget = forms.TextInput(attrs={'class': 'form-control'})
                elif widget == forms.Textarea:
                    self.fields[field].widget = forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
                elif widget == forms.NumberInput:
                    self.fields[field].widget = forms.NumberInput(attrs={'class': 'form-control'})
                elif widget == forms.Select:
                    self.fields[field].widget = forms.Select(attrs={'class': 'form-control'})

            for field, value in instance.get_specific_data().items():
                self.initial[field] = value
                
    def save(self, commit=True):
        post = super().save(commit=False)
        post_type = post.post_type

        if post_type == "stage":
            post.stage.company = self.cleaned_data.get("company")
            post.stage.duration = self.cleaned_data.get("duration")
            post.stage.subject = self.cleaned_data.get("subject")
            post.stage.stage_type = self.cleaned_data.get("stage_type")
            post.stage.save()
        elif post_type == "housing":
            post.housing.housing_location = self.cleaned_data.get("housing_location")
            post.housing.housing_description = self.cleaned_data.get("housing_description")
            post.housing.save()
        elif post_type == "transportation":
            post.transportation.departure = self.cleaned_data.get("departure")
            post.transportation.destination = self.cleaned_data.get("destination")
            post.transportation.departure_time = self.cleaned_data.get("departure_time")
            post.transportation.save()
        elif post_type == "club_event":
            post.clubevent.club = self.cleaned_data.get("club")
            post.clubevent.specialization = self.cleaned_data.get("specialization")
            post.clubevent.seat_capacity = self.cleaned_data.get("seat_capacity")
            post.clubevent.club_contact_info = self.cleaned_data.get("club_contact_info")
            post.clubevent.save()
        elif post_type == "social_event":
            post.socialevent.price = self.cleaned_data.get("price")
            post.socialevent.social_contact_info = self.cleaned_data.get("social_contact_info")
            post.socialevent.save()

        post.save()
        return post
