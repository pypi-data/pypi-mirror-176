import os

def get_name_of_path(path):
    if not "sub" in path and not "ses" in path:
        return path
    else:
        return " ".join(path.replace(".nii.gz", "").replace(".nii", "").split("_")[2:])

if __name__ == '__main__':
    print(get_name_of_path(r"D:\Results\GLIOBIOPSY\derivative\sub-003\ses-01\anat\sub-003_ses-01_FLAIR_brain_1mm.nii.gz"))