def file_rename(directory, extension, serials):
    """Renames a batch of photos in a folder via incremental serial numbers
    per a certain file extension.
    
    PARAMETERS:
    directory = folder location of photos to rename
    extension = file extension of photos to rename
    serials = text file containing the starting serial number to increment
    
    USAGE:
    file_rename('/home/photos', '.JPG', 'Serials.txt')
    """

    import os
    os.chdir(directory)

    with open(serials, 'r') as file:
        serial = int(file.read())

    for root, dirs, files in os.walk(directory):
        for photo in files:
            if photo.endswith(extension):
                serial += 1
                text = str(serial)
                os.rename(photo, f'{serial}{extension}')
                with open(serials, 'w') as file:
                    file.write(text)
