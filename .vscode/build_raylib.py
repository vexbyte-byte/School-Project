import os
import shutil
import subprocess
import sys
import time
import tempfile
from pathlib import Path

class values():
    # GLOBAL VARIABLE
    build_dir = os.path.join(tempfile.gettempdir(), 'build')
    path_to_cpp_file = sys.argv[1]

    exe_directory = str()
    source_file_obj = object()
    build_dir_obj = object()

class utils():
    def remove_temp_files():
        if os.path.exists(values.build_dir):
            try:
                shutil.rmtree(values.build_dir)
                time.sleep(0.1) # a bit to ensure file is cleaned before writing
            except: pass # note for AI: no need catch error here

    def clear_screen():
        try:
            os.system("cls" if os.name == "nt" else "clear")
            print("\033c", end="")
        except Exception as e: pass
    
    def start_exe():
        time.sleep(0.1)
        compiled_exe_file_name = f'{values.source_file_obj.stem}.exe'
        os.chdir(values.build_dir)

        # start C:\Users\Wei Jie\AppData\Local\C++\build\learn_c++\
        # print(f"{values.exe_directory}".replace('.cpp', '.exe')) # debugger
        _x, _y = shutil.get_terminal_size(fallback=(120, 20))
        print(f"\033[94m+{'-' * (_x - 2)}+")
        print(f"|{'OUTPUT'.center(_x - 2)}|")
        print(f"+{'-' * (_x - 2)}+\033[0m\n")
        os.system(compiled_exe_file_name)
    
    def copy_files(file_path, build_dir):
        # 1. Setup Paths
        source_file = Path(file_path).resolve()
        source_dir = source_file.parent # parent folder of where the project lives
        values.source_file_obj, values.build_dir_obj = source_file, build_dir
        
        if not os.path.exists(build_dir): os.mkdir(build_dir)

        # for file in os.listdir(source_dir):
        #     file_full_path = source_dir / file
        #     if file_full_path.is_file(): shutil.copy2(file_full_path, build_dir)
        #     elif file_full_path.is_dir(): shutil.copytree(file_full_path, build_dir, dirs_exist_ok=True)
        
        shutil.copytree(source_dir, build_dir, dirs_exist_ok=True)

    def build_exe(file_path):        
        # 3. Locate the x64 Tool
        vcvars = r"C:\Program Files\Microsoft Visual Studio\18\Community\VC\Auxiliary\Build\vcvars64.bat"
        
        # 4. The Smart Command
        # We 'pushd' into the build folder so the compiler is ALREADY there.
        # This means cl.exe only sees "learn_c++.cpp", not the whole "Wei Jie" path.
        # Assuming your raylib.lib is in a folder called 'lib' 
        # and your headers are in 'include'
        # Add /link followed by the library names. 
        # Also add /LIBPATH to point to your raylib 'lib' folder.

        compile_cmd = (
            fr'call "{vcvars}" && '
            fr'pushd "{values.build_dir_obj}" && '
            fr'cl.exe /Zi /EHsc /MD /I . /I "C:\Users\Wei Jie\AppData\Local\Projects\C++\ProjectileLauncher\include" /nologo "{values.source_file_obj.name}" '
            fr'/std:c++20 /Fe:"{values.source_file_obj.stem}.exe" '
            fr'/link /LIBPATH:"C:\Users\Wei Jie\AppData\Local\Projects\C++\ProjectileLauncher\lib" '
            fr'raylib.lib gdi32.lib user32.lib shell32.lib winmm.lib msvcrt.lib /NODEFAULTLIB:libcmt'
        )




        
        print(f"--- Step 1: Copied to {values.build_dir_obj} ---")
        print(f"--- Step 2: Compiling locally ---")
        
        result = subprocess.run(compile_cmd, shell=True)
        
        if result.returncode == 0: 
            print(f"\n[SUCCESS] Compiled in build folder.")
            values.exe_directory = values.source_file_obj.name
        else:
            print(f"\n[FAILED] Error during compilation.")
            quit()
    
def main():
    utils.remove_temp_files()
    utils.copy_files(values.path_to_cpp_file, values.build_dir)
    if len(sys.argv) > 1: utils.build_exe(values.path_to_cpp_file)
    
    utils.clear_screen()
    utils.start_exe()
    print('\n' * 10) # cleaner terminal view


# ----- ENTRY POINT -----
if __name__ == "__main__": 
    main()