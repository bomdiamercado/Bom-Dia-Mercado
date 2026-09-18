import os
import re
import sys
import anthropic

TITULO = os.environ.get("TITULO", "")
TEXTO  = os.environ.get("TEXTO", "")

# Detecta qual arquivo gerar
titulo_lower = TITULO.lower()
if any(p in titulo_lower for p in ["cambio", "câmbio", "dolar", "dólar"]):
    arquivo_saida  = "dolar.html"
    arquivo_instr  = "instrucoes-cambio.txt"
    og_image       = "https://bomdiamercado.github.io/Bom-Dia-Mercado/dolar-preview.png"
else:
    arquivo_saida  = "index.html"
    arquivo_instr  = "instrucoes-bomdia.txt"
    og_image       = "https://bomdiamercado.github.io/Bom-Dia-Mercado/preview.png"

# Lê instruções e modelo
with open(arquivo_instr, encoding="utf-8") as f:
    instrucoes = f.read()

with open("modelo-completo.html", encoding="utf-8") as f:
    modelo = f.read()

# Monta prompt
prompt = f"""Instruções:
{instrucoes}

Modelo HTML de referência:
{modelo}

Texto do boletim de hoje:
{TEXTO}

Gere o HTML completo do relatório de hoje seguindo as instruções e o modelo acima."""

# Chama API Anthropic
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=16000,
    messages=[{"role": "user", "content": prompt}]
)

html = message.content[0].text

# Remove cercas de código se existirem
html = re.sub(r"^```[a-z]*\n?", "", html.strip())
html = re.sub(r"\n?```$", "", html.strip())

# Garante que começa com <!doctype
if not html.lower().startswith("<!doctype"):
    print("ERRO: resposta não é HTML válido", file=sys.stderr)
    sys.exit(1)

# ── INJEÇÃO GARANTIDA DO og:image ──────────────────────────────
OG_IMAGE_TAG = f"""  <meta property="og:image" content="{og_image}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">"""

# Remove qualquer og:image já existente (evita duplicata)
html = re.sub(r'\s*<meta property="og:image[^"]*"[^>]*>', "", html)

# Injeta logo após og:type ou og:site_name ou twitter:card, o que aparecer primeiro
for ancora in ['og:type"', 'og:site_name"', 'twitter:card"']:
    padrao = rf'(<meta property="{ancora}[^>]*>)'
    if re.search(padrao, html):
        html = re.sub(padrao, r'\1\n' + OG_IMAGE_TAG, html, count=1)
        break
# ────────────────────────────────────────────────────────────────

# Salva arquivo
with open(arquivo_saida, "w", encoding="utf-8") as f:
    f.write(html)

print(f"✅ {arquivo_saida} gerado com sucesso.")
