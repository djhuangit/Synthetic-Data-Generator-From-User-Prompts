#!/bin/bash
# Test if the server is running correctly

echo "=========================================="
echo "Testing Gradio Server"
echo "=========================================="
echo ""

# Test health endpoint
echo "1. Testing health endpoint..."
HEALTH=$(curl -s http://localhost:8000/health)
echo "$HEALTH" | jq '.' 2>/dev/null || echo "$HEALTH"
echo ""

# Check demo mode
DEMO_MODE=$(echo "$HEALTH" | jq -r '.demo_mode' 2>/dev/null)
if [ "$DEMO_MODE" = "true" ]; then
    echo "   ✅ Demo mode is enabled"
else
    echo "   ⚠️  Demo mode: $DEMO_MODE"
    echo "   Did you start with DEMO_MODE=true?"
fi
echo ""

# Test root redirect
echo "2. Testing / (root)..."
ROOT=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/)
echo "   Status: $ROOT"
if [ "$ROOT" = "307" ]; then
    echo "   ✅ Redirects to /gradio"
else
    echo "   ⚠️  Expected 307, got $ROOT"
fi
echo ""

# Test /gradio
echo "3. Testing /gradio..."
GRADIO=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/gradio)
echo "   Status: $GRADIO"
if [ "$GRADIO" = "200" ]; then
    echo "   ✅ Gradio is accessible!"
    echo ""
    echo "=========================================="
    echo "✅ Server is working correctly!"
    echo "=========================================="
    echo ""
    echo "Open in your browser:"
    echo "  http://localhost:8000/"
    echo "  http://localhost:8000/gradio"
    echo ""
    echo "If you still see 'Not Found':"
    echo "  1. Clear your browser cache (Ctrl+Shift+R)"
    echo "  2. Try incognito/private mode"
    echo "  3. Try a different browser"
else
    echo "   ❌ Not Found (Status: $GRADIO)"
    echo ""
    echo "=========================================="
    echo "❌ Problem detected!"
    echo "=========================================="
    echo ""
    echo "Possible causes:"
    echo "  1. Server not started with DEMO_MODE=true"
    echo "  2. Server not fully started yet"
    echo "  3. Gradio failed to mount"
    echo ""
    echo "Try:"
    echo "  1. Stop the server (Ctrl+C)"
    echo "  2. Restart: DEMO_MODE=true uv run uvicorn main:app --reload"
    echo "  3. Wait for: '✅ Gradio interface mounted at /gradio'"
    echo "  4. Run this script again"
fi
echo ""
