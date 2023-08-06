# -*- coding: utf-8 -*-
import os
import logging
import paramiko
import stat

from manoutils.wrapper.wrapper import develLogWrapper
from manoutils.config.ConfigManager import configMgr

logger = configMgr.getLogger()


class SftpClient(object):
    def connect(self, host='', port='', username='', password=''):
        transport = paramiko.Transport((host, port))
        transport.connect(username=username, password=password)
        self.__transport = transport
        self.__sftp = paramiko.SFTPClient.from_transport(self.__transport)

    def close(self):
        self.__transport.close()

    @develLogWrapper
    def uploadFile(self, localFileName, remoteFileName):
        # file_name = self.create_file()
        self.__sftp.put(localFileName, remoteFileName)

    @develLogWrapper
    def downloadFile(self, remoteFileName, localFileName):
        self.__sftp.get(remoteFileName, localFileName)

    @develLogWrapper
    def cmd(self, command):
        ssh = paramiko.SSHClient()
        ssh._transport = self.__transport
        stdin, stdout, stderr = ssh.exec_command(command)
        result = stdout.read()
        print (str(result, encoding='utf-8'))
        return result

    @develLogWrapper
    def downloadDir(self, remoteDirName, localDirName):
        if not os.path.exists(localDirName):
            os.makedirs(localDirName)
        fileNames = self.__sftp.listdir_attr(remoteDirName)
        for fileName in fileNames:
            if stat.S_ISDIR(fileName.st_mode):
                localDirName = os.path.join(localDirName, fileName.filename)
                remoteDirName = os.path.join(remoteDirName, fileName.filename) + "/"
                if not os.path.exists(localDirName):
                    os.makedirs(localDirName)
                self.downloadDir(remoteDirName=remoteDirName, localDirName=localDirName)
            else:
                localFileName = os.path.join(localDirName, fileName.filename)
                remoteFileName = remoteDirName + '/' + fileName.filename
                self.__sftp.get(remoteFileName, localFileName)

    @develLogWrapper
    def getRemoteFileNames(self, remoteDirName):
        remoteFileNames = list()
        fileNames = self.__sftp.listdir_attr(remoteDirName)
        for fileName in fileNames:
            if stat.S_ISDIR(fileName.st_mode):
                remoteFileNames = remoteFileNames + self.getRemoteFileNames(remoteDirName + "/" + fileName.filename)
            else:
                remoteFileNames.append(os.path.join(remoteDirName, fileName.filename))
        return remoteFileNames
