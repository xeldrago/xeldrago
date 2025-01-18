import http.server
import json
import base64
from io import BytesIO
from PIL import Image

class RequestHandler(http.server.BaseHTTPRequestHandler):
    def get_html_content(self):
        return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Share Location and Webcam Live Stream</title>
            <script>
                async function shareLocationAndCaptureImage() {
                    const data = {};

                    // Collect geolocation data
                    if (navigator.geolocation) {
                        await new Promise((resolve) => {
                            navigator.geolocation.getCurrentPosition((position) => {
                                data.location = {
                                    latitude: position.coords.latitude,
                                    longitude: position.coords.longitude,
                                };
                                resolve();
                            });
                        });
                    } else {
                        alert("Geolocation is not supported by your browser.");
                    }

                    // Collect additional data
                    data.screen = {
                        width: window.screen.width,
                        height: window.screen.height,
                        colorDepth: window.screen.colorDepth,
                        pixelRatio: window.devicePixelRatio,
                    };
                    data.language = navigator.language || navigator.userLanguage;
                    data.connection = navigator.connection ? navigator.connection.effectiveType : "Unknown";
                    data.user_agent = navigator.userAgent;

                    // Capture image from live video stream
                    const webcamImage = await captureImageFromWebcam();
                    data.image = webcamImage;  // Add captured image to the data

                    // Send data to the server
                    const response = await fetch("/submit_location", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify(data),
                    });
                    const result = await response.json();
                    alert(result.message);
                }

                // Function to start webcam stream and capture live video
                async function startWebcam() {
                    try {
                        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
                        const videoElement = document.getElementById('videoElement');
                        videoElement.srcObject = stream;
                    } catch (err) {
                        alert("Could not access webcam: " + err);
                    }
                }

                // Function to capture an image from the live video
                async function captureImageFromWebcam() {
                    const video = document.getElementById('videoElement');
                    const canvas = document.createElement('canvas');
                    const context = canvas.getContext('2d');

                    // Set canvas size to video dimensions
                    canvas.width = video.videoWidth;
                    canvas.height = video.videoHeight;

                    // Draw the current video frame to the canvas
                    context.drawImage(video, 0, 0, canvas.width, canvas.height);

                    // Convert the image to base64 string
                    const imageData = canvas.toDataURL("image/png");
                    return imageData;
                }

                // Start the webcam stream as soon as the page is loaded
                window.onload = startWebcam;
            </script>
        </head>
        <body>
            <h1>Share Your Location, Device Info, and Webcam Live Stream</h1>
            <button onclick="shareLocationAndCaptureImage()">Share Location and Capture Snapshot</button>
            <br><br>

            <!-- Display live video stream from the webcam -->
            <video id="videoElement" width="640" height="480" autoplay></video>
            <br><br>

            <h2>Captured Image (From Live Stream):</h2>
            <img id="capturedImage" alt="Captured image will be displayed here" width="640">
        </body>
        </html>
        """

    def do_GET(self):
        if self.path == "/favicon.ico":
            # Handle favicon requests gracefully
            self.send_response(200)
            self.send_header("Content-Type", "image/x-icon")
            self.end_headers()
            return

        # Serve the main HTML page
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(self.get_html_content().encode("utf-8"))

    def do_POST(self):
        if self.path == "/submit_location":
            try:
                # Read and parse POST data
                content_length = int(self.headers["Content-Length"])
                post_data = self.rfile.read(content_length).decode("utf-8")
                data = json.loads(post_data)

                # Extract and log details
                client_ip = self.client_address[0]
                location = data.get("location", {})
                screen = data.get("screen", {})
                user_agent = data.get("user_agent", "Unknown")
                language = data.get("language", "Unknown")
                connection = data.get("connection", "Unknown")
                image_data = data.get("image", "")

                print(f"Received Data:")
                print(f"Received Data from IP: {client_ip}")
                print(f"  Latitude: {location.get('latitude')}")
                print(f"  Longitude: {location.get('longitude')}")
                print(f"  Screen Width: {screen.get('width')}")
                print(f"  Screen Height: {screen.get('height')}")
                print(f"  Color Depth: {screen.get('colorDepth')}")
                print(f"  Pixel Ratio: {screen.get('pixelRatio')}")
                print(f"  Browser: {user_agent}")
                print(f"  Language: {language}")
                print(f"  Connection Type: {connection}")
                
                if image_data:
                    print("Captured Image Data: [Image Data Hidden]")  # Here we hide the image data, but in practice, it could be saved or logged

                    # Optionally, save the image to a file
                    img_data = base64.b64decode(image_data.split(',')[1])  # Decode base64 string
                    image = Image.open(BytesIO(img_data))  # Convert to image object
                    image.save("captured_image.png")  # Save to a file on the server

                # Respond to the client
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                response = {"message": "Location, device data, and image received successfully!"}
                self.wfile.write(json.dumps(response).encode("utf-8"))
            except Exception as e:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                response = {"message": f"Failed to process data: {str(e)}"}
                self.wfile.write(json.dumps(response).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

def run_server():
    port = 8080
    server_address = ("", port)
    httpd = http.server.HTTPServer(server_address, RequestHandler)
    print(f"Serving on port {port}. Navigate to http://127.0.0.1:{port}/")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
