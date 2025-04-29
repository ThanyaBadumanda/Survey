from django.http import HttpResponse

def home_view(request):
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Server Status</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f0f8ff;
                color: #333;
                text-align: center;
                padding-top: 100px;
            }
            .status {
                font-size: 2rem;
                margin-bottom: 10px;
            }
            .emoji {
                font-size: 4rem;
            }
        </style>
    </head>
    <body>
        <div class="emoji">🚀</div>
        <div class="status">Server is up and running!</div>
        <p>Everything is working smoothly 🛠️</p>
    </body>
    </html>
    """
    return HttpResponse(html_content)
