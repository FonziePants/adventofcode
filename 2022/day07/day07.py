def read_data(file_path,debug=True):
    file = open(file_path, "r")

    data = []
    for line in file:
        if not line.rstrip():
            continue
        sline = line.rstrip()
        data.append(sline)
        
    file.close()
    if debug: print(data)
    return data

def is_dir(input):
    return input.startswith('dir ')

def get_command(input):
    if not input.startswith('$ '):
        return None
    else: return input[2:].split()

class File:
    def __init__(self, input, dir) -> None:
        parts = input.split()
        self.size = int(parts[0])
        self.name = parts[1]
        self.dir = dir
        self.path = dir.fullpath()
    
    def fullpath(self):
        return '{p}/{n}'.format(p=self.path, n=self.name)
    
    def __repr__(self) -> str:
        return 'FILE: {p} (size={s})'.format(
            p=self.fullpath(),
            s=self.size,
        )
    
class Directory:
    def __init__(self, name, dir) -> None:
        self.name = name
        self.dir = dir
        self.path = dir.fullpath() if dir is not None else ''
    
    def fullpath(self):
        return '{p}/{n}'.format(p=self.path, n=self.name)
    
    def __repr__(self) -> str:
        return 'DIR:  {p}'.format(p=self.fullpath())

def format_data(data):
    i = 0
    directories = {}
    files = {}
    current_dir = None
    while i < len(data):
        row = data[i]
        cmd = get_command(row)
        if cmd is not None:
            if cmd[0] == 'cd':
                dir_string = cmd[1]
                dir_fp = '{pd}/{cd}'.format(pd=current_dir.fullpath() if current_dir is not None else '',cd=dir_string)
                if dir_string == '..':
                    current_dir = current_dir.dir
                elif dir_fp in directories:
                    current_dir = directories[dir_fp]
                else:
                    current_dir = Directory(dir_string, current_dir)
                    directories[current_dir.fullpath()] = current_dir
        else:
            if is_dir(row):
                dir_string = row[4:]
                dir_fp = '{pd}/{cd}'.format(pd=current_dir.fullpath() if current_dir is not None else '',cd=dir_string)
                if dir_fp not in directories:
                    new_dir = Directory(dir_string, current_dir)
                    directories[current_dir.fullpath()] = new_dir
            else:
                filepath = '{d}/{f}'.format(d=current_dir.fullpath(),f=row.split()[1])
                if filepath not in files:
                    files[filepath] = File(row, current_dir)
        i += 1

    dir_sizes = {d: 0 for d in directories}

    for fpath in files:
        file = files[fpath]
        dir = file.dir
        while dir is not None:
            dir_sizes[dir.fullpath()] = dir_sizes[dir.fullpath()] + file.size
            dir = dir.dir
    return directories, files, dir_sizes

def part1(dir_sizes):
    limit = 100000
    sum = 0
    for ds in dir_sizes:
        if dir_sizes[ds] <= limit:
            sum += dir_sizes[ds]
    return sum

def part2(dir_sizes):
    total_space = 70000000
    needed_space = 30000000
    used_space = max(dir_sizes[ds] for ds in dir_sizes)
    delete_space = needed_space-(total_space-used_space)
    smallest_space = total_space
    for ds in dir_sizes:
        if delete_space <= dir_sizes[ds] <= smallest_space:
            smallest_space = dir_sizes[ds]
    return smallest_space

def run_program(debug=False):
    file_path = 'test.txt' if debug else 'day07.txt'
    
    data = read_data(file_path, debug)
    directories, files, dir_sizes = format_data(data)

    if debug:
        print('Directories:')
        for dir in directories:
            print(dir)
        print('\nFiles:')
        for file in files:
            print(file)
        print('\nDirectory Sizes:')
        for ds in dir_sizes:
            print('{0}: {1}'.format(ds, dir_sizes[ds]))

    print(part1(dir_sizes)) # 1449447
    print(part2(dir_sizes)) # 8679207

run_program(False)