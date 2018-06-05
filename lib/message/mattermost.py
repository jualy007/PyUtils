#!/usr/bin/python
# -*- coding:utf-8 -*-

from mattermostdriver import Driver


class MattermostClient():
    '''
    This is Mattermost Client lib
    '''

    def __init__(self, host, user, password):
        self.mmClient = Driver({
            'url': host,
            'port': 80,
            'login_id': user,
            'password': password,
            'scheme': 'http'
        })

        self.mmClient.login()

    def sendMsgToChannel(self, team, channel, msg):
        self.mmClient.posts.create_post({
            'channel_id':
            self._getChannelId(team, channel),
            'message':
            msg
        })

    def sendMsgToUser(self, name, msg):
        #Create a direct message channel
        id = self._createDirectChannnel(name)

        self.mmClient.posts.create_post({'channel_id': id, 'message': msg})

    def _getUserId(self, name):
        if name.__contains__('@'):
            return self.mmClient.users.get_user_by_email(name).get('id')
        else:
            return self.mmClient.users.get_user_by_username(name).get('id')

    def _getChannelId(self, team, channel):
        return self.mmClient.channels.get_channel_by_name_and_team_name(
            team, channel).get('id')

    def _createDirectChannnel(self, name):
        peers = [
            self._getUserId(name),
            self.mmClient.users.get_user(user_id='me').get('id')
        ]
        res = self.mmClient.channels.create_direct_message_channel(peers)
        return res.get('id')

    def _uploadFile(self, id, file):
        res = self.mmClient.files.upload_file(
            channel_id=id, files={'files': (file, open(file))})
        return res.get('file_infos')[0].get('id')

    def sendFileToUser(self, name, msg, file):
        id = self._createDirectChannnel(name)
        file_id = self._uploadFile(id, file)

        self.mmClient.posts.create_post({
            'channel_id': id,
            'message': msg,
            'file_ids': [file_id]
        })

    def sendFileToChannel(self, team, channel, msg, file):
        id = self._getChannelId(team, channel)
        file_id = self._uploadFile(id, file)

        self.mmClient.posts.create_post({
            'channel_id': id,
            'message': msg,
            'file_ids': [file_id]
        })


if __name__ == '__main__':
    pass
