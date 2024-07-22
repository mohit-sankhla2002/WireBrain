from authApp import models as authModel
from . import models

class Webhook:
    def __init__(self,data,messenger):
        self.data = data
        self.messenger = messenger
        self.teamMobile = data['entry'][0]['changes'][0]['value']['metadata']['display_phone_number']
        self.changed_field = messenger.changed_field(data)

    def saveReceiveMessage(self, id, type, message, timestamp, mobile, teamId):
        body={'messageId':id,'type':type, "body":message, "statusLog":[{"received":timestamp}]}
        models.chats.update_one({'contactId':self.teamMobile, 'teamId':teamId, 'recipientId':mobile},
                                            {'$push': {'chats':body},'$set': {'universalTimestamp': timestamp}})
        
    def saveSentMessage(self, id, type, message, mobile, teamId, status_log):
         contact = models.chats.find_one({'contactId': self.teamMobile, 'recipientId':mobile, 'teamId': teamId})
         if contact:
            query = {"chats.messageId": id}
            document = models.chats.find_one(query)
            if document:
                models.chats.update_one(query,{"$push": {"chats.$.statusLog" :status_log}})
            else:
                new_chat = {
                        'messageId': id,
                        'type': type,
                        'body': message,
                        'statusLog': [status_log]
                    }
                models.chats.update_one(
                        {'contactId': self.teamMobile, 'teamId': teamId, 'recipientId':mobile},
                        {'$push': {'chats': new_chat}}
                    )
    def sendMessage(self):
            data = self.data
            messenger = self.messenger
            messageId = data['entry'][0]['changes'][0]['value']['statuses'][0]['id']
            mobile = data['entry'][0]['changes'][0]['value']['statuses'][0]['recipient_id']
            record = messenger.get_delivery(data)
            user = authModel.User.objects.get(phone=self.teamMobile)
            timestamp = data['entry'][0]['changes'][0]['value']['statuses'][0]['timestamp']
            if messageId in messenger.messages_store and messenger.messages_store[messageId]['message_type']=='text':
                        content = messenger.messages_store[messageId]['message_content']
                        report = {record:timestamp}
                        self.saveSentMessage(messageId,"text",content,mobile,user.team.id, report)

            elif messageId in messenger.messages_store and messenger.messages_store[messageId]['message_type']=='image':
                imageId = messenger.messages_store[messageId]['message_content']
                report = {record:timestamp}
                self.saveSentMessage(messageId,"image",imageId,mobile,user.team.id, report)
            
            elif messageId in messenger.messages_store and messenger.messages_store[messageId]['message_type']=='video':
                videoId = messenger.messages_store[messageId]['message_content']
                report = {record:timestamp}
                self.saveSentMessage(messageId,"video",videoId,mobile,user.team.id, report)
            
            elif messageId in messenger.messages_store and messenger.messages_store[messageId]['message_type']=='audio':
                audioId = messenger.messages_store[messageId]['message_content']
                report = {record:timestamp}
                self.saveSentMessage(messageId,"audio",audioId,mobile,user.team.id, report)
            
            elif messageId in messenger.messages_store and messenger.messages_store[messageId]['message_type']=='document':
                documentId = messenger.messages_store[messageId]['message_content']
                report = {record:timestamp}
                self.saveSentMessage(messageId,"document",documentId,mobile,user.team.id, report)
    
    def receiveMessage(self):
        data=self.data
        changed_field=self.changed_field
        messenger=self.messenger
        if changed_field == "messages":
            mobile = messenger.get_mobile(data)
            user = authModel.User.objects.get(phone=self.teamMobile)
            timestamp=messenger.get_message_timestamp(data)
            if mobile:
                contact=models.chats.find_one({'teamId':user.team.id,'contactId': self.teamMobile, 'recipientId':mobile})

                if not contact:
                    contact_data = {'contactId': self.teamMobile,'recipientId': mobile,'teamId': user.team.id, "universalTimestamp":timestamp,'chats': []}
                    models.chats.insert_one(contact_data)

                message_type = messenger.get_message_type(data)
                messageId = messenger.get_message_id(data)

                if message_type == "text":
                    message = messenger.get_message(data)
                    self.saveReceiveMessage(messageId,"text",message,timestamp,mobile,user.team.id)
                
                elif message_type == "image":
                    image = messenger.get_image(data)
                    image_id = image["id"]
                    self.saveReceiveMessage(messageId,"image",image_id,timestamp,mobile,user.team.id)

                elif message_type == "video":
                    video = messenger.get_video(data)
                    video_id = video["id"]
                    self.saveReceiveMessage(messageId,"video",video_id,timestamp,mobile,user.team.id)

                elif message_type == "audio":
                    audio = messenger.get_audio(data)
                    audio_id = audio["id"]
                    self.saveReceiveMessage(messageId,"audio",audio_id,timestamp,mobile,user.team.id)

                elif message_type == "document":
                    file = messenger.get_document(data)
                    file_id = file["id"]
                    self.saveReceiveMessage(messageId,"document",file_id,timestamp,mobile,user.team.id)