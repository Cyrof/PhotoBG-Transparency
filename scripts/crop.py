from PIL import Image
import os 
from pathlib import Path
from tqdm import tqdm
import numpy as np 
from concurrent.futures import ThreadPoolExecutor


class Crop: 
    def __init__(self):
        """
        Initialise the Crop class
        
        Attributes: 
        - path (Path): The root directory of the project. 
        - img_path (Path): The directory containing the images to be processed.
        - output_path (Path): The directory where processed images will be saved.
        - images (list): A list to store image file paths to be processed.
        """
        self.path = Path(__file__).parent.absolute().parent.absolute() # Set the root path of the project 
        self.img_path = Path.joinpath(self.path, "images/") # Set the path to the images directory 
        self.output_path = Path.joinpath(self.path, "t_images/") # Set the path to the output directory
        self.images = None # Initialise images as None
    
    def load_images(self):
        """
        Load all iamges from the img_path directory and store their paths in the images attribute.

        This method searches recursively within the img_path directory for all files and stores their paths in the im ages list.
        """
        self.images = [file for file in self.img_path.glob('**/*')]


    def process_image(self, img_path, threshold=200):
        """
        Process a single image by making its background transparent based on the specified threshold.

        Parameters: 
        - img_path (str): The path to the image to be processed.
        - threshold (int): The RGB value above which the background is considered to be "white" and will be made transparent. Default is 200.

        This method converts the image to RGBA mode, creates a mask for pixels above the threshold, 
        applies the mask to make thos pixels transparent, and saves the processed image to the output directory.
        """
        im = Image.open(img_path).convert("RGBA") # open the image and convert it to RGBA mode
        data = np.array(im) # convert image data to a NumPy array

        # create mask for pixels above threshold
        r, g, b, a = data[:, :, 0], data[:, :, 1], data[:, :, 2], data[:, :, 3]
        # create a mask where the RGB values are above the threshold (considered as background)
        mask = (r > threshold) & (g > threshold) & (b > threshold)

        # Apply mask to make pixels transparent
        data[mask] = [255, 255, 255, 0]

        # save the processed image
        result_img = Image.fromarray(data, "RGBA")
        # result_img.save(str(Path(img_path).parent / f'trimmed_{Path(img_path).name}.png'))
        result_img.save(self.output_path / f'transparent_{Path(img_path).stem + '.png'}')
    

    def make_transparent(self, threshold=200):
        """
        process all images in the images list to make their backgrounds transparent.

        Parameters: 
        - threshold (int): The RGB value above which the background is considered to be "white"
                           and will be made transparent. Default is 200.

        This method uses a ThreadPoolExecutor to process images concurrently, speeding up 
        the operation for large batches of images. Progress is displayed using a tqdm progress bar. 
        """
        with ThreadPoolExecutor() as executor: 
            # use a threadPoolExecutor to process images concurrently
            list(tqdm(
                executor.map(lambda img: self.process_image(img, threshold), self.images), 
                desc="Making background transparent", # Description for the progress bar 
                total=len(self.images) # total number of images to process
            ))