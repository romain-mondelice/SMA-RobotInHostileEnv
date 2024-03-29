class Message:
    def __init__(self, sender, receiver, content):
        self.sender = sender
        self.receiver = receiver
        self.content = content

class MessageService:
    __instance = None

    @staticmethod
    def get_instance():
        if MessageService.__instance is None:
            MessageService()
        return MessageService.__instance

    def __init__(self):
        self.messages = []
        if MessageService.__instance is None:
            MessageService.__instance = self
            self.messages = []
            self.instant_delivery = True

    def set_instant_delivery(self, instant_delivery):
        self.instant_delivery = instant_delivery

    def send_message(self, sender, receiver, content):
        message = Message(sender, receiver, content)
        if self.instant_delivery:
            receiver.receive_message(message)
        else:
            self.messages.append(message)

    def dispatch_messages(self):
        print("self.messages >>> ", self.messages)
        for message in self.messages:
            message.receiver.receive_message(message)
            print("Dispatching message: ", message.content)
        self.messages.clear()