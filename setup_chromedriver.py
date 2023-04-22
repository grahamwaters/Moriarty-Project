import platform
import requests
import zipfile
import os

def download_chromedriver():
    print("Downloading ChromeDriver...")
    base_url = "https://chromedriver.storage.googleapis.com/"
    latest_version_url = base_url + "LATEST_RELEASE"
    response = requests.get(latest_version_url)
    latest_version = response.text.strip()

    system = platform.system()
    bitness = platform.architecture()[0]

    if system == "Windows":
        if bitness == "64bit":
            file_name = "chromedriver_win32.zip"
        else:
            raise Exception("ChromeDriver does not support 32-bit Windows")
    elif system == "Linux":
        if bitness == "64bit":
            file_name = "chromedriver_linux64.zip"
        else:
            file_name = "chromedriver_linux32.zip"
    elif system == "Darwin":
        file_name = "chromedriver_mac64.zip"
    else:
        raise Exception("Unsupported operating system: {}".format(system))

    download_url = base_url + latest_version + "/" + file_name
    response = requests.get(download_url)

    with open(file_name, "wb") as file:
        file.write(response.content)

    with zipfile.ZipFile(file_name, "r") as zip_ref:
        zip_ref.extractall()

    os.remove(file_name)
    print("Downloaded and extracted ChromeDriver for {} {}.".format(system, bitness))

if __name__ == "__main__":
    download_chromedriver()
