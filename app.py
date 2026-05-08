from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import base64

app = Flask(__name__)
CORS(app)


def generate_pollinations_image(prompt):
    """
    Generate image using Pollinations AI
    No API key required
    """

    image_url = f"https://image.pollinations.ai/prompt/{prompt}"

    response = requests.get(
        image_url,
        timeout=120
    )

    return response.content


@app.route('/generate', methods=['POST'])
def generate_image():
    """Generate image from prompt using Pollinations AI"""

    try:

        data = request.json

        prompt = data.get('prompt', '')

        width = data.get('width', 1024)
        height = data.get('height', 1024)
        steps = data.get('steps', 4)

        # Validation
        if not prompt:
            return jsonify({
                'error': 'Prompt is required'
            }), 400

        print(f"\nGenerating image: {prompt[:60]}...")
        print(f"Parameters: {width}x{height}, steps={steps}")

        # Generate image using Pollinations AI
        image_bytes = generate_pollinations_image(prompt)

        # Convert image to base64
        img_base64 = base64.b64encode(
            image_bytes
        ).decode('utf-8')

        print("✓ Image generated successfully!")

        return jsonify({
            'success': True,
            'image': img_base64,
            'message': 'Image generated successfully'
        })

    except requests.exceptions.Timeout:

        return jsonify({
            'error': 'Request timeout',
            'message': 'The request took too long.'
        }), 504

    except Exception as e:

        print(f"Error: {str(e)}")

        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""

    return jsonify({
        'status': 'healthy',
        'model': 'Pollinations AI',
        'api': 'Pollinations AI Free API',
        'note': 'No API key required'
    })


@app.route('/')
def index():
    """Serve the main HTML page"""

    return send_from_directory(
        'views',
        'index.html'
    )


@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files"""

    return send_from_directory(
        'views',
        filename
    )


if __name__ == '__main__':

    print("\n" + "=" * 70)
    print(" 🎨 NRB AI IMAGE GENERATOR ")
    print("=" * 70)

    print(" Server running at:")
    print(" http://localhost:5000")

    print("\n Model:")
    print(" Pollinations AI")

    print("\n API:")
    print(" Free - No API Key Required")

    print("=" * 70)

    print("\n✓ Ready to generate images!\n")

    print("=" * 70 + "\n")

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )