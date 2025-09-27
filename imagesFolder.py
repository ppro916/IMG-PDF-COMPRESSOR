from PIL import Image
import os

def compress_images(input_folder, max_size_kb):
    output_folder = os.path.join(input_folder, "compressed")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    successful_count = 0
    total_count = 0

    for filename in os.listdir(input_folder):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            total_count += 1
            img_path = os.path.join(input_folder, filename)
            
            try:
                img = Image.open(img_path)
                
                # PNG with transparency ला RGB मध्ये convert करा
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                
                output_path = os.path.join(output_folder, filename)
                quality = 95  # जास्तीत जास्त quality पासून सुरुवात
                
                # पहिली सेव्ह
                img.save(output_path, optimize=True, quality=quality)
                
                # File size KB मध्ये तपासा (bytes to KB)
                current_size_kb = os.path.getsize(output_path) / 1024
                
                if current_size_kb <= max_size_kb:
                    print(f"✓ {filename} - {current_size_kb:.1f} KB (quality: {quality})")
                    successful_count += 1
                    img.close()
                    continue
                
                # quality कमी करून पुन्हा प्रयत्न
                quality_step = 5
                min_quality = 20  # किमान quality मर्यादा
                
                while current_size_kb > max_size_kb and quality > min_quality:
                    quality -= quality_step
                    if quality < min_quality:
                        quality = min_quality
                    
                    img.save(output_path, optimize=True, quality=quality)
                    current_size_kb = os.path.getsize(output_path) / 1024
                    
                    if current_size_kb <= max_size_kb:
                        break
                
                final_size_kb = os.path.getsize(output_path) / 1024
                
                if final_size_kb <= max_size_kb:
                    print(f"✓ {filename} - {final_size_kb:.1f} KB (quality: {quality})")
                    successful_count += 1
                else:
                    print(f"✗ {filename} - {final_size_kb:.1f} KB (मर्यादेपेक्षा मोठे)")
                
                img.close()  # Resource release
                
            except Exception as e:
                print(f"✗ {filename} - त्रुटी: {str(e)}")

    print(f"\nकाम पूर्ण झाले!")
    print(f"एकूण images: {total_count}")
    print(f"यशस्वीरित्या कॉम्प्रेस केलेले: {successful_count}")
    print(f"Output folder: {output_folder}")

def get_valid_input(prompt, input_type=float, default_value=None):
    """वैध इनपुट मिळवण्यासाठी सहाय्यक फंक्शन"""
    while True:
        try:
            user_input = input(prompt)
            if user_input.strip() == "" and default_value is not None:
                return default_value
            return input_type(user_input)
        except ValueError:
            print("कृपया वैध संख्या टाइप करा!")

if __name__ == "__main__":
    print("=== Image Compression Tool ===")
    print("हा प्रोग्राम तुमच्या images ला specified size मध्ये compress करेल.")
    
    # फोल्डर पाथ विचारा
    folder_path = input("कृपया तुमच्या images folder चा full path टाइप करा: ").strip()
    
    # फोल्डर अस्तित्वात आहे का ते तपासा
    while not os.path.exists(folder_path):
        print("हा फोल्डर सापडला नाही! कृपया पुन्हा प्रयत्न करा.")
        folder_path = input("कृपया तुमच्या images folder चा full path टाइप करा: ").strip()
    
    # कमाल size विचारा
    print("\nकिती KB च्या आत images हव्या आहेत?")
    print("सुचना: 100-500 KB ची मर्यादा सामान्यतः चांगली राहते.")
    max_size_kb = get_valid_input("कमाल file size (KB मध्ये) [डिफॉल्ट: 300]: ", float, 300.0)
    
    # मर्यादा तपासा
    if max_size_kb < 10:
        print("मर्यादा खूप कमी आहे! किमान 10 KB सेट करत आहे.")
        max_size_kb = 10
    elif max_size_kb > 5000:
        print("मर्यादा खूप जास्त आहे! कमाल 5000 KB सेट करत आहे.")
        max_size_kb = 5000
    
    print(f"\nकॉम्प्रेशन सुरू होत आहे... ({max_size_kb} KB च्या आत)")
    print("-" * 50)
    
    compress_images(folder_path, max_size_kb)
    
    input("\nPress Enter to exit...")
