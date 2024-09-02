import os
import math
import zipfile
import cv2
import numpy as np
import Utils.MenuHandler as m

class DataHandler:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.load_config()
        
    def load_config(self):
        import config

        self.block_size = config.block_size
        self.width = config.width
        self.height = config.height
        self.fps = config.fps
        self.rgb = config.rgb
        self.src = config.src
        self.out = config.out
        self.video_out = config.video_out
        self.video_in = config.video_in
        self.zip_out = config.zip_out
        self.invalid_size = False

        if self.height % self.block_size or self.height % self.block_size:
            self.stdscr.clear()
            m.set_string(self.stdscr, 0, 0, "Invalid block size, make sure that the both the width and height are divisible by the block size", colorCode=3, stop=True)
            self.invalid_size = True

    # Data to video + needed functions
    def dataToVideo(self):
        if self.invalid_size:
            return
        
        self.stdscr.clear()
        if self.rgb:
            num_rows, num_cols = self.stdscr.getmaxyx()
            m.set_string(self.stdscr, num_rows-1, 0, "USING RGB MODE", colorCode=4)

        self.zip_all_files_in_folder()
        colors = self.file_to_color()
        # self.create_video_from_colors(colors)
        self.stdscr.getch()

    def zip_all_files_in_folder(self):
        m.set_string(self.stdscr, 0, 0, "Zipping all the files in source folder")

        with zipfile.ZipFile(self.out, 'w') as zipf:
            for foldername, subfolders, filenames in os.walk(self.src):
                if not filenames:
                    m.set_string(self.stdscr, 1, 0, "No files found")
                    self.stdscr.getch()
                    exit()

                totalFiles = len(filenames)

                for idx, filename in enumerate(filenames):
                    m.set_string(self.stdscr, 1, 0, f"Zipping {filename}")
                    m.set_string(self.stdscr, 2, 0, f"Total progress: {idx + 1}/{totalFiles} - {round((idx + 1/totalFiles)*100, 1)}%")
                    file_path = os.path.join(foldername, filename)
                    arcname = os.path.relpath(file_path, self.src)
                    zipf.write(file_path, arcname)

        m.set_string(self.stdscr, 2, 0, "Finished zipping files", colorCode=2)

    def file_to_color(self):
        file_size = os.path.getsize(self.out)
        m.set_string(self.stdscr, 3, 0, f"Started converting {file_size} bytes into colors")

        colors = []
        frame_counter = 0

        # Preparazione video
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(self.video_out, fourcc, self.fps, (self.width, self.height), isColor=bool(self.rgb))

        with open(self.out, 'rb') as file:
            progress = 1
            while True:
                byte = file.read(1)
                m.set_string(self.stdscr, 4, 0, f"Progress: {progress}/{file_size} - {round((progress/file_size)*100, 1)}%")
                if not byte:
                    if colors:
                        frame = self.create_frame(iter(colors))
                        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR) if self.rgb else frame
                        out.write(frame)
                    m.set_string(self.stdscr, 4, 0, "Finished converting", colorCode=2)
                    break

                bits = f"{ord(byte):08b}"
                progress += 1

                if self.rgb:
                    r = int(bits, 2)

                    byte = file.read(1)
                    progress += 1
                    if not byte:
                        break
                    bits = f"{ord(byte):08b}"
                    g = int(bits, 2)

                    byte = file.read(1)
                    progress += 1
                    if not byte:
                        break
                    bits = f"{ord(byte):08b}"
                    b = int(bits, 2)

                    colors.extend([[r, g, b]])
                else:
                    colors.extend([255 if bit == '1' else 0 for bit in bits])

                if len(colors) >= (self.width * self.height) // (self.block_size * self.block_size):
                    frame = self.create_frame(iter(colors))
                    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR) if self.rgb else frame
                    out.write(frame)
                    frame_counter += 1
                    m.set_string(self.stdscr, 5, 0, f"Saved frame {frame_counter}")
                    colors = []

        out.release()
        m.set_string(self.stdscr, 6, 0, f"Video saved as {self.video_out}", colorCode=2)



    def create_frame(self, bitstream):
        frame = np.zeros((self.height, self.width, 3 if self.rgb else 1), dtype=np.uint8)

        for y in range(0, self.height, self.block_size):
            for x in range(0, self.width, self.block_size):
                try:
                    bit = next(bitstream)
                    color = bit
                    frame[y:y+self.block_size, x:x+self.block_size] = color
                except StopIteration:
                    frame[y:, x:] = [0, 0, 0] if self.rgb else 0
                    return frame

        return frame


    #Legacy, non più utilizzata
    '''
    def create_video_from_colors(self, colors):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(self.video_out, fourcc, self.fps, (self.width, self.height), isColor=bool(self.rgb))

        total_pixels = self.width * self.height
        num_blocks = math.ceil(len(colors) / (total_pixels // (self.block_size*self.block_size)))

        m.set_string(self.stdscr, 5, 0, f"Creating video with {num_blocks} frames")

        bitstream = iter(colors)

        for frame_idx in range(num_blocks):
            m.set_string(self.stdscr, 6, 0, f"Elaborating frame {frame_idx}/{num_blocks}")
            frame = self.create_frame(bitstream)
            
            # Debug: Salva il frame come immagine per la verifica
            # cv2.imwrite(f"frame_{frame_idx:04d}.png", frame)

            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR) if self.rgb else frame
            out.write(frame)

        out.release()
        m.set_string(self.stdscr, 6, 0, f"Video saved as {self.video_out}", colorCode=2)
    '''

    # Video to Data + needed functions
    def videoToData(self):
        if self.invalid_size:
            return

        self.stdscr.clear()
        m.set_string(self.stdscr, 1, 0, f"Extracting bits and saving them to {self.zip_out}")

        with open(self.zip_out, 'wb') as zip_file:
            cap = cv2.VideoCapture(self.video_in)
            bits = []
            currFrame = 1
            total_bytes = 0
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            while cap.isOpened():
                m.set_string(self.stdscr, 2, 0, f"Processing frame {currFrame}/{total_frames} - {round((currFrame/total_frames)*100, 1)}%")

                ret, frame = cap.read()
                if not ret:
                    break

                # Gestione del frame in scala di grigi se RGB è disabilitato
                if not self.rgb:
                    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                else:
                    gray_frame = frame  # Mantieni il frame come RGB

                for y in range(0, self.height, self.block_size):
                    for x in range(0, self.width, self.block_size):
                        if self.rgb:
                            pixel = gray_frame[y, x]
                            # Usa la media dei canali R, G e B per ottenere un valore unico
                            pixel_value = np.mean(pixel)
                        else:
                            pixel_value = gray_frame[y, x]

                        bit = 1 if pixel_value > 128 else 0
                        bits.append(bit)

                        if len(bits) == 8:
                            byte = 0
                            for bit in bits:
                                byte = (byte << 1) | bit
                            zip_file.write(bytes([byte]))
                            bits = []
                            total_bytes += 1
                            m.set_string(self.stdscr, 3, 0, f"Total bytes written: {total_bytes}")

                currFrame += 1

            # Gestione dei bit rimanenti (se presenti)
            if bits:
                byte = 0
                for bit in bits:
                    byte = (byte << 1) | bit
                zip_file.write(bytes([byte]))
                total_bytes += 1
                m.set_string(self.stdscr, 3, 0, f"Total bytes written: {total_bytes}")

            cap.release()
            cv2.destroyAllWindows()
            m.set_string(self.stdscr, 4, 0, f"Finished extracting bits and saved data to {self.zip_out}", colorCode=2, stop=True)


#Legacy non più usate

'''
    def video_to_bits(self):
        m.set_string(self.stdscr, 1, 0, f"Extracting bits from video")

        cap = cv2.VideoCapture(self.video_in)
        bits = []

        currFrame = 1
        while cap.isOpened():
            m.set_string(self.stdscr, 2, 0, f"Reading bits from frame {currFrame}")

            ret, frame = cap.read()
            if not ret:
                break

            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            for y in range(0, self.height, self.block_size):
                for x in range(0, self.width, self.block_size):
                    pixel = gray_frame[y, x]
                    
                    bits.append(1 if pixel > 128 else 0)

            currFrame+=1

        cap.release()
        cv2.destroyAllWindows()

        m.set_string(self.stdscr, 2, 0, f"Finished reading all bits in frames", colorCode=2)
        return bits

    def bits_to_bytes(self, bits):
        m.set_string(self.stdscr, 3, 0, f"Converting {len(bits)} bits to bytes")

        bytes_list = []
        for i in range(0, len(bits), 8):
            m.set_string(self.stdscr, 4, 0, f"Converting bits {i} - {i+8}")
            byte = 0
            for bit in bits[i:i+8]:
                byte = (byte << 1) | bit
            bytes_list.append(byte)

        m.set_string(self.stdscr, 4, 0, f"Finished converting bits to bytes", colorCode=2)
        
        return bytes(bytes_list)

    def save_zip(self, byte_data):
        m.set_string(self.stdscr, 5, 0,f"Saving data to {self.zip_out}")
        with open(self.zip_out, 'wb') as f:
            f.write(byte_data)
        m.set_string(self.stdscr, 5, 0,f"Finished saving data", colorCode=2, stop=True)
'''