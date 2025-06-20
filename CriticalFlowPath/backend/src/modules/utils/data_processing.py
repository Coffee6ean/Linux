import os
from datetime import datetime, timedelta

class DataProcessing:
    def __init__(self, input_file_path, input_file_basename, input_file_extension, 
                 project_start_date, project_finish_date, input_file_workweek, 
                 output_file_dir, project_data):
        self.input_path = input_file_path
        self.input_basename = input_file_basename
        self.input_extension = input_file_extension
        self.start_date = project_start_date
        self.finish_date = project_finish_date
        self.input_workweek = input_file_workweek
        self.output_path = output_file_dir
        self.project_data = project_data

        #Structure
        self.calendar_weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    
    @staticmethod
    def main(auto=True, input_file_path=None, input_file_basename=None, input_file_extension=None, 
             project_start_date=None, project_finish_date=None, input_file_workweek=None, 
             output_file_dir=None, project_data=None):
        if auto:
            project = DataProcessing.auto_generate_ins(
                input_file_path, 
                input_file_basename, 
                input_file_extension, 
                project_start_date,
                project_finish_date,
                input_file_workweek,
                output_file_dir,
                project_data
            )
        else:
            project = DataProcessing.generate_ins()

        module_data = {
            "details": {
                "workweek": [],
                "calendar": {},
            },
            "logs": {
                "start": DataProcessing.return_valid_date(),
                "finish": None,
                "run-time": None,
                "status": [],
           },
            "content": {}
        }

        if project:
            proc_dict, workweek_days = project.restructure_project_dates()
            module_data["content"] = proc_dict
            module_data["details"]["workweek"] = workweek_days
            module_data["details"]["calendar"] = project.determine_new_calendar(
                project.start_date, project.finish_date, workweek_days
            )
        else:
            module_data["logs"]["status"] = {
                DataProcessing.__name__: "Error. Module's instance was not generated correctly"
            }

        module_data["logs"]["finish"] = DataProcessing.return_valid_date()
        module_data["logs"]["run-time"] = DataProcessing.calculate_time_duration(
            module_data["logs"].get("start"), 
            module_data["logs"].get("finish")
        )

        return module_data

    @staticmethod
    def generate_ins():
        input_file = DataProcessing.return_valid_file(
            input("Please enter the path to the file or directory: ").strip()
        )
        output_file_dir = DataProcessing.return_valid_path(
            "Please enter the directory to save the new module results: "
        )

        ins = DataProcessing(
            input_file.get("path"), 
            input_file.get("basename"), 
            input_file.get("extension"), 
            output_file_dir
        )

        return ins
        
    @staticmethod
    def auto_generate_ins(input_file_path, input_file_basename, input_file_extension, 
                          project_start_date, project_finish_date, input_file_workweek, 
                          output_file_dir, project_data):
        ins = DataProcessing(
            input_file_path, 
            input_file_basename, 
            input_file_extension, 
            project_start_date,
            project_finish_date,
            input_file_workweek,
            output_file_dir,
            project_data
        )
        
        return ins

    @staticmethod
    def return_valid_date() -> str:
        now = datetime.now()
        date_str = now.strftime("%d-%b-%y %H:%M:%S")

        return date_str

    @staticmethod
    def calculate_time_duration(start_date:str, finish_date:str, 
                                date_format:str="%d-%b-%y %H:%M:%S") -> float|int:
        try:
            start_time = datetime.strptime(start_date, date_format)
            finish_time = datetime.strptime(finish_date, date_format)

            minutes_duration = (finish_time - start_time).total_seconds()

            return minutes_duration
        except (ValueError, TypeError) as e:
            print(f"Error calculating runtime: {e}")
            return -1

    def restructure_project_dates(self):
        proc_dict = self.project_data
        workweek_days = self._extract_workweek()

        for entry in proc_dict:
            self._verify_workweek_range(entry, workweek_days)

        return proc_dict, workweek_days

    def _extract_workweek(self):
        workdays = self.input_workweek.split('-')
        if len(workdays) != 2:
            return [] 
        
        init_day, final_day = workdays[0], workdays[-1]

        if init_day not in self.calendar_weekdays or final_day not in self.calendar_weekdays:
            return []

        start_idx = self.calendar_weekdays.index(init_day)
        end_idx = self.calendar_weekdays.index(final_day)

        if start_idx <= end_idx:
            workweek = self.calendar_weekdays[start_idx:end_idx + 1]
        else:
            workweek = self.calendar_weekdays[start_idx:] + self.calendar_weekdays[:end_idx + 1]
        
        return workweek

    def _verify_workweek_range(self, entry_dict:dict, workweek_list:list) -> None:
        start_date = datetime.strptime(entry_dict["start"], "%d-%b-%Y")
        end_date = datetime.strptime(entry_dict["finish"], "%d-%b-%Y")

        date_range = [start_date + timedelta(days=day) for day in range((end_date - start_date).days + 1)]

        dates = {
            "original": [date.strftime("%d-%b-%Y") for date in date_range],
            "processed": [
                date.strftime("%d-%b-%Y") for date in date_range 
                if self.calendar_weekdays[date.weekday()] in workweek_list
            ],
        }

        entry_dict["dates"] = dates

    def determine_new_calendar(self, project_start:str, project_finish:str, workweek_days:list) -> dict:
        try:
            start_date = datetime.strptime(project_start, "%d-%b-%Y")
            finish_date = datetime.strptime(project_finish, "%d-%b-%Y")
        except ValueError:
            raise ValueError(
                "Invalid date format. Please use DD-MMM-YYYY"
            )

        if start_date > finish_date:
            print(
                "Warning: Project start date is after project finish date. Returning an empty dictionary."
            )
            return {}

        calendar_days = (finish_date - start_date).days + 1

        original_days_list = []
        new_days_list = []
        for i in range(calendar_days):
            current_date = start_date + timedelta(days=i)
            original_days_list.append(current_date.strftime("%d-%b-%Y"))

            if self.calendar_weekdays[current_date.weekday()] in workweek_days:
                new_days_list.append(current_date.strftime("%d-%b-%Y"))
            

        proc_dict = {
            "original": {
                "start_date": project_start,
                "finish_date": project_finish,
                "days": {
                    "list": original_days_list,
                    "total": len(original_days_list),
                },
            },
            "processed": {
                "start_date": new_days_list[0] if new_days_list else None,
                "finish_date": new_days_list[-1] if new_days_list else None,
                "days": {
                    "list": new_days_list,
                    "total": len(new_days_list),
                },
            },
        }

        return proc_dict


if __name__ == "__main__":
    module_data = DataProcessing.main(False)
