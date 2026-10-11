import subprocess
import os

# 1. Configuration - Use raw strings (r"") for all paths
vcvars_path = r"C:\Program Files\Microsoft Visual Studio\18\Community\VC\Auxiliary\Build\vcvars64.bat"
work_dir = r"C:\Users\Wei Jie\AppData\Local\C++"
include_path = r"C:\Users\Wei Jie\AppData\Local\C++\OpenCL-Headers"
lib_folder = r"C:\Users\Wei Jie\AppData\Local\C++\OpenCL-SDK-v2025.07.23-Win-x64\OpenCL-SDK-v2025.07.23-Win-x64\lib"

# 2. Pre-check: Let's see which path is actually failing before we run the shell
if not os.path.exists(vcvars_path):
    print(f"❌ VS Path missing: {vcvars_path}")
if not os.path.exists(work_dir):
    print(f"❌ Work directory missing: {work_dir}")

# 3. Construct the command
# We use /d to ensure drive switching and wrap paths in escaped double-quotes
compile_cmd = f'cd /d "{work_dir}" && cl /EHsc /I"{include_path}" gpu_acceleration.cpp /link /LIBPATH:"{lib_folder}" OpenCL.lib'

# The full command chains the environment activation with the compilation
full_command = f'"{vcvars_path}" && {compile_cmd}'

print("Starting x64 Native Environment and Compiling...\n")

# 4. Execute
result = subprocess.run(full_command, shell=True, capture_output=True, text=True)

# 5. Output Results
if result.stdout:
    print("--- STDOUT ---")
    print(result.stdout)

if result.stderr:
    print("--- ERRORS ---")
    print(result.stderr)

# 6. Success Check
if result.returncode == 0:
    print("\n✅ Compilation Successful!")
    # Optional: Run the program immediately
    # os.system(f'"{work_dir}\\gpu_acceleration.exe"')
else:
    print("\n❌ Compilation Failed.")