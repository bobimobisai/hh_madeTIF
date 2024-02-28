import os
import requests
from PIL import Image
from io import BytesIO
from zipfile import ZipFile


def download_images():
    base = "https://disk.yandex.ru/d/V47MEP5hZ3U1kg"
    url = f"https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={base}"
    response = requests.get(url)
    download_url = response.json()["href"]
    return download_url


def extract_zip(zip_file, output_folder):
    with ZipFile(zip_file, "r") as zip_ref:
        zip_ref.extractall(output_folder)


def cleanup(zip_file):
    os.remove(zip_file)


def download_zip(url):
    response = requests.get(url)
    with open("images.zip", "wb") as f:
        f.write(response.content)


def download_and_extract_images(url, output_folder):
    download_zip(url)
    extract_zip("images.zip", output_folder)
    cleanup("images.zip")


def print_folder_names(input_folder, output_file):
    if not os.path.exists(input_folder):
        return
    folders = [
        folder
        for folder in os.listdir(input_folder)
        if os.path.isdir(os.path.join(input_folder, folder))
    ]
    count = 0
    for folder in folders:
        folder_path = os.path.join(input_folder, folder)

        image_paths = [
            os.path.join(folder_path, img)
            for img in os.listdir(folder_path)
            if img.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp"))
        ]

        images = []

        for img_path in image_paths:
            image = Image.open(img_path)
            images.append(image)

        merged_image = Image.new(
            "RGB", (images[0].width, images[0].height * len(images))
        )

        for i, img in enumerate(images):
            merged_image.paste(img, (0, i * img.height))

        count += 1
        parts = output_file.split(".")
        partthh = f"{parts[0]}{count}.tif"
        merged_image.save(partthh, format="TIFF")


def go_tif():
    output_folder = "extracted_images"
    zip_url = download_images()
    download_and_extract_images(zip_url, output_folder)
    print("Изображения извлечены в папку:", output_folder)

    input_folder = "extracted_images\\Для тестового"
    output_file = "tets_.tif"
    print_folder_names(input_folder, output_file)
    print("Okey, pleasee check")


if __name__ == "__main__":
    go_tif()
