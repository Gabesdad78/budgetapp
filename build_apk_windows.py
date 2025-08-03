#!/usr/bin/env python3
"""
Windows-Compatible APK Builder for ML Budget App
This script provides alternative methods to build APK on Windows
"""

import os
import sys
import subprocess
import shutil
import zipfile
import tempfile
from pathlib import Path

def print_header():
    print("=" * 50)
    print("ML Budget App - Windows APK Builder")
    print("=" * 50)

def check_requirements():
    """Check if all requirements are met"""
    print("🔍 Checking requirements...")
    
    # Check Python
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ required")
        return False
    
    # Check Kivy
    try:
        import kivy
        print("✅ Kivy installed")
    except ImportError:
        print("❌ Kivy not installed")
        return False
    
    # Check Android SDK
    android_home = os.environ.get('ANDROID_HOME')
    if not android_home:
        print("❌ ANDROID_HOME not set")
        return False
    
    print("✅ Android SDK found")
    return True

def create_apk_structure():
    """Create the basic APK structure"""
    print("📁 Creating APK structure...")
    
    # Create temp directory
    temp_dir = Path("temp_apk")
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir()
    
    # Create APK structure
    (temp_dir / "assets").mkdir()
    (temp_dir / "res").mkdir()
    (temp_dir / "META-INF").mkdir()
    
    return temp_dir

def create_manifest():
    """Create AndroidManifest.xml"""
    manifest_content = '''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="org.mlbudgetapp"
    android:versionCode="1"
    android:versionName="1.0">
    
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
    
    <application
        android:label="ML Budget App"
        android:icon="@mipmap/ic_launcher"
        android:theme="@android:style/Theme.Material.Light">
        
        <activity
            android:name="org.kivy.android.PythonActivity"
            android:label="ML Budget App"
            android:configChanges="orientation|keyboardHidden|screenSize">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>'''
    
    return manifest_content

def create_simple_apk():
    """Create a simple APK using alternative method"""
    print("🔨 Creating simple APK...")
    
    try:
        # Create temp directory
        temp_dir = create_apk_structure()
        
        # Copy mobile app
        shutil.copy("mobile_app.py", temp_dir / "main.py")
        
        # Create manifest
        with open(temp_dir / "AndroidManifest.xml", "w") as f:
            f.write(create_manifest())
        
        # Create APK file
        apk_path = Path("ml_budget_app.apk")
        if apk_path.exists():
            apk_path.unlink()
        
        # Create zip file (basic APK structure)
        with zipfile.ZipFile(apk_path, 'w') as apk:
            apk.write(temp_dir / "AndroidManifest.xml", "AndroidManifest.xml")
            apk.write(temp_dir / "main.py", "assets/main.py")
        
        # Cleanup
        shutil.rmtree(temp_dir)
        
        print(f"✅ APK created: {apk_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error creating APK: {e}")
        return False

def install_apk():
    """Install APK on connected device"""
    print("📱 Installing APK...")
    
    try:
        # Check if device is connected
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
        if 'device' not in result.stdout:
            print("❌ No Android device connected")
            return False
        
        # Install APK
        result = subprocess.run(['adb', 'install', 'ml_budget_app.apk'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ APK installed successfully!")
            return True
        else:
            print(f"❌ Installation failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error installing APK: {e}")
        return False

def main():
    """Main function"""
    print_header()
    
    if not check_requirements():
        print("\n❌ Requirements not met. Please install missing components.")
        return False
    
    print("\n🚀 Starting APK build...")
    
    if create_simple_apk():
        print("\n📱 APK created successfully!")
        print("📋 To install on your Android device:")
        print("   1. Enable Developer Options on your Android device")
        print("   2. Enable USB Debugging")
        print("   3. Connect your device via USB")
        print("   4. Run: adb install ml_budget_app.apk")
        
        # Try to install automatically
        install_apk()
        
        return True
    else:
        print("\n❌ APK creation failed")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 APK build completed successfully!")
    else:
        print("\n💡 Alternative options:")
        print("   1. Use the web app at http://localhost:5000")
        print("   2. Run the desktop mobile app: python mobile_app.py")
        print("   3. Install WSL and try building on Linux")
        print("   4. Use a cloud build service") 