import requests
import os
from bs4 import BeautifulSoup
import time


def download_pdf(url, destination_folder):
    response = requests.get(url)
    if response.status_code == 200:
        file_name = url.split("/")[-1]
        file_path = os.path.join(destination_folder, file_name)
        with open(file_path, "wb") as file:
            file.write(response.content)
        print(f"Downloaded {file_name} successfully.")
    else:
        print(f"Failed to download {url}. Status code: {response.status_code}")


def filter_pdf_links(url):
    response = requests.get(url)
    pdf_links = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        links = soup.find_all("a")
        for link in links:
            href = link.get("href")
            if href and href.endswith(".pdf"):
                pdf_links.append(href)
    else:
        print(f"Failed to fetch {url}. Status code: {response.status_code}")

    return pdf_links


def download_all_pdfs(url, destination_folder):
    pdf_links = filter_pdf_links(url)
    for pdf_link in pdf_links:
        full_url = (
            "https://website.com" + pdf_link if pdf_link.startswith("/") else pdf_link
        )
        download_pdf(full_url, destination_folder)
        time.sleep(2)


def save_links(url, destination_file):
    links = filter_pdf_links(url)
    with open(destination_file, "w") as file:
        for link in links:
            file.write("https://website.com" + link + "\n")
    print(f"Saved {len(links)} links to {destination_file}.")


# Example usage
url = "https://website.com/files"
destination_folder = r"C:/desktop/destination_folder"  # destination folder path
destination_file = r"C:/desktop/destination_file"  # destination file path
download_all_pdfs(url, destination_folder)
save_links(url, destination_file)
