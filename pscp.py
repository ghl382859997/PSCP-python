# encoding:utf-8

import paramiko
import sys
import os
import stat

def ssh_connect(hostname, username, password, port=22):
    try:

        ssh = paramiko.SSHClient()

        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        

        ssh.connect(hostname, port, username, password)
        
        return ssh
        
    except Exception as e:
        return None

def sftp_pull_file(remote_file, local_file, ssh):
    try:

        sftp = ssh.open_sftp()


        sftp.get(remote_file, local_file)
        

        sftp.close()

        return True
        
    except Exception as e:
        print("false:get remote file failed!")
        return False
    
def sftp_push_file(local_file, remote_file, ssh):
    try:

        sftp = ssh.open_sftp()

        sftp.put(local_file, remote_file)
        

        sftp.close()

        return True
    except Exception as e:
        return False

def sftp_push_folder(local_folder, remote_folder, ssh):
    try:

        sftp = ssh.open_sftp()

        files = os.listdir(local_folder)

        for file in files:
            tempPath = os.path.join(local_folder,file)
            if os.path.isfile(tempPath):
                local_path = tempPath.replace('\\','/')
                remote_path = os.path.join(remote_folder,file)
                remote_path = remote_path.replace('\\','/')
                try:
                    sftp.stat(remote_folder)
                except FileNotFoundError:
                    sftp.mkdir(remote_folder)
                try:
                    sftp.put(local_path, remote_path)
                except:
                    return False
            elif os.path.isdir(tempPath):
                 if file.startswith('.'):
                    continue
                 else:
                    tempDir = os.path.join(remote_folder,file)
                    tempDir = tempDir.replace('\\','/')
                    try:
                        sftp.stat(tempDir)
                    except FileNotFoundError:
                        sftp.mkdir(tempDir)
                    sftp_push_folder(tempPath.replace('\\','/'),tempDir,ssh)

        sftp.close()
        return True

    except Exception as e:
        print(f"error:{e}")


if __name__ == "__main__":

    if len(sys.argv) != 7:
        print("Usage: p_scp.exe <username> <password> <hostname> <local_path> <remote_path> <transprot type>")
        sys.exit(1)
    username = sys.argv[1]  # 远程服务器用户名
    password = sys.argv[2]  # 远程服务器密码
    hostname = sys.argv[3]  # 远程服务器IP地址
    local_path = sys.argv[4]  # 本地文件路径
    remote_path = sys.argv[5]  # 远程服务器文件路径

    type = sys.argv[6]

    

    ssh = ssh_connect(hostname, username, password, 22)

    if ssh is not None:
        if type == "push":
            if os.path.isfile(local_path):
                tempName = os.path.basename(local_path)
                remote_path = os.path.join(remote_path,os.path.basename(local_path))
                remote_path = remote_path.replace('\\','/')
                res = sftp_push_file(local_path,remote_path,ssh)
                if res:
                    print("success")
                else:
                    print("error")
            elif os.path.isdir(local_path):
                sftp = ssh.open_sftp()
                parentDir = os.path.basename(local_path)
                parentDir = os.path.join(remote_path,parentDir)
                try:
                    sftp.stat(parentDir)
                except:
                    sftp.mkdir(parentDir)
                sftp.close()
                res = sftp_push_folder(local_path,parentDir,ssh)
                if res:
                    print("success")
                else:
                    print("error")
        elif type == "pull":
            sftp_pull_file(remote_path,local_path,ssh)
    else:
        print("error,connect")
    sys.exit()

