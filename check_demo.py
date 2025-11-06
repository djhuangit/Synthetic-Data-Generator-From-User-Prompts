#!/usr/bin/env python3
"""Quick diagnostic to check demo mode setup."""

import os
import sys

# Set demo mode
os.environ["DEMO_MODE"] = "true"

print("=" * 60)
print("Demo Mode Diagnostic")
print("=" * 60)

# Check 1: Environment
print("\n1. Environment Variables:")
print(f"   DEMO_MODE: {os.getenv('DEMO_MODE')}")
print(f"   OPENAI_API_KEY: {'Set' if os.getenv('OPENAI_API_KEY') else 'Not set (OK for demo)'}")

# Check 2: Config
print("\n2. Configuration:")
try:
    from src.core.config import settings
    print(f"   settings.DEMO_MODE: {settings.DEMO_MODE}")
    settings.validate_settings()
    print("   ✅ Config validation passed")
except Exception as e:
    print(f"   ❌ Config error: {e}")
    sys.exit(1)

# Check 3: Gradio
print("\n3. Gradio:")
try:
    import gradio as gr
    print(f"   ✅ Gradio version: {gr.__version__}")
except Exception as e:
    print(f"   ❌ Gradio import failed: {e}")
    sys.exit(1)

# Check 4: Gradio App
print("\n4. Gradio App:")
try:
    from src.frontend.gradio_app import app as gradio_app
    print(f"   ✅ Gradio app created")
except Exception as e:
    print(f"   ❌ Gradio app failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Check 5: FastAPI
print("\n5. FastAPI App:")
try:
    from main import app
    print(f"   ✅ FastAPI app created")

    # Check routes
    routes = [route.path for route in app.routes]
    has_gradio = any("/gradio" in path for path in routes)

    print(f"\n6. Routes Check:")
    print(f"   Total routes: {len(routes)}")
    print(f"   Has /gradio routes: {has_gradio}")

    if has_gradio:
        gradio_routes = [r for r in routes if "/gradio" in r]
        print(f"   Gradio routes found: {len(gradio_routes)}")
        print(f"   ✅ Gradio is mounted!")
    else:
        print(f"   ⚠️  Gradio routes not found")
        print(f"   Available routes: {routes[:10]}")

except Exception as e:
    print(f"   ❌ FastAPI check failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ All diagnostics passed!")
print("=" * 60)
print("\nTo run the server:")
print("  DEMO_MODE=true uv run uvicorn main:app --reload")
print("\nThen access:")
print("  http://localhost:8000/       (redirects to Gradio)")
print("  http://localhost:8000/gradio (Gradio UI)")
print("  http://localhost:8000/docs   (API docs)")
print("=" * 60)
