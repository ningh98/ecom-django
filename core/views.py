from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic
from .forms import ContactForm
from django.shortcuts import reverse
from cart.models import Order
# Create your views here.

class ProfileView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context.update({
            "orders": Order.objects.filter(user=self.request.user, ordered=True)
        })
        return context

class HomeView(generic.TemplateView):
    template_name = 'index.html'

class ContactView(generic.FormView):
    form_class = ContactForm
    template_name = 'contact.html'

    def get_success_url(self):
        return reverse("contact")
    
    def form_valid(self, form):
        messages.info(self.request, "Thanks for getting in touch. We have received your message.")
        name = form.cleaned_data.get('name')
        email = form.cleaned_data.get('email')
        message = form.cleaned_data.get('message')

        full_message = f"""
                Received message bleow from {name}, {email}
                _________________________


                {message}
                """
        send_mail(
            subject="Received contact form submission",
            message=full_message,
            from_email=settings.DEFAULT_FORM_EMAIL,
            recipient_list=[settings.NOTIFY_EMAIL]

        )
        return super(ContactView, self).form_valid(form)

