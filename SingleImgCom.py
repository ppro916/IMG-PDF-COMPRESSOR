from PIL import Image
import os

def compress_image(input_path, target_kb=50):
    folder, filename = os.path.split(input_path)
    output_folder = os.path.join(folder, "compressed")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    output_path = os.path.join(output_folder, filename)

    img = Image.open(input_path)
    quality = 85
    width, height = img.size

    img.save(output_path, optimize=True, quality=quality)

    # Loop until file size under target
    while os.path.getsize(output_path) > target_kb * 1024:
        # कमी quality करून बघ
        if quality > 20:
            quality -= 5
        else:
            # जर quality आधीच खूप कमी असेल तर resolution कमी कर
            width = int(width * 0.9)
            height = int(height * 0.9)
            img = img.resize((width, height), Image.Resampling.LANCZOS)
        
        img.save(output_path, optimize=True, quality=quality)

    size_kb = os.path.getsize(output_path) // 1024
    print(f"{filename} → {size_kb} KB (saved in {output_folder})")

if __name__ == "__main__":
    image_path = input("कृपया image चा full path द्या: ")
    target = int(input("Target size (KB मध्ये) द्या (उदा. 50): "))
    compress_image(image_path, target_kb=target)
    input("Press Enter to exit...")
