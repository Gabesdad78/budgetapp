#!/usr/bin/env python3
"""
APK Builder Script for ML Budget App
Automates the process of building the Android APK
"""

import os
import subprocess
import sys
import platform

def check_requirements():
    """Check if buildozer is installed"""
    try:
        subprocess.run(['buildozer', '--version'], capture_output=True, check=True)
        print("✅ Buildozer is installed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Buildozer not found")
        return False

def install_buildozer():
    """Install buildozer if not present"""
    print("📦 Installing buildozer...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'buildozer'], check=True)
        print("✅ Buildozer installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install buildozer")
        return False

def setup_android_sdk():
    """Setup Android SDK and NDK"""
    print("🔧 Setting up Android SDK...")
    
    # Check if ANDROID_HOME is set
    android_home = os.environ.get('ANDROID_HOME')
    if not android_home:
        print("⚠️  ANDROID_HOME not set. Please install Android Studio and set ANDROID_HOME")
        return False
    
    print(f"✅ Android SDK found at: {android_home}")
    return True

def build_apk():
    """Build the APK using buildozer"""
    print("🚀 Starting APK build...")
    
    try:
        # Initialize buildozer if buildozer.spec doesn't exist
        if not os.path.exists('buildozer.spec'):
            print("📝 Creating buildozer.spec...")
            subprocess.run(['buildozer', 'init'], check=True)
        
        # Build the APK
        print("🔨 Building APK (this may take 10-20 minutes)...")
        result = subprocess.run(['buildozer', 'android', 'debug'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ APK built successfully!")
            print("📱 APK location: bin/mlbudgetapp-1.0-debug.apk")
            return True
        else:
            print("❌ APK build failed")
            print("Error output:")
            print(result.stderr)
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False

def main():
    """Main build process"""
    print("=" * 50)
    print("ML Budget App - APK Builder")
    print("=" * 50)
    
    # Check if we're on a supported platform
    if platform.system() not in ['Linux', 'Darwin']:
        print("⚠️  APK building is best supported on Linux/macOS")
        print("   Windows users may need to use WSL or a virtual machine")
    
    # Check and install buildozer
    if not check_requirements():
        if not install_buildozer():
            return False
    
    # Setup Android SDK
    if not setup_android_sdk():
        print("⚠️  Please install Android Studio and set ANDROID_HOME")
        print("   Then run this script again")
        return False
    
    # Build the APK
    if build_apk():
        print("\n🎉 APK build completed successfully!")
        print("\n📱 To install on your Android device:")
        print("1. Enable 'Developer Options' in Android Settings")
        print("2. Enable 'USB Debugging'")
        print("3. Connect your device via USB")
        print("4. Run: adb install bin/mlbudgetapp-1.0-debug.apk")
        return True
    else:
        print("\n❌ APK build failed")
        print("Please check the error messages above")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1) 