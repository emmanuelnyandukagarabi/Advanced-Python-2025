# Written by ahmed khalil ahmed.khalil@areasciencepark.it
#
import os
import sys

# Import SEM processing classes: metadata extractor, cleaner, and visualizer
from semmeta import SEMMeta, CLEANER, SEMVisualizer

# Define the main function of the script
def main():
    # Ensure the user provides an image path as a command-line argument
    if len(sys.argv) < 2:
        raise SystemExit(f"usage: {sys.argv[0]} <SEM image path>")

    # Get the SEM image path from command-line arguments
    semimage = sys.argv[1]

    # Extract the image name (without extension) for output naming
    image_name = os.path.splitext(os.path.basename(semimage))[0]

    # Create the output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)

    # Check if the file exists and has a supported SEM extension
    if os.path.isfile(semimage) and semimage.endswith(SEMMeta.semext):
        print(f"\nProcessing SEM IMAGE:", semimage)

        # Attempt to open and validate the SEM image
        img = SEMMeta.OpenCheckImage(semimage)

        if img:
            print("Good image for processing", semimage)

            # Extract raw EXIF metadata and tag identifiers
            image_metadata, image_tags = SEMMeta.ImageMetadata(img)
            exif_keys, exif_number = SEMMeta.SEMEXIF
            found_exif_metadata, none_exif_metadata = SEMMeta.GetExifMetadata(img, exif_keys, exif_number)

            # Merge found and missing EXIF metadata into a dictionary
            allexif_metadict = SEMMeta.ExifMetaDict(found_exif_metadata, none_exif_metadata)

            # Extract instrument-specific metadata (e.g., from filename or headers)
            instrument_metadata = SEMMeta.GetInsMetadata
            instrument_meta_dict = SEMMeta.InsMetaDict(instrument_metadata)

            # Merge EXIF and instrument metadata into a single dictionary
            SEM_FULLMD_Dict = {**allexif_metadict, **instrument_meta_dict}

            # Define output paths for raw and cleaned metadata JSON files
            output_path_raw = os.path.join("output", f"{image_name}_raw.json")
            output_path_cleaned = os.path.join("output", f"{image_name}_cleaned.json")

            # Save raw metadata to JSON
            SEMMeta.WriteSEMJson(output_path_raw, SEM_FULLMD_Dict)

            # Clean the raw metadata and save the cleaned version
            cleaned_data = CLEANER.process(output_path_raw)
            CLEANER.save_cleaned(output_path_cleaned)

            # Visualize the SEM image alongside its cleaned metadata table
            visualizer = SEMVisualizer(json_path=output_path_cleaned, image_path=semimage)
            visualizer.show_image_with_table()

        else:
            # Handle case where image could not be opened or validated
            print("Bad image for processing", semimage)
    else:
        # Handle case where file is missing or has an unsupported extension
        print("Invalid image path or unsupported format:", semimage)

# Run the main function only if this script is executed directly (not imported)
if __name__ == "__main__":
    main()
