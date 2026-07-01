#!/usr/bin/env python3
"""
Image Extraction Tool
Python 3.12 compatible
Cross-platform: Ubuntu + Windows
"""

from __future__ import annotations

import os
import re
import zipfile
from pathlib import Path
from tkinter import (
    Frame,
    Tk,
    Toplevel,
    filedialog,
    messagebox,
    Text,
    Scrollbar,
    Button,
    Label,
    Entry,
    StringVar,
    BOTH,
    RIGHT,
    LEFT,
    Y,
    END,
)

# ============================================================
# CONFIG
# ============================================================

DELETE_ARCHIVE_AFTER_EXTRACTION = True

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".bmp",
    ".gif",
    ".tiff",
}

# ============================================================
# GUI HELPERS
# ============================================================


def create_root() -> Tk:
    """
    Create hidden Tk root.
    """
    root = Tk()
    root.withdraw()
    return root


def get_home_directory() -> Path:
    """
    Cross-platform home directory.
    """
    return Path.home()


def select_first_archive() -> Path | None:
    """
    Open native file explorer for archive selection.
    """

    root = create_root()

    file_path = filedialog.askopenfilename(
        title="Select Archive File",
        initialdir=get_home_directory(),
        filetypes=[("ZIP files", "*.zip")],
    )

    root.destroy()

    if not file_path:
        return None

    return Path(file_path)


def select_output_parent() -> Path | None:
    """
    Select output parent folder.
    """

    root = create_root()

    folder = filedialog.askdirectory(
        title="Select Parent Output Folder",
        initialdir=get_home_directory(),
        mustexist=True,
    )

    root.destroy()

    if not folder:
        return None

    return Path(folder)


def show_archive_selection_window(
    archives: list[Path],
) -> None:
    """
    Large resizable archive preview window.
    """

    root = Tk()

    root.title("Selected Archives")

    window_height = min(
        700,
        max(360, len(archives) * 22),
    )

    root.geometry(f"760x{window_height}")

    # Allow proper resizing behavior
    root.rowconfigure(1, weight=1)
    root.columnconfigure(0, weight=1)

    # ========================================================
    # HEADER
    # ========================================================

    header_label = Label(
        root,
        text=f"Selected {len(archives)} archives",
        font=("Arial", 14, "bold"),
    )

    header_label.grid(
        row=0,
        column=0,
        pady=10,
        sticky="ew",
    )

    # ========================================================
    # TEXT AREA CONTAINER
    # ========================================================

    text_container = Frame(root)

    text_container.grid(
        row=1,
        column=0,
        padx=10,
        pady=5,
        sticky="nsew",
    )

    text_container.rowconfigure(0, weight=1)
    text_container.columnconfigure(0, weight=1)

    # ========================================================
    # TEXT AREA
    # ========================================================

    text_frame = Text(
        text_container,
        wrap="none",
        font=("Consolas", 10),
    )

    text_frame.grid(
        row=0,
        column=0,
        sticky="nsew",
    )

    scrollbar = Scrollbar(
        text_container,
        command=text_frame.yview,
    )

    scrollbar.grid(
        row=0,
        column=1,
        sticky="ns",
    )

    text_frame.configure(
        yscrollcommand=scrollbar.set
    )

    for archive in archives:

        text_frame.insert(
            END,
            f"{archive}\n",
        )

    text_frame.config(state="disabled")

    # ========================================================
    # BUTTON AREA
    # ========================================================

    button_frame = Frame(root)

    button_frame.grid(
        row=2,
        column=0,
        pady=10,
        sticky="ew",
    )

    continue_button = Button(
        button_frame,
        text="Continue",
        command=root.destroy,
        height=2,
        width=20,
    )

    continue_button.pack()

    root.mainloop()


def confirm_final_output_path(
    detected_path: Path,
) -> Path | None:
    """
    Editable confirmation dialog for final output path.
    """

    root = Tk()
    root.title("Confirm Final Extraction Path")
    root.geometry("720x150")

    Label(
        root,
        text="Confirm or Edit Final Extraction Path:",
        font=("Arial", 12, "bold"),
    ).pack(pady=10)

    path_var = StringVar(value=str(detected_path))

    entry = Entry(
        root,
        textvariable=path_var,
        width=95,
        font=("Consolas", 10),
    )

    entry.pack(padx=20, pady=10)

    result = {"path": None}

    def confirm() -> None:
        result["path"] = Path(path_var.get())
        root.destroy()

    Button(
        root,
        text="Start Extraction",
        command=confirm,
        height=2,
        width=20,
    ).pack(pady=20)

    root.mainloop()

    return result["path"]


# ============================================================
# ARCHIVE HELPERS
# ============================================================
def split_zip_path(path: str) -> list[str]:
    """
    ZIP archives always use forward slashes internally.

    This function normalizes ZIP paths safely
    across Windows and Linux.
    """

    normalized = path.replace("\\", "/")

    return [
        part
        for part in normalized.split("/")
        if part
    ]


def find_related_archives(
    selected_archive: Path,
) -> list[Path]:
    """
    Detect matching archives.

    Example:
        Wedding - 0001.zip
        Wedding - 0002.zip
    """

    match = re.match(
        r"^(.*?)(\d+)\.zip$",
        selected_archive.name,
    )

    if not match:
        return [selected_archive]

    prefix = match.group(1)

    archives = sorted(
        selected_archive.parent.glob(
            f"{prefix}*.zip"
        )
    )

    return archives


def detect_main_folder_name(
    archive_path: Path,
) -> str:
    """
    Detect actual image parent folder.

    ZIP paths always use forward slashes internally,
    regardless of operating system.
    """

    with zipfile.ZipFile(archive_path) as zip_file:

        for member in zip_file.infolist():

            parts = split_zip_path(member.filename)

            extension = os.path.splitext(
                member.filename
            )[1].lower()

            if extension in IMAGE_EXTENSIONS:

                # Wrapper/Wedding/image.jpg
                if len(parts) >= 3:
                    return parts[1]

                # Wedding/image.jpg
                if len(parts) >= 2:
                    return parts[0]

    return "Extracted_Images"


def extract_images(
    archive_path: Path,
    output_folder: Path,
) -> int:
    """
    Extract image files directly into final folder.
    """

    image_count = 0

    with zipfile.ZipFile(archive_path) as zip_file:

        members = zip_file.infolist()

        image_members = []

        for member in members:

            extension = os.path.splitext(
                member.filename
            )[1].lower()

            if extension in IMAGE_EXTENSIONS:
                image_members.append(member)

        print(
            f"\nCurrent archive: {archive_path}"
        )

        print(
            f"Extracting "
            f"{len(image_members)} total images "
            f"to:\n{output_folder}"
        )

        for member in image_members:

            parts = split_zip_path(member.filename)

            # Remove top wrapper folder
            #
            # Example:
            # Wrapper/Wedding/Album/image.jpg
            #
            # becomes:
            # Wedding/Album/image.jpg

            if len(parts) >= 2:
                relative_parts = parts[1:]
            else:
                relative_parts = parts

            relative_path = os.path.join(
                *relative_parts
            )

            destination = os.path.join(
                output_folder,
                relative_path,
            )

            destination_parent = os.path.dirname(
                destination
            )

            os.makedirs(
                destination_parent,
                exist_ok=True,
            )

            # Handle duplicate filenames

            counter = 1

            original_destination = destination

            while os.path.exists(destination):

                filename = os.path.basename(
                    original_destination
                )

                stem, extension = os.path.splitext(
                    filename
                )

                destination = os.path.join(
                    destination_parent,
                    f"{stem}_{counter}"
                    f"{extension}",
                )

                counter += 1

            with zip_file.open(member) as source:
                with open(destination, "wb") as target:
                    target.write(source.read())

            image_count += 1

    return image_count


# ============================================================
# MAIN
# ============================================================


def main() -> None:

    first_archive = select_first_archive()

    if not first_archive:
        print("No archive selected.")
        return

    archives = find_related_archives(
        first_archive
    )

    show_archive_selection_window(
        archives
    )

    output_parent = select_output_parent()

    print("output parent:",output_parent)

    if not output_parent:
        print("No output folder selected.")
        return

    main_folder_name = detect_main_folder_name(
        archives[0]
    )

    print("main folder name:",main_folder_name)

    detected_output = os.path.join(output_parent, main_folder_name)

    print("detected_output:",detected_output)

    final_output_folder = (
        confirm_final_output_path(
            detected_output
        )
    )

    if not final_output_folder:
        print("Extraction cancelled.")
        return

    os.makedirs(final_output_folder, exist_ok=True)

    total_images = 0

    for archive in archives:

        try:

            extracted = extract_images(
                archive,
                final_output_folder,
            )

            total_images += extracted

            if (
                DELETE_ARCHIVE_AFTER_EXTRACTION
            ):
                os.remove(archive)

                print(
                    f"Deleted archive:\n"
                    f"{archive}"
                )

        except Exception as error:

            print(
                f"\nERROR processing:\n"
                f"{archive}\n"
                f"{error}"
            )

    print("\n===================================")
    print("Extraction Complete")
    print(
        f"Total Images Extracted: "
        f"{total_images}"
    )
    print(
        f"Final Output Folder:\n"
        f"{final_output_folder}"
    )
    print("===================================")

    root = create_root()

    messagebox.showinfo(
        "Extraction Complete",
        f"Successfully extracted "
        f"{total_images} images.\n\n"
        f"Output Folder:\n"
        f"{final_output_folder}",
    )

    root.destroy()


if __name__ == "__main__":
    main()