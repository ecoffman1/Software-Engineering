# photon-main
Main software for Photon Laser Tag

## Contributors

| Username      | Name               |
|---------------|--------------------|
| HaplessGnome  | Joey Davenport     |
| Ecoffman1     | Ethan Coffman      |
| funcRandy     | Randall Wade       |
| nickjachim    | Nicholas Jachim    |

## Install Requirements

1. **Install required system packages** (for Debian-based systems):

    ```bash
    sudo apt-get install python3-pip
    sudo apt-get install python3-venv
    sudo apt-get install python3-tk
    sudo apt-get install python3-dev
    sudo apt-get install libpq-dev
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

## Run the Program

To start the program:

```bash
python3 ui.py

