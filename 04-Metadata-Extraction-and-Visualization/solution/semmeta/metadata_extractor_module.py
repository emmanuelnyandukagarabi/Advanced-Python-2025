# Written by ahmed khalil ahmed.khalil@areasciencepark.it
#
# Import modules for file system operations (os) and command-line argument handling/system access (sys)
import os, sys

# Import plotting, numerical, and image processing libraries
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ExifTags  # Image processing and metadata handling

# Import JSON module for reading and writing metadata
import json


# SEMMetaData Class Initialization
class SEMMetaData:
    def __init__(self, image_metadata={}, semext=('tif', 'TIF'), semInsTag=[34118]):
        # Store accepted SEM image file extensions
        self.semext = semext 
        
        # Initialize dictionary to hold extracted image metadata
        self.image_metadata = image_metadata
        
        # Store SEM-specific EXIF tag identifiers (e.g., 34118 for instrument metadata)
        self.semInsTag = semInsTag
        
        # Initialize array to hold image tag identifiers
        self.image_tags = np.array([], dtype='int')


    def OpenCheckImage(self, image):
        """
        Opens an image file and verifies its accessibility and format.
        Returns the opened image object if successful,
        """
        # Check if image has a supported extension
        if image.endswith(self.semext):
            try:
                # Attempt to open the image using PIL
                img = Image.open(image)
                return img
            except IOError:
                # Print error if image cannot be opened
                print('[ERROR]', image)
                return False


    def ImageMetadata(self, img):
        """
        Extracts raw metadata and tag identifiers including 34118 
        from a SEM image.
        """
        # Extract raw tag dictionary from image
        self.image_metadata = img.tag
        
        # Convert tag keys to NumPy array for fast lookup
        self.image_tags = np.array(self.image_metadata) 
        
        # Return both raw metadata and tag identifiers
        return self.image_metadata, self.image_tags
        

    @property    
    def SEMEXIF(self):
        """
        Provides access to standard EXIF tag mappings from PIL.
        
        Returns:
            - exif_keys (list): Human-readable EXIF tag names
            - exif_number (list): Corresponding numeric tag identifiers used in image metadata.
        """
        # Reverse the PIL EXIF tag dictionary to map names to numeric keys
        exif_dict = {k: v for v, k in ExifTags.TAGS.items()}
        
        # Extract all tag names (keys) from the reversed dictionary
        exif_keys = [key for key in exif_dict]
        
        # Extract corresponding numeric identifiers for each tag name
        exif_number = [exif_dict[k] for k in exif_keys]
        
        # Return both tag names and their numeric codes
        return exif_keys, exif_number 
        

    # Extract Standard EXIF Metadata from SEM Image
    def GetExifMetadata(self, img, exif_keys, exif_number):
        """
        Extracts standard EXIF metadata from a SEM image.
        """
        # Extract available EXIF metadata from image using known tag numbers
        found_exif_metadata = [(img.tag[idx][:], word) for idx, word in zip(exif_number, exif_keys) if idx in self.image_tags]
        
        # Mark EXIF fields not found in the image with None
        none_exif_metadata = [(word, None) for num, word in zip(exif_number, exif_keys) if num not in self.image_tags] 
        
        # Return both found and missing metadata
        return found_exif_metadata, none_exif_metadata


    # Construct Unified EXIF Metadata Dictionary
    def ExifMetaDict(self, found_exif_metadata, none_exif_metadata):
        """
        Creates a unified dictionary from found and missing EXIF metadata entries.
        Returns:
            - dict: Combined dictionary of EXIF metadata, excluding 'ColorMap' entries.         
        """ 
        # Convert found metadata to dictionary, skipping 'ColorMap'
        found_metadict = dict((subl[1], subl[0][0]) for subl in found_exif_metadata if subl[1] != "ColorMap")
        
        # Convert missing metadata to dictionary with None values, skipping 'ColorMap'
        none_metadict = dict((subl[0], subl[1]) for subl in none_exif_metadata if subl[0] != "ColorMap")
        
        # Merge found and missing metadata into one dictionary
        allexif_metadict = {**found_metadict, **none_metadict}
        
        # Return the unified metadata dictionary
        return allexif_metadict 


    @property
    def GetInsMetadata(self):
        '''
        Extracts instrument-specific metadata from SEM image EXIF tag 34118.
        Returns:
            - list: a cleaned and escaped list of instrument metadata strings.
            - and an empty list if tag 34118 is not found.
        ''' 
        try:
            # Find the value associated with EXIF tag 34118
            pairs = [params for tag, params in self.image_metadata.items() if tag == self.semInsTag[0]]
            
            # Unpack the first matching entry (instrument metadata)
            instrument_metadata, *_ = pairs[0]  

            # Clean the instrument metadata by skipping the first N lines
            random_size_tag = 35
            instrument_metadata = [instrument_metadata][0].split("\r\n")[random_size_tag:]          

        # Handle case where tag 34118 is not found
        except IndexError:
            instrument_metadata = []
        
        # Return cleaned instrument metadata or empty list
        return instrument_metadata


    # Parse Instrument Metadata from Tag 34118
    def InsMetaDict(self, list):
        """
        Converts a flat list of instrument metadata into a structured dictionary.
        Returns:
            - dict: of all the information contained in the 34118 tag  
            - and an empty dictionary if parsing fails.      
        """
        try:
            # Initialize key and value lists
            ins_keys, ins_values = [], []
            
            # Separate alternating entries into keys and values
            for idx, val in enumerate(list):
                if idx % 2 == 0:
                    ins_keys.append(val)
                else:
                    ins_values.append(val)

            # Combine keys and values into a dictionary
            instrument_meta_dict = {k: v for k, v in zip(ins_keys, ins_values)}
            
        # Handle parsing errors gracefully
        except Exception as e:            
            print("Error parsing instrument metadata:", str(e))
            instrument_meta_dict = {}
        
        # Return structured instrument metadata dictionary
        return instrument_meta_dict
        
        
    # Export SEM Metadata to JSON Format    
    def WriteSEMJson(self, file, semdict):   
        """
        Open the file in write mode and serialize the metadata dictionary
        """
        # Open output file and write metadata dictionary as JSON
        with open(file, "w") as semoutfile:
            json.dump(semdict, semoutfile)
        return   
