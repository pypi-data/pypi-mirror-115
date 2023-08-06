import sys, os, getopt, time
from types import new_class


def get_inpts():
    f = True
    while f:
        pkg_name             = input("What would you like to call your package (*): ")
        version              = input("Whats the version of your programm (*): ")
        description          = input("Describe your Project shortly (*): ")
        long_description     = input("Describe your Project in detail (*): ")
        author               = input("The Author of the Project (*): ")
        author_email         = input("The email of the Author (*): ")
        install_rewuirements = input("What extra packages are needed for your programm seperated by a '-': ")
        keywords             = input("Select some keywords seperated by a '-': ")
        if not pkg_name or not version or not description or not long_description or not author or not author_email:
            os.system("clear")
            print("It seems like you didn't fill out all the important requirements (all with '*')! Try again\n\n")
            f = True
        else:
            f = False
        if not install_rewuirements:
            new_isntall_reqs = []
        else:
            new_isntall_reqs: list = install_rewuirements.split("-")
        if not keywords:
            new_keywds = []
        else:
            new_keywds: list = keywords.split("-")
    return pkg_name, version, description, long_description, author, author_email, new_isntall_reqs, new_keywds


def main(opts, args):
    file_path = opts[0][1]
    pkg_name, version, description, long_description, author, author_email, install_rewuirements, keywords = get_inpts()
    os.makedirs(f"bass-folder/{pkg_name}")

    with open("./bass-folder/" + "setup.py" ,"w") as setup:
        setup.write("from setuptools import setup, find_packages\nimport codecs\nimport os\n\n")
        setup.write(f"VERSION='{version}'\nDESCRIPTION = '{description}'\n\n")
        setup.write(f"setup(\n   name='{pkg_name}',\n")
        setup.write(f"   version='{version}',\n")
        setup.write(f"   author='{author}',\n")
        setup.write(f"   author_email='{author_email}',\n")
        setup.write(f"   description='{description}',\n")
        setup.write(f"   long_description_content_type='text/markdown',\n")
        setup.write(f"   long_description='{long_description}',\n")
        setup.write(f"   packages=find_packages(),\n")
        setup.write(f"   install_requires={install_rewuirements},\n")
        setup.write(f'   keywords="{keywords}"')
        setup.write("\n)")
        setup.close()
    os.system("clear")

    with open(f"./bass-folder/{pkg_name}/" + "__init__.py", "w") as init:
        init.close()
    
    with open(f"{file_path}", "r") as user_file:
        file_code = user_file.read()
    
    with open(f"./bass-folder/{pkg_name}/" + f"{pkg_name}.py", "w") as new_file:
        new_file.write(file_code)
    
    
    os.system("cd bass-folder && python3 setup.py sdist bdist_wheel && pip3 install twine && twine upload dist/*")
    os.system("del bass-folder")

if __name__=="__main__":
    opts, args = getopt.getopt(sys.argv[1:], "f:", ["filepath"])
    main(opts, args)
