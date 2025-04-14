import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
from urllib.parse import quote

fileName = ""
q = False
up = False


class DownloadHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>Download {os.path.basename(fileName)}</title>
            </head>
            <body>
                <a href="/download" download>{os.path.basename(fileName)}</a>
            </body>
            </html>
            """.encode('utf-8')
            )


        elif self.path == "/download":
            if not os.path.exists(fileName):
                self.send_error(404)
                return

            downloadFile = open(fileName, "rb")

            self.send_response(200)
            self.send_header('Content-Type', 'application/octet-stream')
            # self.send_header('Content-Disposition', f'attachment; filename="{os.path.basename(fileName)}"')
            self.send_header(
                'Content-Disposition',
                f'attachment; filename="{quote(os.path.basename(fileName))}"; filename*=UTF-8\'\'{quote(os.path.basename(fileName))}'
            )
            self.send_header('Content-Length', str(os.path.getsize(fileName)))
            self.end_headers()
            while True:
                uploadData = downloadFile.read(5242880)
                if not uploadData:
                    break
                self.wfile.write(uploadData)

            downloadFile.close()

        else:
            self.send_error(400)

"""
def run(savePath, port):
    global path
    global q
    if not savePath:
        path = "."
    else:
        path = savePath
    server_address = ("", port)
    with ThreadingHTTPServer(server_address, UploadHandler) as UploadServer:
        upload_server_thread = Thread(target=UploadServer.serve_forever)
        upload_server_thread.daemon = True
        upload_server_thread.start()

        print(f"Server started on http://0.0.0.0:{port}")


        while True:
            if q == True:
                UploadServer.shutdown()
                upload_server_thread.join()
                q = False
                break
"""
def run(file, port):
    global fileName
    global q
    global up
    fileName = file
    print(file)
    server_address = ("", port)




    with ThreadingHTTPServer(server_address, DownloadHandler) as DownloadServer:
        download_server_thread = Thread(target=DownloadServer.serve_forever)
        download_server_thread.daemon = True
        download_server_thread.start()
        up = True

        while True:
            if q == True:
                DownloadServer.shutdown()
                download_server_thread.join()
                q = False
                up = False
                break



if __name__ == "__main__":
    run(".txt", 9091)