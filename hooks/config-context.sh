#!/usr/bin/env bash
# Injeta no contexto da sessão a configuração que o PO preencheu ao ativar o
# plugin (userConfig). Prioridade: variáveis CLAUDE_PLUGIN_OPTION_* (exportadas
# pelo Claude para processos de hook); como alternativa, os argumentos
# (substituição ${user_config.*}).
# Uso: config-context.sh [confluence_site] [confluence_spaces] [doc_space_key] [doc_root_folder_id]

# Normaliza um valor: placeholder não substituído conta como vazio; remove
# espaços e quebras de linha/caracteres de controle (o valor vira contexto do
# modelo, então não pode carregar texto arbitrário multilinha).
clean() {
  local v="$1"
  case "$v" in *'user_config.'*) v="" ;; esac
  printf '%s' "$v" | tr -d '[:space:][:cntrl:]'
}

# pick <variável de ambiente> <argumento posicional>
pick() {
  local v
  v="$(clean "${!1:-}")"
  [ -z "$v" ] && v="$(clean "${2:-}")"
  printf '%s' "$v"
}

site="$(pick CLAUDE_PLUGIN_OPTION_CONFLUENCE_SITE "${1:-}")"
spaces="$(pick CLAUDE_PLUGIN_OPTION_CONFLUENCE_SPACES "${2:-}")"
doc_space="$(pick CLAUDE_PLUGIN_OPTION_DOC_SPACE_KEY "${3:-}")"
doc_folder="$(pick CLAUDE_PLUGIN_OPTION_DOC_ROOT_FOLDER_ID "${4:-}")"

show() { printf '%s' "${1:-(não configurado)}"; }

echo "[product-tools] Configuração do PO:"
echo "[product-tools]   confluence_site = $(show "$site")"
echo "[product-tools]   confluence_spaces (base de conhecimento do /refine) = $(show "$spaces")"
echo "[product-tools]   doc_space_key (destino do /document-feature) = $(show "$doc_space")"
echo "[product-tools]   doc_root_folder_id (folder dos domínios no /document-feature) = $(show "$doc_folder")"
exit 0
