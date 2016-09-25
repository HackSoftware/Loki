from django.core.mail.backends.console import EmailBackend
import json


class SendGridConsoleBackend(EmailBackend):

    def write_message(self, message):
        merge_data_str = json.dumps(message.merge_data, indent=4, ensure_ascii=False).encode('utf8')
        self.stream.write(merge_data_str)
        self.stream.write("\n")
        super().write_message(message)
