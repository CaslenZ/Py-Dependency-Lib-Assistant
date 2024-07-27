import ast
import subprocess
import os

def get_dependencies(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        tree = ast.parse(file.read())
    dependencies = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for name in node.names:
                dependencies.add(name.name)
        elif isinstance(node, ast.ImportFrom):
            dependencies.add(node.module)
    return dependencies

def install_missing_dependencies(dependencies, python_executable):
    installed = []
    missing = []
    for dep in dependencies:
        try:
            subprocess.check_call((python_executable, "-c", f"import {dep}"))
            print(f"{dep} 已安装")
            installed.append(dep)
        except subprocess.CalledProcessError:
            print(f"{dep} 未安装，尝试安装...")
            try:
                subprocess.check_call((python_executable, "-m", "pip", "install", dep))
                print(f"{dep} 安装成功")
                installed.append(dep)
            except subprocess.CalledProcessError:
                print(f"安装 {dep} 失败")
                missing.append(dep)
    return installed, missing

def main():
    python_executable = "python"  # 可根据实际情况修改为具体的 Python 解释器路径
    file_path = input("请输入 Python 脚本的路径: ")
    if not os.path.exists(file_path):
        print("文件不存在，请重新输入。")
        return
    dependencies = get_dependencies(file_path)
    print("检测到的依赖库:", dependencies)
    installed, missing = install_missing_dependencies(dependencies, python_executable)
    print("已安装的依赖库:", installed)
    if missing:
        print("以下依赖库安装失败:", missing)

if __name__ == "__main__":
    main()