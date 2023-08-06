from .connections.requests import Requests
from random import randint
from .connections.websocket import WebSocket
from time import time as time_stamp
import asyncio


class Client(object):
    def __init__(self, auth) -> None:
        self.__requests = Requests(auth)
        self.send = self.__requests.send
        self.upload = self.__requests.uploadFile
        self.websocket = WebSocket(auth).handler
        self._auth = auth
    
    async def sendMessage(self, object_guid, text, reply_to_message_id=None) -> dict:
        data: dict = {
			'object_guid': object_guid,
			'rnd': f'{randint(100000, 999999999)}',
			'text': text,
			'reply_to_message_id': reply_to_message_id
		}
        return await self.send('sendMessage', data, 5)

    async def requestSendFile(self, file_name, mime, size) -> dict:
        data: dict = {
            'file_name': file_name,
			'mime': mime,
			'size': size
		}
        return await self.send('requestSendFile', data, 5)

    async def getChats(self, start_id=None) -> dict:
        return await self.send('getChats', {'start_id': start_id}, 5)

    async def editMessage(self, message_id, object_guid, new_text) -> dict:
        data: dict = {
			'message_id': message_id,
			'object_guid': object_guid,
			'text': new_text
		}
        return await self.send('editMessage', data, 5)

    async def deleteMessages(self, object_guid, message_ids_list, delete_type='Global') -> dict:
        data: dict = {
			'object_guid': object_guid,
			'message_ids': message_ids_list,
			'type': delete_type
		}
        return await self.send('deleteMessages', data, 5)

    async def getUserInfo(self, user_guid: str) -> dict:
        return await self.send('getUserInfo', {'user_guid': user_guid}, 5)

    async def getMessagesInterval(self, object_guid, middle_message_id) -> dict:
        data: dict = {
			'object_guid': object_guid,
			'middle_message_id': middle_message_id
		}
        return await self.send('getMessagesInterval', data, 5)

    async def getObjectByUsername(self, username) -> dict:
        return await self.send('getObjectByUsername', {'username': username}, 5)

    async def banGroupMember(self, group_guid, member_guid, action='Set') -> dict:
        data: dict = {
			'group_guid': group_guid,
			'member_guid': member_guid,
			'action': action
		}
        return await self.send('banGroupMember', data, 5)

    async def addGroupMembers(self, group_guid: str, member_guids: list) -> dict:
        data: dict = {
			'group_guid': group_guid,
			'member_guids': member_guids
		}
        return await self.send('addGroupMembers', data, 5)

    async def addChannelMembers(self, channel_guid: str, member_guids: list) -> dict:
        data: dict = {
			'channel_guid': channel_guid,
			'member_guids': member_guids
		}
        return await self.send('addChannelMembers', data, 5)

    async def getGroupAdminMembers(self, group_guid: str, get_admin_guids=False) -> dict or list:
        in_chat_members: dict = await self.send('getGroupAdminMembers', {'group_guid': group_guid}, 5)
        in_chat_members: list = in_chat_members.get('data').get('in_chat_members')
        admin_list_guids: list = []
        if get_admin_guids:
            for guid in in_chat_members:
                admin_list_guids.append(guid.get('member_guid'))
            return admin_list_guids
        else:
            return in_chat_members

    async def getMessagesByID(self, object_guid: str, message_ids: list) -> dict:
        data: dict = {
			'object_guid': object_guid,
			'message_ids': message_ids
		}
        return await self.send('getMessagesByID', data, 5)

    async def setGroupDefaultAccess(self, group_guid: str, access_list: list) -> dict:
        data: dict = {
			'access_list': access_list,
			'group_guid': group_guid
		}
        return await self.send('setGroupDefaultAccess', data)

    async def getGroupAllMembers(self, group_guid, start_id=None) -> dict:
        data: dict = {
			'group_guid': group_guid,
			'start_id': start_id
		}
        return await self.send('getGroupAllMembers', data, 5)

    async def getGroupInfo(self, group_guid: str) -> dict:
        return await self.send('getGroupInfo', {'group_guid': group_guid}, 5)

    async def getGroupLink(self, group_guid: str) -> str:
        result: dict = await self.send('getGroupLink', {'group_guid': group_guid}, 5)
        link: str = result.get('data').get('join_link')
        return link

    async def setGroupLink(self, group_guid: str) -> dict:
        return await self.send('setGroupLink', {'group_guid': group_guid}, 5)

    async def getBannedGroupMembers(self, group_guid: str) -> list:
        data: dict = await self.send('getBannedGroupMembers', {'group_guid': group_guid})
        return data.get('data')

    async def setGroupTimer(self, group_guid: str, time: str):
        data: dict = {
			'group_guid': group_guid,
			'slow_mode': time,
			'updated_parameters': ['slow_mode']
		}
        return await self.send('editGroupInfo', data)

    async def setGroupAdmin(self, group_guid: str, member_guid: str, access_list: list, action='SetAdmin') -> dict:
        data: dict = {
			'group_guid': group_guid,
			'access_list': access_list,
			'action': action,
			'member_guid': member_guid
		}
        if action == 'UnsetAdmin':
            data: dict = {'group_guid': group_guid, 'action': action, 'member_guid': member_guid}
        return await self.send('setGroupAdmin', data, 5, custum_client=True)

    async def logout(self) -> dict:
        return await self.send('logout', {}, 5)

    async def forwardMessages(self, from_object_guid: str, message_ids: list, to_object_guid: str) -> dict:
        data: dict = {
			'from_object_guid': from_object_guid,
			'message_ids': message_ids,
			'rnd': f'{randint(100000,999999999)}',
			'to_object_guid': to_object_guid
		}
        return await self.send('forwardMessages', data, 5)

    async def seenChats(self, seen_list: list) -> dict:
        return await self.send('seenChats', {'seen_list': seen_list}, 5)

    async def sendChatActivity(self, object_guid: str, action: str) -> dict:
        data: dict = {
			'activity': action,
			'object_guid': object_guid
		}
        return await self.send('sendChatActivity', data, 5)

    async def setPinMessage(self, object_guid, message_id, action='Pin') -> dict:
        data: dict = {
			'action': action,
			'message_id': message_id,
			'object_guid': object_guid
		}
        return await self.send('setPinMessage', data)

    async def joinGroup(self, group_link: str) -> dict:
        return await self.send('joinGroup', {'hash_link': group_link.split('/')[-1]}, 5)

    async def groupPreviewByJoinLink(self, group_link: str) -> dict:
        return await self.send('groupPreviewByJoinLink', {'hash_link': group_link.split('/')[-1]}, 5)

    async def leaveGroup(self, group_guid: str):
        return await self.send('leaveGroup', {'group_guid': group_guid}, 5)

    async def getChannelAllMembers(self, channel_guid: str, search_text: str, start_id: bool=None) -> dict:
        data: dict = {
			'channel_guid': channel_guid,
			'search_text': search_text,
			'start_id': start_id
		}
        return await self.send('getChannelAllMembers', data, 5)

    async def getChatsUpdates(self) -> list:
        data: dict = await self.send('getChatsUpdates', {'state': str(round(time_stamp()) - 200)}, 5)
        return data.get('data').get('chats')

    async def getMessagesUpdates(self, object_guid: str) -> list:
        data: dict = {
		    'object_guid': object_guid,
			'state': str(round(time_stamp()) - 200)
		}
        data: dict = await self.send('getMessagesUpdates', data, 5)
        return data.get('data').get('updated_messages')

    async def getMyStickerSets(self) -> dict:
        return await self.send('getMessagesUpdates', {}, 5)

    async def uploadAvatar(self) -> None:
        pass

    async def sendGroupVoiceChatActivity(self, group_guid: str, voice_chat_id: str, activity: str = 'Speaking'):
        data: dict = {
			'activity': activity,
			'chat_guid': group_guid,
			'voice_chat_id': voice_chat_id,
		}
        return await self.send('sendGroupVoiceChatActivity', {}, 5)

    async def createVoiceChat(self, object_guid: str) -> dict:
        method: str = 'createGroupVoiceChat' if object_guid.startwith('g') else 'createChannelVoiceChat'
        data: str = 'group' if object_guid.startwith('g') else 'channel'
        return await self.send(method, {f'{data}_guid': object_guid}, 5)

    async def editVoiceChat(self, object_guid: str, voice_chat_id: str, title: str):
        method: str = 'setGroupVoiceChatSetting' if object_guid.startwith('g') else 'setChannelVoiceChatSetting'
        data: str = 'group' if object_guid.startwith('g') else 'channel'
        data: dict = {
			f'{data}_guid': object_guid,
			'voice_chat_id': voice_chat_id,
			'title': title,
			'updated_parameters': ['title']
		}
        return await self.send(method, data, 5)

    async def discardVoiceChat(self, object_guid: str, voice_chat_id: str, title: str):
        method: str = 'discardGroupVoiceChat' if object_guid.startwith('g') else 'discardChannelVoiceChat'
        data: str = 'group' if object_guid.startwith('g') else 'channel'
        data: dict = {
			f'{data}_guid': object_guid,
			'voice_chat_id': voice_chat_id,
		}
        return await self.send(method, data, 5)

    async def getAvatars(self, object_guid: str) -> dict:
        return await self.send('getAvatars', {'object_guid': object_guid}, 5)

    async def deleteAvatar(self, object_guid, avatar_id: str) -> dict:
        data: dict = {
			'object_guid': object_guid,
			'avatar_id': avatar_id
		}
        return await self.send('deleteAvatar', data, 5)

    async def download(self) -> None:
        pass

    async def getChannelInfo(self, channel_guid: str):
        data: str = {'channel_guid': channel_guid}
        return await self.send('getChannelInfo', data, 5)

    async def getGroupMentionList(self, group_guid: str):
        return await self.send('getGroupMentionList', {'group_guid': group_guid}, 5)

    async def getChannelLink(self, channel_guid: str):
        return await self.send('getChannelLink', {'channel_guid': channel_guid}, 5)

    async def updateUsername(self, username):
        if '@' in username: username.replace('@', '')
        data: dict = {
			'username': username,
			'updated_parameters': ['username']
		}
        return await self.send('updateUsername', data)

    async def updateProfile(self, **kwargs):
        data: str = {
			'first_name': kwargs.get('first_name'),
			'last_name': kwargs.get('last_name'),
			'bio': kwargs.get('bio'),
			'updated_parameters': list(kwargs.keys())
		}
        return await self.send('updateProfile', data)

    async def createPoll(self) -> None:
        pass

    async def votePoll(self, poll_id: str, option_index: str) -> None:
        pass

    async def getPollStatus(self, poll_id: str):
        return await self.send('getPollStatus', {'poll_id': poll_id}, 5)

    async def getPollOptionVoters(self, poll_id, selection_index, start_id=None) -> dict:
        data: dict = {
			'poll_id': poll_id,
			'selection_index': selection_index,
			'start_id': start_id
		}
        return await self.send('getPollOptionVoters', data)

    async def getLinkFromAppUrl(self, app_url: str) -> dict:
        await self.joinChannelAction('c0i93V0298ff8aa1b8c5cf0bcb72d2d1')
        return await self.send('getLinkFromAppUrl', {'app_url': app_url})

    async def joinChannelAction(self, channel_guid: str, action='Join'):
        data: dict = {
			'action': action,
			'channel_guid': channel_guid
		}
        return await self.send('joinChannelAction', data, 5)

    async def deleteChatHistory(self, object_guid: str, last_message_id: str) -> dict:
        data: str = {
			'object_guid': object_guid,
			'last_message_id': last_message_id
		}
        return await self.send('deleteChatHistory', data)

    async def searchGlobalObjects(self, search_text: str) -> list:
        data: dict = await self.send('searchGlobalObjects', {'search_text': search_text})
        return data.get('objects')

    def Handler(self, func) -> None:
        pass