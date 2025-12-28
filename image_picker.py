#!/usr/bin/env python3
"""
Image Shortlisting Tool
Python 3.12 compatible
"""

import os
import sys
import json
import shutil
import threading
from pathlib import Path
from typing import List

import pygame
from PIL import Image


STATE_FILE = "shortlist_state.json"
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
WINDOW_BG_COLOR = (30, 30, 30)


def scan_images(root_dir: Path) -> List[Path]:
    images = []
    for path in sorted(root_dir.rglob("*")):
        if path.suffix.lower() in SUPPORTED_EXTENSIONS:
            images.append(path)
    return images


def load_state() -> dict | None:
    if Path(STATE_FILE).exists():
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def save_state(state: dict) -> None:
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def copy_image_async(src: Path, dst_dir: Path) -> None:
    def worker():
        dst_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst_dir / src.name)

    threading.Thread(target=worker, daemon=True).start()


def fit_image_to_screen(image: Image.Image, screen_size):
    image.thumbnail(screen_size, Image.LANCZOS)
    return image


def run_viewer(images: List[Path], output_dir: Path, start_index: int):
    pygame.init()
    pygame.display.set_caption("Image Picker")

    screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    index = start_index

    while True:
        screen.fill(WINDOW_BG_COLOR)

        img_path = images[index]
        pil_img = Image.open(img_path).convert("RGB")
        pil_img = fit_image_to_screen(pil_img, screen.get_size())
        img_surface = pygame.image.fromstring(
            pil_img.tobytes(), pil_img.size, pil_img.mode
        )

        rect = img_surface.get_rect(center=screen.get_rect().center)
        screen.blit(img_surface, rect)

        pygame.display.flip()

        save_state({
            "images_root": str(images[0].parents[len(images[0].parents) - 1]),
            "output_dir": str(output_dir),
            "current_index": index,
            "total_images": len(images)
        })

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit(0)

                elif event.key == pygame.K_RIGHT:
                    index = min(index + 1, len(images) - 1)

                elif event.key == pygame.K_LEFT:
                    index = max(index - 1, 0)

                elif event.key == pygame.K_RETURN:
                    copy_image_async(img_path, output_dir)

        clock.tick(60)


def prompt_new_operation():
    images_dir = Path(input("Enter path to images directory: ").strip()).expanduser()
    output_dir = Path(input("Enter path to shortlist output directory: ").strip()).expanduser()

    if not images_dir.exists():
        print("❌ Images directory does not exist.")
        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)

    images = scan_images(images_dir)
    if not images:
        print("❌ No images found.")
        sys.exit(1)

    save_state({
        "images_root": str(images_dir),
        "output_dir": str(output_dir),
        "current_index": 0,
        "total_images": len(images)
    })

    run_viewer(images, output_dir, 0)


def prompt_resume_operation(state: dict):
    images_dir = Path(state["images_root"])
    output_dir = Path(state["output_dir"])
    start_index = state["current_index"]

    images = scan_images(images_dir)
    run_viewer(images, output_dir, start_index)


def main():
    print("\n=== Image Shortlisting Tool ===\n")
    state = load_state()

    if state:
        print("1. Resume last operation")
        print("2. Start new operation")
        choice = input("Select option (1/2): ").strip()

        if choice == "1":
            prompt_resume_operation(state)
        elif choice == "2":
            prompt_new_operation()
        else:
            print("Invalid choice.")
    else:
        prompt_new_operation()


if __name__ == "__main__":
    main()
