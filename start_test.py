import os
from cf.config import project_path
from ReadCase import get_files,run_task

def check_folder():
    children_folder = ["error_img", "log"]

    for folder in children_folder:
        if not os.path.exists(os.path.join(project_path, folder)):
            os.makedirs(folder)


if __name__ == '__main__':
    # 文件检查
    check_folder()
    # 执行
    for file in get_files():
        run_task(file)
    # 生成报告
    os.system("allure generate ./data -o ./report --clean")

