import csv
import os
import shutil
import subprocess

# Third-party
import git

FILENAME  = 'find.csv'
REPOSITORIES = './repositories/'

def main():
    try:
        os.remove(FILENAME)
    except:
        pass
    with open('search.csv') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            full_name, url, stars, description = row
            grep_repository(full_name, url, stars, description)

def grep_repository(full_name, url, stars, description):
    print(full_name + ': ', end='')
    directory = REPOSITORIES + full_name
    git.Repo.clone_from(url, directory, depth=1)
    is_app = False
    for root, dirs, files in os.walk(directory):
        root_lower = root.lower()
        if 'sample' in root_lower or 'example' in root_lower:
            continue
        files = [file for file in files if file.endswith('.swift')]
        for filename in files:
            filepath = os.path.join(root, filename)
            if 'UIApplicationDelegate' in open(filepath).read():
                is_app = True
                break
        if is_app:
            break
    if is_app:
        print('Application?')
        with open(FILENAME, 'a') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow([full_name, url, stars, description])
    else:
        print('Not Application')
    shutil.rmtree(REPOSITORIES)

if __name__ == '__main__':
    main()
