import json
import sys

TIPOS = {
    "clínica": ["clínica", "clinica", "consultório", "paciente", "fisioterap", "psicólog"],
    "restaurante": ["restaurante", "lanchonete", "padaria", "cardápio", "delivery"],
    "salão de beleza": ["salão", "barbearia", "estética", "manicure"],
"loja": ["loja", "produtos", "vendas"],
}

PALAVRAS_URGENTES = ["urgente", "o quanto antes", "essa semana", "amanhã", "hoje"]

JA_TEM_SITE = ["meu site", "tenho site", "tenho um site", "site atual", "site antigo"]


def ler_mensagem(caminho):
    with open(caminho, encoding="utf-8") as arquivo:
        return arquivo.read()


def descobrir_tipo(mensagem):
    texto = mensagem.lower()
    for tipo, palavras in TIPOS.items():
        for palavra in palavras:
            if palavra in texto:
                return tipo
    return "não informado"


def descobrir_urgencia(mensagem):
    texto = mensagem.lower()
    for palavra in PALAVRAS_URGENTES:
        if palavra in texto:
            return "alta"
    return "média"


def perguntas_faltantes(mensagem):
    texto = mensagem.lower()
    perguntas = []

    if "instagram" not in texto and "meu site" not in texto:
        perguntas.append("Você já tem site ou perfil em rede social?")

    if "r$" not in texto and "orçamento" not in texto and "valor" not in texto:
        perguntas.append("Qual faixa de investimento você tem em mente?")

    if "instagram" not in texto and "site" not in texto:
        perguntas.append("Você já tem site ou perfil em rede social?")

    if "whatsapp" not in texto and "agenda" not in texto:
        perguntas.append("Como o cliente deve entrar em contato: WhatsApp, formulário ou agenda?")

    return perguntas

def claude_simulado(mensagem):
    """Finge ser a API do Claude: mesmo formato de resposta, sem internet e sem custo."""
    perguntas = perguntas_faltantes(mensagem)
    rascunho = (
        "Olá, obrigada pela mensagem. Para montar uma proposta que faça sentido, "
        "preciso entender alguns pontos: " + " ".join(perguntas) + " MKLA Pixel."
    )
    return {
        "resumo": mensagem.strip()[:120],
        "tipo_negocio": descobrir_tipo(mensagem),
        "urgencia": descobrir_urgencia(mensagem),
        "perguntas_faltantes": perguntas,
        "rascunho_resposta": rascunho,
        "origem": "simulado",
    }


def analisar(mensagem, usar_api_real=False):
    if usar_api_real:
        raise NotImplementedError("A chamada real ao Claude ainda não foi escrita.")
    return claude_simulado(mensagem)

mensagem = ler_mensagem(sys.argv[1])
resultado = analisar(mensagem)
print(json.dumps(resultado, ensure_ascii=False, indent=2))