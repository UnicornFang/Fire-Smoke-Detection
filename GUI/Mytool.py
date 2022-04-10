import winreg


class tool():
    @staticmethod
    def get_desktop():
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')  # 利用系统的链表
        return str(winreg.QueryValueEx(key, "Desktop")[0])  # 返回的是Unicode类型数据


if __name__ == '__main__':
    print(tool.get_desktop())
