import sys,os,socket
import argparse
from rich.console import Console
import mxpi,platform
from rich.table import Table


def cmds(cmd):
    os.system(cmd)

def get_host_ip():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
            #print(ip)
            return ip
        finally:
            s.close()

def main():
    parser = argparse.ArgumentParser()
    parser.description='You can specify ip and port'
    parser.add_argument("-b", "--ip", help="Ip Address", default=False)
    parser.add_argument("-p", "--post", help="Access Port", default=False)
    parser.add_argument("-r", "--run", help="Run Program", default=False)
    args = parser.parse_args()
    if args.run==False:
        if args.ip==False:
            ip=get_host_ip()
        else:
            ip=args.ip
        if args.post==False:
            post='80'
        else:
            post=args.post
        Version='1.1.0'
        console = Console()
        table = Table(title="[red]M x P i[/red]",style="bold")
        table.add_column("Version:"+Version, style="cyan", no_wrap=True,justify="center")
        table.add_row("Info: Welcome to MxPi("+Version+"):smiley: !",style="bold")
        table.add_row("")
        table.add_row("MxPi启动成功,打开:http://"+ip+':'+post,style="bold #0cd45c")
        table.add_row("")
        table.add_row("(Ctrl+C或者关闭终端即可关闭MxPi)",style="bold red")
        console.print(table, justify="center")
        console.rule("程序输出信息")
        #console.print("---------------------------------------------------------------------------------",style=" red")
        #console.print("Welcome to MxPi(1.1.0)!:smiley:   System:"+platform.system()+"   IP: "+ip+":"+post,style="bold red")
        #console.print("---------------------------------------------------------------------------------",style=" red")
        if(platform.system()=='Windows'):
            #console.print("MxPi启动成功,打开:http://"+ip+':'+post,style=" #0cd45c")
            #console.print("",style=" red")
            #console.print("(Ctrl+C或者关闭终端即可关闭MxPi)",style="red")
            cmds('cd '+os.path.dirname(mxpi.__file__)+' & daphne mxpi.app.asgi:django_application -b '+ip+" -p "+post+" -v 0")
        else:
            #console.print("MxPi启动成功,打开:http://"+ip+':'+post ,style="bold #0ba248")
            #console.print("(Ctrl+C或者关闭终端即可关闭MxPi)",style="bold red")
            cmds('cd '+os.path.dirname(mxpi.__file__)+' & sudo daphne mxpi.app.asgi:django_application -b '+ip+" -p "+post+" -v 0")
    else:
        if(platform.system()=='Windows'):
            cmds('python '+os.path.abspath(os.path.dirname(mxpi.__file__))+'/file/test.py')
        else:
            cmds('sudo python3 '+os.path.abspath(os.path.dirname(mxpi.__file__))+'/file/test.py')


main()