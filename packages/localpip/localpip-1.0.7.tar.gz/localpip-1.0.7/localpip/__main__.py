import os
import subprocess
import sys
import urllib
from ctypes import Structure, byref, windll
from ctypes.wintypes import BOOL, LPWSTR
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

import requests
from bs4 import BeautifulSoup
from pypac import PACSession, get_pac

lpip_version = "1.0.7"
__author__ = "Alex BOURG"
__copyright__ = "Copyright 2021"
__license__ = "GPL"
__version__ = lpip_version
__email__ = "alex.bourg@outlook.com"
__status__ = "Production"
appname = 'localpip'


url = 'https://github.com/alexbourg/localpip/tree/main/Packages'
url_download = 'https://raw.githubusercontent.com/alexbourg/localpip/main/Packages/'
path_download = r'C:\Program64\Python\Packages'


def exitapp():
    os._exit(0)


def info(error, details):
    print()
    print("*" * 100, '\n')
    print("## Enter the command in the following format:")

    def print_heading():
        # print("\n")
        print("\u250C" + "\u2500"*35 + "\u252C" + "\u2500"*45 + "\u2510")
        print("\u2502" + " Action" + " "*28 +
              "\u2502" + " Command" + " "*37 + "\u2502")
        print("\u251c" + "\u2500" * 35 + "\u253c" + "\u2500" * 45 + "\u2524")

    def print_row(hop, delay):
        h_format = "{0:{align}{width}}".format(hop, align="<", width=34)
        d_format = "{0:{align}{width}}".format(delay, align="<", width=44)
        print("\u2502" + " " + h_format + "\u2502" + " " + d_format + "\u2502")

    def print_sep():
        print("\u251c" + "\u2500" * 35 + "\u253c" + "\u2500" * 45 + "\u2524")

    def print_end():
        print("\u2514" + "\u2500" * 35 + "\u2534" + "\u2500" * 45 + "\u2518")

    print_heading()
    print_row('Package management', f'{appname} <Action> <PackageName>')
    print_sep()
    print_row('To install local repo', f'{appname} install or lpip download')
    print_sep()
    print_row('To update the local repo', f'{appname} update')
    print_sep()
    print_row('Upgrade lpip ', f'{appname} upgrade')
    print_sep()
    print_row('About lpip  ', f'{appname} about')
    print_sep()
    print("\u251c" + " " * 32 + "Examples" + " " * 41 + "\u2524")
    print_sep()
    print_row('Install one package', f'{appname} install pandas')
    print_sep()
    print_row('Install multiple packages',
              f'{appname} install pandas openpyxl Keras')
    print_sep()
    print_row('Install requirement file', f'{appname} install req')
    print_sep()
    print_row('Uninstall package', f'{appname} uninstall pandas')
    print_sep()
    print_row('Upgrade package', f'{appname} upgrade pandas')
    print_sep()
    print_row('Online upgrade package', f'{appname} onlineupgrade pandas')
    print_sep()
    print_row('List installed packages', f'{appname} list')
    print_end()
    print()
    print(error, details)
    print()
    print("*" * 100)
    print()
    exitapp()


def install(package, action, path):
    if package == 'pdfminer':
        package = 'pdfminer.six'

    # Install command
    if action == "install":
        print()
        print("*" * 100)
        print(f" Installing {package}...")
        print()
        print()

        if "pip" in package:
            os.system(
                f"python -m pip install --upgrade pip --no-index --find-links {path}"
            )

        elif "numpy==1.19.2" in package and sys.version_info.minor == 9:
            # pass
            print(
                f" {package} is not compatible with Python 39, higher version will be installed.")

        else:
            # try:
            #     os.system(f"pip {action} --no-index --find-links {path} {package}")
            # except:
            #     print(f"{package} is not available in the local repo")
            #     print(f"Try installing using the regular pip > pip install {package}")
            if os.path.isdir(r'C:\Program64\Python\Packages'):
                out = subprocess.Popen(
                    ["pip", action, "--no-index",
                        "--find-links", path, package],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                )
                stdout, stderr = out.communicate()
                x = stdout.decode("utf-8")
                print(' ', x)
            else:
                x = ''
            if "Could not find a version that satisfies" in x or not os.path.isdir(r'C:\Program64\Python\Packages'):
                print(f" {package} is not available in the local repo.")
                print("_"*50)
                print(f" Installing {package} from the internet...")
                print("_"*50)
                os.system(f"pip install {package}")
            print()
            print(f"*****{package} installation has been completed!*****\n")
            print("*" * 100)

    # Uninstall command
    elif action == "uninstall":
        print()
        print('*'*100)
        print(f" Uninstalling {package} ...")
        print()
        print()
        os.system(f"pip {action} {package} -y")
        print()
        print(f"*****{package} uninstallation has been completed!*****\n")
        print("*" * 100)

    elif action == "download":
        print()
        print('*'*100)
        print(f" Downloading {package} ...")
        print()
        print()
        os.system(f"pip {action} {package}")
        print()
        print(f"*****{package} download has been completed!*****\n")
        print("*" * 100)

    elif action == "wheel":
        print()
        print('*'*100)
        print(f" Creating wheel for {package} ...")
        print()
        print()
        os.system(f"pip {action} {package}")
        print()
        print(f"*****{package} wheel command has been completed!*****\n")
        print("*" * 100)

    # Upgrade command
    elif action == "upgrade":
        print()
        print(
            " *******************************************************************************************************"
        )
        print(f" Upgrading {package} ...")
        print()
        print()
        if "pip" in package:
            os.system(
                f"python -m pip install --upgrade pip --no-index --find-links {path}"
            )
        elif "numpy==1.19.2" in package and sys.version_info.minor == 9:
            print(f"{package} is not compatible with current Python version")
        else:
            os.system(
                f"pip install --no-index --find-links {path} {package} -U")
            # os.system(f"pip install {package} -U")
        print()
        print(f"*****{package} upgrade has been completed!*****\n")
        print("*" * 100)

    elif action == "onlineupgrade":
        print()
        print(
            " *******************************************************************************************************"
        )
        print(f" Upgrading {package} ...")
        print()
        print()
        if "pip" in package:
            os.system(
                f"python -m pip install --upgrade pip --no-index --find-links {path}"
            )
        elif "numpy==1.19.2" in package and sys.version_info.minor == 9:
            print(f"{package} is not compatible with current Python version")
        else:
            # os.system(
            # f"pip install --no-index --find-links {path} {package} -U")
            os.system(f"pip install {package} -U")
        print()
        print(f"*****{package} upgrade has been completed!*****\n")
        print("*" * 100)


def pip_list():
    print()
    os.system(f"pip list")
    print()
    exitapp()


def lpip_remove():
    # Remove the old packages folder
    print()
    print('*'*100, '\n')
    pip = input(
        " lpip repository will be uninstalled, are you sure you want to continue? (yes/no): "
    ).lower()
    print()
    if pip.startswith("y"):
        command = 'if (Test-Path "C:\\Program64\\Python\\Packages") {Remove-Item "C:\\Program64\\Python\\Packages" -Recurse -Force}'
        start_PS = powershell(command)
        if start_PS.returncode != 0:
            print("Error: command 1")
        else:
            print("*" * 100, '\n')
            print(" Lpip repository has been uninstalled successfully!\n")
            print("*" * 100)
            print()
    else:
        print("*" * 100)
        print()


def lpip_about():
    print()
    print("*" * 100, '\n')
    print(
        f" - Lpip v{lpip_version} is an offline package manager for Python.\n")
    print(" - It solves packages dependencies conflict issues and compiling errors.\n")
    print(" - Internet access is required only for the first time of downloading localpip repository.\n")
    print(" - Once downloaded, you can install packages completely offline.\n")
    print(" - For technical issues or suggestions, please visit lpip/issues\n")


def lpip_upgrade():
    os.system(f"python -m pip install --upgrade lpip")


def powershell(cmd):
    completed = subprocess.run(
        ["powershell", "-Command", cmd], capture_output=True)
    return completed


def download_packages(action):
    path_script = os.path.realpath(__file__)
    path_script = path_script[: path_script.rfind("\\")]
    print("*" * 100, '\n')

    if action == "install":
        print(
            " Local repo is not installed. Installation could take up to 10 minutes, depending on your internet speed."
        )
    else:
        print(
            " Local repo will be updated. The update could take up to 10 minutes, depending on your internet speed."
        )

    download = input("\n Do you want to continue? (yes/no): ").lower()
    print()
    print("*" * 100)
    print()

    if download.startswith("y"):
        packages_list_new, packages_list_old = [], []

        def get_response(link, connection_type):
            if connection_type == 'direct':
                r = requests.get(link, allow_redirects=True,
                                 proxies=urllib.request.getproxies(), timeout=4)

            elif connection_type == 'pac_url':
                class WINHTTP_CURRENT_USER_IE_PROXY_CONFIG(Structure):
                    _fields_ = [('fAutoDetect', BOOL), ('lpszAutoConfigUrl', LPWSTR),
                                ('lpszProxy', LPWSTR), ('lpszProxyBypass', LPWSTR), ]
                winhttp = windll.winhttp
                ie_proxy_info = WINHTTP_CURRENT_USER_IE_PROXY_CONFIG()
                proxy_info = winhttp.WinHttpGetIEProxyConfigForCurrentUser(
                    byref(ie_proxy_info))
                pac = ie_proxy_info.lpszAutoConfigUrl
                pac = get_pac(url=pac)
                session = PACSession(pac)
                r = session.get(link, allow_redirects=True, timeout=4)

            elif connection_type == 'pac_session':
                session = PACSession()
                r = session.get(link, allow_redirects=True, timeout=4)

            return r

        def check_connection_type():
            try:
                r = requests.get(url, allow_redirects=True,
                                 proxies=urllib.request.getproxies(), timeout=3)
                if r:
                    connection_type = 'direct'
            except:
                try:
                    class WINHTTP_CURRENT_USER_IE_PROXY_CONFIG(Structure):
                        _fields_ = [('fAutoDetect', BOOL), ('lpszAutoConfigUrl', LPWSTR),
                                    ('lpszProxy', LPWSTR), ('lpszProxyBypass', LPWSTR), ]
                    winhttp = windll.winhttp
                    ie_proxy_info = WINHTTP_CURRENT_USER_IE_PROXY_CONFIG()
                    proxy_info = winhttp.WinHttpGetIEProxyConfigForCurrentUser(
                        byref(ie_proxy_info))
                    pac = ie_proxy_info.lpszAutoConfigUrl
                    pac = get_pac(url=pac)
                    session = PACSession(pac)
                    r = session.get(url, allow_redirects=True, timeout=3)
                    if r:
                        connection_type = 'pac_url'
                except:
                    try:
                        session = PACSession()
                        r = session.get(url, allow_redirects=True, timeout=3)
                        if r:
                            connection_type = 'pac_session'
                    except:
                        connection_type = 'PS'
            return connection_type

        def get_update(connection_type):
            response = get_response(url, connection_type)
            if response:
                soup = BeautifulSoup(response.content, 'html.parser')
                packages = soup.find_all(
                    "a", class_="js-navigation-open Link--primary")
                for package in packages:
                    package = package.text
                    packages_list_new.append(package)
            else:
                print('*'*100, '\n')
                print('Failed to retrieve updates...\n')
                print('*'*100)

        def get_current_packages():
            try:
                os.makedirs(path_download)
            except:
                pass

            try:
                for file in os.listdir(path_download):
                    if file.endswith(".whl") or file.endswith(".txt") or file.endswith(".tar.gz"):
                        packages_list_old.append(file)
            except:
                pass

        def delete_old_packages():
            obsolete_list = [
                item for item in packages_list_old if item not in packages_list_new]
            if obsolete_list:
                for idx, package in enumerate(obsolete_list):
                    if 'tensorflow' not in package:
                        path_package = os.path.join(path_download, package)
                        if os.path.isfile(path_package):
                            os.remove(path_package)
                            print(
                                f' - Deleting {str(idx+1).zfill(2)}/{len(obsolete_list)} {package}')
                        else:  # Show an error ##
                            print(" Error: %s file not found" % package)
                print('-'*50)

        def download_packages(connection_type):
            download_list = [
                item for item in packages_list_new if item not in packages_list_old]
            for idx, package in enumerate(download_list):
                response = get_response(
                    f'{url_download}/{package}', connection_type)
                if response:
                    print(
                        f' - Downloading {str(idx+1).zfill(2)}/{len(download_list)} {package}')
                    open(rf'{path_download}\{package}',
                         'wb').write(response.content)
                else:
                    print(
                        f' - Failed {str(idx).zfill(2)}/{len(download_list)} {package}')
            print()

        use_PS = False
        connection_type = check_connection_type()
        print()
        print('-'*50)
        print(' - Connection type: ', connection_type)
        print('-'*50)
        print()

        if connection_type != 'PS':
            try:
                get_update(connection_type)
                get_current_packages()
                delete_old_packages()
                download_packages(connection_type)
            except Exception as e:
                print('-'*100)
                print(' - Connection issue: ')
                print(' ', e)
                print()
                print(' - Retrying... ')
                print('-'*100)

                import time
                for i in range(4):
                    try:
                        packages_list_new, packages_list_old = [], []
                        get_update(connection_type)
                        get_current_packages()
                        delete_old_packages()
                        download_packages(connection_type)
                    except:
                        time.sleep(4)
                        if i == 3:
                            use_PS = True

        if connection_type == 'PS' or use_PS:
            print()
            print("Download is starting ...")
            print()
            command = 'if (Test-Path "C:\\Program64\\Python\\temp") {Remove-Item "C:\\Program64\\Python\\temp" -Recurse -Force}'
            start_PS = powershell(command)
            if start_PS.returncode != 0:
                print("Error: command 0")

            create_temp = r"New-Item -Path C:\Program64\Python -Name \"temp\" -ItemType directory -Force"
            PS_create_temp = powershell(create_temp)

            downloadPath = r"'C:\Program64\Python\temp\LocalPIP.zip'"
            downloadUrl = (
                "'https://codeload.github.com/alexbourg/localpip/zip/refs/heads/main'"
            )

            download_with_proxy = f"$ProgressPreference = 'SilentlyContinue' ; $proxyurl = ([System.Net.WebRequest]::GetSystemWebproxy()).GetProxy({downloadUrl}) ; Invoke-WebRequest {downloadUrl} -Proxy $proxyurl -ProxyUseDefaultCredentials -OutFile {downloadPath}"

            download_no_proxy = f"$ProgressPreference = 'SilentlyContinue' ; Invoke-WebRequest {downloadUrl} -OutFile {downloadPath}"

            PS_download_noproxy = powershell(download_no_proxy)
            if PS_download_noproxy.returncode != 0:
                PS_download_proxy = powershell(download_with_proxy)
                if PS_download_proxy.returncode != 0:
                    print("An error occured: %s", PS_download_proxy.stderr)
                    print()
                    print("*" * 100)
                    print(
                        " lpip couldn't be installed, please check your internet connection"
                    )
                    print(" Or manually install the repository:")
                    print(
                        "   1. Download the packages from this link: https://codeload.github.com/alexbourg/localpip/zip/refs/heads/main"
                    )
                    print(
                        '   2. Extract the zip file and copy the "Packages" folder to "C:\\Program64\\Python" path'
                    )
                    print("*" * 100)
                    command = 'if (Test-Path "C:\\Program64\\Python\\temp") {Remove-Item "C:\\Program64\\Python\\temp" -Recurse -Force}'
                    start_PS = powershell(command)
                    exitapp()
                else:
                    proxy_status = 1
                    print(" Download is almost complete.")
                    print()
                    print(" Downloading the last package, please wait...")
            else:
                proxy_status = 0
                print(" Download is almost complete.")
                print()
                print(" Downloading the last package, please wait...")

            # Remove the old packages folder
            command = 'if (Test-Path "C:\\Program64\\Python\\Packages") {Remove-Item "C:\\Program64\\Python\\Packages" -Recurse -Force}'
            start_PS = powershell(command)
            if start_PS.returncode != 0:
                print("Error: command 1")

            # Extract the zip file
            if os.path.isfile(r"C:\Program Files\7-Zip\7z.exe"):
                command = (
                    r"$ProgressPreference = 'SilentlyContinue' ; Get-ChildItem C:\Program64\Python\temp\LocalPIP.zip | % { & "
                    + '"C:\\Program Files\\7-Zip\\7z.exe" "x" $_.fullname "-oC:\\Program64\\Python\\temp\\" }'
                )
                start_PS = powershell(command)
                if start_PS.returncode != 0:
                    print("Error: command 2")
            else:
                command = r"$ProgressPreference = 'SilentlyContinue' ; Expand-Archive -LiteralPath 'C:\Program64\Python\temp\LocalPIP.zip' -DestinationPath C:\Program64\Python\temp"
                start_PS = powershell(command)
                if start_PS.returncode != 0:
                    print("Error: command 2.5")

            # Copy packages to the find destination folder
            command = 'Copy-Item -Path "C:\\Program64\\Python\\temp\\LocalPIP-main\\Packages" -Destination "C:\\Program64\\Python" -Force -Recurse'
            start_PS = powershell(command)
            if start_PS.returncode != 0:
                print("Error: command 3")

            command = 'if (Test-Path "C:\\Program64\\Python\\temp") {Remove-Item "C:\\Program64\\Python\\temp" -Recurse -Force}'
            start_PS = powershell(command)
            if start_PS.returncode != 0:
                print("Error: command 5")

            if os.path.isfile(r"C:\Program64\Python\Packages\zlinks.txt"):
                links = r"C:\Program64\Python\Packages\zlinks.txt"
                with open(links) as file:
                    for link in file:
                        if "tensorflow" in link:
                            link = link.replace(" ", "")
                            link = link.replace("\n", "")
                            if "cp39" in link:
                                tensor39 = f'"{link}"'
                                tensor39_name = tensor39[tensor39.rfind(
                                    "/") + 1:]
                                tensor39_name = tensor39_name.replace('"', "")
                            if "cp38" in link:
                                tensor38 = f'"{link}"'
                                tensor38_name = tensor38[tensor38.rfind(
                                    "/") + 1:]
                                tensor38_name = tensor38_name.replace('"', "")

                    if sys.version_info.minor == 9:
                        downloadPath = fr"C:\Program64\Python\Packages\{tensor39_name}"
                        if proxy_status == 0:
                            download_no_proxy = fr"$ProgressPreference = 'SilentlyContinue' ; Invoke-WebRequest {tensor39} -OutFile {downloadPath}"
                            PS_download_noproxy = powershell(download_no_proxy)
                            if PS_download_noproxy.returncode != 0:
                                print("Error: command 6")
                        elif proxy_status == 1:

                            download_with_proxy = f"$ProgressPreference = 'SilentlyContinue' ; $proxyurl = ([System.Net.WebRequest]::GetSystemWebproxy()).GetProxy({tensor39}) ; Invoke-WebRequest {tensor39} -Proxy $proxyurl -ProxyUseDefaultCredentials -OutFile {downloadPath}"
                            PS_download_proxy = powershell(download_with_proxy)
                            if PS_download_proxy.returncode != 0:
                                print("Error: command 7")

                    elif sys.version_info.minor == 8:
                        downloadPath = fr"C:\Program64\Python\Packages\{tensor38_name}"

                        if proxy_status == 0:
                            download_no_proxy = fr"$ProgressPreference = 'SilentlyContinue' ; Invoke-WebRequest {tensor38} -OutFile {downloadPath}"
                            PS_download_noproxy = powershell(download_no_proxy)
                            if PS_download_noproxy.returncode != 0:
                                print("Error: command 8")
                        elif proxy_status == 1:
                            download_with_proxy = f"$ProgressPreference = 'SilentlyContinue' ; $proxyurl = ([System.Net.WebRequest]::GetSystemWebproxy()).GetProxy({tensor38}) ; Invoke-WebRequest {tensor38} -Proxy $proxyurl -ProxyUseDefaultCredentials -OutFile {downloadPath}"
                            PS_download_proxy = powershell(download_with_proxy)
                            if PS_download_proxy.returncode != 0:
                                print("Error: command 9")

        print("*" * 100, '\n')
        if action == "update":
            print(f" lpip repo has been updated successfully!\n")
        else:
            print(f" lpip repo has been {action}ed successfully!\n")
        print("*" * 100)


# defining the command
def check_action(action):
    if action == "install".lower():
        return "install"
    elif action == "uninstall".lower():
        return "uninstall"
    elif action == "upgrade".lower():
        return "upgrade"
    elif action == "wheel".lower():
        return "wheel"
    elif action == "download".lower():
        return "download"
    elif action == "onlineupgrade".lower():
        return "onlineupgrade"
    else:
        info("Error: wrong option > ", action)


# defining the packages folder path
def check_packages():
    path_script = os.path.realpath(__file__)
    path_script = path_script[: path_script.rfind("\\")]
    package_dir = os.path.isdir(r"C:\Program64\Python\Packages")
    if package_dir:
        path = r"C:\Program64\Python\Packages"
        return path
    elif any(File.endswith(".whl") for File in os.listdir(path_script)):
        path = path_script
        return path
    else:
        try:
            download_packages("install")
            path = r"C:\Program64\Python\Packages"
            return path
        except Exception as e:
            print(e, e.args)
            print("Connection error: packages download failed.")
            exitapp()


def select_file():
    filetypes = (('text files', '*.txt'),)
    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    showinfo(
        title='Selected File',
        message=filename
    )
    return filename


def main(args=None):
    try:
        if len(sys.argv) == 1:
            info("Status: Not enough", "arguments")

        # mypip list
        elif "list" in sys.argv:
            pip_list()

        # initialzie mypip update/ download
        elif len(sys.argv) == 2:
            if sys.argv[1].lower() == "update":
                download_packages("update")
            elif sys.argv[1].lower() == "download" or sys.argv[1].lower() == "install":
                if os.path.isdir(fr"C:\Program64\Python\Packages"):
                    print()
                    print('*'*100, '\n')
                    # download = input(
                    #     " lpip repo is already installed. Do you want to update it? (yes/no): ").lower()
                    # if download.startswith("y"):
                    #     print()
                    print(" lpip repo is already installed.\n")
                    download_packages("update")
                    # else:
                    #     print('*'*100)
                    #     print()
                else:
                    download_packages("install")
            elif sys.argv[1].lower() == "about":
                lpip_about()
                print('*'*100, '\n')
                exitapp()
            elif sys.argv[1].lower() == "help" or sys.argv[1].lower() == "/?":
                lpip_about()
                info(" Enjoy", "coding!")

            elif (
                sys.argv[1].lower() == "remove"
                or sys.argv[1].lower() == "delete"
                or sys.argv[1].lower() == "uninstall"
            ):
                lpip_remove()

            elif sys.argv[1].lower() == "upgrade":
                print('*'*100, '\n')
                lpip_upgrade()
                print('\n', '*'*100)

            elif (
                sys.argv[1].lower() == "--version"
                or sys.argv[1].lower() == "--v"
                or sys.argv[1].lower() == "version"
                or sys.argv[1].lower() == "-v"
            ):
                print('*'*100, '\n')
                print(f" lpip v{lpip_version}\n")
                print('*'*100)
                exitapp()

            else:
                info(" Status: command is too short", "...")

        # install packages
        elif len(sys.argv) == 3:
            action = check_action(sys.argv[1])
            if action == "install" or action == "upgrade":
                path = check_packages()
                if (
                    sys.argv[2] == "all".lower()
                    or sys.argv[2] == "tout".lower()
                    or sys.argv[2] == "tous".lower()
                ):
                    requirements = fr"{path}\requirements.txt"
                    with open(requirements) as file:
                        for req in file:
                            install(req, action, path)
                elif (
                    sys.argv[2] == "req".lower()
                    or sys.argv[2] == "requirement".lower()
                    or sys.argv[2] == "requirements".lower()
                    or sys.argv[2] == "exigence".lower()
                ):
                    requirements = select_file()
                    try:
                        with open(requirements) as file:
                            for req in file:
                                # req = req.replace(" ", "")
                                req = req.split(" ")
                                for i in req:
                                    if i != "":
                                        install(i, action, path)
                    except:
                        info(" Error: ", "check the requirement file!")
                else:
                    req = sys.argv[2]
                    install(req, action, path)
            elif action == "uninstall":
                req = sys.argv[2]
                if (
                    sys.argv[2] == "all"
                    or sys.argv[2] == "tous"
                    or sys.argv[2] == "tout"
                ):
                    print()
                    print("*" * 100)
                    print(" Please enter the package name you want to uninstall.")
                    print("*" * 100)
                    print()
                else:
                    install(req, action, None)
            else:
                req = sys.argv[2]
                install(req, action, None)

        elif len(sys.argv) > 3:
            action = check_action(sys.argv[1])
            if action != "uninstall" or action != "download" or action != "wheel":
                path = check_packages()
            requirements = sys.argv[2:]
            for req in requirements:
                install(req, action, path)

    except Exception as e:
        info(e, e.args)


if __name__ == "__main__":
    sys.exit(main())