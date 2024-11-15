import data
import build_data
import county_demographics
import copy

#TO DO: adjust code for percentages, do testing

global Demographics
global File_Name

Demographics = build_data.get_data()
File_Name = "inputs/ca.ops" #INSTRUCTIONS: put the relative path of the operations file here

class Operations:
        
    #ADJUST CODE WHERE PERCENTAGES ARE USED IN DATA: In population function: ethnicity, age, education, "persons below poverty level" within income, 

    def display(demographics: list[data.CountyDemographics]) -> None: #prints all data for all current counties
        for county in demographics:
            for key in vars(county):
                print(key, ":")
                if type(vars(county)[key]) == list:
                    for value in vars(county)[key]:
                        print("\t", value)
                else:
                    print("\t", vars(county)[key])
            print("\n")

    def filter_state(demographics: list[data.CountyDemographics], state_abbreviation: str) -> list[data.CountyDemographics]: #filters demographics by state
        reduced_demographics = [demographic for demographic in demographics if demographic.state == state_abbreviation]
        print(f"Filter: state == {state_abbreviation} ({len(reduced_demographics)} entries)")
        return(reduced_demographics)

    def filter_gt(demographics: list[data.CountyDemographics], threshold: float, field: str) -> list[data.CountyDemographics]: #filters demographics by exceeding a threshold value of some field
        if "." in field:
            split_field = field.split(".")
            reduced_demographics = [demographic for demographic in demographics if vars(demographic)[split_field[0].lower()][split_field[1]] < float(threshold)]
        else:
            reduced_demographics = [demographic for demographic in demographics if vars(demographic)[field] < threshold]
        print(f"Filter: {field} gt {threshold} ({len(reduced_demographics)} entries)")
        return reduced_demographics

    def filter_lt(demographics: list[data.CountyDemographics], threshold: float, field: str) -> list[data.CountyDemographics]: #filters demographics by being below a threshold value of some field
        if "." in field:
            split_field = field.split(".")
            reduced_demographics = [demographic for demographic in demographics if vars(demographic)[split_field[0]][split_field[1]] > threshold]
        else:
            reduced_demographics = [demographic for demographic in demographics if vars(demographic)[field] > threshold]
        print(f"Filter: {field} lt {threshold} ({len(reduced_demographics)} entries)")
        return reduced_demographics

    def population_total(demographics: list[data.CountyDemographics]) -> list[data.CountyDemographics]: #returns the total population among given counties
        total_population = sum([county.population['2014 Population'] for county in demographics])
        print(f"2014 population: {total_population}")
        return total_population

    def population(demographics: list[data.CountyDemographics], field: str) -> list[data.CountyDemographics]: #returns the total supopulation of some field among given counties
        if "." in field:
            split_field = field.split(".")
            if "persons below poverty level" in split_field:
                pass
            else:
                total_subpopulation = sum([vars(county)[split_field[0].lower()][split_field[1]] for county in demographics])
        else:   
            if "ethnicity" in field or "age" in field or "education" in field:
                pass
            else:
                total_subpopulation = sum([vars(county)[field] for county in demographics])
        print(f"2014 {field} population: {total_subpopulation}")
        return total_subpopulation

    def percent(demographics: list[data.CountyDemographics], field: str) -> float: #returns the percentage of specified sub-population within the total population among the given counties
        percentage = (Operations.population(demographics, field) / Operations.population_total(demographics)) * 100
        print(f"2014 {field} percentage: {percentage}")
        return percentage

def process_operations_file(file_name: str) -> None:
    Demographics_Copy = copy.deepcopy(Demographics)
    file = open(file_name, "r")
    try:
        file = open(file_name, "r")
    except:
        print("Error opening file")
        exit()
    
    lines = file.readlines()
    print(len(lines), "records loaded")

    current_line_num = 0
    for line in lines:
        current_line_num += 1
        split_line = "".join(line.split("\n"))
        split_line = split_line.split(":")
        try: #execute the operation
            if not split_line:
                pass
            elif split_line[0] == "display":
                Operations.display(Demographics_Copy)
            elif split_line[0] == "filter-gt":
                Demographics_Copy = Operations.filter_gt(Demographics_Copy, split_line[2], split_line[1])
            elif split_line[0] == "filter-lt":
                Demographics_Copy = Operations.filter_lt(Demographics_Copy, split_line[2], split_line[1])
            elif split_line[0] == "population-total":
                Operations.population_total(Demographics_Copy)
            elif split_line[0] == "population":
                Operations.population(Demographics_Copy, split_line[1])
            elif split_line[0] == "percent":
                Operations.percent(Demographics_Copy, split_line[1])
            elif split_line[0] == "filter-state":
                Demographics_Copy = Operations.filter_state(Demographics_Copy, split_line[1])
            else:
                print("No operation found -- Line", current_line_num)
        except IndexError:
            print("Inputs not found (index error) -- Line", current_line_num)

if __name__ == "__main__":
    process_operations_file(File_Name)
    print(vars(Demographics[0]))
    print(vars(Demographics[1]))