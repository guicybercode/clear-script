#!/usr/bin/env python3

import time
import subprocess
import os
import shutil
from pathlib import Path

SCREENSHOTS_DIR = "screenshots"
EXAMPLES_DIR = "examples"

def setup_directories():
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    os.makedirs(EXAMPLES_DIR, exist_ok=True)
    print(f"Created directories: {SCREENSHOTS_DIR} and {EXAMPLES_DIR}")

def start_flask_server():
    print("Starting Flask server in background...")
    process = subprocess.Popen(
        ["python", "app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid if hasattr(os, 'setsid') else None
    )
    time.sleep(5)
    return process

def take_screenshots_with_playwright():
    try:
        from playwright.sync_api import sync_playwright
        
        print("Taking screenshots with Playwright...")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={'width': 1200, 'height': 800})
            
            page.goto('http://localhost:5000')
            time.sleep(2)
            
            window_element = page.locator('.window')
            window_element.screenshot(path=f'{SCREENSHOTS_DIR}/main-interface.png')
            print("✓ Screenshot: main-interface.png")
            
            page.screenshot(path=f'{SCREENSHOTS_DIR}/full-page.png', full_page=True)
            print("✓ Screenshot: full-page.png")
            
            title_bar = page.locator('.title-bar')
            title_bar.screenshot(path=f'{SCREENSHOTS_DIR}/title-bar.png')
            print("✓ Screenshot: title-bar.png")
            
            browser.close()
            return True
    except ImportError:
        print("Playwright not installed. Install with: pip install playwright && playwright install chromium")
        return False
    except Exception as e:
        print(f"Error taking screenshots: {e}")
        return False

def create_example_images():
    print("\nCreating example images from processed files...")
    
    sem_fundo_dir = Path("sem_fundo")
    originais_dir = Path("originais")
    
    if not sem_fundo_dir.exists():
        print("No 'sem_fundo' directory found. Skipping example images.")
        return
    
    image_files = list(sem_fundo_dir.glob("*.png"))[:2]
    
    if not image_files:
        print("No processed images found. Skipping example images.")
        return
    
    for i, processed_file in enumerate(image_files, 1):
        filename = processed_file.name
        
        processed_path = sem_fundo_dir / filename
        original_path = originais_dir / filename
        
        if processed_path.exists():
            shutil.copy2(processed_path, f"{EXAMPLES_DIR}/example{i}-after.png")
            print(f"✓ Created: example{i}-after.png")
        
        if original_path.exists():
            shutil.copy2(original_path, f"{EXAMPLES_DIR}/example{i}-before.png")
            print(f"✓ Created: example{i}-before.png")
        else:
            print(f"⚠ Original not found for {filename}, using processed as before")
            if processed_path.exists():
                shutil.copy2(processed_path, f"{EXAMPLES_DIR}/example{i}-before.png")

def create_placeholder_images():
    print("\nCreating placeholder images...")
    
    from PIL import Image, ImageDraw, ImageFont
    
    try:
        screenshots = [
            ("main-interface.png", 1200, 600),
            ("preview.png", 1200, 400),
            ("progress.png", 1200, 200)
        ]
        
        for filename, width, height in screenshots:
            img = Image.new('RGB', (width, height), color='#C0C0C0')
            draw = ImageDraw.Draw(img)
            
            text = filename.replace('.png', '').replace('-', ' ').title()
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
            except:
                font = ImageFont.load_default()
            
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            position = ((width - text_width) // 2, (height - text_height) // 2)
            
            draw.text(position, text, fill='#000000', font=font)
            img.save(f"{SCREENSHOTS_DIR}/{filename}")
            print(f"✓ Created placeholder: {filename}")
    except Exception as e:
        print(f"Error creating placeholders: {e}")

def main():
    print("=" * 50)
    print("Screenshot Generator for Background Remover")
    print("=" * 50)
    
    setup_directories()
    
    flask_process = None
    
    try:
        flask_process = start_flask_server()
        
        success = take_screenshots_with_playwright()
        
        if not success:
            print("\nFalling back to placeholder images...")
            create_placeholder_images()
        
        create_example_images()
        
        print("\n" + "=" * 50)
        print("Screenshot generation completed!")
        print(f"Check the '{SCREENSHOTS_DIR}' and '{EXAMPLES_DIR}' directories.")
        print("=" * 50)
        
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if flask_process:
            try:
                if hasattr(os, 'setsid'):
                    os.killpg(os.getpgid(flask_process.pid), 15)
                else:
                    flask_process.terminate()
                flask_process.wait(timeout=5)
            except:
                flask_process.kill()
            print("Flask server stopped.")

if __name__ == "__main__":
    main()
