import data
import build_data
import county_demographics
import copy
import sys

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
Demographics = build_data.get_data()

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

    def filter_gt(demographics: list[data.CountyDemographics], threshold: str, field: float, print_bool = True) -> list[data.CountyDemographics]: #filters demographics by exceeding a threshold value of some field
        split_field = field.split(".")
        reduced_demographics = [demographic for demographic in demographics if vars(demographic)[split_field[0].lower()][split_field[1]] > threshold]
        if print_bool:
            print(f"Filter: {field} gt {threshold} ({len(reduced_demographics)} entries)")
        return reduced_demographics

    def filter_lt(demographics: list[data.CountyDemographics], threshold: float, field: str, print_bool = True) -> list[data.CountyDemographics]: #filters demographics by being below a threshold value of some field
        split_field = field.split(".")
        reduced_demographics = [demographic for demographic in demographics if vars(demographic)[split_field[0].lower()][split_field[1]] < threshold]
        if print_bool:
            print(f"Filter: {field} lt {threshold} ({len(reduced_demographics)} entries)")
        return reduced_demographics

    def population_total(demographics: list[data.CountyDemographics], print_bool = True) -> list[data.CountyDemographics]: #returns the total population among given counties
        total_population = sum([county.population['2014 Population'] for county in demographics])
        if print_bool:
            print(f"2014 population: {total_population}")
        return total_population

    def population(demographics: list[data.CountyDemographics], field: str, print_bool = True) -> list[data.CountyDemographics]: #returns the total supopulation of some field among given counties
        split_field = field.split(".")
        if "Persons Below Poverty Level" in split_field or "Education" in split_field or "Ethnicity" in split_field or "Ethnicities" in split_field or "Age" in split_field: #adjust for percentage value
            total_subpopulation = sum([(vars(county)[split_field[0].lower()][split_field[1]] / 100) * county.population['2014 Population'] for county in demographics])
        else:
            total_subpopulation = sum([vars(county)[split_field[0].lower()][split_field[1]] for county in demographics])
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

def process_operations_file(file_name: str) -> None: #Goes through an operations file and executes all of the operations detected
    global Demographics

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
        try: #execute the operation: If incorrect number of inputs for the given operation, print that, else do the operation. If some error comes up, print that.
            if not split_line:
                pass
            elif split_line[0] == "display":
                if len(split_line) > 1:
                    print("Invalid operation: Too many entries. -- Line", current_line_num)
                else:
                    Operations.display(Demographics_Copy)
            elif split_line[0] == "filter-gt":
                if len(split_line) != 3:
                    print("Invalid operation: Wrong number of entries. -- Line", current_line_num)
                else:
                    Demographics_Copy = Operations.filter_gt(Demographics_Copy, float(split_line[2]), split_line[1])
            elif split_line[0] == "filter-lt":
                if len(split_line) != 3:
                    print("Invalid operation: Wrong number of entries. -- Line", current_line_num)
                else:
                    Demographics_Copy = Operations.filter_lt(Demographics_Copy, float(split_line[2]), split_line[1])
            elif split_line[0] == "population-total":
                if len(split_line) > 1:
                    print("Invalid operation: Too many entries. -- Line", current_line_num)
                else:
                    Operations.population_total(Demographics_Copy)
            elif split_line[0] == "population":
                if len(split_line) != 2:
                    print("Invalid operation: Wrong number of entries. -- Line", current_line_num)
                else:
                    Operations.population(Demographics_Copy, split_line[1])
            elif split_line[0] == "percent":
                if len(split_line) != 2:
                    print("Invalid operation: Wrong number of entries. -- Line", current_line_num)
                else:
                    Operations.percent(Demographics_Copy, split_line[1])
            elif split_line[0] == "filter-state":
                if len(split_line) != 2:
                    print("Invalid operation: Wrong number of entries. -- Line", current_line_num)
                elif len(split_line[1]) != 2:
                    print("Invalid state abbreviation -- Line", current_line_num)
                else:
                    Demographics_Copy = Operations.filter_state(Demographics_Copy, split_line[1])
            else:
                print("No valid operation found -- Line", current_line_num)
        except ValueError:
            print("Invalid input(s) detected -- Line", current_line_num)
        except KeyError:
            print("Invalid input(s) detected -- Line", current_line_num)
        except:
            print("Invalid input or no such data exists -- Line", current_line_num)
    
    file.close()

if __name__ == "__main__":
    #File_Name = f"inputs/{input("No file detected in command-line arguments. Enter the file name: ")}.ops" if len(sys.argv) == 1 else sys.argv[1]
    try:
        File_Name = sys.argv[1]
        process_operations_file(File_Name)
    except IndexError:
        print("No file detected in the command-line arguments.")
        exit()
    #print(vars(Demographics[0]))
    #print(vars(Demographics[1]))

    exit()