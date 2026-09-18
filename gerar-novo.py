#!/usr/bin/env python3
import os
import sys
import json
import re
from anthropic import Anthropic

def get_issue_data():
    """Extrai dados da issue do GitHub Actions"""
    title = os.getenv('ISSUE_TITLE', '')
    body = os.getenv('ISSUE_BODY', '')
    
    if not title or not body:
        print("ERROR: ISSUE_TITLE ou ISSUE_BODY vazios")
        sys.exit(1)
    
    return title, body

def generate_html_with_claude(title, body):
    """Usa Claude para gerar o HTML do relatório"""
    client = Anthropic()
    
    prompt = f"""Você é um expert em gerar HTML para relatórios financeiros em português.

Título da issue: {title}
Conteúdo do boletim:
{body}

Gere um HTML completo e bem formatado que:
1. Tenha um header com logo SVG do "Bom Dia Mercado" (um sol laranja)
2. Exiba o conteúdo do boletim de forma estruturada
3. Tenha seções para JUROS, DÓLAR, BOLSA, ELEIÇÕES, PETRÓLEO, PETROBRAS
4. Inclua um painel com cotações (Dólar, Ibovespa, Brent, T-Note)
5. Inclua a agenda do dia com emojis de bandeiras
6. Tenha cores profissionais (azul escuro #1a3a52, laranja #f5a623, branco)
7. Seja responsivo para mobile

Retorne APENAS o HTML completo, sem explicações. Comece com <!DOCTYPE html>"""
    
    try:
        message = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=4000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        html_content = message.content[0].text
        return html_content
    except Exception as e:
        print(f"ERROR na API Claude: {str(e)}")
        sys.exit(1)

def inject_metadata(html_content, title):
    """Injeta tags de meta dados e og:image no HTML"""
    # Extrai data do título (ex: "Sexta-feira, 18 de Setembro")
    date_str = title.replace("Bom Dia Mercado", "").strip()
    
    # Cria meta tags
    meta_tags = f"""    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Bom Dia Mercado - {date_str}">
    <meta property="og:title" content="Bom Dia Mercado — {date_str}">
    <meta property="og:description" content="Bom Dia Mercado - Relatório diário de mercado">
    <meta property="og:image" content="https://bomdiamercado.github.io/Bom-Dia-Mercado/preview.png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:type" content="article">
    <meta name="robots" content="noindex, nofollow">
    <meta name="twitter:card" content="summary_large_image">"""
    
    # Substitui ou injeta as meta tags
    if '<head>' in html_content:
        html_content = html_content.replace('<head>', f'<head>\n{meta_tags}')
    elif '<HEAD>' in html_content:
        html_content = html_content.replace('<HEAD>', f'<HEAD>\n{meta_tags}')
    else:
        # Se não tiver head, injeta após DOCTYPE
        html_content = html_content.replace('</head>', f'{meta_tags}\n</head>', 1)
    
    return html_content

def save_html(html_content, filename='index.html'):
    """Salva o HTML em arquivo"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✓ HTML salvo em {filename}")
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
    
    # Gera HTML com Claude
    print("Gerando HTML com Claude...")
    html_content = generate_html_with_claude(title, body)
    
    # Injeta meta dados
    html_content = inject_metadata(html_content, title)
    
    # Salva arquivo
    save_html(html_content)
    
    print("✓ Relatório gerado com sucesso!")

if __name__ == '__main__':
    main()
