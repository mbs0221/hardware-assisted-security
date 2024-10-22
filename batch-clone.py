#!/usr/bin/python3

import os
import subprocess
import yaml

# 读取 YAML 文件
yaml_file = "modules.yaml"

with open(yaml_file, "r") as file:
    courses = yaml.safe_load(file)

# 定义课程根目录
base_dir = "./"  # 替换成你存放课程的根目录

def git_clone(repo_url, target_dir):
    """如果指定目录不存在，克隆仓库到该目录"""
    if not os.path.exists(target_dir):
        print(f"Cloning {repo_url} to {target_dir}...")
        subprocess.run(["git", "clone", repo_url, target_dir])
    else:
        print(f"Directory {target_dir} already exists.")
        subprocess.run(["git", "submodule", "add", repo_url, target_dir])

def git_move(old_dir, new_dir):
    """移动已存在的Git仓库"""
    if os.path.exists(old_dir):
        print(f"Moving {old_dir} to {new_dir}...")
        subprocess.run(["git", "mv", old_dir, new_dir])
    else:
        print(f"Directory {old_dir} does not exist, cannot move.")

def process_courses(courses):
    """处理课程配置，检查文件夹和Git仓库"""
    for category, repos in courses.items():
        category_dir = os.path.join(base_dir, category)
        if not os.path.exists(category_dir):
            os.makedirs(category_dir)

        for repo in repos:
            repo_name = repo.split("/")[-1]
            target_dir = os.path.join(category_dir, repo_name)
            repo_url = f"https://github.com/{repo}.git"

            # 检查目标目录是否存在
            if not os.path.exists(target_dir):
                # 如果不存在，检查仓库是否已经在本地
                local_repo_dir = os.path.join(base_dir, repo_name)
                if os.path.exists(local_repo_dir):
                    # 如果仓库已经clone到本地，移动到目标目录
                    git_move(local_repo_dir, target_dir)
                else:
                    # 如果仓库没有被克隆，执行git clone
                    git_clone(repo_url, target_dir)
            else:
                print(f"Course {repo_name} already exists in {target_dir}")
                subprocess.run(["git", "submodule", "add", repo_url, target_dir])

if __name__ == "__main__":
    process_courses(courses)
