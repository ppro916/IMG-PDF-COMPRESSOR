import os
import sys
import subprocess
from pathlib import Path

def check_ghostscript():
    """Ghostscript इन्स्टॉल्ड आहे का ते तपासा"""
    try:
        subprocess.run(["gswin64c" if os.name == 'nt' else "gs", "--version"], 
                      capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_ghostscript_instructions():
    """Ghostscript इन्स्टॉल करण्यासाठी सूचना"""
    print("\n" + "="*60)
    print("Ghostscript आवश्यक आहे!")
    print("="*60)
    
    if os.name == 'nt':  # Windows
        print("Ghostscript इन्स्टॉल करण्यासाठी:")
        print("1. https://ghostscript.com/releases/gsdnld.html वरून डाउनलोड करा")
        print("2. Windows 64-bit साठी gswin64c.exe इन्स्टॉल करा")
        print("3. System PATH मध्ये Ghostscript जोडा")
        print("4. प्रोग्राम पुन्हा रन करा")
    else:  # Linux/Mac
        print("Linux वर इन्स्टॉल करा: sudo apt-get install ghostscript")
        print("Mac वर इन्स्टॉल करा: brew install ghostscript")
    
    print("\nआवश्यक Ghostscript कमांड:")
    print("Windows: gswin64c")
    print("Linux/Mac: gs")
    print("="*60)

def split_pdf_ghostscript(input_pdf, output_folder, page_prefix=None):
    """Ghostscript वापरून PDF चे पेजेस वेगळे करा"""
    
    if page_prefix is None:
        page_prefix = Path(input_pdf).stem
    
    # Ghostscript कमांड तयार करा
    gs_command = [
        "gswin64c" if os.name == 'nt' else "gs",
        "-dNOPAUSE",
        "-dBATCH",
        "-dSAFER",
        "-sDEVICE=pdfwrite",
        f"-sOutputFile={output_folder}/{page_prefix}_page_%d.pdf",
        input_pdf
    ]
    
    try:
        print(f"PDF स्प्लिट करत आहे: {Path(input_pdf).name}")
        result = subprocess.run(gs_command, capture_output=True, text=True, check=True)
        
        # तयार झालेल्या फाइल्स मोजा
        output_files = list(Path(output_folder).glob(f"{page_prefix}_page_*.pdf"))
        
        print(f"✅ {len(output_files)} पेजेस वेगळे करण्यात यशस्वी")
        return len(output_files)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ त्रुटी: Ghostscript चालवताना अडचण")
        print(f"Error: {e.stderr}")
        return 0

def get_pdf_page_count(pdf_path):
    """PDF मधील एकूण पेजेस मोजा"""
    try:
        # pdfinfo किंवा Ghostscript द्वारे पेज काऊंट मिळवा
        gs_command = [
            "gswin64c" if os.name == 'nt' else "gs",
            "-q",
            "-dNODISPLAY",
            "-c",
            f"({pdf_path}) (r) file runpdfbegin pdfpagecount = quit"
        ]
        
        result = subprocess.run(gs_command, capture_output=True, text=True, check=True)
        return int(result.stdout.strip())
    except:
        # Alternative method
        try:
            gs_command = [
                "gswin64c" if os.name == 'nt' else "gs",
                "-dNODISPLAY",
                "-q",
                f"--permit-file-read={pdf_path}",
                "-c",
                f"({pdf_path}) (r) file runpdfbegin pdfpagecount == quit"
            ]
            result = subprocess.run(gs_command, capture_output=True, text=True, check=True)
            return int(result.stdout.strip())
        except:
            return 0

def process_folder(input_folder):
    """फोल्डरमधील सर्व PDF फाइल्स प्रोसेस करा"""
    
    # आउटपुट फोल्डर तयार करा
    output_folder = Path(input_folder) / "split_pdfs"
    output_folder.mkdir(exist_ok=True)
    
    # सर्व PDF फाइल्स शोधा
    pdf_files = list(Path(input_folder).glob("*.pdf"))
    pdf_files.extend(Path(input_folder).glob("*.PDF"))
    
    if not pdf_files:
        print("❌ या फोल्डरमध्ये कोणतीही PDF फाइल सापडली नाही!")
        return
    
    print(f"\n📁 {len(pdf_files)} PDF फाइल्स सापडल्या:")
    
    total_pages = 0
    successful_files = 0
    
    for pdf_file in pdf_files:
        print(f"\n📄 प्रोसेसिंग: {pdf_file.name}")
        
        # पेज काऊंट तपासा
        page_count = get_pdf_page_count(str(pdf_file))
        
        if page_count == 0:
            print(f"   ❌ पेज काऊंट मिळू शकला नाही किंवा PDF खराब आहे")
            continue
        
        print(f"   📊 एकूण पेजेस: {page_count}")
        
        # PDF स्प्लिट करा
        success_count = split_pdf_ghostscript(str(pdf_file), str(output_folder))
        
        if success_count > 0:
            total_pages += success_count
            successful_files += 1
            print(f"   ✅ यशस्वीरित्या {success_count} पेजेस वेगळे केले")
        else:
            print(f"   ❌ स्प्लिट करण्यात अयशस्वी")
    
    # सारांश
    print(f"\n" + "="*60)
    print("📊 प्रक्रिया पूर्ण झाली!")
    print("="*60)
    print(f"एकूण PDF फाइल्स: {len(pdf_files)}")
    print(f"यशस्वी फाइल्स: {successful_files}")
    print(f"एकूण वेगळे केलेले पेजेस: {total_pages}")
    print(f"आउटपुट फोल्डर: {output_folder}")
    print("="*60)

def main():
    """मुख्य प्रोग्राम"""
    print("=== PDF Page Splitter ===")
    print("हा प्रोग्राम PDF फाइलचे प्रत्येक पेज वेगळ्या PDF फाइलमध्ये स्प्लिट करते")
    print("आवश्यकता: Ghostscript इन्स्टॉल्ड असणे आवश्यक आहे\n")
    
    # Ghostscript तपासा
    if not check_ghostscript():
        install_ghostscript_instructions()
        input("\nPress Enter to exit...")
        return
    
    print("✅ Ghostscript सापडले - प्रोग्राम सुरू करणे शक्य आहे")
    
    # इनपुट फोल्डर विचारा
    while True:
        folder_path = input("\nकृपया PDF फाइल्स असलेल्या फोल्डरचा पाथ टाइप करा: ").strip()
        
        if not folder_path:
            print("❌ कृपया वैध फोल्डर पाथ टाइप करा!")
            continue
            
        folder_path = Path(folder_path)
        
        if not folder_path.exists():
            print("❌ हा फोल्डर अस्तित्वात नाही! कृपया पुन्हा प्रयत्न करा.")
            continue
            
        if not folder_path.is_dir():
            print("❌ हा फोल्डर नाही! कृपया डिरेक्टरीचा पाथ टाइप करा.")
            continue
            
        break
    
    # प्रक्रिया सुरू करा
    try:
        process_folder(folder_path)
    except Exception as e:
        print(f"\n❌ अनपेक्षित त्रुटी: {str(e)}")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
