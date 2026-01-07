#!/usr/bin/env python3
"""
MatVerse ACOA - Sistema Autônomo de Consciência Omega-Min

Ponto de entrada principal para executar o sistema completo.
"""

import argparse
import asyncio
import logging
import sys
from pathlib import Path

# Adiciona caminho do módulo
sys.path.insert(0, str(Path(__file__).parent))

from matverse import get_system_info


async def run_core():
    """Executa o módulo Core."""
    from matverse.core import StateManager, MeasurementEngine, Ledger, Gate
    from matverse.api import create_app

    logger = logging.getLogger(__name__)
    logger.info("Iniciando MatVerse Core...")

    # Inicializa componentes
    state = StateManager(node_id="matverse-node-001")
    engine = MeasurementEngine(node_id="matverse-node-001")
    ledger = Ledger(node_id="matverse-node-001", batch_size=10)
    gate = Gate(node_id="matverse-node-001")

    # Inicializa API
    app = create_app()

    logger.info("MatVerse Core iniciado")

    return app, state, engine, ledger, gate


async def run_all():
    """Executa todos os módulos."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    logger = logging.getLogger(__name__)

    # Banner
    info = get_system_info()
    print("=" * 60)
    print(f"MatVerse ACOA v{info['version']}")
    print(f"Author: {info['author']}")
    print("=" * 60)
    print(f"Módulos disponíveis: {', '.join(info['modules'])}")
    print("=" * 60)

    logger.info("Iniciando sistema MatVerse ACOA...")

    try:
        # Core + API
        await run_core()

        logger.info("Sistema MatVerse ACOA iniciado com sucesso!")

        # Mantém running
        while True:
            await asyncio.sleep(60)

    except KeyboardInterrupt:
        logger.info("Encerrando sistema...")
    except Exception as e:
        logger.error(f"Erro fatal: {e}")
        raise


async def run_core_only():
    """Executa apenas o Core e mantém o processo ativo."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    logger = logging.getLogger(__name__)
    logger.info("Iniciando MatVerse Core (modo isolado)...")

    try:
        await run_core()
        logger.info("MatVerse Core iniciado com sucesso!")

        while True:
            await asyncio.sleep(60)

    except KeyboardInterrupt:
        logger.info("Encerrando MatVerse Core...")
    except Exception as e:
        logger.error(f"Erro fatal no Core: {e}")
        raise


async def run_android_packager(args):
    """Executa o módulo de empacotamento Android."""
    from matverse.packager.android import AndroidPackager, AndroidPackagerConfig

    logger = logging.getLogger(__name__)
    logger.info("Iniciando módulo de empacotamento Android...")

    # Configuração
    config = AndroidPackagerConfig(
        node_id=args.node_id,
        project_root=Path(args.project),
        module_name=args.module,
        build_type=args.type,
        output_dir=Path(args.output),
        android_home=Path(args.android_home) if args.android_home else None,
        keystore_path=Path(args.keystore) if args.keystore else None,
        keystore_password=args.ks_pass,
        key_alias=args.key_alias,
        key_password=args.key_pass,
    )

    # Cria packager e executa
    packager = AndroidPackager(config)
    receipt = packager.package(
        skip_build=args.skip_build,
        skip_align=args.skip_align,
        skip_sign=args.skip_sign,
    )

    logger.info("Empacotamento Android concluído!")
    return receipt


def main():
    """Ponto de entrada principal."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    parser = argparse.ArgumentParser(
        description="MatVerse ACOA - Sistema Autônomo de Consciência Omega-Min",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")

    subparsers = parser.add_subparsers(dest="command", help="Comandos disponíveis")

    # Comando 'run' - Executa o sistema completo
    run_parser = subparsers.add_parser("run", help="Executa o sistema completo")
    run_parser.set_defaults(func=lambda a: asyncio.run(run_all()))

    # Comando 'core' - Executa apenas o módulo Core
    core_parser = subparsers.add_parser("core", help="Executa o módulo Core")
    core_parser.set_defaults(func=lambda a: asyncio.run(run_core_only()))

    # Comando 'android' - Empacotamento Android
    android_parser = subparsers.add_parser(
        "android",
        help="Empacotamento Android",
        description="Orquestra build, assinatura e distribuição de APKs",
    )
    android_parser.add_argument(
        "--project",
        default=".",
        help="Raiz do projeto Android (default: .)",
    )
    android_parser.add_argument(
        "--module",
        default="app",
        help="Nome do módulo (default: app)",
    )
    android_parser.add_argument(
        "--type",
        default="release",
        choices=["debug", "release"],
        help="Tipo de build (default: release)",
    )
    android_parser.add_argument(
        "--output",
        default="dist",
        help="Diretório de saída (default: dist)",
    )
    android_parser.add_argument(
        "--android-home",
        default=None,
        help="Caminho do ANDROID_HOME/ANDROID_SDK_ROOT",
    )
    android_parser.add_argument(
        "--keystore",
        default=None,
        help="Caminho do keystore para assinatura",
    )
    android_parser.add_argument(
        "--key-alias",
        default=None,
        help="Alias da chave no keystore",
    )
    android_parser.add_argument(
        "--ks-pass",
        default=None,
        help="Senha do keystore",
    )
    android_parser.add_argument(
        "--key-pass",
        default=None,
        help="Senha da chave",
    )
    android_parser.add_argument(
        "--skip-build",
        action="store_true",
        help="Pula a etapa de build",
    )
    android_parser.add_argument(
        "--skip-align",
        action="store_true",
        help="Pula a etapa de alinhamento",
    )
    android_parser.add_argument(
        "--skip-sign",
        action="store_true",
        help="Pula a etapa de assinatura",
    )
    android_parser.add_argument(
        "--node-id",
        default="matverse-android-packager",
        help="ID do nó (default: matverse-android-packager)",
    )
    android_parser.set_defaults(func=lambda a: asyncio.run(run_android_packager(a)))

    # Comando 'info' - Exibe informações do sistema
    info_parser = subparsers.add_parser("info", help="Exibe informações do sistema")
    info_parser.set_defaults(func=lambda a: print_system_info())

    # Parse argumentos
    args = parser.parse_args()

    if not args.command:
        # Se nenhum comando, exibe ajuda
        parser.print_help()
        sys.exit(1)

    # Executa comando
    args.func(args)


def print_system_info():
    """Exibe informações do sistema."""
    info = get_system_info()
    print("=" * 60)
    print(f"MatVerse ACOA v{info['version']}")
    print(f"Author: {info['author']}")
    print("=" * 60)
    print(f"Modules: {', '.join(info['modules'])}")
    print(f"Python: {sys.version}")
    print(f"Platform: {sys.platform}")
    print("=" * 60)


if __name__ == "__main__":
    main()
