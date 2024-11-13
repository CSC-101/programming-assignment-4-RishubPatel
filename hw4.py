import data
import build_data
import county_demographics
import copy

global Demographics
Demographics = build_data.get_data()
File_Name = "inputs/" + "pop_field.ops" #INSTRUCTIONS: put the name of the operations file here

class Operations:
        
    #might wanna make reduced_demographics a global thing or not
    #STILL PSUEDOCODE
    #adjust code if you are returned percentages

    def display(demographics: list[data.CountyDemographics]) -> None: #prints all data for all current counties
        [[print(county.attribute) for attribute in county.vars()] for county in demographics()]

    def filter_state(demographics: list[data.CountyDemographics], state_abbreviation: str) -> list[data.CountyDemographics]: #filters demographics by state
        reduced_demographics = [demographic for demographic in demographics if demographic.state == state_abbreviation]
        print(f"Filter: state == {state_abbreviation} ({len(reduced_demographics)} entries)")
        return(reduced_demographics)

    def filter_gt(demographics: list[data.CountyDemographics], threshold: float, field: str) -> list[data.CountyDemographics]: #filters demographics by exceeding a threshold value of some field
        reduced_demographics = [demographic for demographic in demographics if demographic.field < threshold]
        print(f"Filter: {field} gt {threshold} ({len(reduced_demographics)} entries)")
        return reduced_demographics

    def filter_lt(demographics: list[data.CountyDemographics], threshold: float, field: str) -> list[data.CountyDemographics]: #filters demographics by being below a threshold value of some field
        reduced_demographics = [demographic for demographic in demographics if demographic.field > threshold]
        print(f"Filter: {field} lt {threshold} ({len(reduced_demographics)} entries)")
        return reduced_demographics

    def population_total(demographics: list[data.CountyDemographics]) -> list[data.CountyDemographics]: #returns the total population among given counties
        total_population = sum([county.population['2014 Population'] for county in demographics])
        print(f"2014 population: {total_population}")
        return total_population

    def population(demographics: list[data.CountyDemographics], field: str) -> list[data.CountyDemographics]: #returns the total supopulation of some field among given counties
        total_subpopulation = sum([county.field for county in demographics])
        print(f"2014 {field} population: {total_subpopulation}")
        return total_subpopulation

    def percent(demographics: list[data.CountyDemographics], field: str) -> float: #returns the percentage of specified sub-population within the total population among the given counties
        percentage = (Operations.population(demographics, field) / Operations.population_total(demographics)) * 100
        print(f"2014 {field} percentage: xyz")
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
        split_line = line.split(":")
        try: #execute the operation
            if not split_line:
                pass
            elif split_line[0] == "display":
                Operations.display(Demographics_Copy)
            elif split_line[0] == "filter-gt":
                Operations.filter_gt(Demographics_Copy, split_line[2], split_line[1])
            elif split_line[0] == "filter-lt":
                Operations.filter_lt(Demographics_Copy, split_line[2], split_line[1])
            elif split_line[0] == "population-total":
                Operations.population_total(Demographics_Copy)
            elif split_line[0] == "population":
                Operations.population(Demographics_Copy, split_line[1])
            elif split_line[0] == "percent":
                Operations.percent(Demographics_Copy, split_line[1])
            else:
                print("No operation found -- Line", current_line_num)
        except IndexError:
            print("Inputs not found (index error) -- Line", current_line_num)

if __name__ == "__main__":
    process_operations_file(File_Name)