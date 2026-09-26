#!/usr/bin/env bash
# Injeta no contexto da sessão a configuração que o PO preencheu ao ativar o
# plugin (userConfig). Os valores chegam pelos argumentos (substituição
# ${user_config.*}) ou, como alternativa, pelas variáveis CLAUDE_PLUGIN_OPTION_*.
# Uso: config-context.sh <confluence_site> <confluence_spaces> <doc_space_key> <doc_root_folder_id>

clean() {
  local v="$1"
  # Argumento não substituído (placeholder literal) conta como vazio.
  case "$v" in *'user_config.'*) v="" ;; esac
  printf '%s' "$v" | tr -d '[:space:]'
}

site="$(clean "${1:-}")"
spaces="$(clean "${2:-}")"
doc_space="$(clean "${3:-}")"
doc_folder="$(clean "${4:-}")"
[ -z "$site" ] && site="$(clean "${CLAUDE_PLUGIN_OPTION_CONFLUENCE_SITE:-}")"
[ -z "$spaces" ] && spaces="$(clean "${CLAUDE_PLUGIN_OPTION_CONFLUENCE_SPACES:-}")"
[ -z "$doc_space" ] && doc_space="$(clean "${CLAUDE_PLUGIN_OPTION_DOC_SPACE_KEY:-}")"
[ -z "$doc_folder" ] && doc_folder="$(clean "${CLAUDE_PLUGIN_OPTION_DOC_ROOT_FOLDER_ID:-}")"

show() { printf '%s' "${1:-(não configurado)}"; }

echo "[product-tools] Configuração do PO:"
echo "[product-tools]   confluence_site = $(show "$site")"
echo "[product-tools]   confluence_spaces (base de conhecimento do /refine) = $(show "$spaces")"
echo "[product-tools]   doc_space_key (destino do /document-feature) = $(show "$doc_space")"
echo "[product-tools]   doc_root_folder_id (folder dos domínios no /document-feature) = $(show "$doc_folder")"
exit 0
