#!/usr/bin/env python3
import os
import sys
import re
from datetime import datetime

def get_issue_data():
    """Extrai dados da issue do GitHub Actions"""
    title = os.getenv('ISSUE_TITLE', '').strip()
    body = os.getenv('ISSUE_BODY', '').strip()
    
    if not title or not body:
        print("ERROR: ISSUE_TITLE ou ISSUE_BODY vazios")
        sys.exit(1)
    
    return title, body

def generate_html(title, body):
    """Gera HTML estruturado com o conteúdo do boletim"""
    
    # Extrai data do título (ex: "Sexta-feira, 18 de Setembro de 2026")
    date_match = re.search(r'(\w+day|\w+),?\s+(\d{1,2})\s+de\s+(\w+)\s+(?:de\s+)?(\d{4})?', title, re.IGNORECASE)
    date_str = title
    if date_match:
        date_str = f"{date_match.group(1)}, {date_match.group(2)} de {date_match.group(3)}"
    
    # Converte o body em HTML (substitui quebras de linha por <br>)
    body_html = body.replace('\n\n', '</p><p>').replace('\n', '<br>')
    body_html = f'<p>{body_html}</p>'
    
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Bom Dia Mercado - {date_str}">
    <meta property="og:title" content="Bom Dia Mercado — {date_str}">
    <meta property="og:description" content="Relatório diário de mercado">
    <meta property="og:image" content="https://bomdiamercado.github.io/Bom-Dia-Mercado/preview.png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:type" content="article">
    <meta name="robots" content="noindex, nofollow">
    <meta name="twitter:card" content="summary_large_image">
    <title>Bom Dia Mercado — {date_str}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background: white;
        }}
        header {{
            background: linear-gradient(135deg, #1a3a52 0%, #2c5aa0 100%);
            color: white;
            padding: 40px 20px;
            text-align: center;
            border-radius: 8px;
            margin-bottom: 30px;
        }}
        header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
        }}
        .sun {{
            font-size: 1.5em;
        }}
        header .date {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        .content {{
            font-size: 1.1em;
            line-height: 1.8;
        }}
        .content p {{
            margin-bottom: 15px;
            text-align: justify;
        }}
        .content br {{
            content: "";
            display: block;
            margin-bottom: 10px;
        }}
        footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            color: #666;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>
                <span class="sun">☀️</span>
                <span>BOM DIA MERCADO</span>
            </h1>
            <div class="date">{date_str}</div>
        </header>
        
        <div class="content">
            {body_html}
        </div>
        
        <footer>
            <p>Bom Dia Mercado · {date_str}</p>
        </footer>
    </div>
</body>
</html>"""
    
    return html

def save_html(html_content, filename='index.html'):
    """Salva o HTML em arquivo"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✓ HTML salvo em {filename}")
        print(f"✓ Tamanho: {len(html_content)} bytes")
        return True
    except Exception as e:
        print(f"ERROR ao salvar {filename}: {str(e)}")
        sys.exit(1)

def main():
    print("Iniciando geração de relatório...")
    
    # Pega dados da issue
    title, body = get_issue_data()
    print(f"✓ Título: {title}")
    print(f"✓ Corpo: {len(body)} caracteres")
    
    # Gera HTML
    print("Gerando HTML...")
    html_content = generate_html(title, body)
    
    # Salva arquivo
    save_html(html_content)
    
    print("✓ Relatório gerado com sucesso!")

if __name__ == '__main__':
    main()
