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
from PIL import Image, ImageOps

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


def load_surface(image_path: Path, screen_size):
    with Image.open(image_path) as img:
        img = ImageOps.exif_transpose(img)
        img = img.convert("RGB")
        img.thumbnail(screen_size, Image.LANCZOS)

        surface = pygame.image.fromstring(
            img.tobytes(), img.size, img.mode
        ).convert()

    return surface


def run_viewer(images_root: Path, images: List[Path], output_dir: Path, start_index: int):
    pygame.init()
    pygame.display.set_caption("Image Picker")

    screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    index = start_index
    needs_redraw = True

    current_surface = None
    next_surface = None
    next_index = None
    prev_surface = None
    prev_index = None
    preload_thread = None

    # Font for image counter overlay
    font_size = 36  # visible but not intrusive
    counter_font = pygame.font.SysFont("DejaVu Sans", font_size, bold=True)

    def preload_surface(target_index):
        nonlocal next_surface, next_index, prev_surface, prev_index

        if target_index < 0 or target_index >= len(images):
            return

        try:
            surface = load_surface(images[target_index], screen.get_size())

            if target_index == index + 1:
                next_surface = surface
                next_index = target_index

            elif target_index == index - 1:
                prev_surface = surface
                prev_index = target_index

        except Exception:
            pass

    def draw_image_counter(surface, index, total):
        text = f"{index + 1} / {total}"
        text_surface = counter_font.render(text, True, (255, 255, 255))

        padding = 12
        bg_rect = text_surface.get_rect()
        bg_rect.topright = (
            surface.get_width() - padding,
            padding
        )

        # Semi-transparent background for readability
        overlay_bg = pygame.Surface(
            (bg_rect.width + 16, bg_rect.height + 10),
            pygame.SRCALPHA
        )
        overlay_bg.fill((0, 0, 0, 140))  # black with transparency

        surface.blit(
            overlay_bg,
            (bg_rect.left - 8, bg_rect.top - 5)
        )
        surface.blit(text_surface, bg_rect)


    while True:
        if needs_redraw:
            screen.fill(WINDOW_BG_COLOR)

            # Use preloaded image if available
            if current_surface is None:
                current_surface = load_surface(images[index], screen.get_size())

                # Preload neighbors once
                if index + 1 < len(images):
                    threading.Thread(
                        target=preload_surface,
                        args=(index + 1,),
                        daemon=True
                    ).start()

                if index - 1 >= 0:
                    threading.Thread(
                        target=preload_surface,
                        args=(index - 1,),
                        daemon=True
                    ).start()

            rect = current_surface.get_rect(center=screen.get_rect().center)
            screen.blit(current_surface, rect)
            draw_image_counter(screen, index, len(images))
            pygame.display.flip()

            needs_redraw = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit(0)

                elif event.key == pygame.K_RIGHT:
                    if index < len(images) - 1:
                        index += 1

                        # SHIFT WINDOW
                        prev_surface = current_surface
                        prev_index = index - 1

                        # Promote preloaded image if it matches
                        if next_surface is not None and next_index == index:
                            current_surface = next_surface
                        else:
                            current_surface = load_surface(images[index], screen.get_size())

                        # Clear old preload
                        next_surface = None
                        next_index = None

                        # PRELOAD NEW NEXT
                        if index + 1 < len(images):
                            threading.Thread(
                                target=preload_surface,
                                args=(index + 1,),
                                daemon=True
                            ).start()

                        needs_redraw = True
                        save_state({
                            "images_root": str(images_root),
                            "output_dir": str(output_dir),
                            "current_index": index,
                            "total_images": len(images)
                        })

                elif event.key == pygame.K_LEFT:
                    if index > 0:
                        index -= 1

                        # SHIFT WINDOW
                        next_surface = current_surface
                        next_index = index + 1

                        if prev_surface is not None and prev_index == index:
                            current_surface = prev_surface
                        else:
                            current_surface = load_surface(images[index], screen.get_size())

                        prev_surface = None
                        prev_index = None

                        # PRELOAD NEW PREVIOUS
                        if index - 1 >= 0:
                            threading.Thread(
                                target=preload_surface,
                                args=(index - 1,),
                                daemon=True
                            ).start()

                        needs_redraw = True
                        save_state({
                            "images_root": str(images_root),
                            "output_dir": str(output_dir),
                            "current_index": index,
                            "total_images": len(images)
                        })

                elif event.key == pygame.K_RETURN:
                    img_path = images[index]
                    print("Picking image:",img_path)
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

    run_viewer(images_dir, images, output_dir, 0)


def prompt_resume_operation(state: dict):
    images_dir = Path(state["images_root"])
    output_dir = Path(state["output_dir"])
    start_index = state["current_index"]

    images = scan_images(images_dir)
    run_viewer(images_dir, images, output_dir, start_index)


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
