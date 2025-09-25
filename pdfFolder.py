import os
import subprocess

def compress_pdf_target(input_path, output_path, target_kb=300):
    quality_levels = ["/prepress", "/printer", "/ebook", "/screen"]
    temp_output = output_path
    for q in reversed(quality_levels):  # start from lowest quality
        subprocess.run([
            "gs",
            "-sDEVICE=pdfwrite",
            "-dCompatibilityLevel=1.4",
            f"-dPDFSETTINGS={q}",
            "-dNOPAUSE",
            "-dBATCH",
            f"-sOutputFile={temp_output}",
            input_path
        ], check=True)

        size_kb = os.path.getsize(temp_output) / 1024
        if size_kb <= target_kb:
            print(f"{os.path.basename(input_path)} compressed to {int(size_kb)} KB using {q}")
            return
    print(f"{os.path.basename(input_path)} could not reach {target_kb} KB, final size {int(size_kb)} KB")

if __name__ == "__main__":
    folder_path = input("कृपया तुमच्या PDF folder चा full path द्या: ")
    output_folder = os.path.join(folder_path, "compressed")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdf"):
            input_file = os.path.join(folder_path, filename)
            output_file = os.path.join(output_folder, filename)
            compress_pdf_target(input_file, output_file, target_kb=300)

    input("सर्व PDF compress झाल्या. Press Enter to exit...")
