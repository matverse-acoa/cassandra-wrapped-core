#!/bin/bash
set -euo pipefail

echo "=========================================="
echo "MatVerse ACOA - Android Packager Setup"
echo "=========================================="

info() {
    echo "[INFO] $1"
}

warn() {
    echo "[WARN] $1"
}

error() {
    echo "[ERROR] $1"
}

info "Verificando Python..."
if ! command -v python3 >/dev/null 2>&1; then
    error "Python 3 não encontrado. Instale Python 3.11+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
info "Python encontrado: $PYTHON_VERSION"

info "Verificando Android SDK..."
if [ -z "${ANDROID_HOME:-}" ] && [ -z "${ANDROID_SDK_ROOT:-}" ]; then
    warn "ANDROID_HOME/ANDROID_SDK_ROOT não definido."
else
    SDK_PATH=${ANDROID_HOME:-$ANDROID_SDK_ROOT}
    info "Android SDK: $SDK_PATH"

    if [ ! -d "$SDK_PATH" ]; then
        error "Diretório do SDK não existe: $SDK_PATH"
        exit 1
    fi

    if [ -d "$SDK_PATH/build-tools" ]; then
        BUILD_TOOLS=$(ls "$SDK_PATH/build-tools" | tail -1)
        info "Build Tools mais recente: $BUILD_TOOLS"
    else
        warn "Build Tools não encontrado em $SDK_PATH/build-tools"
    fi
fi

info "Verificando estrutura do projeto..."
REQUIRED_DIRS=(
    "matverse"
    "matverse/packager"
)

for dir in "${REQUIRED_DIRS[@]}"; do
    if [ ! -d "$dir" ]; then
        error "Diretório necessário não encontrado: $dir"
        exit 1
    fi
    info "Diretório encontrado: $dir"
done

REQUIRED_FILES=(
    "matverse/__init__.py"
    "matverse/packager/__init__.py"
    "matverse/packager/transport.py"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        error "Arquivo necessário não encontrado: $file"
        exit 1
    fi
    info "Arquivo encontrado: $file"
done

info "Instalando MatVerse ACOA em modo desenvolvimento..."
python3 -m pip install -e .

info "Setup concluído."
