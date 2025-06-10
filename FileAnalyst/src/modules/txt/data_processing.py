import os
import sys
import time
import csv
from ollama import Client

sys.path.append('../')
#from CriticalFlowPath.keys.secrets import OPENAI_KEY, CLUADE_KEY

class DataProcessing():
    def __init__(self, input_files_path, output_files_path):
        #self.openai_client = OpenAI(api_key= OPENAI_KEY)
        #self.cluade_client = anthropic.Anthropic(api_key=CLUADE_KEY)
        self.input_path = input_files_path
        self.output_path = output_files_path

    @staticmethod
    def main():
        project = DataProcessing.generate_ins()
        project.interpret_text(project.output_path, project.output_path, "processed_test")

    @staticmethod
    def generate_ins():
        input_files_path = input("Enter the image(s) directory to process: ")
        output_files_path = input("Enter the file directory to save the processed images: ")

        return DataProcessing(input_files_path, output_files_path)

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
        
        file_dir = [file for file in DataProcessing.get_type_files(input_dir, "txt") if "clean" in file][0]
        
        with open(file_dir, 'r') as file_reader:
            normalized_text = file_reader.read()

        chunk_size = 1500
        text_chunks = [normalized_text[i:i + chunk_size] for i in range(0, len(normalized_text), chunk_size)]
        processed_texts = []

        for chunk in text_chunks:
            print(chunk + "\n")   
            """ prompt = self.create_prompt(chunk)
            #processed_text = self.call_openai_api(prompt)
            #processed_text = self.call_claude_api(prompt)
            processed_text = self.call_ollama(prompt)

            if processed_text:
                processed_texts.append(processed_text)
            
            time.sleep(20) """
        
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
    
    def prompt_message(self, input_text):
        return f"""
        You are a text processing assistant. Clean and structure the following input, ensuring it’s coherent, error-free, and organized.

        - Correct spelling and formatting errors.
        - Remove irrelevant details and extraneous characters.
        - Organize into a table with these columns:
            Phase | Location | Trade | Activity Name | Color | Activity Code | Start | Finish
        
        Here is the text to clean:
        {input_text}

        Output the cleaned text in the specified format.
        """
    
    def prompt_message_2(self, input_text):
        return f"""
        You are a text processing assistant. Clean and structure the following input, ensuring it’s coherent, error-free, and organized.

        - Correct spelling and formatting errors.
        - Remove irrelevant details and extraneous characters.
        - Organize into a table with these columns:
            Phase, Location, Trade, Activity Name, Color, Activity Code, Start, Finish
        
        Output the cleaned text in CSV format, separated by commas, with the respective headers.

        Here is the text to clean:
        {input_text}
        """

    def call_ollama(self, prompt):
        try:
            client = Client(
                host='http://localhost:11434',
                headers={'x-some-header': 'some-value'}
            )
            response = client.chat(model='llama2', messages=[
                {
                    'role': 'user',
                    'content': prompt,
                },
            ])
        except Exception as e:
            print(f"Error during Ollama API call: {e}")
            return None

        return response['message']['content']

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

def test():
    client = Client(
        host='http://localhost:11434',
        headers={'x-some-header': 'some-value'}
    )
    response = client.chat(model='llama2', messages=[
        {
            'role': 'user',
            'content': 'Why is the sky blue?',
        },
    ])

    return response['message']['content']

if __name__ == "__main__":
    DataProcessing.main()
    #print(DataProcessing.get_type_files("/home/coffee_6ean/Linux/CriticalFlowPath/src/local_results/output_images", "txt"))
    #print(test())

    """
    You are a text processing assistant. Clean and structure the following input, ensuring it’s coherent, error-free, and organized.

        - Correct spelling and formatting errors.
        - Remove irrelevant details and extraneous characters.
        - Organize into a table with these columns:
            Phase | Location | Trade | Activity Name | Color | Activity Code | Start | Finish
        
        Here is the text to clean:
        G-CON-1490 *vllestone: Permanent Power Established from Xcel to Site od 20-Nov-24 “0d
        G-CON-1860 Startup Pumps 2d | 22-Nov-24 | 25-Nov-24 “tid 
        G-CON-1920 Startup HVLV Big Fans 2d | 25Nov-24 | 26-Nov-24 80d 
        G-CON-1970 Startup Elecirical - Generator /ATS /MTS Sd | 22-Nov-24 | 02-Dec-24 26d 
        G-CON-1510 *Nllestone: Ready for Permanent Power in Building od 03-Dec-24 19d

        Output the cleaned text in the specified format.
    """

    """
    <|start_of_role|>system<|end_of_role|>{
        You are a text processing assistant. Clean and structure the following input, ensuring it’s coherent, error-free, and organized.
        - Correct spelling and formatting errors.
        - Remove irrelevant details and extraneous characters.
        - Organize into a table with these columns:
            Activity Code, Activity Name, Start, Finish, Float
        }<|end_of_text|> 
    <|start_of_role|>user<|end_of_role|>{
        Output the cleaned text in CSV format, separated by commas

        Here is the text to clean:
        | Milestone: Consiruction Substantial Completion (680 Calenda [ Od tH-Apr25\" Bid
    }<|end_of_text|> 
    <|start_of_role|>assistant<|end_of_role|>
    """
