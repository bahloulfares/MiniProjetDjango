from urllib import request
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from .forms import PostForm, StageForm, HousingForm, TransportationForm, ClubEventForm, SocialEventForm, PostTypeForm ,CommentForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, UserCreationForm
from .models import Post, Stage, Housing, Transportation, ClubEvent, SocialEvent, Comment, Like,Notification
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.http import HttpResponseForbidden , HttpResponseBadRequest, HttpResponseNotAllowed ,HttpResponseRedirect
from django.views.generic.edit import FormView
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@method_decorator(login_required, name='dispatch')
class PostCreateView(CreateView):
    model = Post
    template_name = 'post_form.html'
    form_class = PostForm
    
    def get_form_class(self):
        # Récupérer le type de publication à partir de la requête GET
        post_type = self.request.GET.get('type')
        
        # Choisir le formulaire approprié en fonction du type de publication
        if post_type == 'stage':
            return StageForm
        elif post_type == 'housing':
            return HousingForm
        elif post_type == 'transportation':
            return TransportationForm
        elif post_type == 'club_event':
            return ClubEventForm
        elif post_type == 'social_event':
            return SocialEventForm
        
        # Par défaut, retourner le formulaire générique de publication
        return PostForm

    def form_valid(self, form):
        # Définir l'auteur de la publication sur l'utilisateur actuel
        form.instance.author = self.request.user
        # Enregistrer le type de formulaire dans la base de données
        form.instance.form_type = self.request.GET.get('type') 
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ajouter le formulaire de sélection du type de publication au contexte
        context['post_type_form'] = PostTypeForm()
        return context

    def get_success_url(self):
        return reverse_lazy('post_list')

class AddCommentView(LoginRequiredMixin, FormView):
    form_class = CommentForm
    template_name = 'comment_form.html'  # Assurez-vous de spécifier le bon template

    def get_success_url(self):
        # Renvoyer vers la page précédente après l'ajout du commentaire
        return self.request.META.get('HTTP_REFERER', reverse_lazy('post_list'))

    def form_valid(self, form):
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, pk=post_id)
        comment = form.save(commit=False)
        comment.post = post
        comment.user = self.request.user
        comment.save()
        # Créer une notification de commentaire seulement si l'utilisateur qui commente n'est pas l'auteur du post
        if post.author != self.request.user:
            Notification.objects.create(user=post.author, post=post, comment=comment, type='comment')
        # Rediriger vers la page précédente après l'ajout du commentaire
        return redirect(self.get_success_url())
    
class UserPostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'user_update_post.html'
    success_url = reverse_lazy('post_list')


class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'user_posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        # Filtrer les publications de l'utilisateur connecté
        user_posts = Post.objects.filter(author=self.request.user)

        # Appliquer les filtres de recherche uniquement sur les publications de l'utilisateur connecté
        queryset = user_posts.order_by('-date')  # Tri par date décroissante
        search_query = self.request.GET.get('recherche')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        return queryset 
    

class CommentListView(ListView):
    model = Comment
    template_name = 'comment_list_modal.html'  # Assurez-vous de créer ce template
    context_object_name = 'comments'

    def get_queryset(self):
        post_id = self.request.GET.get('post_id')
        return Comment.objects.filter(post_id=post_id)

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return JsonResponse({'message': 'La publication a été supprimée avec succès.', 'success_url': success_url})

class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.all().order_by('-date')
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(author__username__icontains=search_query)
            )
        post_type = self.request.GET.get('post_type')
        if post_type:
            queryset = queryset.filter(post_type=post_type)
        form_type = self.request.GET.get('form_type')
        if form_type:
            queryset = queryset.filter(form_type=form_type)
        sort_by = self.request.GET.get('sort_by')
        if sort_by:
            queryset = queryset.order_by(sort_by)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['notifications'] = Notification.objects.filter(user=self.request.user, is_read=False)
        context['unread_notifications'] = context['notifications'].count()
        return context

    def mark_notifications_as_read(self):
        notifications = Notification.objects.filter(user=self.request.user, is_read=False)
        notifications.update(is_read=True)  # Update all unread notifications in one query



class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

def login_view(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('post_list')
    return render(request, 'registration/login.html', {'form': form})

def custom_password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            return render(request, 'registration/password_reset_done.html')
    else:
        form = PasswordResetForm()
    return render(request, 'registration/password_reset.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('post_list')

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

def index(request):
    return render(request, 'index.html')


@login_required
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        # Vérifiez si l'utilisateur connecté a l'autorisation de supprimer le commentaire
        if request.user == comment.user:
            # Créer une notification de suppression de commentaire
            Notification.objects.create(user=comment.post.author, post=comment.post, comment=comment, type='comment_delete')
            comment.delete_comment()  # Utilisation de la méthode de modèle pour supprimer le commentaire
            return JsonResponse({'message': 'Le commentaire a été supprimé avec succès.'})
        else:
            return JsonResponse({'error': 'Vous n\'avez pas l\'autorisation de supprimer ce commentaire.'}, status=403)  # Status 403 pour accès interdit
    else:
        return JsonResponse({'error': 'La méthode de requête n\'est pas autorisée.'}, status=405)  # Status 405 pour méthode non autorisée
    
@login_required
def add_like(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_id)
        
        # Vérifier si l'utilisateur a déjà aimé le post
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        
        if created:
            # Créer une notification de like seulement si l'utilisateur qui aime n'est pas l'auteur du post
            if post.author != request.user:
                Notification.objects.create(user=post.author, post=post, type='like', liker=request.user)
        
        else:
            like.delete()  # Supprimer le like s'il existe déjà
        
        # Récupérer le nom de l'utilisateur qui a aimé le post
        liker_name = request.user.username
        
        # Retourner le nombre total de likes pour le post
        return JsonResponse({'like_count': post.likes.count(), 'liker_name': liker_name})
    
    else:    
        # Si la demande n'est pas de type POST, renvoyer une erreur
        return JsonResponse({'error': 'La requête doit être de type POST'})
    
@login_required
def delete_like(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    like = Like.objects.filter(post=post, user=request.user).first()
    if like:
        like.delete()
    return JsonResponse({'like_count': post.likes.count()})


def post_confirm_delete(request):
    return render(request, 'studenthelp/post_confirm_delete.html')    

class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_update_form.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Post, pk=self.kwargs['pk'])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        post = self.get_object()
        initial_data = {}

        if post.form_type == 'stage':
            initial_data.update({
                'company': post.stage.company,
                'duration': post.stage.duration,
                'subject': post.stage.subject,
                'stage_type': post.stage.stage_type,
            })
        elif post.form_type == 'housing':
            initial_data.update({
                'housing_location': post.housing.housing_location,
                'housing_description': post.housing.housing_description,
            })
        elif post.form_type == 'transportation':
            initial_data.update({
                'departure': post.transportation.departure,
                'destination': post.transportation.destination,
                'departure_time': post.transportation.departure_time,
            })
        elif post.form_type == 'club_event':
            initial_data.update({
                'club': post.clubevent.club,
                'specialization': post.clubevent.specialization,
                'seat_capacity': post.clubevent.seat_capacity,
                'club_contact_info': post.clubevent.club_contact_info,
            })
        elif post.form_type == 'social_event':
            initial_data.update({
                'price': post.socialevent.price,
                'social_contact_info': post.socialevent.social_contact_info,
            })

        kwargs['initial'] = initial_data
        return kwargs

    def form_valid(self, form):
        post = form.save(commit=False)

        if post.form_type == "stage":
            stage = post.stage
            stage.company = form.cleaned_data.get("company")
            stage.duration = form.cleaned_data.get("duration")
            stage.subject = form.cleaned_data.get("subject")
            stage.stage_type = form.cleaned_data.get("stage_type")
            stage.save()
        elif post.form_type == "housing":
            housing = post.housing
            housing.housing_location = form.cleaned_data.get("housing_location")
            housing.housing_description = form.cleaned_data.get("housing_description")
            housing.save()
        elif post.form_type == "transportation":
            transportation = post.transportation
            transportation.departure = form.cleaned_data.get("departure")
            transportation.destination = form.cleaned_data.get("destination")
            transportation.departure_time = form.cleaned_data.get("departure_time")
            transportation.save()
        elif post.form_type == "club_event":
            club_event = post.clubevent
            club_event.club = form.cleaned_data.get("club")
            club_event.specialization = form.cleaned_data.get("specialization")
            club_event.seat_capacity = form.cleaned_data.get("seat_capacity")
            club_event.club_contact_info = form.cleaned_data.get("club_contact_info")
            club_event.save()
        elif post.form_type == "social_event":
            social_event = post.socialevent
            social_event.price = form.cleaned_data.get("price")
            social_event.social_contact_info = form.cleaned_data.get("social_contact_info")
            social_event.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_list')
