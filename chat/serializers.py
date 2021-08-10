def serialize_message(msg_obj):
    return {
        'sender': msg_obj.sender.email,
        'content': msg_obj.content,
        'created_on': msg_obj.created_on,
    }