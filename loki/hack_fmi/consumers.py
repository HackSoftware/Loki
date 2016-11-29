from channels import Group


def ws_connect(message):
    Group("invitations").add(message.reply_channel)


def ws_disconnect(message):
    Group("invitations").discard(message.reply_channel)
