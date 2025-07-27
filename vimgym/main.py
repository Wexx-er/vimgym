"""
VimGym Main Application

The main entry point for the VimGym application, handling CLI arguments,
initialization, and coordination of all components.
"""

import sys
import os
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from . import __version__
from .core.user import UserManager, User
from .core.progress import ProgressManager  
from .core.session import SessionManager
from .core.database import JSONDatabase
from .simulator.simulator import VimSimulator
from .modules.content_manager import ContentManager
from .features.lesson_runner import LessonRunner, LessonNavigator
from .ui.themes import get_theme
from .ui.menus import MainMenu, ModuleSelectionMenu


class VimGym:
    """Main VimGym application class."""
    
    def __init__(self, data_dir: Optional[Path] = None):
        """Initialize VimGym application.
        
        Args:
            data_dir: Optional custom data directory path
        """
        self.console = Console()
        self.theme = get_theme("dark")
        
        # Set up data directory
        if data_dir:
            self.data_dir = Path(data_dir)
        else:
            self.data_dir = self._get_default_config_path()
        
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize core components
        self.database = JSONDatabase(self.data_dir)
        self.user_manager = UserManager(self.database)
        self.progress_manager = ProgressManager(self.database)
        self.session_manager = SessionManager(self.database)
        
        # Initialize learning components
        self.simulator = VimSimulator()
        self.content_manager = ContentManager(self.data_dir)
        self.module_manager = self.content_manager.get_module_manager()
        
        # Initialize lesson runner
        self.lesson_runner = LessonRunner(
            self.console,
            self.simulator, 
            self.progress_manager,
            self.module_manager
        )
        
        self.lesson_navigator = LessonNavigator(
            self.module_manager,
            self.progress_manager
        )
        
        # Current state
        self.current_user: Optional[User] = None
        self.running = True
    
    def _get_default_config_path(self) -> Path:
        """Get default configuration directory."""
        if sys.platform == "win32":
            appdata = os.environ.get('APPDATA')
            if appdata:
                return Path(appdata) / 'VimGym'
            else:
                return Path.home() / 'AppData' / 'Roaming' / 'VimGym'
        else:
            # Linux/macOS
            return Path.home() / '.config' / 'vimgym'
    
    def run(self) -> None:
        """Run the main application loop."""
        try:
            self._show_welcome()
            self._initialize_user()
            self._main_loop()
        except KeyboardInterrupt:
            self._handle_shutdown()
        except Exception as e:
            self.console.print(f"[red]Error: {e}[/red]")
            if "--debug" in sys.argv:
                import traceback
                traceback.print_exc()
            self._handle_shutdown()
    
    def _show_welcome(self) -> None:
        """Display welcome screen."""
        welcome_text = Text("🏋️ VimGym", style="bold cyan")
        subtitle = Text("Interactive Vim Training", style="dim")
        version_text = Text(f"Version {__version__}", style="dim italic")
        
        panel = Panel(
            welcome_text + "\n" + subtitle + "\n" + version_text,
            border_style="bright_blue",
            padding=(1, 2)
        )
        
        self.console.print(panel)
        self.console.print()
    
    def _initialize_user(self) -> None:
        """Initialize or select user."""
        users = self.user_manager.list_users()
        
        if not users:
            # Create first user
            self.console.print("[yellow]Welcome! Let's create your profile.[/yellow]")
            username = click.prompt("Enter your username", type=str).strip()
            
            if username:
                self.current_user = self.user_manager.create_user(username)
                self.console.print(f"[green]Welcome to VimGym, {username}![/green]")
            else:
                self.console.print("[red]Invalid username. Exiting.[/red]")
                sys.exit(1)
        else:
            # Select existing user or create new
            self.console.print("[cyan]Select a user profile:[/cyan]")
            
            for i, user in enumerate(users, 1):
                last_active = user.last_active.strftime("%Y-%m-%d") if user.last_active else "Never"
                self.console.print(f"  {i}. {user.username} (last active: {last_active})")
            
            self.console.print(f"  {len(users) + 1}. Create new user")
            
            choice = click.prompt(
                "Your choice", 
                type=click.IntRange(1, len(users) + 1)
            )
            
            if choice <= len(users):
                self.current_user = users[choice - 1]
                self.console.print(f"[green]Welcome back, {self.current_user.username}![/green]")
            else:
                username = click.prompt("Enter username for new profile", type=str).strip()
                if username:
                    self.current_user = self.user_manager.create_user(username)
                    self.console.print(f"[green]Welcome to VimGym, {username}![/green]")
                else:
                    self.console.print("[red]Invalid username. Exiting.[/red]")
                    sys.exit(1)
    
    def _main_loop(self) -> None:
        """Main application loop."""
        if not self.current_user:
            return
        
        # Set user for lesson runner
        self.lesson_runner.set_user(self.current_user)
        
        # Update user's last active time
        self.user_manager.update_user_activity(self.current_user.id)
        
        while self.running:
            self.console.clear()
            self._show_welcome()
            
            # Get user progress for menu
            user_progress = self.progress_manager.get_user_progress(self.current_user.id)
            
            # Show main menu
            self.console.print("[bold]📚 What would you like to do?[/bold]\n")
            self.console.print("1. 🚀 Start Learning (Module Selection)")
            self.console.print("2. ⏩ Continue Learning (Resume)")
            self.console.print("3. 🎯 Practice Mode (Free Simulator)")
            self.console.print("4. 📊 View Statistics")
            self.console.print("5. ⚙️ Settings")
            self.console.print("6. ❓ Help")
            self.console.print("0. 🚪 Exit")
            
            choice = click.prompt(
                "\nSelect an option", 
                type=click.Choice(['0', '1', '2', '3', '4', '5', '6'])
            )
            
            if choice == '0':
                self.running = False
            elif choice == '1':
                self._show_module_selection()
            elif choice == '2':
                self._continue_learning()
            elif choice == '3':
                self._start_practice_mode()
            elif choice == '4':
                self._show_statistics()
            elif choice == '5':
                self._show_settings()
            elif choice == '6':
                self._show_help()
    
    def _show_module_selection(self) -> None:
        """Show module selection menu."""
        user_progress = self.progress_manager.get_user_progress(self.current_user.id)
        available_modules = self.module_manager.get_available_modules(user_progress)
        
        if not available_modules:
            self.console.print("[yellow]No modules available. This shouldn't happen![/yellow]")
            click.pause()
            return
        
        self.console.print("\n[bold]📚 Available Modules:[/bold]\n")
        
        for i, module in enumerate(available_modules, 1):
            completion = module.calculate_completion(user_progress)
            status = "✅" if completion >= 1.0 else "🔄" if completion > 0 else "🔒"
            self.console.print(f"{i}. {status} {module.title} ({completion:.0%} complete)")
            self.console.print(f"   [dim]{module.description}[/dim]")
            self.console.print(f"   [dim]Est. duration: {module.estimated_duration} minutes[/dim]\n")
        
        self.console.print("0. Back to main menu")
        
        choice = click.prompt(
            "Select a module", 
            type=click.IntRange(0, len(available_modules))
        )
        
        if choice > 0:
            selected_module = available_modules[choice - 1]
            self._start_module(selected_module.id)
    
    def _start_module(self, module_id: str) -> None:
        """Start a specific module."""
        module = self.module_manager.get_module(module_id)
        if not module:
            self.console.print(f"[red]Module {module_id} not found![/red]")
            return
        
        # Get next lesson for this module
        user_progress = self.progress_manager.get_user_progress(self.current_user.id)
        next_lesson = module.get_next_lesson(user_progress)
        
        if next_lesson:
            self._start_lesson(module_id, next_lesson.id)
        else:
            self.console.print(f"[green]🎉 Module '{module.title}' is already completed![/green]")
            click.pause()
    
    def _continue_learning(self) -> None:
        """Continue from where user left off."""
        # Find next available lesson
        next_lesson_info = self.lesson_navigator.get_next_lesson(
            self.current_user.id,
            "",  # Will search all modules
            ""
        )
        
        if next_lesson_info:
            module_id, lesson_id = next_lesson_info
            lesson_path = self.lesson_navigator.get_lesson_path(module_id, lesson_id)
            self.console.print(f"[blue]Continuing with: {lesson_path}[/blue]")
            click.pause("Press Enter to start...")
            self._start_lesson(module_id, lesson_id)
        else:
            self.console.print("[green]🎉 Congratulations! You've completed all available lessons![/green]")
            click.pause()
    
    def _start_lesson(self, module_id: str, lesson_id: str) -> None:
        """Start a specific lesson."""
        self.console.clear()
        
        if self.lesson_runner.start_lesson(module_id, lesson_id):
            # Enter lesson interaction loop
            self._lesson_interaction_loop()
        else:
            click.pause("Press Enter to return to main menu...")
    
    def _lesson_interaction_loop(self) -> None:
        """Handle user input during lesson."""
        self.console.print("\n[dim]💡 Type Vim commands or special commands starting with ':'[/dim]")
        self.console.print("[dim]Available: :hint, :skip, :restart, :help, :quit[/dim]\n")
        
        while True:
            try:
                lesson_info = self.lesson_runner.get_current_lesson_info()
                if not lesson_info:
                    break
                
                # Get user input
                user_input = click.prompt("", prompt_suffix="> ", show_default=False)
                
                if not user_input.strip():
                    continue
                
                # Process input
                result = self.lesson_runner.process_user_input(user_input)
                
                if result.get("error"):
                    self.console.print(f"[red]Error: {result['error']}[/red]")
                    break
                
                # Check if lesson completed
                if lesson_info.get("is_completed"):
                    break
                
                # Handle quit
                if "quit" in result.get("message", "").lower():
                    break
                    
            except KeyboardInterrupt:
                self.console.print("\n[yellow]💡 Use ':quit' to exit the lesson properly.[/yellow]")
            except EOFError:
                break
    
    def _start_practice_mode(self) -> None:
        """Start practice mode with simulator."""
        self.console.print("\n[blue]🎯 Starting practice mode...[/blue]")
        self.console.print("[dim]Free Vim simulator - practice any commands you want![/dim]")
        
        # Reset simulator
        self.simulator.reset()
        self.simulator.buffer.set_content("Welcome to VimGym practice mode!\nTry some Vim commands here.\nUse :quit to exit.")
        
        click.pause("Press Enter to start practice...")
        
        while True:
            try:
                self.console.clear()
                self.console.print("[bold]🎯 Practice Mode - Free Vim Simulator[/bold]")
                self.console.print("[dim]Type ':quit' to exit practice mode[/dim]\n")
                
                # Show current buffer state
                self._display_simulator_state()
                
                # Get user input
                user_input = click.prompt("", prompt_suffix="vim> ", show_default=False)
                
                if user_input.strip() == ":quit":
                    break
                
                # Execute in simulator
                response = self.simulator.process_input(user_input)
                
                if response.error:
                    self.console.print(f"[red]Error: {response.error}[/red]")
                    click.pause("Press Enter to continue...")
                    
            except KeyboardInterrupt:
                self.console.print("\n[yellow]💡 Use ':quit' to exit practice mode.[/yellow]")
                click.pause()
            except EOFError:
                break
        
        self.console.print("[green]✅ Exiting practice mode.[/green]")
    
    def _display_simulator_state(self) -> None:
        """Display current simulator state."""
        content = self.simulator.buffer.get_content()
        mode = self.simulator.buffer.mode.value
        cursor_pos = self.simulator.buffer.cursor_pos
        
        # Display buffer content with cursor
        lines = content.split('\n') if content else ['']
        
        self.console.print("[dim]Buffer:[/dim]")
        for i, line in enumerate(lines):
            if i == cursor_pos[0]:
                # Show cursor position
                if cursor_pos[1] < len(line):
                    cursor_line = line[:cursor_pos[1]] + "[reverse]" + line[cursor_pos[1]] + "[/reverse]" + line[cursor_pos[1]+1:]
                else:
                    cursor_line = line + "[reverse] [/reverse]"
                self.console.print(f"{i+1:2d}: {cursor_line}")
            else:
                self.console.print(f"{i+1:2d}: {line}")
        
        self.console.print(f"\n[dim]Mode: [bold]{mode.upper()}[/bold] | Cursor: {cursor_pos}[/dim]\n")
    
    def _show_statistics(self) -> None:
        """Show user statistics."""
        if not self.current_user:
            return
        
        user_progress = self.progress_manager.get_user_progress(self.current_user.id)
        
        self.console.print("\n[bold]📊 Your VimGym Statistics[/bold]\n")
        
        # Basic stats
        total_time = user_progress.get_total_time_spent()
        completed_modules = user_progress.get_completed_modules()
        
        self.console.print(f"⏱️  Total Learning Time: {total_time // 60}h {total_time % 60}m")
        self.console.print(f"📚 Modules Completed: {len(completed_modules)}")
        self.console.print(f"🔥 Learning Streak: {user_progress.get_learning_streak()} days")
        
        # Module progress
        self.console.print("\n[bold]Module Progress:[/bold]")
        for module in self.module_manager.get_all_modules():
            completion = module.calculate_completion(user_progress)
            status = "✅" if completion >= 1.0 else f"{completion:.0%}"
            self.console.print(f"  {status} {module.title}")
        
        click.pause("\nPress Enter to continue...")
    
    def _show_settings(self) -> None:
        """Show settings menu."""
        while True:
            self.console.print("\n[bold]⚙️ Settings[/bold]\n")
            self.console.print("1. 🎨 Change Theme")
            self.console.print("2. 🔄 Reset Progress")
            self.console.print("3. 📤 Export Progress")
            self.console.print("4. 📁 Show Data Directory")
            self.console.print("0. 🔙 Back to Main Menu")
            
            choice = click.prompt(
                "Select option", 
                type=click.Choice(['0', '1', '2', '3', '4'])
            )
            
            if choice == '0':
                break
            elif choice == '1':
                self.console.print("[yellow]🚧 Theme changing coming soon![/yellow]")
                click.pause()
            elif choice == '2':
                if click.confirm("⚠️ Are you sure you want to reset ALL progress?"):
                    self.progress_manager.reset_user_progress(self.current_user.id)
                    self.console.print("[green]✅ Progress reset successfully.[/green]")
                else:
                    self.console.print("[blue]❌ Reset cancelled.[/blue]")
                click.pause()
            elif choice == '3':
                self.console.print("[yellow]🚧 Export feature coming soon![/yellow]")
                click.pause()
            elif choice == '4':
                self.console.print(f"📁 Data directory: {self.data_dir}")
                click.pause()
    
    def _show_help(self) -> None:
        """Show help information."""
        help_text = f"""
[bold]🏋️ VimGym Help[/bold]

VimGym is an interactive Vim tutor that helps you learn Vim through 
hands-on practice in a safe simulated environment.

[bold]🎯 Features:[/bold]
• 7 learning modules from basics to advanced
• Interactive Vim simulator with real-time feedback
• Progress tracking and achievements
• Practice mode for free experimentation
• Hints and guided learning

[bold]📚 Learning Path:[/bold]
1. Vim Basics & Introduction
2. Movement & Navigation  
3. Text Editing
4. Search & Replace
5. File Operations
6. Advanced Features
7. Configuration & Plugins

[bold]🎮 How to Use:[/bold]
• Use number keys to navigate menus
• In lessons, type Vim commands directly
• Use :hint for help, :skip to skip exercises
• Practice mode lets you experiment freely

[bold]💾 Data Location:[/bold]
{self.data_dir}

[bold]Version:[/bold] {__version__}
        """
        
        self.console.print(help_text)
        click.pause("\nPress Enter to continue...")
    
    def _handle_shutdown(self) -> None:
        """Handle application shutdown."""
        self.console.print("\n[yellow]📴 Shutting down VimGym...[/yellow]")
        
        if self.current_user:
            # Save any pending data
            self.user_manager.save_user(self.current_user)
            self.console.print("[green]💾 Progress saved. Happy Vim learning! 🎉[/green]")


@click.command()
@click.option('--data-dir', type=click.Path(), help='Custom data directory')
@click.option('--debug', is_flag=True, help='Enable debug mode')
@click.version_option(version=__version__)
def main(data_dir: Optional[str], debug: bool) -> None:
    """🏋️ VimGym - Interactive Vim Training in your terminal."""
    
    if debug:
        import logging
        logging.basicConfig(level=logging.DEBUG)
    
    # Convert data_dir to Path if provided
    data_path = Path(data_dir) if data_dir else None
    
    # Create and run application
    app = VimGym(data_path)
    app.run()


if __name__ == "__main__":
    main()