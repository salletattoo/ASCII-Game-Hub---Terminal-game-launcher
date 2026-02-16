#!/usr/bin/env python3
"""
ASCII GAME HUB - Terminal Game Launcher
Themed fonts, centered layout, shows ONLY installed games
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from typing import Dict, List, Tuple, Callable, Optional
import textwrap


class Config:
    """Application configuration"""
    STORY_GAMES = ["rogue", "nethack", "crawl", "angband", "gearhead", "colossal-cave-adventure", "slashem", "cataclysm", "qud", "open-adventure", "brogue", "omega-rpg", "moria"]
    ACTION_GAMES = ["robotfindskitten", "tint", "tty-solitaire", "tetrinet-client", "petris", "greed", "asciijump", "nsnake", "piu-piu", "curseofwar", "ascii-patrol", "moon-buggy", "ninvaders", "openra", "openttd"]
    BOARD_GAMES = ["nettoe","bastard tetris", "trader", "chroma-curses", "nudoku", "nbsdgames", "empire", "vitetris", "sudoku", "freesweep", "gnugo", "netris", "gnuminishogi", "cavezofphear", "bsdgames", "bastet", "zivot", "npush", "2048", "gomoku", "hangman", "atc", "gnome-mines", "gnome-sudoku"]
    
    # Game categories with their headers
    CATEGORIES = {
        "1": ("Story / Roguelike", STORY_GAMES, "story_header"),
        "2": ("Action / Arcade", ACTION_GAMES, "action_header"),
        "3": ("Boards / Classics", BOARD_GAMES, "boards_header"),
    }


class Terminal:
    """Terminal control utilities"""
    
    @staticmethod
    def get_terminal_size():
        """Get terminal dimensions"""
        try:
            columns, rows = shutil.get_terminal_size()
            return columns, rows
        except:
            return 80, 34
    
    @staticmethod
    def clear():
        """Clear terminal screen"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    @staticmethod
    def get_key() -> str:
        """Get single keypress without Enter"""
        if os.name == 'posix':
            import termios
            import tty
            import select
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                # Check if data is available
                if select.select([sys.stdin], [], [], 0.1)[0]:
                    ch = sys.stdin.read(1)
                else:
                    ch = ''
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch
        else:
            import msvcrt
            if msvcrt.kbhit():
                return msvcrt.getch().decode('utf-8')
            return ''
    
    @staticmethod
    def pause():
        """Wait for keypress"""
        print("\n" + " " * 20 + "Press any key to continue...")
        while True:
            key = Terminal.get_key()
            if key:
                break
    
    @staticmethod
    def center_block(text: str, width: Optional[int] = None) -> str:
        """Center an entire block of text"""
        if width is None:
            width, _ = Terminal.get_terminal_size()
        
        lines = text.split('\n')
        max_line_length = max((len(line.rstrip()) for line in lines if line.strip()), default=0)
        left_padding = max(0, (width - max_line_length) // 2)
        
        centered = []
        for line in lines:
            if line.strip():
                centered.append(' ' * left_padding + line.rstrip())
            else:
                centered.append('')
        return '\n'.join(centered)
    
    @staticmethod
    def layout_menu_left_art_right(menu_content: str, art_content: str, terminal_width: int = None) -> str:
        """Layout with menu on left and art on right with proper spacing"""
        if terminal_width is None:
            terminal_width, _ = Terminal.get_terminal_size()
        
        menu_lines = menu_content.split('\n')
        art_lines = art_content.split('\n')
        
        # Calculate widths
        menu_width = max((len(line) for line in menu_lines), default=40)
        art_width = 30  # Fixed width for art
        
        # Add spacing between menu and art
        spacing = 8
        
        # Make sure we have at least as many lines
        max_lines = max(len(menu_lines), len(art_lines))
        while len(menu_lines) < max_lines:
            menu_lines.append('')
        while len(art_lines) < max_lines:
            art_lines.append('')
        
        # Combine lines
        result = []
        for i in range(max_lines):
            menu_part = menu_lines[i]
            art_part = art_lines[i] if i < len(art_lines) else ''
            
            # Pad menu part to fixed width
            if len(menu_part) < menu_width:
                menu_part = menu_part.ljust(menu_width)
            
            # Pad art part to fixed width
            if len(art_part) < art_width:
                art_part = art_part.ljust(art_width)
            
            result.append(menu_part + ' ' * spacing + art_part)
        
        return '\n'.join(result)


class GameDetector:
    """Game installation detection"""
    
    @staticmethod
    def is_installed(game: str) -> bool:
        """Check if game is installed and in PATH"""
        return shutil.which(game) is not None
    
    @staticmethod
    def get_available_games(games: List[str]) -> List[str]:
        """Return list of installed games"""
        return [g for g in games if GameDetector.is_installed(g)]


class ASCIIArt:
    """Themed ASCII art headers with different fonts"""
    
    @staticmethod
    def get_story_art() -> str:
        """ASCII art for Story/Roguelike menu (right side)"""
        return textwrap.dedent("""

       /     \     
      ((     ))    
  ===  \\_v_//  ===
    ====)_^_(====  
    ===/ O O \===  
    = | /_ _\ | =  
   =   \/_ _\/   = 
        \_ _/     
        (o_o)     
         VwV      

        """).strip('\n')
    
    @staticmethod
    def get_action_art() -> str:
        """ASCII art for Action/Arcade menu (right side)"""
        return textwrap.dedent("""                             

            __          
          _|  |_         
        _|      |_       
       |  _    _  |     
       | |_|  |_| |     
    _  |  _    _  |  _  
   |_|_|_| |__| |_|_|_| 
     |_|_        _|_|   
       |_|      |_|     
                        
       
        """).strip('\n')
    
    @staticmethod
    def get_boards_art() -> str:
        """ASCII art for Boards/Classics menu (right side) - Chess pattern like in example"""
        return textwrap.dedent("""
                   
                 a b c d e f g h
              8 │_│#│_│#│_│#│_│#│ 8
              7 │#│_│#│_│#│_│#│_│ 7
              6 │_│#│_│#│_│#│_│#│ 6
              5 │#│_│#│_│#│_│#│_│ 5
              4 │_│#│_│#│_│#│_│#│ 4
              3 │#│_│#│_│#│_│#│_│ 3
              2 │_│#│_│#│_│#│_│#│ 2
              1 │#│_│#│_│#│_│#│_│ 1
                 a b c d e f g h
                ┌──────────────┐
                │  CHECKMATE   │
                └──────────────┘
        """).strip('\n')
    
    @staticmethod
    def story_header() -> str:
        """FANTASY / MERLIN THEME - Celtic, mystical font"""
        return textwrap.dedent("""
            ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
            ░░                                           ░░
            ░░   .---.  _______  .---.  ,---.  .-.   .-. ░░
            ░░  ( .-._)|__   __|/ .-. ) | .-.\  \ \_/ )/ ░░
            ░░ (_) \     )| |   | | |(_)| `-'/   \   (_) ░░
            ░░ _  \ \   (_) |   | | | | |   (     ) (    ░░
            ░░( `-'  )    | |   \ `-' / | |\ \    | |    ░░
            ░░ `----'     `-'    )---'  |_| \)\  /(_|    ░░
            ░░                   (_)         (__)(__)    ░░
            ░░---------- Dungeons & Dragons -------------░░
            ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
        """).strip('\n')
    
    @staticmethod
    def action_header() -> str:
        """ACTION / SPEED THEME - Racing, fast, aggressive font"""
        return textwrap.dedent("""
            ╔══════════════════════════════════════════════════════════╗
            ║  $$$$$$\   $$$$$$\ $$$$$$$$\ $$$$$$\  $$$$$$\  $$\   $$\ ║
            ║ $$  __$$\ $$  __$$\\__ $$  __|\_$$  _|$$  __$$\ $$$\  $$ |║
            ║ $$ /  $$ |$$ /  \__|  $$ |     $$ |  $$ /  $$ |$$$$\ $$ |║
            ║ $$$$$$$$ |$$ |        $$ |     $$ |  $$ |  $$ |$$ $$\$$ |║
            ║ $$  __$$ |$$ |        $$ |     $$ |  $$ |  $$ |$$ \$$$$ |║
            ║ $$ |  $$ |$$ |  $$\   $$ |     $$ |  $$ |  $$ |$$ |\$$$ |║
            ║ $$ |  $$ |\$$$$$$  |  $$ |   $$$$$$\  $$$$$$  |$$ | \$$ |║
            ║ \__|  \__| \______/   \__|   \______| \______/ \__|  \__|║
            ║                                                          ║
            ║ ===================== SHOOT & RUN =======================║
            ╚══════════════════════════════════════════════════════════╝
        """).strip('\n')
    
    @staticmethod
    def boards_header() -> str:
        """BOARDS / CLASSICS THEME - Chess, timeless, elegant font"""
        return textwrap.dedent("""
            ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
            ░░  ___                                      ___             ░░   
            ░░ (   )                                    (   )            ░░   
            ░░  | |.-.    .--.     .---.  ___         .-.| |     .--.    ░░ 
            ░░  | /   \  /    \   / .-, \(   )..~,   /   \ |   /  _  \   ░░
            ░░  |  .-. ||  .-. ; (__) ; | | ' .-. ; |  .-. |  . .' `. ;  ░░
            ░░  | |  | || |  | |   .'`  | |  / (___)| |  | |  | '   | |  ░░
            ░░  | |  | || |  | |  / .'| | | |       | |  | |  _\_`.(___) ░░
            ░░  | |  | || |  | | | /  | | | |       | |  | | (   ). '.   ░░
            ░░  | '  | || '  | | ; |  ; | | |       | '  | |  | |  `\ |  ░░
            ░░  ' `-' ; '  `-' / ' `-'  | | |       ' `-'  /  ; '._,' '  ░░
            ░░   `.__.   `.__.'  `.__.'_.(___)       `.__,'    '.___.'   ░░
            ░░  ******************* Card & Classics *******************  ░░                                           
            ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
        """).strip('\n')
    
    @staticmethod
    def main_header() -> str:
        """Main menu header"""
        return textwrap.dedent("""
           ╔═════════════════════════════════════════════════════════════════════════════╗
           ║ █████╗ ███████╗ ██████╗██╗██╗     ██████╗  █████╗ ███╗   ███╗███████╗███████╗
           ║██╔══██╗██╔════╝██╔════╝██║██║    ██╔════╝ ██╔══██╗████╗ ████║██╔════╝██╔════╝
           ║███████║███████╗██║     ██║██║    ██║  ███╗███████║██╔████╔██║█████╗  ███████╗
           ║██╔══██║╚════██║██║     ██║██║    ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝  ╚════██║
           ║██║  ██║███████║╚██████╗██║██║    ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗███████║
           ║╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝╚═╝     ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚══════╝
           ║                      -T E R M I N A L   H U B-                              ║
           ╚═════════════════════════════════════════════════════════════════════════════╝
        """).strip('\n')


class GameMenu:
    """Interactive game menu system - Shows ONLY installed games"""
    
    def __init__(self):
        self.detector = GameDetector()
        self.ascii = ASCIIArt()
        self.width, self.height = Terminal.get_terminal_size()
    
    def display_header(self, header_func: Callable):
        """Display centered header"""
        header = header_func()
        centered_header = Terminal.center_block(header)
        print(centered_header)
        print()
    
    def display_game_list(self, games: List[str], category_name: str) -> Tuple[List[str], Dict[int, str], str]:
        """Display ONLY installed games - formatted for left side"""
        available = self.detector.get_available_games(games)
        game_map = {}
        
        # Create the left side content (menu)
        menu_lines = []
        
        if not available:
            menu_lines.append("┌──────────────────────────────────────┐")
            menu_lines.append("│                                      │")
            menu_lines.append("│     ✖ No games installed! ✖          │")
            menu_lines.append("│                                      │")
            menu_lines.append("├──────────────────────────────────────┤")
            menu_lines.append("│ Install some games:                  │")
            menu_lines.append("│ $ sudo apt update                    │")
            menu_lines.append("│ $ sudo apt install <game-name>       │")
            menu_lines.append("└──────────────────────────────────────┘")
        else:
            # Top border
            menu_lines.append("┌──────────────────────────────────────┐")
            
            # Category title
            menu_lines.append(f"│{category_name:^38}│")
            
            # Separator
            menu_lines.append("├──────────────────────────────────────┤")
            
            # Game list with numbers (two columns if many games)
            if len(available) > 10:
                # Two columns layout
                mid = (len(available) + 1) // 2
                first_col = available[:mid]
                second_col = available[mid:]
                
                for i in range(max(len(first_col), len(second_col))):
                    left_game = f"{i+1}) {first_col[i]}" if i < len(first_col) else ""
                    right_game = f"{i+mid+1}) {second_col[i]}" if i < len(second_col) else ""
                    
                    # Pad to fit in two columns
                    left_padded = left_game.ljust(18)
                    line = f"│ {left_padded} {right_game:<18} │"
                    menu_lines.append(line)
                    
                    # Map game numbers
                    if i < len(first_col):
                        game_map[i+1] = first_col[i]
                    if i < len(second_col):
                        game_map[i+mid+1] = second_col[i]
            else:
                # Single column layout
                for idx, game in enumerate(available, 1):
                    line = f"│   {idx}) {game:<30}  │"
                    menu_lines.append(line)
                    game_map[idx] = game
            
            # Bottom part with back option
            menu_lines.append("├──────────────────────────────────────┤")
            menu_lines.append("│   0) Back to Main Menu               │")
            menu_lines.append("└──────────────────────────────────────┘")
        
        # Add prompt at the bottom (will be displayed separately)
        prompt = "Select game number: "
        
        return available, game_map, '\n'.join(menu_lines), prompt
    
    def run_game_menu(self, category_name: str, games: List[str], header_func: Callable, art_func: Callable):
        """Run interactive menu for a game category"""
        while True:
            Terminal.clear()
            
            # Display the big header
            self.display_header(header_func)
            
            # Get the menu and art
            available, game_map, menu_content, prompt = self.display_game_list(games, category_name)
            art_content = art_func()
            
            if not available:
                # Show menu and art with no games message
                full_display = Terminal.layout_menu_left_art_right(menu_content, art_content)
                print(full_display)
                print("\n" + prompt, end='')
                Terminal.pause()
                return
            
            # Add some spacing before the layout
            print()
            
            # Combine menu on left with art on right
            full_display = Terminal.layout_menu_left_art_right(menu_content, art_content)
            print(full_display)
            
            # Print prompt on new line with proper positioning
            print("\n" + prompt, end='')
            
            try:
                choice = input().strip()
            except (KeyboardInterrupt, EOFError):
                choice = "0"
            
            if choice == "0":
                return
            
            try:
                game_num = int(choice)
                if game_num in game_map:
                    game = game_map[game_num]
                    self.launch_game(game)
                else:
                    self.show_error("Invalid selection!")
            except ValueError:
                self.show_error("Please enter a valid number!")
    
    def launch_game(self, game: str):
        """Launch a game with proper terminal handling"""
        Terminal.clear()
        cols, _ = Terminal.get_terminal_size()
        
        print("\n" * 2)
        print(" " * ((cols - 30) // 2) + " ╔══════════════════════════════╗")
        print(" " * ((cols - 30) // 2) + f"║     LAUNCHING: {game:<12}    ║")
        print(" " * ((cols - 30) // 2) + " ╚══════════════════════════════╝")
        print("\n" * 2)
        print(" " * ((cols - 40) // 2) + "Press Ctrl+C to return to menu when game exits")
        print("\n" * 1)
        
        try:
            # Save terminal state and run game
            subprocess.run([game], stderr=subprocess.STDOUT)
        except FileNotFoundError:
            self.show_error(f"Error: {game} not found!")
        except KeyboardInterrupt:
            pass  # Gracefully return to menu
        except Exception as e:
            self.show_error(f"Error launching {game}: {e}")
    
    def show_error(self, message: str):
        """Show centered error message"""
        cols, _ = Terminal.get_terminal_size()
        print("\n" + " " * ((cols - len(message) - 4) // 2) + "╔" + "═" * (len(message) + 2) + "╗")
        print(" " * ((cols - len(message) - 4) // 2) + f"║ {message} ║")
        print(" " * ((cols - len(message) - 4) // 2) + "╚" + "═" * (len(message) + 2) + "╝")
        Terminal.pause()
    
    def main_menu(self):
        """Main application menu - Centered, clean"""
        while True:
            Terminal.clear()
            cols, rows = Terminal.get_terminal_size()
            
            # Main header
            header = self.ascii.main_header()
            print(Terminal.center_block(header))
            print()
            
            # Menu box
            box_width = 50
            left_pad = max(0, (cols - box_width) // 2)
            
            print(" " * left_pad + "┌" + "─" * (box_width - 2) + "┐")
            print(" " * left_pad + "│" + " " * (box_width - 2) + "│")
            print(" " * left_pad + "│            1) Story / Roguelike                │")
            print(" " * left_pad + "│            2) Action / Arcade                  │")
            print(" " * left_pad + "│            3) Boards / Classics                │")
            print(" " * left_pad + "│" + " " * (box_width - 2) + "│")
            print(" " * left_pad + "│                    0) Exit                     │")
            print(" " * left_pad + "│" + " " * (box_width - 2) + "│")
            print(" " * left_pad + "└" + "─" * (box_width - 2) + "┘")
            print()
            
            prompt = " " * ((cols - 20) // 2) + "Select category: "
            
            try:
                choice = input(prompt).strip()
            except (KeyboardInterrupt, EOFError):
                choice = "0"
            
            if choice == "0":
                self.quit()
                break
            elif choice in Config.CATEGORIES:
                name, games, header = Config.CATEGORIES[choice]
                header_func = getattr(self.ascii, header)
                
                # Select the appropriate art for right side
                if choice == "1":
                    art_func = self.ascii.get_story_art
                elif choice == "2":
                    art_func = self.ascii.get_action_art
                else:
                    art_func = self.ascii.get_boards_art
                
                self.run_game_menu(name, games, header_func, art_func)
            else:
                self.show_error("Invalid selection!")
    
    def quit(self):
        """Clean exit with style"""
        Terminal.clear()
        cols, _ = Terminal.get_terminal_size()
        
        farewell = """
        ╔══════════════════════════════════════╗
        ║                                      ║
        ║         Thanks for playing!          ║
        ║                                      ║
        ║             GAME OVER                ║
        ║                                      ║
        ╚══════════════════════════════════════╝
                                   by ASC11AM0N
        """
        
        print(Terminal.center_block(farewell))
        print("\n" * 2)
        sys.exit(0)


def main():
    """Application entry point"""
    try:
        menu = GameMenu()
        menu.main_menu()
    except KeyboardInterrupt:
        Terminal.clear()
        cols, _ = Terminal.get_terminal_size()
        print("\n" * (Terminal.get_terminal_size()[1]//2))
        sys.exit(0)


if __name__ == "__main__":
    main()