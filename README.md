# photon-main
Main software for Photon Laser Tag

## Contributors

| Username      | Name               |
|---------------|--------------------|
| HaplessGnome  | Joey Davenport     |
| Ecoffman1     | Ethan Coffman      |
| funcRandy     | Randall Wade       |
| nickjachim    | Nicholas Jachim    |

## For Graders
To run a release of the Photon Laser Tag software from GitHub:

1. **Navigate to the Releases page** on the [Photon Laser Tag GitHub repository](https://github.com/ecoffman1/Software-Engineering/releases).

2. **Download the latest release**:
   - Find the latest version and download the `.exe` file.

3. **Make the file executable** (for Linux):
   - After downloading the `.exe` named "Photon", navigate to the folder containing it in your terminal.

   ```bash
   chmod +x Photon
   ```

4. **Run the exe**:
    ```bash
    ./Photon
    ```


## Install Requirements

1. **Install required system packages** (for Debian-based systems):

    ```bash
    ./dev_setup.bash
    ```

2. **Create a virtual environment:**

    ```bash
    python3 -m venv venv
    ```

3. **Activate the virtual environment:**

    On Debian:

    ```bash
    source venv/bin/activate 
    ```

4. **Install Python dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

5. **For devs to build:**
    ```bash
    pyinstaller main.spec
    ```


## Run the Program

To start the program in venv:

```bash
python3 main.py
```

To start the program after being built navigate to /dist and use ./Photon (on the executable)
