import data
import build_data
import county_demographics
import copy

''' Testing:

Files that have matched sample outputs so far:
pop
pop_field
percent_fields
filter_state
ca
high_school_lt_60
bachelors_gt_60

'''

global Demographics
global Unknown_Error

Unknown_Error = False
Demographics = build_data.get_data()
File_Name = f"inputs/{input("Enter the file name: ")}.ops"

class Operations:

    def display(demographics: list[data.CountyDemographics]) -> None: #prints all data for all current counties
        print()
        for county in demographics:
            print(county.state.upper(), " ", county.county.upper())
            print("\t", county.age)
            print("\t", county.education)
            print("\t", county.ethnicities)
            print("\t", county.income)
            print("\t", county.population)
            print("\t", county.age)
        print()

    def filter_state(demographics: list[data.CountyDemographics], state_abbreviation: str, print_bool = True) -> list[data.CountyDemographics]: #filters demographics by state
        reduced_demographics = [demographic for demographic in demographics if demographic.state == state_abbreviation]
        if print_bool:
            print(f"Filter: state == {state_abbreviation} ({len(reduced_demographics)} entries)")
        return(reduced_demographics)

    def filter_gt(demographics: list[data.CountyDemographics], threshold: float, field: str, print_bool = True) -> list[data.CountyDemographics]: #filters demographics by exceeding a threshold value of some field
        if "." in field:
            split_field = field.split(".")
            reduced_demographics = [demographic for demographic in demographics if vars(demographic)[split_field[0].lower()][split_field[1]] > float(threshold)]
        else:
            reduced_demographics = [demographic for demographic in demographics if vars(demographic)[field] > threshold]
        if print_bool:
            print(f"Filter: {field} gt {threshold} ({len(reduced_demographics)} entries)")
        return reduced_demographics

    def filter_lt(demographics: list[data.CountyDemographics], threshold: float, field: str, print_bool = True) -> list[data.CountyDemographics]: #filters demographics by being below a threshold value of some field
        if "." in field:
            split_field = field.split(".")
            reduced_demographics = [demographic for demographic in demographics if vars(demographic)[split_field[0].lower()][split_field[1]] < float(threshold)]
        else:
            reduced_demographics = [demographic for demographic in demographics if vars(demographic)[field] < threshold]
        if print_bool:
            print(f"Filter: {field} lt {threshold} ({len(reduced_demographics)} entries)")
        return reduced_demographics

    def population_total(demographics: list[data.CountyDemographics], print_bool = True) -> list[data.CountyDemographics]: #returns the total population among given counties
        total_population = sum([county.population['2014 Population'] for county in demographics])
        if print_bool:
            print(f"2014 population: {total_population}")
        return total_population

    def population(demographics: list[data.CountyDemographics], field: str, print_bool = True) -> list[data.CountyDemographics]: #returns the total supopulation of some field among given counties
        if "." in field:
            split_field = field.split(".")
            if "Persons Below Poverty Level" in split_field or "Education" in split_field or "Ethnicity" in split_field or "Ethnicities" in split_field or "Age" in split_field: #adjust for percentage value
                total_subpopulation = sum([(vars(county)[split_field[0].lower()][split_field[1]] / 100) * county.population['2014 Population'] for county in demographics])
            else:
                total_subpopulation = sum([vars(county)[split_field[0].lower()][split_field[1]] for county in demographics])
        else:   
            if "Ethnicity" in field or "Age" in field or "Education" or "Ethnicities" in field: #adjust for percentage value
                total_subpopulation = sum([(vars(county)[field] / 100) * county.population['2014 Population'] for county in demographics])
            else:
                total_subpopulation = sum([vars(county)[field] for county in demographics])
        if print_bool:
            print(f"2014 {field} population: {total_subpopulation}")
        return total_subpopulation

    def percent(demographics: list[data.CountyDemographics], field: str, print_bool = True) -> float: #returns the percentage of specified sub-population within the total population among the given counties
        total_pop = Operations.population_total(demographics, False)
        if total_pop == 0:
            percentage = 0
        else:
            percentage = (Operations.population(demographics, field, False) / total_pop) * 100
        if print_bool:
            print(f"2014 {field} percentage: {percentage}")
        return percentage

def process_operations_file(file_name: str) -> None:
    global Demographics
    global Unknown_Error

    Demographics_Copy = copy.deepcopy(Demographics)
    try:
        file = open(file_name, "r")
    except:
        print("Error opening file")
        exit()
    
    lines = file.readlines()
    print(len(Demographics_Copy), "records loaded")

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
        except ValueError:
            print("Invalid input(s) detected -- Line", current_line_num)
        except KeyError:
            print("Invalid input(s) detected -- Line", current_line_num)
        except:
            print("UNKNOWN ERROR -- Line", current_line_num)
            Unknown_Error = current_line_num

if __name__ == "__main__":
    process_operations_file(File_Name)
    '''if type(Unknown_Error) != bool:
        print("#" * 200)
        print("Unknown Error: ".upper(), Unknown_Error)
        print("#" * 200)'''
    #print(vars(Demographics[0]))
    #print(vars(Demographics[1]))