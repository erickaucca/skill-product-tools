#!/usr/bin/env bash
# Injeta no contexto da sessão a configuração de Confluence que o PO preencheu
# ao ativar o plugin (userConfig). O valor chega pelos argumentos (substituição
# ${user_config.*}) ou, como alternativa, pelas variáveis CLAUDE_PLUGIN_OPTION_*.

clean() {
  local v="$1"
  # Argumento não substituído (placeholder literal) conta como vazio.
  case "$v" in *'user_config.'*) v="" ;; esac
  printf '%s' "$v" | tr -d '[:space:]'
}

spaces="$(clean "${1:-}")"
site="$(clean "${2:-}")"
[ -z "$spaces" ] && spaces="$(clean "${CLAUDE_PLUGIN_OPTION_CONFLUENCE_SPACES:-}")"
[ -z "$site" ] && site="$(clean "${CLAUDE_PLUGIN_OPTION_CONFLUENCE_SITE:-}")"

if [ -n "$spaces" ]; then
  echo "[product-tools] Configuração do PO: espaço(s) do Confluence da base de conhecimento do /refine = ${spaces}"
  [ -n "$site" ] && echo "[product-tools] Site do Confluence = ${site}"
else
  echo "[product-tools] Nenhum espaço do Confluence configurado para o /refine (configuração do plugin em branco)."
fi
exit 0
