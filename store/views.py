from http import HTTPStatus

import stripe
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DetailView

from store.models import Lessons, Product, Order
from users.forms import UserRegistrationForm
from users.models import User


class IndexPageView(CreateView):
    model = User
    template_name = 'store/index.html'
    form_class = UserRegistrationForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(IndexPageView, self).get_context_data()
        context['all_products'] = Product.objects.all()
        return context


class LessonsDetailView(DetailView):
    model = Lessons
    template_name = 'store/lessons.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(LessonsDetailView, self).get_context_data()
        context['all_lessons'] = Lessons.objects.all()

        return context


class OrderCreateView(DetailView):
    model = Order

    def get(self, request, *args, **kwargs):
        order = Order.objects.create(initiator=request.user, product=Product.objects.get(id=kwargs['pk']))
        checkout_session = stripe.checkout.Session.create(
            line_items=[{
                'price': Product.objects.get(id=kwargs['pk']).stripe_product_price_id,
                'quantity': 1,
            }
                ],
            metadata={'order_id': order.id},
            mode='payment',
            success_url='{}{}'.format(settings.DOMAIN_NAME, reverse('users:profile',
                                                                    kwargs={
                                                                        'pk': order.initiator.pk})),
            cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('store:store')),
        )
        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        update_after_payment(session)

    return HttpResponse(status=200)


def update_after_payment(session):
    order_id = int(session.metadata.order_id)
    order = Order.objects.filter(id=order_id)
    order.update(status=1)
    user = User.objects.filter(id=order.first().initiator.pk)
    user.update(status=Order.objects.get(id=order_id).product.id)


