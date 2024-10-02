import os
import fitz
import hashlib

class Documents:
    def __init__(self, directory="",
     hash_file=""):
        self.directory = directory
        self.hash_file = hash_file

    def _compute_directory_hash(self):
        """Compute a hash based on file names, sizes, and modification times in the directory."""
        hash_md5 = hashlib.md5()
        files_list = sorted([x for x in os.listdir(self.directory) if x.endswith('.pdf')])

        for pdf_file in files_list:
            pdf_path = os.path.join(self.directory, pdf_file)
            file_stat = os.stat(pdf_path)
            # Update hash with file name, size, and modification time
            hash_md5.update(pdf_file.encode('utf-8'))
            hash_md5.update(str(file_stat.st_size).encode('utf-8'))
            hash_md5.update(str(file_stat.st_mtime).encode('utf-8'))
            
        return hash_md5.hexdigest()

    def _load_previous_hash(self):
        """Load the previously saved hash from file, if it exists."""
        if os.path.exists(self.hash_file):
            with open(self.hash_file, "r") as f:
                return f.read().strip()
        return None

    def _save_current_hash(self, current_hash):
        """Save the current hash to the hash file."""
        with open(self.hash_file, "w") as f:
            f.write(current_hash)

    def detect_change(self):
        """Determine if there has been a change in the directory."""
        current_hash = self._compute_directory_hash()
        previous_hash = self._load_previous_hash()

        if current_hash != previous_hash:
            self._save_current_hash(current_hash)
            return True
        return False

    def load_magic(self):
        print("############## DOCUMENTS ####################")
        """Loads multiple PDFs from the specified directory and extracts text and metadata from each page, if changes are detected."""
        

        pdfs_data = []
        files_list = [x for x in os.listdir(self.directory) if x.endswith('.pdf')]

        for pdf_file in files_list:
            pdf_path = os.path.join(self.directory, pdf_file)
            doc = fitz.open(pdf_path)
            pdf_title = os.path.basename(pdf_path)

            for page_number, page in enumerate(doc):
                text = page.get_text()

                pdfs_data.append({
                    "pdf_title": pdf_title,
                    "page_number": page_number,
                    "page_token_count": len(text.split()),
                    "text": text
                })
        
        return pdfs_data

