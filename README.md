# Visitor Counter SCRC

This project is a simple visitor counter web application built using Python.

## Installation

1. Make sure you have Python installed on your system.
2. Clone this repository:

    ```bash
    git clone https://github.com/lokabhiram/visitor-counter-scrc.git
    ```

3. Navigate to the project directory:

    ```bash
    cd visitor-counter-scrc
    ```

4. Install dependencies using pip:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. After installing the dependencies, you can run the application using:

    ```bash
    python main.py
    ```

2. Visit [http://127.0.0.1:5000/visitor_count](http://127.0.0.1:5000/visitor_count) in your web browser to see the output.
3. Additionally, to display the visitor count on a MAX7219 LED display module connected to an ESP32 microcontroller:
   
   - Connect the MAX7219 module to your ESP32 as follows:
     - VCC to ESP32 5V or 3.3V (based on your module's requirements)
     - GND to ESP32 GND
     - DIN to ESP32 pin 15
     - CS to ESP32 pin 2
     - CLK to ESP32 pin 4
   
   Ensure that the ESP32 is powered properly and both devices share a common ground.

## Contributors

- [Lokabhiram](https://github.com/lokabhiram)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
