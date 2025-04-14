import os
import random
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
import sys

q = False
path = ""
up = False

class UploadHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/upload":
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Error: Missing Content-Length header")
                return

            content_type = self.headers.get('Content-Type')
            boundary = content_type.split('boundary=')[1].encode()

            self.rfile.readline(content_length)
            contentDeposition = self.rfile.readline(content_length)
            self.rfile.readline(content_length)
            self.rfile.readline(content_length)

            # get the file name
            parts = contentDeposition.decode('utf-8').split(";")
            filename = ""
            for part in parts:
                if 'filename=' in part:
                    filename = part.split('=', 1)[1].split("\"")[1]
                    break


            # open and save file
            if not os.path.exists(fr"{path}\{filename}"):  # if exist, get a new name
                file = open(fr"{path}\{filename}", "ab")
            else:
                # get a random name
                tempName = ""
                for i in range(0, 9):
                    tempName += random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
                file = open(fr"{path}\{tempName + "_" + filename}", "ab")
            remain = content_length
            while True:
                if remain > 10240000 * 2:
                    data = self.rfile.read(10240000)
                    remain -= 10240000
                elif remain > 1024000 * 2:
                    data = self.rfile.read(1024000)
                    remain -= 1024000
                elif remain > 102400 * 2:
                    data = self.rfile.read(102400)
                    remain -= 102400
                elif remain > 10240 * 2:
                    data = self.rfile.read(10240)
                    remain -= 10240
                elif remain > 128 * 2:
                    data = self.rfile.read(128)
                    remain -= 128
                else:
                    data = self.rfile.readline(1024000)
                if boundary in data:
                    break

                file.write(data)
            file.close()



            # 返回响应
            self.send_response(200)
            self.end_headers()

        else:
            self.send_error(400, "No file uploaded")

    def do_GET(self):


        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write("""
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Upload file</title>
            </head>
            <body>
              <form id="uploadForm" enctype="multipart/form-data">
                <input type="file" name="file" id="fileInput">
                <input type="submit" value="Upload">
              </form>
              <progress id="progressBar" value="0" max="100" style="width: 50%"></progress>
              <p id="status"></p>

              <script>
                document.getElementById('uploadForm').addEventListener('submit', function(e) {
                  e.preventDefault(); 

                  const fileInput = document.getElementById('fileInput');
                  const file = fileInput.files[0];
                  if (!file) {
                    return alert('select file');
                  }

                  const xhr = new XMLHttpRequest();
                  const formData = new FormData();
                  formData.append('file', file);


                  xhr.upload.addEventListener('progress', function(e) {
                  if (e.lengthComputable) {
                    const percent = (e.loaded / e.total) * 100;
                    document.getElementById('progressBar').value = percent;
                    document.getElementById('status').innerText = `${Math.round(percent)}%`;
                  }
               });


               xhr.onload = function() {
                 if (xhr.status === 200) {
                   document.getElementById('status').innerText = 'success';
                 } else {
                   document.getElementById('status').innerText = 'fail';
                 }
               };


               xhr.open('POST', '/upload', true);
               xhr.send(formData);
             });
           </script>
         </body>
         </html>
            """.encode("utf-8"))
        else:
            self.send_error(404, "File not found")


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def run(savePath, port):
    global path
    global q
    global up
    if not savePath:
        path = resource_path("uploads")
    else:
        path = savePath


    server_address = ("", port)
    with ThreadingHTTPServer(server_address, UploadHandler) as UploadServer:
        upload_server_thread = Thread(target=UploadServer.serve_forever)
        upload_server_thread.daemon = True
        upload_server_thread.start()
        up = True

        while True:
            if q == True:
                UploadServer.shutdown()
                upload_server_thread.join()
                q = False
                up = False
                break


if __name__ == "__main__":
    run(r".\uploads", 9091)