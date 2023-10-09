import itertools
import string
from rarfile import RarFile
from tqdm import tqdm

charset = string.ascii_letters + string.digits + string.punctuation 
password_length = 7

rar_file_path = 'file path'
progress_file = 'progress.txt'  # File to store progress

try:
    with open(progress_file, 'r') as f:
        last_attempt = int(f.readline())  
except FileNotFoundError:
    last_attempt = 0 

try:
    with RarFile(rar_file_path, 'r') as myrar:
        file_names = myrar.namelist()

        total_attempts = len(charset) ** password_length

       
        with tqdm(total=total_attempts, initial=last_attempt, desc="Brute-forcing", unit="password") as pbar:
            for length in range(1, password_length + 1):
                for password_attempt in itertools.product(charset, repeat=length):
                    password = ''.join(password_attempt)
                    try:
                        myrar.extractall(pwd=password)
                        print(f'Success! Password found: {password}')
                        break
                    except Exception as e:
                        pass
                    pbar.update(1)  
                    last_attempt += 1  

                    if last_attempt % 1000 == 0:
                        with open(progress_file, 'w') as f:
                            f.write(str(last_attempt))  #

except KeyboardInterrupt:
    print("Brute-force attack interrupted by the user.")
except Exception as e:
    print(f"An error occurred: {e}")

# Remove the progress file after the attack is completed successfully
import os
os.remove(progress_file)
