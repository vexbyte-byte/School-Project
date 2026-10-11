import os
import shutil
import subprocess
import sys
import time
import tempfile
from pathlib import Path

class values():
    # GLOBAL VARIABLES
    build_dir = os.path.join(tempfile.gettempdir(), 'microbit_build')
    path_to_cpp_file = sys.argv[1]

    # Change this path to point to your ARM compiler install location!
    arm_gcc_bin = r"C:\Program Files (x86)\Arm GNU Toolchain arm-none-eabi\bin"
    
    # Path to your extracted microbit-samples folder from earlier
    microbit_lib = r"C:\Users\Wei Jie\AppData\Local\Projects\C++\MicroBit\microbit-samples"

    hex_file_path = str()
    source_file_obj = object()
    build_dir_obj = object()

class utils():
    def remove_temp_files():
        if os.path.exists(values.build_dir):
            try:
                shutil.rmtree(values.build_dir)
                time.sleep(0.1) 
            except: pass 

    def clear_screen():
        try:
            os.system("cls" if os.name == "nt" else "clear")
            print("\033c", end="")
        except Exception as e: pass
    
    def deploy_to_microbit():
        """
        Instead of executing an EXE, this checks if your micro:bit is 
        plugged into your laptop via USB and deploys the hex file automatically!
        """
        time.sleep(0.1)
        _x, _y = shutil.get_terminal_size(fallback=(120, 20))
        print(f"\033[94m+{'-' * (_x - 2)}+")
        print(f"|{'DEPLOYMENT'.center(_x - 2)}|")
        print(f"+{'-' * (_x - 2)}+\033[0m\n")

        # Automatically look for the MICROBIT drive letter (e.g., D:\ or E:\)
        microbit_drive = None
        for letter in 'DEFGHIJKLMNOPQRSTUVWXYZ':
            if os.path.exists(f"{letter}:\\DETAILS.TXT"): # A micro:bit always has this file
                microbit_drive = f"{letter}:\\"
                break

        if microbit_drive:
            print(f"[FOUND] micro:bit detected at drive {microbit_drive}")
            print("Flashing firmware... (The yellow light on back will blink rapidly)")
            shutil.copy2(values.hex_file_path, microbit_drive)
            print("[SUCCESS] Flashing complete! Your firmware is running.")
        else:
            print("[NOTICE] micro:bit not found over USB. Hex file saved in build directory:")
            print(f" -> {values.hex_file_path}")
    
    def copy_files(file_path, build_dir):
        source_file = Path(file_path).resolve()
        source_dir = source_file.parent 
        values.source_file_obj, values.build_dir_obj = source_file, build_dir
        
        if not os.path.exists(build_dir): os.mkdir(build_dir)
        shutil.copytree(source_dir, build_dir, dirs_exist_ok=True)

    def build_hex(file_path):        
        # Paths to the internal compiler executables
        gpp = os.path.join(values.arm_gcc_bin, "arm-none-eabi-g++.exe")
        objcopy = os.path.join(values.arm_gcc_bin, "arm-none-eabi-objcopy.exe")
        
        # Include paths for your V1.5 core layers
        inc_paths = f'-I . -I "{values.microbit_lib}" -I "{values.microbit_lib}/source"'
        
        # Target compiler flags for the Nordic nRF51822 chip inside micro:bit V1.5
        mcu_flags = "-mcpu=cortex-m0 -mthumb -O2"
        
        # 1. Compile C++ to object file, then link to elf binary, then extract hex file
        # Using pushd exactly like your original script to avoid whitespace issues
        compile_cmd = (
            f'pushd "{values.build_dir_obj}" && '
            f'"{gpp}" {mcu_flags} {inc_paths} -DLOG_MESSAGES=1 "{values.source_file_obj.name}" -o firmware.elf && '
            f'"{objcopy}" -O ihex firmware.elf firmware.hex'
        )
        
        print(f"--- Step 1: Synced to {values.build_dir_obj} ---")
        print(f"--- Step 2: Cross-compiling for ARM Cortex-M0 ---")
        
        result = subprocess.run(compile_cmd, shell=True)
        
        if result.returncode == 0: 
            print(f"\n[SUCCESS] Compiled target binary.")
            values.hex_file_path = os.path.join(values.build_dir, "firmware.hex")
        else:
            print(f"\n[FAILED] Error during ARM compilation compilation.")
            quit()
    
def main():
    utils.remove_temp_files()
    utils.copy_files(values.path_to_cpp_file, values.build_dir)
    if len(sys.argv) > 1: utils.build_hex(values.path_to_cpp_file)
    
    utils.clear_screen()
    utils.deploy_to_microbit()
    print('\n' * 5)


if __name__ == "__main__": 
    main()