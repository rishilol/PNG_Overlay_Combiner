# PNG Overlay Combiner

A web application that combines two PNG images using various blending modes (XOR, Add, Subtract, Average, Max, Min, AND, OR).

## Features

- Upload two PNG images
- Combine images using multiple blending modes
- Real-time preview of results
- Download combined images
- Modern web interface

## Setup

### Backend Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Flask server:
```bash
python app.py
```

The backend server will run on `http://localhost:5001`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies and start the development server:
```bash
./setup_frontend.sh
```

The frontend will be available at `http://localhost:3000`

## Project Structure

- `app.py` - Flask backend server
- `combine.py` - Image processing logic
- `frontend/` - React frontend application
- `uploads/` - Temporary storage for uploaded images
- `output/` - Storage for processed images

## API Endpoints

- `POST /api/combine` - Combine two images
- `GET /output/<filename>` - Retrieve processed images

## License

MIT License 