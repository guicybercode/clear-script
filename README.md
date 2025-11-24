# Background Remover - Retro Edition

A web-based image processing application implementing a pixel-level background removal algorithm with a retro graphical user interface inspired by Windows 95/98 design paradigms.

**Repository**: [https://github.com/guicybercode/clear-script](https://github.com/guicybercode/clear-script)

## Features

- **Multiple Image Upload** - Concurrent processing of multiple image files
- **Before/After Preview** - Comparative visualization of original and processed images
- **Adjustable Tolerance** - Configurable threshold parameter for background detection (range: 0-50)
- **Batch Processing** - Asynchronous batch processing with progress monitoring
- **Download Options** - Individual file download or compressed archive export (ZIP format)
- **Retro Interface** - Historical UI design implementation

## Screenshots

### Main Interface
![Main Interface](screenshots/main-interface.png)
*The retro-styled main interface with file selection and settings*

### Image Preview
![Image Preview](screenshots/preview.png)
*Before and after comparison of processed images*

### Processing Progress
![Processing Progress](screenshots/progress.png)
*Real-time progress bar during batch processing*

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/guicybercode/clear-script.git
cd clear-script
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to:
```
http://localhost:5000
```

## Usage

1. **Image Selection**: Utilize the file input interface to select one or more image files
2. **Tolerance Configuration**: Adjust the tolerance parameter via the slider control
   - Lower threshold values (0-10): Strict mode, removes only pixels with RGB values approaching (255, 255, 255)
   - Higher threshold values (30-50): Permissive mode, removes pixels within the specified tolerance range
3. **Processing Execution**: Initiate the background removal algorithm via the process button
4. **Output Retrieval**: Download processed images individually or as a compressed archive

## Supported Formats

- PNG
- JPG/JPEG
- GIF
- BMP

## Project Structure

```
logo/
├── app.py                 # Flask application
├── remover_fundo.py       # Background removal module
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css     # Retro styling
│   └── js/
│       └── main.js       # Frontend logic
├── uploads/              # Temporary upload folder
├── originais/            # Original images storage
└── sem_fundo/            # Processed images (transparent background)
```

## Technical Specifications

### Backend Architecture
- **Flask** - WSGI web application framework
- **Pillow (PIL)** - Python Imaging Library for image manipulation
- **Werkzeug** - WSGI utility library for file upload management

### Frontend Implementation
- Standard HTML5, CSS3, and ECMAScript (JavaScript)
- Custom CSS styling implementing Windows 95/98 visual design patterns
- Zero external JavaScript dependencies

## Algorithm Description

The application implements a pixel-level background removal algorithm using the following procedure:

1. **Color Space Conversion**: Transform input image to RGBA color space
2. **Pixel Analysis**: Iterate through each pixel, extracting RGB channel values
3. **Threshold Comparison**: For each pixel, compare RGB values against the white threshold (255 - tolerance)
4. **Alpha Channel Modification**: If pixel meets threshold criteria, set alpha channel to 0 (fully transparent)
5. **Pixel Preservation**: Maintain original RGB values for non-background pixels
6. **Output Generation**: Export processed image in PNG format with alpha channel transparency

## Configuration

You can modify the following in `app.py`:

- `MAX_CONTENT_LENGTH`: Maximum file upload size (default: 50MB)
- `UPLOAD_FOLDER`: Temporary upload directory
- Server host and port

## License

This project is distributed under an open source license, permitting both personal and commercial utilization.

## Contributing

Contributions to this project are accepted through the standard pull request workflow. Please ensure code follows established conventions and includes appropriate documentation.

## Acknowledgments

- Interface design inspired by historical Windows 95/98 graphical user interface specifications
- Implemented using Flask web framework and Pillow image processing library

---

## Demo Images

### Example 1: Logo Processing
![Example 1](examples/example1-before.png)
*Before: Logo with white background*

![Example 1 Result](examples/example1-after.png)
*After: Logo with transparent background*

### Example 2: Multiple Images
![Example 2](examples/example2-batch.png)
*Batch processing multiple logos*

---

**"너희는 내가 너희에게 명령한 모든 것을 지키고 행하라. 그것을 더하거나 감하지 말라."**

**申命記 12:32**

