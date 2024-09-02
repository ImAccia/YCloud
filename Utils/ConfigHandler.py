import curses
import Utils.MenuHandler as m

class ConfigHandler:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.settings = self.load_config()
        self.keys = list(self.settings.keys())
        self.values = list(self.settings.values())
        self.current_row_idx = 0

    def load_config(self):
        import config

        return {
            "block_size": config.block_size,
            "width": config.width,
            "height": config.height,
            "fps": config.fps,
            "rgb": config.rgb,
            "src": config.src,
            "out": config.out,
            "video_out": config.video_out,
            "video_in": config.video_in,
            "zip_out": config.zip_out
        }

    def save_config(self):
        with open("config.py", "w") as f:
            f.write(f"# Video settings\n")
            f.write(f"block_size = {self.values[self.keys.index('block_size')]}\n")
            f.write(f"width = {self.values[self.keys.index('width')]}\n")
            f.write(f"height = {self.values[self.keys.index('height')]}\n")
            f.write(f"fps = {self.values[self.keys.index('fps')]}\n\n")
            f.write(f"rgb = {self.values[self.keys.index('rgb')]}\n\n")
            
            f.write(f"# Paths\n")
            f.write(f"src = \"{self.sanitize(self.values[self.keys.index('src')])}\"\n")
            f.write(f"out = \"{self.sanitize(self.values[self.keys.index('out')])}\"\n")
            f.write(f"video_out = \"{self.sanitize(self.values[self.keys.index('video_out')])}\"\n")
            f.write(f"video_in = \"{self.sanitize(self.values[self.keys.index('video_in')])}\"\n")
            f.write(f"zip_out = \"{self.sanitize(self.values[self.keys.index('zip_out')])}\"\n")

    def edit(self):
        while True:
            self.stdscr.clear()

            for idx, key in enumerate(self.keys):
                if idx == self.current_row_idx:
                    self.stdscr.attron(curses.color_pair(1))
                    self.stdscr.addstr(idx, 0, f"{key}: {self.values[idx]}")
                    self.stdscr.attroff(curses.color_pair(1))
                else:
                    self.stdscr.addstr(idx, 0, f"{key}: {self.values[idx]}")

            self.stdscr.refresh()

            key = self.stdscr.getch()

            if key == curses.KEY_UP and self.current_row_idx > 0:
                self.current_row_idx -= 1
            elif key == curses.KEY_DOWN and self.current_row_idx < len(self.keys) - 1:
                self.current_row_idx += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                self.modify_value()
            elif key == 27:  # ESC key to exit
                break

        self.save_config()
        self.stdscr.clear()
        self.load_config()

    def modify_value(self):
        self.stdscr.clear()
        key = self.keys[self.current_row_idx]
        current_value = self.values[self.current_row_idx]
        self.stdscr.addstr(0, 0, f"Enter new value for {key} (current: {current_value}): ")
        curses.echo()
        new_value = self.stdscr.getstr(1, 0).decode('utf-8')
        curses.noecho()

        if new_value.strip():
            if key in ["block_size", "width", "height", "fps"]:
                try:
                    self.values[self.current_row_idx] = int(new_value)
                except:
                    self.stdscr.clear()
                    m.set_string(self.stdscr, 0, 0, f"{new_value} is an invalid value, provide a valid value to proceed", stop=True, colorCode=3)
                    self.modify_value()
                    
            else:
                self.values[self.current_row_idx] = new_value

    def sanitize(self, val):
        return val.replace("\\", "\\\\")