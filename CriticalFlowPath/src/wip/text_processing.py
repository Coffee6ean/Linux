import os
import sys
import time
import csv
from openai import OpenAI
import anthropic


sys.path.append('../')
from CriticalFlowPath.keys.secrets import OPENAI_KEY, CLUADE_KEY

class TextProcessing():
    def __init__(self, input_files_path, output_files_path):
        self.openai_client = OpenAI(api_key= OPENAI_KEY)
        self.cluade_client = anthropic.Anthropic(api_key=CLUADE_KEY)
        self.input_path = input_files_path
        self.output_path = output_files_path

    @staticmethod
    def main():
        project = TextProcessing.generate_ins()
        project.interpret_text(project.input_path, project.output_path, "processed_test")

    @staticmethod
    def generate_ins():
        input_files_path = input("Enter the image(s) directory to process: ")
        output_files_path = input("Enter the file directory to save the processed images: ")

        return TextProcessing(input_files_path, output_files_path)

    @staticmethod
    def get_type_files(input_dir, file_type):
        file_list = []

        if os.path.isfile(input_dir):
            if input_dir.endswith(file_type):
                file_list.append(os.path.abspath(input_dir))
            else:
                print(f"Error: The file '{input_dir}' does not match the specified type '{file_type}'.")

        elif os.path.isdir(input_dir):
            files = os.listdir(input_dir)
            for file in files:
                if file.endswith(file_type):
                    file_path = os.path.join(input_dir, file)
                    file_list.append(os.path.abspath(file_path))

        else:
            print(f"Error: '{input_dir}' is neither a valid file nor a directory.")

        return file_list

    def interpret_text(self, input_dir, output_path, output_basename):
        if not os.path.exists(input_dir):
            print(f"Error: Input file {input_dir} does not exist.")
            return
        
        file_dir = [file for file in TextProcessing.get_type_files(input_dir, 'txt') if "clean" in file][0]
        
        with open(file_dir, 'r') as file_reader:
            normalized_text = file_reader.read()

        chunk_size = 3000
        text_chunks = [normalized_text[i:i + chunk_size] for i in range(0, len(normalized_text), chunk_size)]

        processed_texts = []

        for chunk in text_chunks:
            prompt = self.create_prompt(chunk)
            #processed_text = self.call_openai_api(prompt)
            processed_text = self.call_claude_api(prompt)

            if processed_text:
                processed_texts.append(processed_text)
            
            time.sleep(20)
        
        self.write_to_csv(output_path, output_basename, processed_texts)

    def create_prompt(self, input_text):
        return f"""
        You are a text processing assistant. Your task is to clean and normalize the following text data. 
        The input may contain errors, inconsistencies, or unclear formatting. 
        Please ensure that the output is coherent and organized, focusing on essential details.

        Here is the text to clean:
        {input_text}

        Please provide a cleaned and structured version with clear formatting.
        Ensure to:
        - Correct any spelling or formatting errors.
        - Remove any extraneous characters or irrelevant information.
        - Organize the data into a clear matrix format with appropriate headers.
        
        Output the cleaned text in a structured format.
        """

    def call_openai_api(self, prompt):
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000
            )

            return response['choices'][0]['message']['content']
        
        except Exception as e:
            print(f"Error during OpenAI API call: {e}")
            return None
    
    def call_claude_api(self, prompt):
        try:
            response = self.cluade_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1024,
            )

            return response.content
        
        except Exception as e:
            print(f"Error during OpenAI API call: {e}")
            return None

    def write_to_csv(self, output_path, output_basename, processed_texts, mode='w'):
        os.makedirs(output_path, exist_ok=True)

        output_dir = os.path.join(output_path, f"{output_basename}.csv")

        with open(output_dir, mode, newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Processed Text'])
            for text in processed_texts:
                writer.writerow([text])

        print(f"Cleaned texts successfully written to {output_dir}")


if __name__ == "__main__":
    TextProcessing.main()
