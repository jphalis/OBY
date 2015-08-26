import string
import random

from .models import Donation


def id_generator(size=8, chars=string.ascii_uppercase + string.digits):
    the_id = "".join(random.choice(chars) for x in range(size))
    try:
        order = Donation.objects.get(order_id=the_id)
        id_generator()
    except Donation.DoesNotExist:
        return the_id
