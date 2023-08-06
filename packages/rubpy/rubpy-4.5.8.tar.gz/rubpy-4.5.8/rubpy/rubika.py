from .connections.requests import Requests
from random import randint
from .connections.websocket import WebSocket
from time import time as time_stamp
from .tools import Tools
from urllib3 import PoolManager
import asyncio
from mutagen.mp3 import MP3
from io import BytesIO
try: from tinytag import TinyTag
except ModuleNotFoundError: TinyTag = None


class Client(object):
    def __init__(self, auth):
        self.__requests = Requests(auth)
        self.send = self.__requests.send
        self.upload = self.__requests.uploadFile
        self.websocket = WebSocket(auth).handler
        self._auth = auth
        self.tools = Tools()
        self.__pool_manager = PoolManager()

    async def sendMessage(self, object_guid, text, reply_to_message_id=None, meta_data=None):
        data = {
			'object_guid': object_guid,
			'rnd': f'{randint(100000, 999999999)}',
			'text': text,
			'reply_to_message_id': reply_to_message_id
		}
        if meta_data != None: data['metadata'] = {'meta_data_parts': meta_data}
        modes = ['**' , '__' , '``']
        for check in modes:
            if check in text:
                meta_data = self.tools.analyzeString(text)
                data['metadata'] = {'meta_data_parts': meta_data.get('metadata')}
                data['text'] = meta_data.get('string')
            else: continue
        return await self.send('sendMessage', data, 5)

    async def sendPhoto(self, object_guid, image, caption=None, reply_to_message_id=None):
        if image.startswith('http'):
            response = self.__pool_manager.request('GET', image)
            response_headers = response.headers
            image_bytes = response.data
            content_length = response_headers.get('content-length')
            content_type = response_headers.get('content-type')
            if content_type == 'image/jpeg':
                image_type = 'jpg'
            else:
                image_type = 'png'
            image_name = f'shayan-heidari{randint(1, 999)}.{image_type}'
            requestSendFile = await self.requestSendFile(image_name, image_type, str(content_length))
            is_uploaded = await self.upload(requestSendFile.get('upload_url'), requestSendFile.get('access_hash_send'), requestSendFile.get('id'), image_bytes)
            width, height = self.tools.getImageSize(image_bytes)
            thumb_inline = self.tools.getThumbnail(image_bytes).decode('utf-8')
            data = {
                'file_inline': {
                    'dc_id': requestSendFile.get('dc_id'),
                    'file_id': requestSendFile.get('id'),
                    'type':'Image',
                    'file_name': image_name,
                    'size': content_length,
                    'mime': image_type,
                    'access_hash_rec': is_uploaded,
                    'width': width,
                    'height': height,
                    'thumb_inline': thumb_inline
                },
                'object_guid': object_guid,
                'text': caption,
                'rnd': f'{randint(100000,999999999)}',
                'reply_to_message_id': reply_to_message_id
            }
            return await self.send('sendMessage', data, 5)
        else:
            with open(image, 'rb') as image_file:
                my_image = image_file.read()
                image_file.close()
            image_type = f'.{image.split(".")[1]}'
            content_length = str(len(my_image))
            image_name = f'shayan-heidari{randint(1, 999)}{image_type}'
            width, height = self.tools.getImageSize(my_image)
            thumb_inline = self.tools.getThumbnail(my_image).decode('utf-8')
            requestSendFile = await self.requestSendFile(image_name, image_type, content_length)
            is_uploaded = await self.upload(requestSendFile.get('upload_url'), requestSendFile.get('access_hash_send'), requestSendFile.get('id'), my_image)
            data = {
                'file_inline': {
                    'dc_id': requestSendFile.get('dc_id'),
                    'file_id': requestSendFile.get('id'),
                    'type':'Image',
                    'file_name': image_name,
                    'size': content_length,
                    'mime': image_type,
                    'access_hash_rec': is_uploaded,
                    'width': width,
                    'height': height,
                    'thumb_inline': thumb_inline
                },
                'object_guid': object_guid,
                'text': caption,
                'rnd': f'{randint(100000,999999999)}',
                'reply_to_message_id': reply_to_message_id
            }
            return await self.send('sendMessage', data, 5)

    async def sendFile(self, object_guid, file, caption=None, reply_to_message_id=None):
        mime = f".{file.split('.')[-1]}"
        file_name = f'shayan-heidari{randint(1, 999)}{mime}'
        data = {
            'file_inline': {
                'dc_id': None,
                'file_id': None,
                'type':'File',
                'file_name': file_name,
                'size': None,
                'mime': mime,
                'access_hash_rec': None
            },
            'object_guid': object_guid,
            'text': caption,
            'rnd': f'{randint(100000,999999999)}',
            'reply_to_message_id': reply_to_message_id
        }
        if file.startswith('http'):
            response = self.__pool_manager.request('GET', file)
            content_length = dict(response.headers).get('Content-Length')
            if content_length == None:
                content_length = dict(response.headers).get('content-length')
            file_bytes = response.data
            requestSendFile = await self.requestSendFile(file_name, mime, content_length)
            is_uploaded = await self.upload(requestSendFile.get('upload_url'), requestSendFile.get('access_hash_send'), requestSendFile.get('id'), file_bytes)
            data['file_inline']['size'] = content_length
            data['file_inline']['dc_id'] = requestSendFile.get('dc_id')
            data['file_inline']['access_hash_rec'] = is_uploaded
            data['file_inline']['file_id'] = requestSendFile.get('id')
        else:
            with open(file, 'rb') as my_file:
                file = my_file.read()
                my_file.close()
            content_length = str(len(file))
            requestSendFile = await self.requestSendFile(file_name, mime, content_length)
            is_uploaded = await self.upload(requestSendFile.get('upload_url'), requestSendFile.get('access_hash_send'), requestSendFile.get('id'), file)
            data['file_inline']['size'] = content_length
            data['file_inline']['dc_id'] = requestSendFile.get('dc_id')
            data['file_inline']['access_hash_rec'] = is_uploaded
            data['file_inline']['file_id'] = requestSendFile.get('id')

        return await self.send('sendMessage', data, 5)

    async def sendVoice(self, object_guid, voice, caption=None, reply_to_message_id=None):
        mime = '.ogg'
        file_name = f'shayan-heidari{randint(1, 999)}{mime}'
        data = {
            'file_inline': {
                'dc_id': None,
                'file_id': None,
                'type':'Voice',
                'file_name': file_name,
                'size': None,
                'time': None,
                'mime': mime,
                'access_hash_rec': None
            },
            'object_guid': object_guid,
            'text': caption,
            'rnd': f'{randint(100000,999999999)}',
            'reply_to_message_id': reply_to_message_id
        }
        if voice.startswith('http'):
            response = self.__pool_manager.request('GET', voice)
            content_length = dict(response.headers).get('Content-Length')
            if content_length == None:
                content_length = dict(response.headers).get('content-length')
            file_bytes = response.data
            duration = await self.get_voice_duration(file_bytes)
            requestSendFile = await self.requestSendFile(file_name, mime, content_length)
            is_uploaded = await self.upload(requestSendFile.get('upload_url'), requestSendFile.get('access_hash_send'), requestSendFile.get('id'), file_bytes)
            data['file_inline']['size'] = content_length
            data['file_inline']['time'] = duration
            data['file_inline']['dc_id'] = requestSendFile.get('dc_id')
            data['file_inline']['access_hash_rec'] = is_uploaded
            data['file_inline']['file_id'] = requestSendFile.get('id')
        else:
            with open(voice, 'rb') as my_file:
                file = my_file.read()
                my_file.close()
            duration = await self.get_voice_duration(file)
            content_length = str(len(file))
            requestSendFile = await self.requestSendFile(file_name, mime, content_length)
            is_uploaded = await self.upload(requestSendFile.get('upload_url'), requestSendFile.get('access_hash_send'), requestSendFile.get('id'), file)
            data['file_inline']['size'] = content_length
            data['file_inline']['time'] = duration
            data['file_inline']['dc_id'] = requestSendFile.get('dc_id')
            data['file_inline']['access_hash_rec'] = is_uploaded
            data['file_inline']['file_id'] = requestSendFile.get('id')

        return await self.send('sendMessage', data, 5)

    async def sendMusic(self, object_guid, music, music_performer = None, file_name = None, caption=None, reply_to_message_id=None):
        mime = f".{music.split('.')[-1]}"
        file_name = f'{file_name}{mime}'
        data = {
            'file_inline': {
                'dc_id': None,
                'file_id': None,
                'auto_play': False,
                'height': 0.0,
                'width': 0.0,
                'music_performer': music_performer,
                'type':'Music',
                'file_name': file_name,
                'size': None,
                'time': None,
                'mime': mime,
                'access_hash_rec': None
            },
            'object_guid': object_guid,
            'text': caption,
            'rnd': f'{randint(100000,999999999)}',
            'reply_to_message_id': reply_to_message_id
        }
        if music.startswith('http'):
            response = self.__pool_manager.request('GET', music)
            content_length = dict(response.headers).get('Content-Length')
            if content_length == None:
                content_length = dict(response.headers).get('content-length')
            file_bytes = response.data
            duration = await self.get_voice_duration(file_bytes)
            requestSendFile = await self.requestSendFile(file_name, mime, content_length)
            is_uploaded = await self.upload(requestSendFile.get('upload_url'), requestSendFile.get('access_hash_send'), requestSendFile.get('id'), file_bytes)
            data['file_inline']['size'] = content_length
            data['file_inline']['time'] = duration
            data['file_inline']['dc_id'] = requestSendFile.get('dc_id')
            data['file_inline']['access_hash_rec'] = is_uploaded
            data['file_inline']['file_id'] = requestSendFile.get('id')
        else:
            with open(music, 'rb') as my_file:
                file = my_file.read()
                my_file.close()
            duration = await self.get_voice_duration(file)
            content_length = str(len(file))
            requestSendFile = await self.requestSendFile(file_name, mime, content_length)
            is_uploaded = await self.upload(requestSendFile.get('upload_url'), requestSendFile.get('access_hash_send'), requestSendFile.get('id'), file)
            data['file_inline']['size'] = content_length
            data['file_inline']['time'] = duration
            data['file_inline']['dc_id'] = requestSendFile.get('dc_id')
            data['file_inline']['access_hash_rec'] = is_uploaded
            data['file_inline']['file_id'] = requestSendFile.get('id')

        return await self.send('sendMessage', data, 5)

    async def get_voice_duration(self, file_bytes):
        file = BytesIO()
        file.write(file_bytes)
        file.seek(0)
        audio = MP3(file)
        return audio.info.length

    async def getVideoDuration(self, video):
        if TinyTag != None:
            return round(TinyTag.get(video).duration * 1000)
        else:
            raise ImportWarning('Plaese install <TinyTag> and try again')

    async def sendGif(self, object_guid, gif, caption=None, reply_to_message_id=None):
        mime = f".{gif.split('.')[-1]}"
        file_name = f'shayan-heidari{randint(1, 999)}{mime}'
        data = {
            'file_inline': {
                'dc_id': None,
                'file_id': None,
                'auto_play': False,
                'height': 300,
                'width': 600,
                'thumb_inline': 'iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAIAAAADnC86AAAAL0lEQVR4nO3NQQ0AAAgEIPVz/Rsbw81BATpJXZiTVSwWi8VisVgsFovFYrFY/DRelEIAZd5yXa4AAAAASUVORK5CYII=',
                'type':'Gif',
                'file_name': file_name,
                'size': None,
                'time': None,
                'mime': mime,
                'access_hash_rec': None
            },
            'object_guid': object_guid,
            'text': caption,
            'rnd': f'{randint(100000,999999999)}',
            'reply_to_message_id': reply_to_message_id
        }
        with open(gif, 'rb') as my_file:
            file = my_file.read()
            my_file.close()
        duration = await self.getVideoDuration(gif)
        content_length = str(len(file))
        requestSendFile = await self.requestSendFile(file_name, mime, content_length)
        is_uploaded = await self.upload(requestSendFile.get('upload_url'), requestSendFile.get('access_hash_send'), requestSendFile.get('id'), file)
        data['file_inline']['size'] = content_length
        data['file_inline']['time'] = duration
        data['file_inline']['dc_id'] = requestSendFile.get('dc_id')
        data['file_inline']['access_hash_rec'] = is_uploaded
        data['file_inline']['file_id'] = requestSendFile.get('id')

        return await self.send('sendMessage', data, 5)

    async def sendVideo(self, object_guid, video, caption=None, reply_to_message_id=None):
        mime = f".{video.split('.')[-1]}"
        file_name = f'shayan-heidari{randint(1, 999)}{mime}'
        data = {
            'file_inline': {
                'dc_id': None,
                'file_id': None,
                'auto_play': False,
                'height': 300,
                'width': 600,
                'thumb_inline': 'iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAIAAAADnC86AAAAL0lEQVR4nO3NQQ0AAAgEIPVz/Rsbw81BATpJXZiTVSwWi8VisVgsFovFYrFY/DRelEIAZd5yXa4AAAAASUVORK5CYII=',
                'type':'Video',
                'file_name': file_name,
                'size': None,
                'time': None,
                'mime': mime,
                'access_hash_rec': None
            },
            'object_guid': object_guid,
            'text': caption,
            'rnd': f'{randint(100000,999999999)}',
            'reply_to_message_id': reply_to_message_id
        }
        with open(video, 'rb') as my_file:
            file = my_file.read()
            my_file.close()
        duration = await self.getVideoDuration(video)
        content_length = str(len(file))
        requestSendFile = await self.requestSendFile(file_name, mime, content_length)
        is_uploaded = await self.upload(requestSendFile.get('upload_url'), requestSendFile.get('access_hash_send'), requestSendFile.get('id'), file)
        data['file_inline']['size'] = content_length
        data['file_inline']['time'] = duration
        data['file_inline']['dc_id'] = requestSendFile.get('dc_id')
        data['file_inline']['access_hash_rec'] = is_uploaded
        data['file_inline']['file_id'] = requestSendFile.get('id')

        return await self.send('sendMessage', data, 5)

    async def requestSendFile(self, file_name, mime, size):
        data = {'file_name': file_name, 'mime': mime, 'size': size}
        response = await self.send('requestSendFile', data, 5)
        return response.get('data')

    async def getChats(self, start_id=None):
        return await self.send('getChats', {'start_id': start_id}, 5)

    async def editMessage(self, message_id, object_guid, new_text, meta_data=None):
        data = {'message_id': message_id, 'object_guid': object_guid, 'text': new_text}
        if meta_data != None: data['metadata'] = {'meta_data_parts': meta_data}
        modes = ['**' , '__' , '``']
        for check in modes:
            if check in new_text:
                meta_data = self.tools.analyzeString(new_text)
                data['metadata'] = {'meta_data_parts': meta_data.get('metadata')}
                data['text'] = meta_data.get('string')
            else: continue
        return await self.send('editMessage', data, 5)

    async def deleteMessages(self, object_guid, message_ids_list, delete_type='Global'):
        data = {
			'object_guid': object_guid,
			'message_ids': message_ids_list,
			'type': delete_type
		}
        return await self.send('deleteMessages', data, 5)

    async def getUserInfo(self, user_guid):
        return await self.send('getUserInfo', {'user_guid': user_guid}, 5)

    async def getMessagesInterval(self, object_guid, middle_message_id):
        data: dict = {'object_guid': object_guid, 'middle_message_id': middle_message_id}
        return await self.send('getMessagesInterval', data, 5)

    async def getObjectByUsername(self, username):
        if '@' in username: username.replace('@', '')
        return await self.send('getObjectByUsername', {'username': username}, 5)

    async def banGroupMember(self, group_guid, member_guid, action='Set'):
        data = {
			'group_guid': group_guid,
			'member_guid': member_guid,
			'action': action
		}
        return await self.send('banGroupMember', data, 5)

    async def addGroupMembers(self, group_guid, member_guids):
        data = {
			'group_guid': group_guid,
			'member_guids': member_guids
		}
        return await self.send('addGroupMembers', data, 5)

    async def addChannelMembers(self, channel_guid, member_guids):
        data = {
			'channel_guid': channel_guid,
			'member_guids': member_guids
		}
        return await self.send('addChannelMembers', data, 5)

    async def getGroupAdminMembers(self, group_guid, get_admin_guids=False):
        in_chat_members = await self.send('getGroupAdminMembers', {'group_guid': group_guid}, 5)
        in_chat_members = in_chat_members.get('data').get('in_chat_members')
        admin_list_guids = []
        if get_admin_guids:
            for guid in in_chat_members:
                admin_list_guids.append(guid.get('member_guid'))
            return admin_list_guids
        else:
            return in_chat_members

    async def getMessagesByID(self, object_guid, message_ids):
        data = {
			'object_guid': object_guid,
			'message_ids': message_ids
		}
        return await self.send('getMessagesByID', data, 5)

    async def setGroupDefaultAccess(self, group_guid, access_list):
        data = {
			'access_list': access_list,
			'group_guid': group_guid
		}
        return await self.send('setGroupDefaultAccess', data)

    async def getGroupAllMembers(self, group_guid, start_id=None):
        data = {
			'group_guid': group_guid,
			'start_id': start_id
		}
        return await self.send('getGroupAllMembers', data, 5)

    async def getGroupInfo(self, group_guid):
        return await self.send('getGroupInfo', {'group_guid': group_guid}, 5)

    async def getGroupLink(self, group_guid):
        result = await self.send('getGroupLink', {'group_guid': group_guid}, 5)
        link = result.get('data').get('join_link')
        return link

    async def setGroupLink(self, group_guid):
        return await self.send('setGroupLink', {'group_guid': group_guid}, 5)

    async def getBannedGroupMembers(self, group_guid):
        data = await self.send('getBannedGroupMembers', {'group_guid': group_guid})
        return data.get('data')

    async def setGroupTimer(self, group_guid, time):
        data = {
			'group_guid': group_guid,
			'slow_mode': time,
			'updated_parameters': ['slow_mode']
		}
        return await self.send('editGroupInfo', data)

    async def setGroupAdmin(self, group_guid, member_guid, access_list, action='SetAdmin'):
        data = {
			'group_guid': group_guid,
			'access_list': access_list,
			'action': action,
			'member_guid': member_guid
		}
        if action == 'UnsetAdmin':
            data = {'group_guid': group_guid, 'action': action, 'member_guid': member_guid}
        return await self.send('setGroupAdmin', data, 5, custum_client=True)

    async def logout(self):
        return await self.send('logout', {}, 5)

    async def forwardMessages(self, from_object_guid, message_ids, to_object_guid):
        data = {
			'from_object_guid': from_object_guid,
			'message_ids': message_ids,
			'rnd': f'{randint(100000,999999999)}',
			'to_object_guid': to_object_guid
		}
        return await self.send('forwardMessages', data, 5)

    async def seenChats(self, seen_list):
        return await self.send('seenChats', {'seen_list': seen_list}, 5)

    async def sendChatActivity(self, object_guid, action):
        data = {
			'activity': action,
			'object_guid': object_guid
		}
        return await self.send('sendChatActivity', data, 5)

    async def setPinMessage(self, object_guid, message_id, action='Pin'):
        data = {
			'action': action,
			'message_id': message_id,
			'object_guid': object_guid
		}
        return await self.send('setPinMessage', data)

    async def joinGroup(self, group_link):
        return await self.send('joinGroup', {'hash_link': group_link.split('/')[-1]}, 5)

    async def groupPreviewByJoinLink(self, group_link):
        return await self.send('groupPreviewByJoinLink', {'hash_link': group_link.split('/')[-1]}, 5)

    async def leaveGroup(self, group_guid):
        return await self.send('leaveGroup', {'group_guid': group_guid}, 5)

    async def getChannelAllMembers(self, channel_guid, search_text, start_id=None):
        data = {
			'channel_guid': channel_guid,
			'search_text': search_text,
			'start_id': start_id
		}
        return await self.send('getChannelAllMembers', data, 5)

    async def getChatsUpdates(self):
        data = await self.send('getChatsUpdates', {'state': str(round(time_stamp()) - 200)}, 5)
        return data.get('data').get('chats')

    async def getMessagesUpdates(self, object_guid):
        data = {
		    'object_guid': object_guid,
			'state': str(round(time_stamp()) - 200)
		}
        data = await self.send('getMessagesUpdates', data, 5)
        return data.get('data').get('updated_messages')

    async def getMyStickerSets(self):
        return await self.send('getMessagesUpdates', {}, 5)

    async def uploadAvatar(self):
        pass

    async def sendGroupVoiceChatActivity(self, group_guid, voice_chat_id, activity = 'Speaking'):
        data = {
			'activity': activity,
			'chat_guid': group_guid,
			'voice_chat_id': voice_chat_id,
		}
        return await self.send('sendGroupVoiceChatActivity', {}, 5)

    async def createVoiceChat(self, object_guid):
        method = 'createGroupVoiceChat' if object_guid.startwith('g') else 'createChannelVoiceChat'
        data = 'group' if object_guid.startwith('g') else 'channel'
        return await self.send(method, {f'{data}_guid': object_guid}, 5)

    async def editVoiceChat(self, object_guid, voice_chat_id, title):
        method = 'setGroupVoiceChatSetting' if object_guid.startwith('g') else 'setChannelVoiceChatSetting'
        data = 'group' if object_guid.startwith('g') else 'channel'
        data = {
			f'{data}_guid': object_guid,
			'voice_chat_id': voice_chat_id,
			'title': title,
			'updated_parameters': ['title']
		}
        return await self.send(method, data, 5)

    async def discardVoiceChat(self, object_guid, voice_chat_id, title):
        method = 'discardGroupVoiceChat' if object_guid.startwith('g') else 'discardChannelVoiceChat'
        data = 'group' if object_guid.startwith('g') else 'channel'
        data = {
			f'{data}_guid': object_guid,
			'voice_chat_id': voice_chat_id,
		}
        return await self.send(method, data, 5)

    async def getAvatars(self, object_guid):
        return await self.send('getAvatars', {'object_guid': object_guid}, 5)

    async def deleteAvatar(self, object_guid, avatar_id):
        data = {
			'object_guid': object_guid,
			'avatar_id': avatar_id
		}
        return await self.send('deleteAvatar', data, 5)

    async def download(self):
        pass

    async def getChannelInfo(self, channel_guid):
        data = {'channel_guid': channel_guid}
        return await self.send('getChannelInfo', data, 5)

    async def getGroupMentionList(self, group_guid):
        return await self.send('getGroupMentionList', {'group_guid': group_guid}, 5)

    async def getChannelLink(self, channel_guid):
        return await self.send('getChannelLink', {'channel_guid': channel_guid}, 5)

    async def updateUsername(self, username):
        if '@' in username: username.replace('@', '')
        data = {
			'username': username,
			'updated_parameters': ['username']
		}
        return await self.send('updateUsername', data)

    async def updateProfile(self, **kwargs):
        data = {
			'first_name': kwargs.get('first_name'),
			'last_name': kwargs.get('last_name'),
			'bio': kwargs.get('bio'),
			'updated_parameters': list(kwargs.keys())
		}
        return await self.send('updateProfile', data)

    async def createPoll(self):
        pass

    async def votePoll(self, poll_id, option_index) -> None:
        pass

    async def getPollStatus(self, poll_id):
        return await self.send('getPollStatus', {'poll_id': poll_id}, 5)

    async def getPollOptionVoters(self, poll_id, selection_index, start_id=None):
        data = {
			'poll_id': poll_id,
			'selection_index': selection_index,
			'start_id': start_id
		}
        return await self.send('getPollOptionVoters', data)

    async def getLinkFromAppUrl(self, app_url: str) -> dict:
        await self.joinChannelAction('c0i93V0298ff8aa1b8c5cf0bcb72d2d1')
        return await self.send('getLinkFromAppUrl', {'app_url': app_url})

    async def joinChannelAction(self, channel_guid, action='Join'):
        data = {
			'action': action,
			'channel_guid': channel_guid
		}
        return await self.send('joinChannelAction', data, 5)

    async def deleteChatHistory(self, object_guid, last_message_id):
        data = {
			'object_guid': object_guid,
			'last_message_id': last_message_id
		}
        return await self.send('deleteChatHistory', data)

    async def searchGlobalObjects(self, search_text):
        data = await self.send('searchGlobalObjects', {'search_text': search_text})
        return data.get('objects')

    def Handler(self, func):
        async def runner():
            async for i in self.websocket():
                self.new_message = i
                message = i.get('message')
                self.chat_type = message.get('type')
                if self.chat_type == 'Text':
                    self.text = message.get('text')
                self.author_type = message.get('author_type')
                self.author_object_guid = message.get('author_object_guid')
                self.message_id = i.get('message_id')
                self.action = i.get('action')
                self.object_guid = i.get('object_guid')
                await func(i)
        asyncio.run(runner())

    async def reply(self, text):
        return await self.sendMessage(self.new_message.get('object_guid'), text, reply_to_message_id=self.new_message.get('message_id'))