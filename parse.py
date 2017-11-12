from preprocess import preprocess_file
from process import process_content
from config import export_dir, import_dir

import glob
import os


if __name__ == "__main__":

    # make folders in export dir
    for folder in ("_drafts", "_posts", "img", "replies", "tmp-download"):
        os.makedirs(os.path.join(export_dir, folder), exist_ok=True)

    all_paths = []
    all_headout = []
    all_post_output = []
    all_cont_args = []

    # TODO: run this in parallel
    all_files = sorted(glob.glob(os.path.join(import_dir, "*.html")))
    for file_name in all_files:
        print("Preprocessing: ", file_name)
        path, head_out, cont_args, header = preprocess_file(file_name)
        all_headout.append(head_out)
        all_cont_args.append(cont_args)
        all_paths.append(path)

    # TODO: run this in parallel
    for cont_args in all_cont_args:
        all_output = []
        print("Processing: ", cont_args[1])
        content_sections = cont_args[0].findAll("div", {"class": "section-content"})

        # iterate through each explicitly divided section
        for c_i, content_section in enumerate(content_sections):
            if c_i > 0:
                all_output.append("---\n\n")
            all_content = content_section.div.children
            post_output = process_content(all_content, cont_args[1], all_paths)
            assert len(post_output) > 0
            all_output.extend(post_output)

        all_post_output.append(all_output)

    for new_path, head, output_lines in zip(all_paths, all_headout, all_post_output):
        with open(os.path.join(export_dir, new_path), "w") as fi:
            fi.write("".join(head))
            fi.write("".join(output_lines))
