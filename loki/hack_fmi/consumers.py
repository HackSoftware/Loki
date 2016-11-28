from channels import Group


# When something connects, add it to the group 
#  i na nqkakvo subitie se prashta suotveten post na grupata
def ws_connect(message):
    Group("invitations").add(message.reply_channel)


def ws_disconnect(message):
    Group("invitations").discard(message.reply_channel)

def ws_echo(message):
    message.reply_channel.send({
        'text': message.content['text'],
    })