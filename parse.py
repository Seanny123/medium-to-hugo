from preprocess import preprocess_file
from process import process_content

import glob
import os


if __name__ == "__main__":
    jekyll_url = "https://seanny123.github.io/articles/"
    import_dir = os.path.join("medium-export")
    export_dir = os.path.join("")

    # make folders in export dir
    for folder in ("_drafts", "_posts", os.path.join("assets", "img"), "replies", "tmp-download"):
        os.makedirs(os.path.join(export_dir, folder), exist_ok=True)

    all_paths = []
    all_headout = []
    all_output = []
    all_cont_args = []

    # TODO: run this in parallel
    all_files = sorted(glob.glob(os.path.join(import_dir, "*.html")))
    for file_name in all_files[-10:-9]:
        print("Preprocessing: ", file_name)
        path, head_out, cont_args, header = preprocess_file(file_name)
        all_headout.append(head_out)
        all_cont_args.append(cont_args)
        all_paths.append(path)

    for cont_args in all_cont_args:
        print("Processing: ", cont_args[1])
        post_output = process_content(cont_args[0], cont_args[1], all_paths, jekyll_url)

        assert len(post_output) > 0

        all_output.append(post_output)

    for new_path, head, output_lines in zip(all_paths, all_headout, all_output):
        with open(os.path.join(export_dir, new_path), "w") as fi:
            fi.write("".join(head))
            fi.write("".join(output_lines))
