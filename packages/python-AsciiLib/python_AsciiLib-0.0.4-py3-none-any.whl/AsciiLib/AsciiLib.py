'''
AsciiLib
by: Alexander J.

AsciiLib is a module for converting visual medias (jpg, png, mp4, etc.) into ascii art versions

Dependencies: os, numpy, pathlib, pillow, and cv2 (A.K.A OpenCV)
'''
# imports
import os, numpy, PIL, cv2
from PIL import Image as Pil_Image
from pathlib import Path
#global functions
def clear():
    print(chr(27)+'[2J')

#classes
class images:
    '''
    This class allows different types of ascii art of a given image's path.
    '''
   
    def __init__(self, image):
        self.image = image
    
    def img2ascii(self, char_list: list=[' ', '.', ':', '-', '=', '+', '*', '#', '%', '@']):
        '''
        A function for converting a given image into normal, uncolored ascii art with a customizable array of characters
        '''
        x, y = os.get_terminal_size()

        try:
            gray_image = Pil_Image.open(self.image).convert('L').resize((x-1,y))
        except FileNotFoundError:
            print('File does not exist.')
        array = numpy.array(gray_image)
        index_array = [[round((len(char_list)-1) * (j) / 255) for j in i] for i in array]
        gray_image.close()

        return ''.join([''.join([char_list[j] for j in i]) +'\n' for i in index_array])

class _videos:
    '''
    This class is dedicated to ascii art of a given video's path. It is recommended to *not* use this class as it is poorly designed and will likely take a very long time to run.
    '''

    def __init__(self, path, __file__):
        self.path = path
        self.dirpath = Path(__file__).parent.resolve()
    
    def frames2ascii(self, char_list: list=[' ', '.', ':', '-', '=', '+', '*', '#', '%', '@']):
        image_list = os.listdir(f'{self.dirpath}\\data')
        path = [f'{self.dirpath}\\data\\{i}' for i in image_list]
        clear()
        for i in path:
            term_size = os.get_terminal_size()
            image = Pil_Image.open(path).convert('L').resize((term_size[0]-2,term_size[1])) # Gets the image, converts to grayscale, then resizes the image to fit the terminal.
            array = numpy.array(image) # Converts image into a usable array nested in order of: list, row of pixels, pixel brightness 0-255
            index_array = [[round((len(char_list)-1) * (alpha) / 255) for alpha in row] for row in array] # Converts brightness values to integers for use as an index of char_list
            image.close() # Prevents memory leaks and speeds up the program significantly, such that the time complexity is O(n) where n is the number of characters being processed
            return (''.join([''.join([char_list[index] for index in index_row]) +'\n' for index_row in index_array]).removesuffix('\n')) # takes the index values per pixel from the index array, then replaces each 'pixel' with a chracter of that index/ brightness
            

    def frames(self):
        cam = cv2.VideoCapture(self.path)

        try:
            # creating a folder named data
            if not os.path.exists('data'):
                os.makedirs('data')
                
        except OSError:
            # if not created then raise error
            print ('Error: Creating directory of data')
        currentframe = 0
        
        # gets the amount of frames in the video
        frame_count = int(cam.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # gets the amount of digits in the frame_count number
        digits = len(str(frame_count))
        print(f'Amount of frames to be created: {frame_count}\n')
        
        while True:
            # reading from frame
            ret,frame = cam.read()

            if ret:
                # adds lead 0's to the front of the frame number
                lead_curframe = f'{currentframe:0{digits}}'
                
                # if video is still left continue creating images
                name = './data/frame' + str(lead_curframe) + '.jpg'
                print('Creating...' + name,  end='\r')

                # writing the extracted images
                cv2.imwrite(name, frame)

                # increasing counter so that it will
                # show how many frames are created
                currentframe += 1
            else:
                size = 0
                for ele in os.scandir(f'{self.dirpath}\\data'):
                    size+=os.stat(ele).st_size
                print('\n\nFrame loading done.\nTotal size: {} kb'.format('{:,}'.format(round(size/1000))))
                break

        # Release all space and windows once done
        cam.release()
        cv2.destroyAllWindows()

        return os.listdir(f'{self.dirpath}\\data')