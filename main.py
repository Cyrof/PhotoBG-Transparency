from scripts.crop import Crop


def main():
    """
    main function to execute the image processing workflow. 

    This function creates an instance of the Crop class, loads all images from the images directory,
    and processes them to make their backgrounds transparent using the make_transparent method.
    """
    # create an instance of the Crop class
    crop = Crop()

    # Load images from the specified directory 
    crop.load_images()

    # Process the images to make their background transparent 
    crop.make_transparent()

if __name__ == "__main__":
    # execute the main function if this script is run as the main module
    main()
