import os, sys
import pprint

# __all__ = ['Hypothesis', 'get_report', 'parse_report']

class Hypothesis:
    def __init__(self):
        self.atoms = False
        self.test_failed = 0
        self.cost_o = 0
        self.cost_not_o = 0
        self.prob_o = 0
        self.prob_not_o = 0
        self.plan_time_o = 0
        self.plan_time_not_o = 0
        self.trans_time = 0
        self.plan_time = 0
        self.test_time = 0
        self.is_true = False

    def output(self):
        print(f"hyp_obj: {self.atoms} with cost of {self.cost_o} and prob of {self.prob_o}\n")

def get_report_func(path_to_folder):

    if path_to_folder.endswith(".tar.bz2"):
        # finding and opening the folder
        os.system('mkdir result-temp')
        os.system(f'tar -xvf {path_to_folder} -C ./result-temp > /dev/null')

        # finding and returning path to report.txt
        if os.path.exists('./result-temp/report.txt'):
            print("Report was found!")
            return './result-temp/report.txt'
        else:
            raise FileNotFoundError("No report was found, exiting...")
    elif path_to_folder.endswith("report.txt"):
        return path_to_folder
    else:
        print("No report file was found, did you input the correct path?")
        raise FileExistsError('No report file was found')


# def get_report_from_arg():

#     # reading in folder name with command line argument
#     path_to_result = ""
#     if len(sys.argv) < 2:
#         raise FileNotFoundError("Please specify the result folder (.tar.bz2) or a report.txt file")

#     elif len(sys.argv) > 2:
#         raise FileNotFoundError("Too many arguments given, only need name of result folder (.tar.bz2) or the path to the report.txt file")
#     else:
#         path_to_result = sys.argv[1]

#     return get_report_func(path_to_result)



def parse_report(path_to_report):

    os.system('rm -rf result-temp')

    path_to_report = os.path.abspath(path_to_report)
    problem_name = path_to_report

    # if the path given is a .tar.bz2 folder, then we will need to extract the report.txt
    if path_to_report.endswith(".tar.bz2"):
        problem_name = os.path.splitext(os.path.splitext(os.path.basename(path_to_report))[0])[0]
        if problem_name.endswith('results'):
            problem_name = problem_name.split('-results')[0]
        path_to_report = get_report_func(path_to_folder=path_to_report)


    # opening and reading the file line by line
    print(f"starting to parse from {problem_name}...")
    f = open(path_to_report, "r")
    lines = f.readlines()

    # looping through the read lines to create the objects
    hyp_objs = []
    for line in lines:
        line = line.strip()
        if 'Hyp_Atoms' in line:

            # creating new hyp object when this line is read in
            hyp_obj = Hypothesis()

            # splitting the read in line to get our info
            atoms = line.split('Hyp_Atoms=')[1]
            atoms_list = atoms.split(",")
            hyp_obj.atoms = atoms_list

            # adding to end of the list
            hyp_objs.append(hyp_obj)

        elif 'Hyp_Test_Failed' in line:

            # splitting the read in line to get our info
            info = line.split('Hyp_Test_Failed=')[1]

            # using the most recent obj and updating attribute
            hyp_objs[-1].test_failed = bool(info)

        elif 'Hyp_Cost_O' in line:

            # splitting the read in line to get our info
            info = line.split('Hyp_Cost_O=')[1]

            # using the most recent obj and updating attribute
            hyp_objs[-1].cost_o = float(info)

        elif 'Hyp_Cost_Not_O' in line:

            # splitting the read in line to get our info
            info = line.split('Hyp_Cost_Not_O=')[1]

            # using the most recent obj and updating attribute
            hyp_objs[-1].cost_not_o = float(info)

        elif 'Hyp_Prob_O' in line:

            # splitting the read in line to get our info
            info = line.split('Hyp_Prob_O=')[1]

            # using the most recent obj and updating attribute
            hyp_objs[-1].prob_o = float(info)

        elif 'Hyp_Prob_Not_O' in line:

            # splitting the read in line to get our info
            info = line.split('Hyp_Prob_Not_O=')[1]

            # using the most recent obj and updating attribute
            hyp_objs[-1].prob_not_o = float(info)

        elif 'Hyp_Plan_Time_O' in line:

            # splitting the read in line to get our info
            info = line.split('Hyp_Plan_Time_O=')[1]

            # using the most recent obj and updating attribute
            hyp_objs[-1].plan_time_o = float(info)

        elif 'Hyp_Plan_Time_Not_O' in line:

            # splitting the read in line to get our info
            info = line.split('Hyp_Plan_Time_Not_O=')[1]

            # using the most recent obj and updating attribute
            hyp_objs[-1].plan_time_not_o = float(info)

        elif 'Hyp_Trans_Time' in line:

            # splitting the read in line to get our info
            info = line.split('Hyp_Trans_Time=')[1]

            # using the most recent obj and updating attribute
            hyp_objs[-1].trans_time = float(info)

        elif 'Hyp_Plan_Time' in line:

            # splitting the read in line to get our info
            info = line.split('Hyp_Plan_Time=')[1]

            # using the most recent obj and updating attribute
            hyp_objs[-1].plan_time = float(info)

        elif 'Hyp_Test_Time' in line:

            # splitting the read in line to get our info
            info = line.split('Hyp_Test_Time=')[1]

            # using the most recent obj and updating attribute
            hyp_objs[-1].test_time = float(info)

        elif 'Hyp_Is_True' in line:

            # splitting the read in line to get our info
            info = line.split('Hyp_Is_True=')[1]

            # using the most recent obj and updating attribute
            hyp_objs[-1].is_true = bool(info)

    # list that stores the objects as a dict
    hyp_obj_dicts = []
    for hyp_obj in hyp_objs:
        hyp_obj_dicts.append(hyp_obj.__dict__)

    pprint.pprint(hyp_obj_dicts)

    os.system('rm -rf result-temp')

    return hyp_obj_dicts


# def main():
#     # path_to_report = get_report_from_arg()
#     parse_report('../test/.txt')

# if __name__ == '__main__':
# 	main()