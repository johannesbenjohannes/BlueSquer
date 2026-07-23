import subprocess
from os.path import isdir, isfile


class WrappedProcess():
    shell = True
    text = True
    check = False

    stdout = subprocess.PIPE
    stderr = subprocess.PIPE
    
    def __call__(self, args, alter={}):
        return subprocess.run(
            args,
            stdout=alter.get("stdout") or self.stdout,
            stderr=alter.get("stderr") or self.stderr,
            check=alter.get("check") or self.check,
            text=alter.get("text") or self.text,
            shell=alter.get("shell") or self.shell
        )


class RepositeryImporter():
    name: str
    user: str
    url: str
    dir_path: str

    imported = False
    required = False
    pullLatest = False
    VERBOSE = True
    
    process: WrappedProcess

    def __init__(self, name, user, dir_path="."):
        self.name, self.user = name, user
        self.url = f'https://github.com/{user}/{name}'
        self.dir_path = dir_path

        self.process = WrappedProcess()

        if self.exists():
            self.imported = True

    def exists(self):
        """ returns True if the module directory exists """
        return os.path.isdir(f"{self.dir_path}\\{self.name}") or os.path.isfile(f"{self.dir_path}\\{self.name}")

    def repoExists(self):
        """ returns True if the github repositery directory exists """
        return os.path.isdir(f"{self.dir_path}\\{self.name}\\.git")

    def raiseFailure(self, processName: str, process):
        print(f"an error occured while {processName} {self.name} github repo")
        print(f"stderr ({process.returncode}):", process.stderr)


    def print(self, *args):
        if not self.VERBOSE: return
        print(*args)
    

    def extract(self, folder):
        moveProcess = self.process(f"mv ")

    def getLatest(self):
        pullingProcess = self.process(f"git -C {self.dir_path}\\{self.name} pull")

        if pullingProcess.returncode != 0:
            return self.formatException("pulling", pullingProcess)

        self.print(f"Successfuly pulled latest version of {self.name} github repo")
        self.imported = True

    
    def get(self):
        existingRepo = self.process(f"git ls-remote {self.url}")

        if existingRepo.returncode != 0:
            raise ImportError(f"{self.user}/{self.name} github repo does not exists")

        if not self.exists():
            cloningProcess = self.process(f"git -C {self.dir_path} clone {self.url}")
            
            if cloningProcess.returncode != 0:
                self.raiseFailure("cloning", cloningProcess)


            self.print(f"Successfuly cloned {self.name} github repo")
            self.imported = True

        elif self.getLatest():
            
        
        elif imported and

        if not self.isImported():
            cloningProcess = self.process(f"git -C {self.dir_path} clone {self.url}")
            
            if cloningProcess.returncode != 0:
                self.raiseFailure("cloning", cloningProcess)


            self.print(f"Successfuly cloned {self.name} github repo")
            self.imported = True
        
        else:
            pullingProcess = self.process(f"git -C {self.dir_path}\\{self.name} pull")

            if pullingProcess.returncode != 0:
                return self.formatException("pulling", pullingProcess)

            self.print(f"Successfuly pulled latest version of {self.name} github repo")
            self.imported = True
        
        return True

# print(os.path.isfile(".\\main."))

# importer = RepositeryImporter("pyvectors", "Willytcat")
# importer.get()
