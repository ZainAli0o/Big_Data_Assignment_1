from hdfs import InsecureClient
import os
import time

# Connect to the HDFS NameNode
client = InsecureClient('http://localhost:9870', user='root')




def create_file(hdfs_path, local_content):
    try:
        with client.write(hdfs_path, encoding='utf-8', overwrite=True) as writer:
            writer.write(local_content)
        print(f"[CREATE] Successfully created file: {hdfs_path}")
    except Exception as e:
        print(f"[CREATE] Error creating file: {e}")


def read_file(hdfs_path):
    try:
        with client.read(hdfs_path, encoding='utf-8') as reader:
            content = reader.read()
        print(f"[READ] Content of {hdfs_path}:\n---\n{content}\n---")
        return content
    except Exception as e:
        print(f"[READ] Error reading file: {e}")
        return None


def append_to_file(hdfs_path, local_content):
    try:
        with client.write(hdfs_path, encoding='utf-8', append=True) as writer:
            writer.write(local_content)
        print(f"[UPDATE] Successfully appended to file: {hdfs_path}")
    except Exception as e:
        print(f"[UPDATE] Error appending to file: {e}")


def delete_file(hdfs_path):
    try:
        if client.status(hdfs_path, strict=False):
            client.delete(hdfs_path)
            print(f"[DELETE] Successfully deleted file: {hdfs_path}")
        else:
            print(f"[DELETE] File not found, nothing to delete: {hdfs_path}")
    except Exception as e:
        print(f"[DELETE] Error deleting file: {e}")


def list_files(hdfs_path):
    """Helper function to list files in an HDFS directory."""
    try:
        files = client.list(hdfs_path)
        print(f"[LIST] Files in '{hdfs_path}': {files}")
        return files
    except Exception as e:
        print(f"[LIST] Error listing files: {e}")
        return []


# --- Main execution block to demonstrate CRUD operations ---
if __name__ == "__main__":
    hdfs_dir = '/user/test'
    hdfs_filepath = f"{hdfs_dir}/my_test_file.txt"

    print("--- Starting HDFS CRUD Operations ---")

    # 0. Clean up and create a base directory
    if client.status(hdfs_dir, strict=False):
        client.delete(hdfs_dir, recursive=True)
        print(f"[CLEANUP] Existing directory removed: {hdfs_dir}")
    client.makedirs(hdfs_dir)

    # 1. List initial state (should be empty)
    list_files(hdfs_dir)

    # 2. CREATE
    initial_content = "Hello from Lahore!\nThis is the first line."
    create_file(hdfs_filepath, initial_content)

    # 3. READ
    read_file(hdfs_filepath)

    # 4. UPDATE (Append)
    content_to_append = "\nThis is a new line, added on a Thursday night."
    append_to_file(hdfs_filepath, content_to_append)

    # 5. READ again to see the changes
    read_file(hdfs_filepath)

    # 6. List files again (should show the file)
    list_files(hdfs_dir)

    # 7. DELETE
    delete_file(hdfs_filepath)

    # 8. Final list to confirm deletion
    list_files(hdfs_dir)

    print("\n--- HDFS CRUD Operations Complete ---")

