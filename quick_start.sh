#!/bin/bash
# Quick Start Script for Tokyo Predictor Roulette Pro
# This script demonstrates CHECK Y TRABAJA (Check and Work)

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║        TOKYO PREDICTOR ROULETTE PRO - QUICK START           ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# CHECK - Verify the system works
echo "📋 STEP 1: CHECK - Running Tests..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 test_tokyo_predictor.py
TEST_RESULT=$?

if [ $TEST_RESULT -eq 0 ]; then
    echo ""
    echo "✅ CHECK PASSED - All tests successful!"
else
    echo ""
    echo "❌ CHECK FAILED - Please review the errors"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# TRABAJA - Run the application
echo "🚀 STEP 2: TRABAJA - Running Application..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 tokyo_predictor.py
APP_RESULT=$?

echo ""
if [ $APP_RESULT -eq 0 ]; then
    echo "✅ TRABAJA - Application is working!"
else
    echo "❌ Application encountered an error"
    exit 1
fi

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                  ✅ SUCCESS - ¡ÉXITO!                       ║"
echo "║                                                              ║"
echo "║  CHECK: ✅ Sistema verificado                               ║"
echo "║  TRABAJA: ✅ Aplicación funcional                           ║"
echo "║                                                              ║"
echo "║  ¡El sistema CHECK Y TRABAJA correctamente!                 ║"
echo "╚══════════════════════════════════════════════════════════════╝"
