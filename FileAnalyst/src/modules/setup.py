import os
from datetime import datetime

import sys
sys.path.append("../")

from .pdf.run import App as RunPdfModule

class Setup:
    allowed_file_types = ["pdf", "txt"]

    def __init__(self) -> None:
        pass

    @staticmethod
    def main(auto, project_ins):
        #print(project_ins.__dict__)

        file_dict = {
                "file_metadata": {
                    "title": "",
                    "path": project_ins.input_path,
                    "basename": project_ins.input_basename,
                    "extension": project_ins.input_extension,
                    "size_bytes": 0,
                    "created_at": Setup.return_valid_date(),
                    "modified_at": {
                        Setup.__name__: Setup.return_valid_date(),
                    },
                    "page_count": 0,
                },
                "pages": {},
                "summary": {
                    "full_text": "Concatenated text of all pages...",
                    "detected_language": "en",
                    "key_phrases": ["project scope", "budget", "timeline"],
                },
                "status": {
                    "success": True,
                    "errors": [],
                    "processed_at": "",
                }
            }

        if project_ins.input_extension == "pdf":
            RunPdfModule.main(
                auto=auto, 
                img_proc=project_ins.img_proc,
                input_file_path=project_ins.input_path,
                input_file_basename=project_ins.input_basename,
                input_file_extension=project_ins.input_extension,
                target_words_list=project_ins.input_words_list,
                output_file_dict=file_dict
            )

    @staticmethod
    def generate_ins():
        pass

    @staticmethod
    def return_valid_date() -> str:
        now = datetime.now()
        date_str = now.strftime("%d-%b-%y_%H-%M-%S")

        return date_str


if __name__ == "__main__":
    Setup.main()    
