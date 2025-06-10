import os

from .data_ingestion import DataIngestion

class App:
    def __init__(self, auto=True, img_proc=False, input_file_path=None, input_file_basename=None, 
                 input_file_extension=None, target_words_list=[], output_file_dict={}) -> None:
        self.img_proc = img_proc
        self.input_path = input_file_path
        self.input_basename = input_file_basename
        self.input_extension = input_file_extension
        self.input_words_list = target_words_list
        self.output_dict = output_file_dict

    @staticmethod
    def main(auto=True, img_proc=False, input_file_path=None, input_file_basename=None, 
             input_file_extension=None, target_words_list=[], output_file_dict={}):
        project = App.generate_ins(
            input_file_path,
            input_file_basename,
            input_file_extension,
            target_words_list,
            output_file_dict
        )

        if project:
            DataIngestion.main(
                auto,
                img_proc,
                input_file_path,
                input_file_basename,
                input_file_extension,
                output_file_dict
            )

    @staticmethod
    def generate_ins(input_file_path=None, input_file_basename=None, input_file_extension=None, 
                     target_words_list=[], output_file_dict={}):
        ins = App(
            input_file_path,
            input_file_basename,
            input_file_extension,
            target_words_list,
            output_file_dict
        )
        
        return ins


if __name__ == "__main__":
    App.main()    
