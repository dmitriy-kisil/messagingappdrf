from django.contrib.auth.models import User


def prepare_queryset_to_json(queryset):
    """
    Make JSON from queryset, removes id`s fields and add sender and receiver.
    Return list with dictionaries for each item in queryset
    """
    response = []
    for message in queryset.values():
        sender_id, receiver_id = message["sender_id"], message["receiver_id"]
        del message["id"], message["sender_id"], message["receiver_id"]
        message["sender"] = User.objects.filter(id=sender_id).values('username')[0]['username']
        message["receiver"] = User.objects.filter(id=receiver_id).values('username')[0]['username']
        response.append(message)
    return response