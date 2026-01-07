#!/usr/bin/env python3
"""
Android Packager CLI - Entry Point

Ponto de entrada dedicado para o módulo de empacotamento Android.
Suporta execução via `python -m matverse.packager` ou `matverse-android`.
"""

import logging
import sys


CLI_HELP = """
MatVerse ACOA - Android Packager

Empacotamento Android automatizado com suporte a:
  - Build de APKs via Gradle
  - Alinhamento de arquivos APK
  - Assinatura com keystore
  - Verificação de assinaturas
  - Geração de receipts

 USO:
    python -m matverse.packager [opções]
    matverse-android [opções]

 OPÇÕES DE BUILD:
    --project PATH      Raiz do projeto Android (default: .)
    --module NAME       Nome do módulo (default: app)
    --type TYPE         Tipo de build: debug|release (default: release)
    --out PATH          Diretório de saída (default: dist)

 OPÇÕES DO SDK:
    --android-home PATH Caminho do ANDROID_HOME/ANDROID_SDK_ROOT

 OPÇÕES DE ASSINATURA:
    --keystore PATH     Caminho do keystore (.jks ou .keystore)
    --key-alias NAME    Alias da chave no keystore
    --ks-pass PASS      Senha do keystore
    --key-pass PASS     Senha da chave (opcional se igual à do keystore)

 OPÇÕES DE CONTROLE:
    --skip-build        Pula a etapa de build (usa APK existente)
    --skip-align        Pula a etapa de alinhamento
    --skip-sign         Pula a etapa de assinatura
    --node-id ID        ID do nó para logs (default: android-packager)

 VARIÁVEIS DE AMBIENTE:
    ANDROID_HOME        Caminho do Android SDK
    MV_KEYSTORE         Caminho do keystore
    MV_KEYSTORE_PASS    Senha do keystore
    MV_KEY_ALIAS        Alias da chave
    MV_KEY_PASS         Senha da chave

 EXEMPLOS:
    # Build release com assinatura
    matverse-android --project ./android-app --type release \\
        --keystore release.keystore --key-alias myapp \\
        --ks-pass mypassword

    # Build debug (sem assinatura)
    matverse-android --project ./android-app --type debug

    # Re-assinar APK existente
    matverse-android --project ./android-app --skip-build \\
        --keystore release.keystore --key-alias myapp
"""


def main():
    """
    Ponto de entrada para empacotamento Android.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    logger = logging.getLogger(__name__)

    # Verifica se deve exibir ajuda
    if any(arg in ("--help", "-h") for arg in sys.argv[1:]):
        print(CLI_HELP)
        return

    # Executa packager
    try:
        from matverse.packager.android.packager import AndroidPackager
        packager = AndroidPackager.from_command_line()
        receipt = packager.package()

        logger.info("=" * 60)
        logger.info("EMPACOTAMENTO ANDROID CONCLUÍDO COM SUCESSO")
        logger.info("=" * 60)
        logger.info(f"Receipt: {receipt.get('receipt_id', 'N/A')}")
        logger.info(f"Artefatos: {len(receipt.get('artifacts', []))}")

    except ImportError as e:
        logger.error("Não foi possível importar o empacotador Android.")
        logger.error(f"Detalhes: {e}")
        logger.error(
            "Verifique se o pacote MatVerse está instalado ou execute via "
            "`python -m matverse.packager` a partir da raiz do repositório."
        )
        sys.exit(1)
    except FileNotFoundError as e:
        logger.error(f"Ferramenta não encontrada: {e}")
        logger.error("Verifique se o Android SDK está instalado e no PATH")
        sys.exit(1)
    except ValueError as e:
        logger.error(f"Erro de configuração: {e}")
        sys.exit(1)
    except RuntimeError as e:
        logger.error(f"Erro no empacotamento: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Operação cancelada pelo usuário")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Erro inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
