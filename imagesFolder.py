from PIL import Image
import os

def compress_images(input_folder, max_size_kb=300):
    # Output folder automatically
    output_folder = os.path.join(input_folder, "compressed")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            img_path = os.path.join(input_folder, filename)
            img = Image.open(img_path)
            output_path = os.path.join(output_folder, filename)

            quality = 85
            img.save(output_path, optimize=True, quality=quality)

            while os.path.getsize(output_path) > max_size_kb * 1024 and quality > 10:
                quality -= 5
                img.save(output_path, optimize=True, quality=quality)

    print(f"सर्व images compress झाल्या. Output folder: {output_folder}")

if __name__ == "__main__":
    # Input box simulation in console
    folder_path = input("कृपया तुमच्या images folder चा full path द्या: ")
    compress_images(folder_path)
    input("Press Enter to exit...")
