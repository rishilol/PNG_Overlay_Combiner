from PIL import Image
import numpy as np
import os
import traceback

def combine_images(image1_path, image2_path, output_dir="output"):
    """
    Combines two images using different methods and saves the results.
    
    Args:
        image1_path: Path to the first image
        image2_path: Path to the second image
        output_dir: Directory to save the output images
    """
    try:
        print(f"\nStarting image combination process:")
        print(f"Image 1: {image1_path}")
        print(f"Image 2: {image2_path}")
        print(f"Output directory: {output_dir}")
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Verify input files exist
        if not os.path.exists(image1_path):
            raise ValueError(f"Image 1 not found at: {image1_path}")
        if not os.path.exists(image2_path):
            raise ValueError(f"Image 2 not found at: {image2_path}")
            
        print("Opening images...")
        # Open and convert images to RGB
        img1 = Image.open(image1_path).convert('RGB')
        img2 = Image.open(image2_path).convert('RGB')
        
        print(f"Image 1 size: {img1.size}")
        print(f"Image 2 size: {img2.size}")
        
        # Resize second image to match first image if needed
        if img1.size != img2.size:
            print(f"Resizing image 2 to match image 1 size: {img1.size}")
            img2 = img2.resize(img1.size, Image.Resampling.LANCZOS)
        
        # Convert to numpy arrays
        arr1 = np.array(img1)
        arr2 = np.array(img2)
        
        print(f"Array 1 shape: {arr1.shape}")
        print(f"Array 2 shape: {arr2.shape}")
        
        # Ensure arrays are uint8
        arr1 = arr1.astype(np.uint8)
        arr2 = arr2.astype(np.uint8)
        
        operations = {
            'xor': lambda a, b: np.bitwise_xor(a, b),
            'add': lambda a, b: np.clip(a + b, 0, 255).astype(np.uint8),
            'sub': lambda a, b: np.abs(a.astype(int) - b.astype(int)).astype(np.uint8),
            'avg': lambda a, b: ((a.astype(int) + b.astype(int)) // 2).astype(np.uint8),
            'max': np.maximum,
            'min': np.minimum,
            'and': np.bitwise_and,
            'or': np.bitwise_or
        }
        
        # Process each operation
        for op_name, op_func in operations.items():
            print(f"Processing {op_name} operation...")
            try:
                result = op_func(arr1, arr2)
                output_path = os.path.join(output_dir, f"{op_name}_result.png")
                Image.fromarray(result).save(output_path)
                print(f"Saved {op_name} result to: {output_path}")
            except Exception as e:
                print(f"Error in {op_name} operation: {str(e)}")
                raise
        
        print("All operations completed successfully")
        return True
        
    except Exception as e:
        print("\nError in combine_images:")
        print(traceback.format_exc())
        raise ValueError(f"Error processing images: {str(e)}")

if __name__ == "__main__":
    # Test the function
    image1_path = "1.png"
    image2_path = "2.png"
    
    try:
        combine_images(image1_path, image2_path)
        print("Done! Check the output directory for results.")
    except Exception as e:
        print(f"Error: {str(e)}")