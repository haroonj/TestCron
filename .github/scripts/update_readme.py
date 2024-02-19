import os
import re
from github import Github

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_NAME = "haroonj/TestCron"  # Change this to your actual repo name

g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO_NAME)

def get_file_list(path):
    """
    Recursively retrieves a list of files in the given directory path.
    """
    contents = repo.get_contents(path)
    file_list = []
    for content in contents:
        if content.type == "dir":
            file_list.extend(get_file_list(content.path))
        else:
            file_list.append(content.path)
    return file_list

def categorize_problems(file_list):
    """
    Categorizes problems into difficulties and formats markdown links.
    """
    problems = {'Easy': [], 'Medium': [], 'Hard': []}
    for file_path in file_list:
        difficulty = None
        if re.search(r'/easy/', file_path):
            difficulty = 'Easy'
        elif re.search(r'/medium/', file_path):
            difficulty = 'Medium'
        elif re.search(r'/hard/', file_path):
            difficulty = 'Hard'

        if difficulty:
            problem_name = re.sub(r'.*/', '', file_path).replace('.java', '').replace('.py', '')
            problem_link = f"* [{problem_name}]({file_path})"
            problems[difficulty].append(problem_link)

    return problems

def update_readme(problems):
    """
    Update the README.md file with the latest list of problems.
    """
    contents = repo.get_contents("README.md")
    readme_content = contents.decoded_content.decode("utf-8")

    # Prepare new sections for the README
    new_sections = {}
    for difficulty, links in problems.items():
        new_section = f"## {'☠' if difficulty == 'Hard' else '💪🏻' if difficulty == 'Medium' else '👶🏻'} {difficulty}\n\n" + "\n".join(sorted(links)) + "\n\n"
        new_sections[difficulty] = new_section

    # Replace the existing sections in the README
    for difficulty, new_section in new_sections.items():
        pattern = re.compile(rf"## [☠💪🏻👶🏻] {difficulty}\n\n.*?(\n\n##|$)", re.DOTALL)
        readme_content = re.sub(pattern, new_section + "\n\n##", readme_content)

    # Update README file on GitHub
    repo.update_file(contents.path, "Update README with latest problems list", readme_content, contents.sha)

def main():
    file_list = get_file_list("src")
    print('file_list', file_list)
    problems = categorize_problems(file_list)
    print('problems', problems)
    update_readme(problems)

if __name__ == "__main__":
    main()
