#!/usr/bin/env python3
"""
Script de validação pré-deployment
Verifica se todas as configurações estão corretas antes de rodar docker-compose
"""

import os
import json
from pathlib import Path

def check_file_exists(filepath, description):
    """Verifica se arquivo existe"""
    if os.path.exists(filepath):
        print(f"✅ {description}")
        return True
    else:
        print(f"❌ {description} - NÃO ENCONTRADO: {filepath}")
        return False

def check_syntax_python(filepath):
    """Verifica sintaxe Python"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            compile(f.read(), filepath, 'exec')
        return True
    except SyntaxError as e:
        print(f"❌ Erro de sintaxe em {filepath}: {e}")
        return False

def validate_requirements():
    """Valida requirements.txt"""
    files = [
        ("spleeter/backend/main.py", "API Principal"),
        ("spleeter/backend/queue/worker.py", "Worker Celery"),
        ("spleeter/backend/queue/celery_app.py", "Configuração Celery"),
        ("spleeter/backend/auth/auth.py", "Autenticação"),
        ("spleeter/backend/models/database.py", "Banco de Dados"),
        ("spleeter/backend/models/user.py", "Modelo de Usuário"),
        ("spleeter/backend/requirements.txt", "Dependências"),
        ("spleeter/backend/Dockerfile", "Dockerfile"),
        ("spleeter/backend/.dockerignore", ".dockerignore"),
        ("spleeter/backend/.env.example", ".env.example"),
        ("spleeter/docker-compose.yml", "Docker Compose"),
    ]
    
    print("\n" + "="*60)
    print("🔍 VALIDAÇÃO PRÉ-DEPLOYMENT")
    print("="*60)
    
    all_ok = True
    
    print("\n📁 Verificando Arquivos:")
    print("-" * 60)
    for filepath, description in files:
        if not check_file_exists(filepath, description):
            all_ok = False
    
    print("\n🐍 Validando Sintaxe Python:")
    print("-" * 60)
    python_files = [
        "spleeter/backend/main.py",
        "spleeter/backend/queue/worker.py",
        "spleeter/backend/queue/celery_app.py",
        "spleeter/backend/auth/auth.py",
        "spleeter/backend/models/database.py",
        "spleeter/backend/models/user.py",
    ]
    
    for filepath in python_files:
        if os.path.exists(filepath):
            if check_syntax_python(filepath):
                print(f"✅ {filepath}")
            else:
                all_ok = False
    
    print("\n📦 Verificando Requirements:")
    print("-" * 60)
    try:
        with open("spleeter/backend/requirements.txt", "r") as f:
            lines = f.readlines()
            req_count = len([l for l in lines if l.strip() and not l.startswith("#")])
            print(f"✅ {req_count} dependências encontradas")
    except:
        print("❌ Erro ao ler requirements.txt")
        all_ok = False
    
    print("\n🐳 Verificando Docker Compose:")
    print("-" * 60)
    try:
        # Validação básica sem yaml
        with open("spleeter/docker-compose.yml", "r") as f:
            content = f.read()
            if "services:" in content:
                print("✅ docker-compose.yml tem estrutura básica válida")
                if "redis:" in content and "api:" in content and "worker:" in content:
                    print("✅ Serviços encontrados: redis, api, worker")
                else:
                    print("⚠️  Alguns serviços esperados não encontrados")
            else:
                raise ValueError("docker-compose.yml sem seção 'services'")
    except Exception as e:
        print(f"❌ Erro ao validar docker-compose.yml: {e}")
        all_ok = False
    
    print("\n" + "="*60)
    if all_ok:
        print("✅ VALIDAÇÃO COMPLETA - PRONTO PARA DEPLOY!")
        print("="*60)
        print("\nExecute na pasta spleeter:")
        print("  docker-compose up --build")
    else:
        print("❌ EXISTEM PROBLEMAS A RESOLVER")
        print("="*60)
    
    return all_ok

if __name__ == "__main__":
    success = validate_requirements()
    exit(0 if success else 1)
