import os
import re
import json
from pypdf import PdfReader
from datetime import datetime

class PdfToJson():
    def __init__(self):
        self.entry_count = 1
        self.parent_count = 1
    
    @staticmethod
    def main():
        pdf_file_path = input("Please enter the path of the PDF file to read: ")
        initial_anchor = input("Please enter the initial anchor tag: ")
        final_anchor = input("Please enter the final anchor tag: ")
        pdf_to_json_instance = PdfToJson()

        if os.path.exists(pdf_file_path) and pdf_file_path.endswith('.pdf'):
            metadata = pdf_to_json_instance.extract_pdf_metadata(pdf_file_path)

            if pdf_to_json_instance.read_uploaded_pdf(pdf_file_path, metadata, initial_anchor, final_anchor) == 0:
                print("PDF processing completed successfully.")
            else:
                print("An error occurred during PDF processing.")
        else:
            print("The specified file does not exist or is not a PDF.")

    @staticmethod
    def convert_date_format(date_str):
        try:
            if isinstance(date_str, str):
                formatted = re.sub('(^)[\D]+', '', date_str)
                date_obj = datetime.strptime(formatted, '%Y.%m.%d')
                return date_obj.strftime('%Y-%m-%dT%H:%M:%SZ')
            else:
                print(f"Invalid date format: {date_str}")
                return ""
        except ValueError:
            print(f"Invalid date format: {date_str}")
            return ""

    def parent_layers_countdown(self, list, parent_obj_curr, parent_obj_act):
        past_parent = parent_obj_curr
        active_parent = parent_obj_act 

        for parent_id in range(self.parent_count, 0, -1):
            if datetime.strptime(active_parent['start'], '%d-%b-%y') <= datetime.strptime(past_parent['start'], '%d-%b-%y') and datetime.strptime(active_parent['finsh'], '%d-%b-%y') >= datetime.strptime(past_parent['finish'], '%d-%b-%y'):
                past_parent["activities"].append(active_parent)
            else:
                list[0]['activities']
                
    def pdf_reformatting(self, pdf_content, initial_anchor, final_anchor):
        content_up_to_final_anchor = re.search(fr'[\S\s]+?(?= {final_anchor})', pdf_content)
        if content_up_to_final_anchor:
            extracted_content = content_up_to_final_anchor.group()
        else:
            print("Error. Invalid content.")
            return [], []

        header_match = re.search(fr'[\S\s]+?({initial_anchor})', extracted_content)
        if header_match:
            header_content = header_match.group()
        else:
            print("Error. Initial anchor tag not found.")
            return [], []

        body_content = re.sub(fr'[\S\s]+?({initial_anchor})', '', extracted_content).strip()
        formatted_header = re.sub('\n', ' ', header_content).split()  
        formatted_body = body_content.splitlines()

        return formatted_header, formatted_body

    def extract_pdf_metadata(self, pdf_file_path):
        filename = os.path.splitext(os.path.basename(pdf_file_path))[0]
        result = filename.split(" - ")
        date_str = result[-1]
        issue_date = self.convert_date_format(date_str) if date_str else ""

        metadata = {
            "document_id": result[0],
            "document_title": result[1] if len(result) > 1 else "",
            "document_subtitle": " - ".join(result[2:-1]) if len(result) > 2 else "",
            "issue_date": issue_date,
            "created_at": datetime.now().isoformat()
        }

        return metadata

    def read_uploaded_pdf(self, pdf_file_path, metadata, initial_anchor, final_anchor):
        if os.path.exists(pdf_file_path) and pdf_file_path.endswith('.pdf'):
            try:
                reader = PdfReader(pdf_file_path)
                first_page = reader.pages[0]
                content_str = first_page.extract_text()
                header, _ = self.pdf_reformatting(content_str, initial_anchor, final_anchor)
                all_bodies = []

                for page in reader.pages:
                    content_str = page.extract_text()
                    _, body = self.pdf_reformatting(content_str, initial_anchor, final_anchor)
                    all_bodies.extend(body)  

                print(f"Extracted Metadata: {json.dumps(metadata, indent=4)}")                
                self.jsonify_parsed_data(metadata, header, all_bodies)
                return 0  
            except Exception as e:
                print(f"An error occurred while processing the PDF: {e}")
                return -1  
        else:
            print("The specified file does not exist or is not a PDF.")
            return -1  

    def parse_header_data(self, formatted_header):
        stdrd_cpm_body = [
            "entry", "parent_id", "id", "name", 
            "activity_name", "activity_code", "phase", "trade", 
            "location", "color", "scope_of_work", "duration", 
            "start", "finish", "total_float", "activities"
        ]
        
        esse_cpm_body = {
            "id": ["id"],
            "name": ["name"],
            "duration": ["duration", "dur"],
            "start": ["start"],
            "finish": ["finish"]
        }

        trimmed_columns = set(col_val.lower() for col_val in formatted_header)
        missing_columns = []

        for stdrd_val, variations in esse_cpm_body.items():
            if any(variation in trimmed_columns for variation in variations):
                pass
            else:
                missing_columns.append(stdrd_val)

        for missing_col in missing_columns:
            print(f"Warning - Essential Column not found: {missing_col}")

        print(f"Extracted Header: {stdrd_cpm_body}")
        return stdrd_cpm_body

    def parse_activity_data(self, raw_data):
        structured_activities = []
        last_parent = None

        for line in raw_data:
            line = line.strip()
            parent_match = re.match(
                r'^(.*?)(\s+\1)\s+(\d+\.?\d*?\s*d)\s+(\d{1,2}-\w{3}-\d{2,4})?\s*([A-Z]?)?\s*(\d{1,2}-\w{3}-\d{2,4})?\s*(-?\d+\.?\d*?d?)?\s*(\w+)?$', 
                line
            )

            if parent_match:
                activity_id = parent_match.group(1).strip()  
                activity_name = activity_id  
                duration = parent_match.group(3).strip()        
                start_date = parent_match.group(4).strip() if parent_match.group(4) else ''  
                finish_date = parent_match.group(6).strip() if parent_match.group(6) else ''  
                total_float = parent_match.group(7) or ''      

                current_parent = {
                    "entry": self.entry_count,
                    "parent_id": self.parent_count,
                    "id": activity_id,
                    "name": activity_name,
                    "activity_name": "",
                    "activity_code": "",
                    "phase": "",
                    "trade": "",
                    "location": "",
                    "color": "",
                    "scope_of_work": "",
                    "duration": duration,
                    "start": start_date,
                    "finish": finish_date,
                    "total_float": total_float,
                    "activities": []  
                }

                structured_activities.append(current_parent)
                last_parent = current_parent  
                self.parent_count += 1  
            else:
                child_match = re.match(
                    r'^([A-Z0-9-]+)\s+(.*?)\s+(\d+\.?\d*?\s*d)\s+(\d{1,2}-\w{3}-\d{2,4})?\s*([A-Z\*]?)?\s*(\d{1,2}-\w{3}-\d{2,4})?\s*(-?\d+\.?\d*?d?)?\s*(\w+)?$', 
                    line
                )
                
                if child_match and last_parent:
                    child_id = child_match.group(1).strip()
                    child_name = child_match.group(2).strip()  
                    child_duration = child_match.group(3).strip()
                    child_start = child_match.group(4).strip() if child_match.group(4) else ''  
                    child_finish = child_match.group(6).strip() if child_match.group(6) else ''  
                    child_total_float = child_match.group(7) or ""
                    
                    child_activity = {
                        "entry": self.entry_count,
                        "parent_id": last_parent["id"],
                        "id": child_id,
                        "name": child_name,
                        "activity_name": "",
                        "activity_code": "",
                        "phase": "",
                        "trade": "",
                        "location": "",
                        "color": "",
                        "scope_of_work": "",
                        "duration": child_duration,
                        "start": child_start,
                        "finish": child_finish,
                        "total_float": child_total_float,
                    }

                    current_parent["activities"].append(child_activity)
                else:
                    structured_activities.append({"raw": line})

            self.entry_count += 1  
        return structured_activities

    def jsonify_parsed_data(self, metadata, header_data, activity_data):
        parsed_header = self.parse_header_data(header_data)
        parsed_activities = self.parse_activity_data(activity_data)
        json_data = {
            "project_metadata": metadata,
            "project_content": {
                "header": parsed_header,
                "body": parsed_activities
            }
        }
        json_output = json.dumps(json_data, indent=2)
        
        output_directory = input("Please enter folder path to store the JSON result: ")
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        output_file = os.path.join(output_directory, 'cpm.json')
        with open(output_file, 'w') as file:
            file.write(json_output)

        print(f"JSON output written to: {output_file}")


if __name__ == "__main__":
    PdfToJson.main()
        