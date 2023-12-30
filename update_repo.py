import subprocess
import os

def update_git_repository(repository_path, branch_name):
    try:
        # Change directory to the Git repository location
        # os.chdir(repository_path)

        # Pull the latest changes from the remote repository
        subprocess.run(['git', 'pull', 'origin', branch_name], check=True)

        # Optionally, commit and push your local changes
        subprocess.run(['git', 'add', 'milestone2.py'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Automated commit'], check=True)
        subprocess.run(['git', 'push', 'origin', branch_name], check=True)

        print("Local repository updated successfully.")

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Set the path to your local Git repository and branch name
    repository_path = ""
    branch_name = "main"  # Replace with your branch name

    update_git_repository(repository_path, branch_name)
