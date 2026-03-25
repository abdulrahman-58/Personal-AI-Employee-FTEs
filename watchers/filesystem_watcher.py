"""
File System Watcher

Monitors a drop folder for new files and creates action files
in the Needs_Action folder for Claude Code to process.

This is the simplest watcher and perfect for the Bronze tier.
Users can drop any file (documents, images, etc.) into the
Inbox folder, and this watcher will create corresponding
action files.
"""

import os
import sys
import hashlib
import json
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from watchers.base_watcher import BaseWatcher


class FileSystemWatcher(BaseWatcher):
    """
    Watches a folder for new files and creates action items.
    
    Use cases:
    - Drop invoices for processing
    - Drop documents for summarization
    - Drop images for analysis
    - Drop any file that needs AI attention
    """
    
    def __init__(self, vault_path: str, check_interval: int = 5):
        """
        Initialize the file system watcher.
        
        Args:
            vault_path: Path to the Obsidian vault root directory
            check_interval: Seconds between checks (default: 5 for responsive file drops)
        """
        super().__init__(vault_path, check_interval)
        
        # Track processed files to avoid duplicates
        self.state_file = self.logs / 'filesystem_watcher_state.json'
        self.processed_files = self._load_state()
        
    def _load_state(self) -> set:
        """Load the set of processed file hashes from state file."""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r') as f:
                    data = json.load(f)
                    return set(data.get('processed_hashes', []))
            except Exception as e:
                self.logger.warning(f'Could not load state file: {e}')
        return set()
    
    def _save_state(self):
        """Save the set of processed file hashes to state file."""
        try:
            with open(self.state_file, 'w') as f:
                json.dump({
                    'processed_hashes': list(self.processed_files),
                    'last_updated': datetime.now().isoformat()
                }, f, indent=2)
        except Exception as e:
            self.logger.error(f'Could not save state file: {e}')
    
    def _get_file_hash(self, filepath: Path) -> str:
        """
        Calculate a hash for a file to track if it's been processed.
        
        Uses file path + size + modification time for efficiency.
        For small files, could use content hash instead.
        """
        stat = filepath.stat()
        content = f"{filepath.absolute()}:{stat.st_size}:{stat.st_mtime}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def check_for_updates(self) -> list:
        """
        Check the Inbox folder for new files.
        
        Returns:
            List of new file paths to process
        """
        new_files = []
        
        if not self.inbox.exists():
            return new_files
        
        # Scan inbox for files (not directories)
        for filepath in self.inbox.iterdir():
            if filepath.is_file() and not filepath.name.startswith('.'):
                file_hash = self._get_file_hash(filepath)
                
                if file_hash not in self.processed_files:
                    new_files.append(filepath)
                    self.processed_files.add(file_hash)
        
        # Save updated state
        if new_files:
            self._save_state()
        
        return new_files
    
    def create_action_file(self, filepath: Path) -> Path:
        """
        Create a .md action file for the dropped file.
        
        Args:
            filepath: Path to the dropped file
            
        Returns:
            Path to the created action file
        """
        stat = filepath.stat()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_name = filepath.stem.replace(' ', '_')
        
        # Create the action file content
        content = f'''---
type: file_drop
original_name: {filepath.name}
original_path: {filepath.absolute()}
size: {stat.st_size}
size_formatted: {self._format_size(stat.st_size)}
created: {datetime.fromtimestamp(stat.st_ctime).isoformat()}
modified: {datetime.fromtimestamp(stat.st_mtime).isoformat()}
received: {datetime.now().isoformat()}
status: pending
priority: normal
---

# File Drop for Processing

## File Information

- **Original Name:** {filepath.name}
- **Size:** {self._format_size(stat.st_size)}
- **Received:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Suggested Actions

- [ ] Review file content
- [ ] Determine required action
- [ ] Process and move to /Done

## Notes

*Add notes about what needs to be done with this file*

---
*Created by FileSystemWatcher*
'''
        
        # Create the action file
        action_filepath = self.needs_action / f'FILE_{safe_name}_{timestamp}.md'
        action_filepath.write_text(content)
        
        return action_filepath
    
    def _format_size(self, size_bytes: int) -> str:
        """Format file size in human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f} TB"


def main():
    """Main entry point for running the watcher."""
    import argparse
    
    parser = argparse.ArgumentParser(description='File System Watcher for AI Employee')
    parser.add_argument(
        '--vault', '-v',
        type=str,
        default=os.getenv('VAULT_PATH', '../AI_Employee_Vault'),
        help='Path to the Obsidian vault (default: ../AI_Employee_Vault or VAULT_PATH env var)'
    )
    parser.add_argument(
        '--interval', '-i',
        type=int,
        default=5,
        help='Check interval in seconds (default: 5)'
    )
    
    args = parser.parse_args()
    
    # Resolve vault path
    vault_path = Path(args.vault).resolve()
    
    if not vault_path.exists():
        print(f"Error: Vault path does not exist: {vault_path}")
        sys.exit(1)
    
    # Create and run watcher
    watcher = FileSystemWatcher(str(vault_path), args.interval)
    watcher.run()


if __name__ == '__main__':
    main()
