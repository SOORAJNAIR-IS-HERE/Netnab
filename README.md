<p align="center">
  <img src="./netnab.png" alt="Headex Logo" width="650"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.13%2B-blue" alt="Python">
  <img src="https://img.shields.io/badge/Tested%20On-Linux-brightgreen" alt="Tested On">
  <img src="https://img.shields.io/badge/automated-yes-cyan" alt="Automated">
  <img src="https://img.shields.io/badge/License-MIT-orange" alt="License">
   <img src="https://img.shields.io/badge/Written In-Python-yellow" alt="License">
</p>

<p align="center">
 <img src="https://img.shields.io/badge/Author-SOORAJNAIR-darkred" alt="License">
   <img src="https://img.shields.io/badge/Opensource-Yes-blue" alt="License">
 </p>
 
Netnab is a powerful network scanning tool designed to streamline network analysis and security assessment. It provides in-depth scans to detect active devices, open ports, and network services. Ideal for IT professionals and security analysts, NetNab helps ensure secure, optimized networks with fast, reliable results.

## Features
**1. Comprehensive Port Scanning**
- Supports both TCP and UDP protocols for a thorough network assessment.
  
**2. User-Friendly Command-Line Interface**
- Simple and intuitive command syntax, making it accessible for users at any skill level.
  
**3. Customizable Scan Options**
- Simple and intuitive command syntax, making it accessible for users at any skill level.

**4. Customizable Scan Options**
- Ability to specify ports, scan types, and target ranges for flexible scanning operations.

**5. Efficient Performance**
- Optimized to handle multiple targets with minimized performance overhead.

**6. Banner Display Control**
- Option to disable banner display when scanning multiple targets for a cleaner output.

**7. Future-Proof**
- Designed with extensibility in mind, making it easier to add new protocols, scan types, and features.

# Installation on Linux

To run Netnab, you can either use this tool with Python/Python3 installed or just move the python file to bin directory. You can clone the repository and install the required dependencies.

**Clone the Repository:**

```python
git clone https://github.com/SOORAJNAIR-IS-HERE/Headex.git
```
**Navigate to the Project Directory**

```python
cd Netnab
```
# Usage

```python
python netnab <Target>
```
## Running globally in Linux

Move to bin Directory

```python
sudo mv netnab /usr/local/bin
```
```python
netnab <Target>
```

**To scan Multiple Targets**

```python
netnab <Target> <Target>
```
## Flags

```html
-h  | help message

-sv | service version

-o  | output format

-p  | Port range

-P  | customisable scan {tcp/udp}

-T  | Timeout

-t  | Threads [1-100]
```

## Install the Required Dependencies

**Update the package list**
```python
sudo apt update
```
**Install Python 3**
```python
sudo apt install python3
```
**Verify the installation**
```python
python3 --version
```


