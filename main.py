import fitz  # PyMuPDF
from PIL import Image
import os
import threading


class Constants:
    INPUT_FOLDER = "./input/"
    OUTPUT_FOLDER = "./output/"


class PDFPageExtractor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.pdf_name = (pdf_path.split("/")[-1]).split(".")[0]

        # Create output folder if it doesn't exist
        if not os.path.exists(Constants.OUTPUT_FOLDER + self.pdf_name):
            os.makedirs(Constants.OUTPUT_FOLDER + self.pdf_name)
            self.already_exist = False
        else:
            self.already_exist = True
        self.extract_pages_to_images()

    def extract_pages_to_images(self):
        if self.already_exist:
            return
        pdf_document = fitz.open(self.pdf_path)

        for page_number in range(pdf_document.page_count):
            page = pdf_document[page_number]
            image = page.get_pixmap(dpi=250)

            # Convert the PyMuPDF image to PIL Image
            pil_image = Image.frombytes(
                "RGB", [image.width, image.height], image.samples
            )

            # Save the image to the output folder
            image_filename = (
                f"{Constants.OUTPUT_FOLDER}{self.pdf_name}/page_{page_number + 1}.png"
            )
            pil_image.save(image_filename)

            print(f"Page {page_number + 1} extracted and saved as {image_filename}")

        pdf_document.close()


inout_files = os.listdir(Constants.INPUT_FOLDER)

tasks = []
for file in inout_files:
    tasks.append(
        threading.Thread(target=PDFPageExtractor, args=(Constants.INPUT_FOLDER + file,))
    )

for task in tasks:
    task.start()

for task in tasks:
    task.join()
