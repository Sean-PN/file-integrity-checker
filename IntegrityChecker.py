import hashlib
import os
import json

def hash_file(filename, algo="sha256"):

    #generate hash of a file using SHA or MD5
    h = hashlib.new(algo)
    
    try:
        with open(filename, 'rb') as f:
            
            while chunk := f.read(8192):    
                h.update(chunk)

        return h.hexdigest()
    
    except FileNotFoundError:
        
        print(f"Error: File {filename} not found.")
        return None



#save hashes in a JSON file
def save_hashes(hash_dict, output_file="hashes.json"):

    with open(output_file, "w") as f:
        
        json.dump(hash_dict, f, indent=4)
    
    print(f"Hashes saved to {output_file}")


#load previously saved hashes
def load_hashes(input_file="hashes.json"):
    
    if not os.path.exists(input_file):
        
        print("No saved hashes found.")
        return {}
    
    with open(input_file, "r") as f:
        return json.load(f)


#create baseline hashes to record file integrity
def create_baseline():

    print("\n--- Create Integrity Baseline ---")
    files = input("Enter file paths separated by commas: ").split(",")
    algo = input("Choose hashing algorithm (sha256/md5): ").strip().lower()
    
    if algo not in ["sha256", "md5"]:
        
        print("Invalid choice, defaulting to sha256.")
        algo = "sha256"

    hash_dict = {}
    
    for f in files:
        
        f = f.strip()
        file_hash = hash_file(f, algo)
        
        if file_hash:
            hash_dict[f] = file_hash
            print(f"{f} -> {file_hash}")

    save_hashes(hash_dict)


#compares current file hashes to previously saved baseline hashes
def check_integrity():
    
    print("\n--- Check File Integrity ---")
    algo = input("Choose hashing algorithm used previously (sha256/md5): ").strip().lower()
    
    if algo not in ["sha256", "md5"]:
        
        print("Invalid choice, defaulting to sha256.")
        algo = "sha256"

    saved_hashes = load_hashes()
    
    if not saved_hashes:
        return

    for f, old_hash in saved_hashes.items():
       
        new_hash = hash_file(f, algo)
        
        if not new_hash:
            continue
        
        if new_hash == old_hash:
            print(f"{f}: OK (no changes)")
        
        else:
            print(f"{f}: ALERT! File has changed!")


#main function featuring loop for user choices
def main():

    print("=== File Integrity Checker ===")
    
    while True:

        print("\nChoose an option:")
        print("1. Create baseline (hash files)")
        print("2. Check integrity (compare with baseline)")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ")
        if choice == "1":
            create_baseline()
        
        elif choice == "2":
            check_integrity()
        
        elif choice == "3":
            print("Exiting Integrity Checker. Goodbye!")
            break
        
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
