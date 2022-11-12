# from ..accounts.models import TFCUser
# from subscriptions.models import Plan
# import datetime


# def subscribe(user: TFCUser, plan: Plan):
#     user.plan = plan
#     user.is_subscribed = True
#     user.subscribed_time = datetime.now()
#     user.save()

# def has_plan(user: TFCUser):
#     if not user.is_subscribed:
#         if user.plan == None:
#             return False
#         elif
#     else:

# def unsubscribe(user: TFCUser):
#     user.is_subscribed = False
#     user.save()
