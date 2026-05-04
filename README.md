# Python-Based Java Runtime Behavior Analysis and Repair System

## Developed By
Navya Sree Ausula  

## File Name
runtime_analysis_system.py  

---

## Project Overview
This system is designed to improve the quality and reliability of Java applications by analyzing how they behave during execution instead of only checking the code before running it. The system uses Python as a controlling layer and Java as the execution environment, which makes it possible to study real runtime behavior in a structured way. It allows users to run Java programs under different conditions, observe how they behave, and identify issues that normally cannot be detected using standard tools. The system also provides clear outputs, reports, and suggestions so that users can easily understand what went wrong and how to fix it. :contentReference[oaicite:0]{index=0}  

---

## Problem Statement
In many real-world applications, errors do not appear during coding or static analysis but only occur when the program is running. These include issues like null pointer exceptions, incorrect logic flow, arithmetic errors, and resource problems. Developers often spend a lot of time trying to reproduce these errors and understand their root cause. Existing tools do not provide full support for runtime analysis and repair suggestions, so developers must manually debug and fix issues, which takes more time and effort. This system is designed to solve this problem by automatically analyzing runtime behavior and supporting developers with clear insights and corrective suggestions. :contentReference[oaicite:1]{index=1}  

---

## System Objectives
- Analyze Java programs during execution instead of only static checking  
- Detect runtime defects such as exceptions and incorrect behavior  
- Generate meaningful insights about execution patterns  
- Provide corrective suggestions for detected issues  
- Support comparison of results before and after applying fixes  
- Maintain logs and reports for better understanding and tracking  

---

## Key Features
- Supports project creation and management for analysis tasks  
- Allows configuration of runtime parameters and execution limits  
- Automatically compiles and executes Java programs  
- Generates different input scenarios for testing  
- Captures execution traces, exceptions, and behavior details  
- Detects and classifies runtime defects  
- Provides patch recommendations for fixing issues  
- Supports comparison between original and updated execution results  
- Generates reports and maintains audit logs  

---

## System Modules
### Project Management
Handles creation, storage, and management of analysis projects  

### Runtime Configuration
Allows setting execution limits, defect categories, and analysis parameters  

### Java Execution Manager
Compiles and runs Java programs under Python control  

### Input Generator
Creates random and boundary-based input scenarios for testing  

### Execution Monitor
Captures runtime behavior such as execution flow and exceptions  

### Defect Analysis
Identifies and classifies runtime issues based on execution data  

### Behavior Inference
Analyzes expected behavior based on execution results  

### Patch Recommendation
Generates possible fixes for detected defects  

### Reporting and Comparison
Creates reports and compares execution results before and after fixes  

### Audit Logging
Records all system activities for tracking and transparency  

---

## System Workflow
1. User creates or selects an analysis project  
2. User configures runtime analysis settings  
3. Java code is compiled through Python control  
4. Input scenarios are generated for execution  
5. Java program is executed under monitoring  
6. Runtime behavior is captured and analyzed  
7. Defects are detected and classified  
8. Expected behavior is inferred  
9. Patch recommendations are generated  
10. Results are displayed and reports are created  

---

## Technologies Used
- Python for orchestration and system logic  
- Java for execution environment  
- Streamlit for user interface  
- OpenJDK for compiling and running Java code  
- JSON or structured storage for data management  

---

## Installation Steps
1. Install Python (version 3.x or above) on your system  
2. Install Java Development Kit (JDK) and ensure it is properly configured  
3. Download or copy the project files into a local folder  
4. Open terminal or command prompt in the project directory  
5. Install required Python libraries using pip install if needed  
6. Ensure Java path is set correctly in your system environment  
7. Run the application using the command  
   python drars_system.py  
8. Open the interface and start using the system  

---

## System Requirements
- Standard desktop or laptop  
- Minimum 8 GB RAM recommended  
- Python installed  
- Java Development Kit installed  
- No need for special hardware or paid tools  

---

## User Roles
### Software Analyst
Creates projects, configures analysis, runs execution, and analyzes defects  

### Java Developer
Submits code, reviews defects, applies fixes, and compares results  

### System Administrator
Manages system configuration, users, and monitoring settings  

---

## Output and Reports
- Runtime defect reports  
- Execution logs and traces  
- Patch recommendations  
- Comparison results  
- Structured reports for documentation  

---

## Conclusion
This system provides a practical and structured approach to analyzing Java programs during execution and improving their quality. It reduces the effort required for debugging by automating defect detection and providing useful repair suggestions. The system is simple to use, flexible, and can be extended further in the future to support more advanced analysis features and larger applications.
