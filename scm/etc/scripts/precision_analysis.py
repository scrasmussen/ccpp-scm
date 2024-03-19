import argparse
import os
import subprocess
import sys
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

# TODO:
#  - [ ] add user argument to cmake "$@" in configure{32,64}
#  - [ ] add run function
#  - [ ] run through all cases compiled

def run_cmd(command):
    try:
        # Run the cmake command
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        # Handle errors if cmake command fails
        print(f"Error running {e}")
        sys.exit()


# Function to run configuration step
def configure32():
    print("Running single precision configuration step")
    command = ["cmake", "src/", "-B", "build32", "-D32BIT=1"]
    run_cmd(command)


# Function to run configuration step
def configure64():
    print("Running double precision configuration step")
    command = ["cmake", "src/", "-B", "build64"]
    run_cmd(command)


# Function to run configuration step
def configure():
    print("Running configuration steps")
    configure32()
    configure64()


# Function to run make step
def make32():
    print("Running single precision make step")
    command = ["make", "-C", "build32", "-j4"]
    run_cmd(command)

# Function to run make step
def make64():
    print("Running double precision make step")
    command = ["make", "-C", "build64", "-j4"]
    run_cmd(command)


# Function to run make step
def make():
    print("Running make steps")
    make32()
    make64()


# Post process single vs. double precision output
def post():
    print("Post processing single vs. double precision output")
    postprocess()


def run32():
    print("Running single precision executable")
    # build32/run_scm.py -c twpice -s SCM_RAP \
    #     --bin_dir $(pwd)/build32 \
    #     --run_dir $(pwd)/output32
    print("Need to finish function, exiting")
    sys.exit()


def run64():
    print("Running double precision executable")
    # build64/run_scm.py -c twpice -s SCM_RAP \
    #     --bin_dir $(pwd)/build32 \
    #     --run_dir $(pwd)/output32
    print("Need to finish function, exiting")
    sys.exit()


# Function to run executable
def run():
    print("Running executables")
    run32()
    run64()


def get_time_dimension(da):
    # Initialize time variable to None
    time = None

    # Iterate over dimensions of the Dataset
    for dim in da.dims:
        if 'time' in dim.lower():
            time = da[dim].name
            break

    # Check if time variable was found
    if time is None:
        print(f"No 'time' dimension matched in {da.name}")
    # else:
    #     print("Found 'time' dimension in the dataset.")
    return time


def calculate_mse(da1, da2):
    """Calculate the mean square error (MSE) between two DataArrays."""
    found_time = True
    time_dim = get_time_dimension(da1)
    if time_dim == None:
        found_time = False
        print(f"No time dimension found in variable {da1.name}")
        return None, found_time

    mse = ((da1 - da2) ** 2).mean(dim=time_dim)
    return mse, found_time


def save_mse_plots(case_dir, mse_dict):
    """Save plots of mean square error (MSE) to a directory."""
    diff_dir = case_dir + '_diff'
    os.makedirs(diff_dir, exist_ok=True)

    for var_name, mse in mse_dict.items():
        plt.figure()
        mse.plot()
        plt.title(f'Mean Square Error for {var_name}')
        plt.xlabel('Latitude')
        plt.ylabel('Longitude')
        plt.savefig(os.path.join(diff_dir, f'{var_name}_mse.png'))
        plt.close()


# Post processing function
def postprocess():
    print('post-processing')
    output_f = 'output.nc'
    output32_dir = 'output32'
    output64_dir = 'output64'
    output32_dirs = sorted([os.path.basename(dirpath) for dirpath, _, _ in os.walk(output32_dir) if os.path.basename(dirpath).startswith('output_')])
    output64_dirs = sorted([os.path.basename(dirpath) for dirpath, _, _ in os.walk(output64_dir) if os.path.basename(dirpath).startswith('output_')])

    vars_equal = []
    vars_diff = []

    # Use set intersection to find directories that exist in both output32 and output64
    case_dirs = set(output32_dirs).intersection(output64_dirs)
    for case_dir in case_dirs:
        f32 = os.path.join(output32_dir, case_dir, output_f)
        f64 = os.path.join(output64_dir, case_dir, output_f)
        # Open f32 and f64 using xarray
        ds32 = xr.open_dataset(f32)
        ds64 = xr.open_dataset(f64)

        # Compare variables and compute mean square error (MSE) for variables that are different
        mse_dict = {}
        for var_name in ds32.data_vars:
            if var_name in ds64.data_vars:
                if np.any(ds32[var_name] != ds64[var_name]):
                    result, time_dim_found = calculate_mse(ds32[var_name], ds64[var_name])
                    if time_dim_found == False:
                        continue
                    mse_dict[var_name] = result
                    vars_diff.append(var_name)
                    diff_f = os.path.join('output_diff',case_dir)
                    print(f"Variable {var_name} differs in output files, writing diff to {diff_f}")
                    # Save plots of mean square error (MSE) to a directory
                    save_mse_plots(diff_f, mse_dict)
                else:
                    vars_equal.append(var_name)
                    print(f"Variable {var_name} is the same in both output files")

    # Write the vars_diff list to a text file
    with open('different_variables.txt', 'w') as f:
        f.write("Equal variables:\n")
        for var in vars_equal:
            f.write(f" - {var}\n")
        f.write("Different variables:\n")
        for var in vars_diff:
            f.write(f" - {var}\n")


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Script to configure, make, and run a program")
    parser.add_argument("--configure", action="store_true", help="Configure CMake for single and double precision")
    parser.add_argument("--configure32", action="store_true", help="Configure CMake for single precision")
    parser.add_argument("--configure64", action="store_true", help="Configure CMake for double precision")
    parser.add_argument("--make", action="store_true", help="Build single and double precision code")
    parser.add_argument("--make32", action="store_true", help="Build single precision code")
    parser.add_argument("--make64", action="store_true", help="Build double precision code")
    parser.add_argument("--post", action="store_true", help="Postprocess the output")
    parser.add_argument("--run", action="store_true", help="Run cases in single and double precision")
    parser.add_argument("--run32", action="store_true", help="Run cases in single precision")
    parser.add_argument("--run64", action="store_true", help="Run cases in double precision")
    args = parser.parse_args()

    # If --help is provided, print help message
    if len(sys.argv) == 1 or "--help" in sys.argv:
        parser.print_help()
        sys.exit()

    # Execute requested step(s)
    if args.configure:
        configure()
    elif args.configure32:
        configure32()
    elif args.configure64:
        configure64()
    elif args.make32:
        make32()
    elif args.make64:
        make64()
    elif args.make:
        make()
    elif args.post:
        post()
    elif args.run:
        run()
    else:
        configure()
        make()
        run()


if __name__ == "__main__":
    main()
