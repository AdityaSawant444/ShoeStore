import os
import shutil
from pathlib import Path

def count_images_in_directory(directory):
    """Count images in a directory"""
    if not os.path.exists(directory):
        return 0
    
    image_extensions = ('.jpg', '.jpeg', '.png', '.webp', '.gif', '.avif')
    count = 0
    for file in os.listdir(directory):
        if file.lower().endswith(image_extensions):
            count += 1
    return count

def get_image_files(directory):
    """Get list of image files in a directory"""
    if not os.path.exists(directory):
        return []
    
    image_extensions = ('.jpg', '.jpeg', '.png', '.webp', '.gif', '.avif')
    image_files = []
    for file in os.listdir(directory):
        if file.lower().endswith(image_extensions):
            image_files.append(file)
    return image_files

def redistribute_images():
    """Redistribute images more evenly between categories"""
    
    # Base paths
    base_path = "static/images"
    categories = ["athletic", "casual", "formal"]
    
    print("Current Image Distribution:")
    print("=" * 50)
    
    # Count current images
    current_counts = {}
    for gender in ["men", "women"]:
        gender_path = os.path.join(base_path, gender)
        for category in categories:
            category_path = os.path.join(gender_path, category)
            count = count_images_in_directory(category_path)
            current_counts[f"{gender}_{category}"] = count
            print(f"{gender.title()} {category.title()}: {count} images")
    
    print("\n" + "=" * 50)
    
    # Calculate total images per gender
    men_total = sum(current_counts[f"men_{cat}"] for cat in categories)
    women_total = sum(current_counts[f"women_{cat}"] for cat in categories)
    
    print(f"Total Men's Images: {men_total}")
    print(f"Total Women's Images: {women_total}")
    
    # Calculate target distribution (divide evenly)
    men_target_per_category = men_total // 3
    women_target_per_category = women_total // 3
    
    print(f"\nTarget Distribution:")
    print(f"Men: {men_target_per_category} images per category")
    print(f"Women: {women_target_per_category} images per category")
    print("=" * 50)
    
    # Create backup directories
    backup_path = "static/images_backup"
    if not os.path.exists(backup_path):
        os.makedirs(backup_path)
    
    # Backup current structure
    print("Creating backup of current images...")
    if os.path.exists(base_path):
        shutil.copytree(base_path, os.path.join(backup_path, "original"), dirs_exist_ok=True)
    
    # Redistribute images
    for gender in ["men", "women"]:
        gender_path = os.path.join(base_path, gender)
        target_per_category = men_target_per_category if gender == "men" else women_target_per_category
        
        print(f"\nRedistributing {gender.title()}'s images:")
        
        # Collect all images for this gender
        all_images = []
        for category in categories:
            category_path = os.path.join(gender_path, category)
            if os.path.exists(category_path):
                image_files = get_image_files(category_path)
                for img_file in image_files:
                    all_images.append((category, img_file))
        
        print(f"Total {gender.title()}'s images: {len(all_images)}")
        
        # Create temporary directories for redistribution
        temp_dir = os.path.join(backup_path, f"{gender}_temp")
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)
        
        # Move all images to temp directory
        for category, img_file in all_images:
            source_path = os.path.join(gender_path, category, img_file)
            temp_path = os.path.join(temp_dir, img_file)
            if os.path.exists(source_path):
                shutil.move(source_path, temp_path)
        
        # Redistribute images evenly
        for i, img_file in enumerate(os.listdir(temp_dir)):
            target_category = categories[i % len(categories)]
            target_path = os.path.join(gender_path, target_category)
            
            # Move image to target category
            source_path = os.path.join(temp_dir, img_file)
            target_file_path = os.path.join(target_path, img_file)
            shutil.move(source_path, target_file_path)
        
        # Clean up temp directory
        shutil.rmtree(temp_dir)
        
        # Show new distribution
        print(f"\nNew {gender.title()}'s distribution:")
        for category in categories:
            category_path = os.path.join(gender_path, category)
            count = count_images_in_directory(category_path)
            print(f"  {category.title()}: {count} images")

if __name__ == "__main__":
    print("Better Image Redistribution Tool")
    print("=" * 50)
    print("This script will redistribute images more evenly between categories.")
    print("A backup will be created in 'static/images_backup/original'")
    
    response = input("\nDo you want to proceed? (y/n): ")
    if response.lower() == 'y':
        redistribute_images()
        print("\nRedistribution complete!")
        print("Backup saved in: static/images_backup/original")
    else:
        print("Operation cancelled.") 