
from .models import *
from .utils import *
from datetime import datetime
from studios.utils import force_drop_classes_once_cancel_subscription


def is_card_valid(card_number, card_expire, security_code):
    # TODO no api to verify
    return True


def make_subscription(user, plan: Plan):
    price = plan.price

    # charge the fee
    print(f'charge {user} ${price}')

    # make user subscribed to the same plan next period automatically
    if not user_has_x(user, 'upcoming_plan'):
        UpComingPlan(
            user=user,
            plan=plan,
        ).save()

    # make charge receipt
    Receipt(
        user=user,
        plan=plan,
        card_number=user.payment_method.card_number,
        amount=price,
    ).save()


def cancel_subscription(user):
    force_drop_classes_once_cancel_subscription(user, datetime.today())

    ratio = (dbtime2utc(user.subscription.expired_time) -
             get_now2utc()) / \
        (dbtime2utc(user.subscription.expired_time) -
         dbtime2utc(user.subscription.subscribed_time))
    refund = user.subscription.plan.price * ratio

    # make refund receipt
    Receipt(
        user=user,
        plan=user.subscription.plan,
        card_number=user.payment_method.card_number,
        amount=refund,
        is_refund=True,
    ).save()

    # delete user upcomming plan automatically
    if user_has_x(user, 'upcoming_plan'):
        user.upcoming_plan.delete()

    # refund the fee
    print(f'refund {user} ${refund}')


def remove_expired_subscription(sub):
    print(f'remove expired subscription of {sub.user}')
    force_drop_classes_once_cancel_subscription(user, datetime.today())
    user = sub.user
    if user_has_x(user, 'upcoming_plan') and user_has_x(user, 'payment_method') and user.upcoming_plan.plan.is_active:
        new_plan = user.upcoming_plan.plan
        sub.delete()
        make_subscription(user, new_plan)
        Subscription(
            plan=new_plan,
            user=user,
            expired_time=utc2dbtime(get_now2utc() + new_plan.interval)
        ).save()
    else:
        sub.delete()
        if user_has_x(user, 'upcoming_plan'):
            user.upcoming_plan.delete()


def remove_all_expired_subscriptions():
    print('check expired subscriptions')
    subs = Subscription.objects.all()
    for sub in subs:
        if get_now2utc() > dbtime2utc(sub.subscribed_time) + sub.plan.interval:
            remove_expired_subscription(sub)
