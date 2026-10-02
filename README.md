# native-vcs-bridge

A unified Python-based integration bridge designed for native communication with multiple Version Control Systems (VCS), including **Git**, **Subversion (SVN)**, **Mercurial (Hg)**, and **Perforce (P4)**.

## 🚀 Project Overview

The **native-vcs-bridge** provides a clean abstraction layer (`base_engine.py`) and specific adapters (`svn_adapter.py`, `mercurial_adapter.py`, `perforce_adapter.py`) to allow modern DevOps tools and workflows to interact directly with legacy or centralized repositories without the need for complex, risky migrations.

## 📁 Repository Structure

*   `main.py`: Main application entry point and Command Line Interface (CLI).
*   `base_engine.py`: Core abstract class defining the standard interface for all adapters.
*   `svn_adapter.py`: Native command implementation for Subversion.
*   `mercurial_adapter.py`: Native command implementation for Mercurial.
*   `perforce_adapter.py`: Native command implementation for Perforce Helix.
*   `setup.py` & `requirements.txt`: Packaging configurations and project dependencies.

## 🛠️ Installation

1. Ensure you have the required command-line clients (`git`, `svn`, `hg`, `p4`) installed and available in your system's PATH.
2. Clone the repository and install the dependencies:

```bash
pip install -r requirements.txt
python setup.py install
```

## ⚖️ License

I have the rarest license on GitHub, check the file to proof
