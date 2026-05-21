from django.db.models import QuerySet

from db.models import Order, Ticket
from db.models import User
from django.db import transaction

def create_order(
    tickets: list,
    username: str,
    date = None,
)-> Order:
        user = User.objects.get(username=username)
        order_data = {"user": user}
        if date:
            order_data["created_at"] = date

        with transaction.atomic():
            order = Order.objects.create(**order_data)
            for ticket in tickets:
                Ticket.objects.create(
                    row=ticket["row"],
                    seat=ticket["seat"],
                    movie_session_id=ticket["movie_session"],
                    order=order
                )

        return order

def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()