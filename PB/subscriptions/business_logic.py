
from .models import *
import datetime
from .utils import *


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
            start_time=datetime.datetime.now() + plan.interval
        ).save()

    # make charge receipt
    Receipt(
        user=user,
        plan=plan,
        card_number=user.payment_method.card_number,
        amount=price,
    ).save()


def cancel_subscription(user):
    ratio = 1 - (datetime.datetime.utcnow() -
                 user.subscription.subscribed_time.replace(tzinfo=None)) / user.subscription.plan.interval
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
