#!/usr/bin/env python3
"""
Convert hardware_options.md to PDF
"""

import markdown2
import os

def markdown_to_html(markdown_file, output_html):
    """Convert markdown file to HTML with formatting"""
    
    # Read the markdown file
    with open(markdown_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Convert markdown to HTML
    html_content = markdown2.markdown(
        markdown_content, 
        extras=['fenced-code-blocks', 'tables', 'header-ids', 'toc']
    )
    
    # Add CSS styling for better appearance
    css_styles = """
    body {
        font-family: Arial, sans-serif;
        font-size: 12pt;
        line-height: 1.6;
        color: #333;
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
    }
    
    h1 {
        color: #2c3e50;
        border-bottom: 3px solid #3498db;
        padding-bottom: 10px;
        font-size: 24pt;
        margin-top: 30px;
    }
    
    h2 {
        color: #34495e;
        border-bottom: 2px solid #95a5a6;
        padding-bottom: 8px;
        font-size: 18pt;
        margin-top: 30px;
        page-break-before: avoid;
    }
    
    h3 {
        color: #2c3e50;
        font-size: 14pt;
        margin-top: 25px;
        page-break-after: avoid;
    }
    
    h4 {
        color: #7f8c8d;
        font-size: 12pt;
        font-weight: bold;
        margin-top: 20px;
    }
    
    code {
        background-color: #f8f9fa;
        padding: 2px 4px;
        border-radius: 3px;
        font-family: 'Courier New', monospace;
        font-size: 10pt;
        color: #e74c3c;
    }
    
    pre {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 5px;
        padding: 15px;
        overflow-x: auto;
        font-family: 'Courier New', monospace;
        font-size: 9pt;
        line-height: 1.4;
        page-break-inside: avoid;
    }
    
    pre code {
        background-color: transparent;
        padding: 0;
        color: #2c3e50;
    }
    
    table {
        border-collapse: collapse;
        width: 100%;
        margin: 15px 0;
        page-break-inside: avoid;
    }
    
    th, td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
    }
    
    th {
        background-color: #f2f2f2;
        font-weight: bold;
    }
    
    ul, ol {
        margin: 10px 0;
        padding-left: 25px;
    }
    
    li {
        margin: 5px 0;
    }
    
    strong {
        color: #2c3e50;
        font-weight: bold;
    }
    
    a {
        color: #3498db;
        text-decoration: none;
    }
    
    a:hover {
        text-decoration: underline;
    }
    
    /* Print styles for PDF conversion */
    @media print {
        body {
            margin: 0;
            padding: 15mm;
        }
        
        h1 {
            page-break-before: auto;
        }
        
        h1, h2, h3, h4 {
            page-break-after: avoid;
        }
        
        pre, table {
            page-break-inside: avoid;
        }
        
        a {
            color: #000;
            text-decoration: none;
        }
        
        @page {
            margin: 20mm;
            @top-center {
                content: "Simple Antenna Analyzer - Hardware Options";
                font-size: 10pt;
                color: #666;
            }
            @bottom-center {
                content: counter(page);
                font-size: 10pt;
                color: #666;
            }
        }
    }
    """
    
    # Combine HTML with CSS
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simple Antenna Analyzer - Hardware Options</title>
    <style>{css_styles}</style>
</head>
<body>
    {html_content}
</body>
</html>"""
    
    # Save HTML file
    try:
        with open(output_html, 'w', encoding='utf-8') as f:
            f.write(full_html)
        print(f"Successfully converted {markdown_file} to {output_html}")
        return True
    except Exception as e:
        print(f"Error converting to HTML: {e}")
        return False

def try_html_to_pdf_conversion(html_file, pdf_file):
    """Try various methods to convert HTML to PDF"""
    
    print("\nAttempting PDF conversion...")
    
    # Method 1: Try using pdfkit (requires wkhtmltopdf)
    try:
        import pdfkit
        pdfkit.from_file(html_file, pdf_file)
        print(f"✓ Successfully created PDF using pdfkit: {pdf_file}")
        return True
    except ImportError:
        print("- pdfkit not available")
    except Exception as e:
        print(f"- pdfkit failed: {e}")
    
    # Method 2: Try using weasyprint
    try:
        from weasyprint import HTML
        HTML(filename=html_file).write_pdf(pdf_file)
        print(f"✓ Successfully created PDF using WeasyPrint: {pdf_file}")
        return True
    except ImportError:
        print("- WeasyPrint not available")
    except Exception as e:
        print(f"- WeasyPrint failed: {e}")
    
    # Method 3: Try using pyppeteer (headless Chrome)
    try:
        import asyncio
        from pyppeteer import launch
        
        async def convert_with_pyppeteer():
            browser = await launch()
            page = await browser.newPage()
            await page.goto(f'file://{os.path.abspath(html_file)}')
            await page.pdf({'path': pdf_file, 'format': 'A4'})
            await browser.close()
        
        asyncio.get_event_loop().run_until_complete(convert_with_pyppeteer())
        print(f"✓ Successfully created PDF using pyppeteer: {pdf_file}")
        return True
    except ImportError:
        print("- pyppeteer not available")
    except Exception as e:
        print(f"- pyppeteer failed: {e}")
    
    return False

if __name__ == "__main__":
    # Input and output files
    input_file = "hardware_options.md"
    html_file = "Hardware_Options_Guide.html"
    pdf_file = "Hardware_Options_Guide.pdf"
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found!")
        exit(1)
    
    # Convert to HTML
    success = markdown_to_html(input_file, html_file)
    
    if success:
        print(f"\n✓ HTML created successfully: {html_file}")
        print(f"File size: {os.path.getsize(html_file) / 1024:.1f} KB")
        
        # Try to convert to PDF
        pdf_success = try_html_to_pdf_conversion(html_file, pdf_file)
        
        if pdf_success:
            print(f"\n✓ PDF created successfully: {pdf_file}")
            print(f"PDF file size: {os.path.getsize(pdf_file) / 1024:.1f} KB")
        else:
            print(f"\n⚠ PDF conversion failed, but HTML file is ready!")
            print(f"\nManual PDF conversion options:")
            print(f"1. Open {html_file} in your browser and use 'Print to PDF'")
            print(f"2. Install wkhtmltopdf and run: wkhtmltopdf {html_file} {pdf_file}")
            print(f"3. Use online converters like https://html-pdf-converter.com/")
            print(f"\nThe HTML file is optimized for PDF printing with proper styling.")
    else:
        print("Failed to create HTML file")
        exit(1) 