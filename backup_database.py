#!/usr/bin/env python3
"""
Database backup utility for the Web Scraper application.
Creates backups of the TinyDB database file.
"""

import os
import shutil
from datetime import datetime
from models.database import DatabaseManager

def create_backup():
    """Create a backup of the database"""
    try:
        backup_filename = f"scraper_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        backup_path = DatabaseManager.backup_database(backup_filename)
        
        print(f"✅ Database backup created: {backup_path}")
        
        # Show database stats
        stats = DatabaseManager.get_database_stats()
        print(f"\n📊 Database Statistics:")
        print(f"   • SEO Analyses: {stats['total_seo_analyses']}")
        print(f"   • Products: {stats['total_products']}")
        print(f"   • Pending Jobs: {stats['pending_jobs']}")
        print(f"   • Database Size: {stats['database_size']} bytes")
        
        return backup_path
        
    except Exception as e:
        print(f"❌ Error creating backup: {e}")
        return None

def restore_backup(backup_path):
    """Restore database from backup"""
    try:
        if not os.path.exists(backup_path):
            print(f"❌ Backup file not found: {backup_path}")
            return False
        
        # Create a backup of current database before restoring
        current_backup = create_backup()
        if current_backup:
            print(f"📦 Current database backed up to: {current_backup}")
        
        # Restore from backup
        db_path = os.path.join(os.getcwd(), 'scraper_data.json')
        shutil.copy2(backup_path, db_path)
        
        print(f"✅ Database restored from: {backup_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error restoring backup: {e}")
        return False

def list_backups():
    """List available backup files"""
    backup_files = []
    for file in os.listdir('.'):
        if file.startswith('scraper_backup_') and file.endswith('.json'):
            backup_files.append(file)
    
    if backup_files:
        print("📁 Available backups:")
        for backup in sorted(backup_files, reverse=True):
            file_size = os.path.getsize(backup)
            file_time = datetime.fromtimestamp(os.path.getmtime(backup))
            print(f"   • {backup} ({file_size} bytes, {file_time.strftime('%Y-%m-%d %H:%M:%S')})")
    else:
        print("📁 No backup files found")
    
    return backup_files

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("🔧 Web Scraper Database Backup Utility")
        print("\nUsage:")
        print("  python backup_database.py backup          - Create a new backup")
        print("  python backup_database.py list            - List available backups")
        print("  python backup_database.py restore <file>  - Restore from backup")
        print("\nExamples:")
        print("  python backup_database.py backup")
        print("  python backup_database.py restore scraper_backup_20241205_143022.json")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "backup":
        create_backup()
    
    elif command == "list":
        list_backups()
    
    elif command == "restore":
        if len(sys.argv) < 3:
            print("❌ Please specify backup file to restore")
            print("Usage: python backup_database.py restore <backup_file>")
            sys.exit(1)
        
        backup_file = sys.argv[2]
        restore_backup(backup_file)
    
    else:
        print(f"❌ Unknown command: {command}")
        print("Available commands: backup, list, restore")
        sys.exit(1)
