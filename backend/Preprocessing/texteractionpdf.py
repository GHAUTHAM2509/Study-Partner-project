import sys, pathlib, pymupdf, os, time # 1. Import the time module
# Import the function to get text from images
from imagedescription import extract_text_from_image, generate_image_description

# This script extracts text and images from a PDF file using PyMuPDF (pymupdf).
# - Extracts all text from each page.
# - Extracts all images from each page, gets their text description using Google Vision API.
# - Combines the page text and image text into a single .txt file.

def extract_text_and_images_from_pdf(fname):
    """
    Extracts text and images from the given PDF file, gets text from the images,
    and combines everything into a single text file.
    """
    # 2. Initialize time trackers
    start_time = time.time()
    last_sleep_time = start_time

    # This list will hold all the content (page text + image text)
    all_content_parts = []
    
    with pymupdf.open(fname) as doc:
        # Create a directory for images, as we still need to save them temporarily
        img_dir = fname + "_images"
        if not os.path.exists(img_dir):
            os.makedirs(img_dir)

        # Process each page one by one
        for i, page in enumerate(doc):
            # 3. Add the sleep logic at the start of the loop
            current_time = time.time()
            if current_time - last_sleep_time >= 60:
                print("Running for over a minute, pausing for 10 seconds to rate-limit...")
                time.sleep(10)
                last_sleep_time = time.time() # Reset the timer after sleeping

            # 1. Extract the main text from the page
            all_content_parts.append(page.get_text())

            # 2. Extract images from the current page
            image_list = page.get_images(full=True)
            if image_list:
                all_content_parts.append("\n--- Images on this page ---\n")

            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                
                # 3. Save the image temporarily
                image_filename = f"image_{i+1}_{img_index+1}.{image_ext}"
                image_filepath = os.path.join(img_dir, image_filename)
                with open(image_filepath, "wb") as img_file:
                    img_file.write(image_bytes)

                # 4. Get the text description from the saved image
                try:
                    image_label = generate_image_description(image_filepath)
                    all_content_parts.append(f"Description for {image_filename}:\n{image_label}\n")
                    image_text = extract_text_from_image(image_filepath)
                    all_content_parts.append(f"Description for {image_filename}:\n{image_text}\n")
                except Exception as e:
                    print(f"Could not process image {image_filename}. Error: {e}")
                    all_content_parts.append(f"Description for {image_filename}: [Error processing image]\n")
            
            # 5. Add the page completion marker
            all_content_parts.append(f"\npage{i+1} complete\n")

    # 6. Join all the collected parts and write to the final .txt file
    final_text = chr(12).join(all_content_parts)
    pathlib.Path(fname + ".txt").write_bytes(final_text.encode("utf-8"))

if __name__ == "__main__":
    # Example usage: process a sample PDF file.
    # Make sure your .env file is configured with the Google API key.
    filename = "tempdoc1.pdf" 
    print(f"Processing {filename}...")
    extract_text_and_images_from_pdf(filename)
    print(f"Finished processing. Output saved to {filename}.txt")


