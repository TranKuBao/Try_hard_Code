from flask import Flask, request, Response, jsonify
from flask_cors import CORS
from Recon_Dirsearch._Dirseach_ import Recon_Directory
import json
import time

app = Flask(__name__)
CORS(app)

# Biến toàn cục lưu scanner hiện tại
current_scanner = {'scanner': None}

def stream_scan(scanner):
    scanner.start_scan()
    while scanner.is_scanning:
        results = scanner.get_results(found_only=False)
        if results:
            yield f"data: {json.dumps(results[-1])}\n\n"
        time.sleep(0.2)
    yield f"data: {json.dumps({'summary': scanner.get_summary(), 'done': True})}\n\n"

@app.route('/recon/dirsearch/scan', methods=['POST'])
def scan_directory():
    data = request.json
    url = data.get('url')
    threads = data.get('threads', 5)
    timeout = data.get('timeout', 5)
    wordlist = data.get('wordlist_file', None)

    if not url:
        return {"error": "Missing url parameter"}, 400

    scanner = Recon_Directory(
        base_url=url,
        threads=threads,
        timeout=timeout,
        callback=None
    )
    if wordlist:
        scanner.wordlist_file = wordlist

    if not scanner._test_connection():
        return {"error": "Cannot connect to target"}, 400

    scanner._load_wordlist()
    current_scanner['scanner'] = scanner  # Lưu scanner hiện tại
    return Response(stream_scan(scanner), mimetype='text/event-stream')

@app.route('/recon/dirsearch/stop', methods=['POST'])
def stop_scan():
    scanner = current_scanner.get('scanner')
    if scanner and scanner.is_scanning:
        scanner.stop()
        return jsonify({'status': 'stopped'}), 200
    return jsonify({'status': 'no scan running'}), 200

if __name__ == '__main__':
    app.run(debug=True, threaded=True) 