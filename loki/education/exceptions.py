class CodeSelectionError(Exception):

    def __init__(self, message):
        self._message = message

    def __str__(self):
        msg = "You can't select non existing row #{}".format(self._message)
        return msg
