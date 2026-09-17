import os, json, re, urllib.request

titulo = (os.environ.get("TITULO") or "").strip().lower()
texto  = os.environ.get("TEXTO") or ""

if any(p in titulo for p in ("cambio", "câmbio", "dolar", "dólar")):
    destino, arquivo_instr = "dolar.html", "instrucoes-cambio.txt"
else:
    destino, arquivo_instr = "index.html", "instrucoes-bomdia.txt"

instrucao = open(arquivo_instr, encoding="utf-8").read()
modelo = open("modelo-completo.html", encoding="utf-8").read()

prompt = (instrucao
          + "\n\n===== MODELO A PREENCHER =====\n\n" + modelo
          + "\n\n===== TEXTO DO BOLETIM =====\n\n" + texto)

req = urllib.request.Request(
    "https://api.anthropic.com/v1/messages",
    data=json.dumps({
        "model": "claude-sonnet-4-6",
        "max_tokens": 16000,
        "messages": [{"role": "user", "content": prompt}],
    }).encode("utf-8"),
    headers={
        "content-type": "application/json",
        "x-api-key": os.environ["ANTHROPIC_API_KEY"],
        "anthropic-version": "2023-06-01",
    },
)

with urllib.request.urlopen(req, timeout=300) as r:
    resposta = json.load(r)

html = "".join(b.get("text", "") for b in resposta["content"])
html = re.sub(r"^\s*```[a-z]*\s*", "", html)
html = re.sub(r"\s*```\s*$", "", html).strip()

if not html.lower().startswith("<!doctype"):
    raise SystemExit("A resposta nao comecou com <!DOCTYPE. Nada foi gravado.")

open(destino, "w", encoding="utf-8").write(html + "\n")
print("Gravado:", destino, len(html), "caracteres")
