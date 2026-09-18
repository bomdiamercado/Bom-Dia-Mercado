#!/usr/bin/env python3
import os
import sys
import re

def get_issue_data():
    """Extrai dados da issue do GitHub Actions"""
    title = os.getenv('ISSUE_TITLE', '').strip()
    body = os.getenv('ISSUE_BODY', '').strip()
    
    if not title or not body:
        print("ERROR: ISSUE_TITLE ou ISSUE_BODY vazios")
        sys.exit(1)
    
    return title, body

def parse_content(body):
    """Parse o conteúdo e identifica seções"""
    lines = body.split('\n')
    
    sections = {}
    current_section = None
    current_content = []
    
    for line in lines:
        # Detecta headers em MAIÚSCULAS (seções)
        if line.isupper() and len(line) > 3 and not line.startswith('###'):
            if current_section:
                sections[current_section] = '\n'.join(current_content).strip()
            current_section = line.strip()
            current_content = []
        else:
            if current_section:
                current_content.append(line)
            else:
                # Antes da primeira seção, é introdução
                if 'intro' not in sections:
                    current_content.append(line)
    
    if current_section:
        sections[current_section] = '\n'.join(current_content).strip()
    elif current_content:
        sections['intro'] = '\n'.join(current_content).strip()
    
    return sections

def format_section(title, content):
    """Formata uma seção em HTML"""
    if not content.strip():
        return f"""        <section class="bom-dia-section">
            <h3>{title}</h3>
            <p>Nenhum dado disponível. Insira o texto do boletim para que esta seção seja preenchida.</p>
        </section>"""
    
    # Converte quebras de linha em parágrafos
    paragraphs = content.split('\n\n')
    content_html = '\n            '.join([f'<p>{p.strip()}</p>' for p in paragraphs if p.strip()])
    
    return f"""        <section class="bom-dia-section">
            <h3>{title}</h3>
            {content_html}
        </section>"""

def generate_html(title, body):
    """Gera HTML bem estruturado com seções"""
    
    # Extrai data (primeira linha geralmente é a data)
    lines = body.split('\n')
    date_str = lines[0].strip() if lines else title
    
    # Parse seções
    sections = parse_content(body)
    
    # Constrói HTML das seções
    sections_html = []
    section_order = ['JUROS', 'DÓLAR', 'BOLSA', 'ELEIÇÕES', 'PETRÓLEO', 'PETROBRAS']
    
    for section_name in section_order:
        if section_name in sections:
            sections_html.append(format_section(section_name, sections[section_name]))
    
    # Qualquer outra seção não prevista
    for section_name, content in sections.items():
        if section_name not in section_order and section_name != 'intro':
            sections_html.append(format_section(section_name, content))
    
    intro_content = sections.get('intro', '')
    
    sections_html_str = '\n'.join(sections_html) if sections_html else """        <section class="bom-dia-section">
            <p>Conteúdo do boletim não disponível.</p>
        </section>"""
    
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
        html {{
            scroll-behavior: smooth;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.7;
            color: #2c3e50;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        header {{
            background: linear-gradient(135deg, #1a3a52 0%, #2c5aa0 100%);
            color: white;
            padding: 50px 30px;
            text-align: center;
        }}
        header h1 {{
            font-size: 2.8em;
            font-weight: 700;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 20px;
            letter-spacing: 2px;
        }}
        .sun {{
            font-size: 2em;
        }}
        header .date {{
            font-size: 1.3em;
            opacity: 0.95;
            font-weight: 300;
            letter-spacing: 0.5px;
        }}
        .content {{
            padding: 40px 30px;
        }}
        .bom-dia-section {{
            margin-bottom: 35px;
            padding-bottom: 25px;
            border-bottom: 2px solid #f0f0f0;
        }}
        .bom-dia-section:last-child {{
            border-bottom: none;
            margin-bottom: 0;
        }}
        .bom-dia-section h3 {{
            color: #f5a623;
            font-size: 1.4em;
            margin-bottom: 15px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            border-bottom: 3px solid #f5a623;
            padding-bottom: 10px;
        }}
        .bom-dia-section p {{
            margin-bottom: 12px;
            text-align: justify;
            font-size: 1.05em;
            line-height: 1.8;
        }}
        .bom-dia-section p:last-child {{
            margin-bottom: 0;
        }}
        footer {{
            background: #f8f9fa;
            text-align: center;
            padding: 20px;
            border-top: 1px solid #e0e0e0;
            color: #666;
            font-size: 0.95em;
        }}
        @media (max-width: 768px) {{
            header h1 {{
                font-size: 1.8em;
                gap: 10px;
            }}
            .sun {{
                font-size: 1.2em;
            }}
            .content {{
                padding: 20px;
            }}
            .bom-dia-section h3 {{
                font-size: 1.2em;
            }}
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
{sections_html_str}
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
