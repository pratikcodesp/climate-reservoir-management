# Templates for HTML elements
def html_head():
    """Generate the HTML head section"""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Climate Resilient Reservoir Management</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f5f5f5;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }
            header {
                background-color: #2c3e50;
                color: white;
                padding: 20px 0;
                text-align: center;
            }
            h1 {
                margin: 0;
            }
            .input-section {
                background-color: white;
                padding: 20px;
                border-radius: 5px;
                margin: 20px 0;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            .visualization-section {
                background-color: white;
                padding: 20px;
                border-radius: 5px;
                margin: 20px 0;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            .chatbot-section {
                background-color: #ecf0f1;
                padding: 20px;
                border-radius: 10px;
                margin: 20px 0;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            .chatbot-input {
                width: 100%;
                padding: 10px;
                margin-bottom: 10px;
                border-radius: 5px;
                border: 1px solid #ddd;
            }
            .chatbot-submit {
                background-color: #2980b9;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
            }
            .chatbot-conversation {
                max-height: 400px;
                overflow-y: auto;
                margin-top: 20px;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: #f9f9f9;
            }
            .user-message {
                display: flex;
                justify-content: flex-end;
                margin-bottom: 10px;
            }
            .user-message-text {
                display: inline-block;
                max-width: 80%;
                background-color: #4da6ff;
                color: white;
                padding: 10px;
                border-radius: 10px;
                margin-left: auto;
                text-align: left;
            }
            .bot-message {
                margin-bottom: 15px;
            }
            .bot-icon {
                width: 30px;
                height: 30px;
                margin-right: 10px;
                vertical-align: top;
            }
            .bot-message-text {
                display: inline-block;
                max-width: 80%;
                background-color: #d5f5e3;
                padding: 10px;
                border-radius: 10px;
            }
            .feedback-buttons {
                margin-top: 5px;
            }
            .feedback-btn {
                border: none;
                background: none;
                cursor: pointer;
                font-size: 16px;
            }
            .feedback-btn:last-child {
                margin-left: 5px;
            }
            .guide-section {
                background-color: #ecf0f1;
                padding: 20px;
                border-radius: 10px;
                margin: 20px 0;
            }
            /* Slider styles */
            .slider-container {
                margin: 15px 0;
            }
            .slider-label {
                font-weight: bold;
                margin-bottom: 5px;
            }
            .slider {
                width: 100%;
            }
        </style>
    </head>
    """

def html_body_start():
    """Generate the start of HTML body section"""
    return """
    <body>
        <div class="container">
            <header>
                <h1>Climate Resilient Reservoir Management</h1>
            </header>
    """

def html_body_end():
    """Generate the end of HTML body section"""
    return """
        </div>
        <!-- This is where Dash will insert its scripts -->
    </body>
    </html>
    """

def html_template():
    """Generate the complete HTML template for the application"""
    return html_head() + html_body_start() + html_body_end()