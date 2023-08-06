from colorama import init
from time import sleep as dd
from sys import exit as tc
import platform
os=platform.system()
def pdios():
    print('判断系统中')
    dd(0.5)
    if (os=='Windows'):
        print('<欢迎Windows系统用户>')
        init(autoreset=True)
    elif (os=='Linux'):
        print('$欢迎Linux系统用户$')
        init(autoreset=False)
    elif (os=='Unix'):
        print('^欢迎Unix用户')
        init(autoreset=False)
    elif (os=='Darwin'):
        print('欢迎Max os用户,以下显示可能出现异常')
        init(autoreset=False)
    else:
        print('无法您的判断系统,请更换设备或到https://pypi.org/ycc找到我的邮箱，报告您的系统,否则将回影响您的视觉感受并出现乱码情况')
        print('你现在可以选择1.退出\n2.我能忍受，开始\n3.输入其他字符退出')
        choose_exit=input('请选择:')
        if choose_exit=='1':
            tc('goodbye')
        elif choose_exit=='2':
            pass
        else:
            tc('goodbye')
#pdios()