#!/bin/bash
# Quick test script to verify environment variables

echo "Checking environment variables..."
echo ""

if [ -z "$GEMINI_API_KEY" ]; then
    echo "❌ GEMINI_API_KEY is NOT set"
else
    echo "✅ GEMINI_API_KEY is set (length: ${#GEMINI_API_KEY})"
fi

if [ -z "$SUPABASE_URL" ]; then
    echo "❌ SUPABASE_URL is NOT set"
else
    echo "✅ SUPABASE_URL is set: $SUPABASE_URL"
fi

if [ -z "$SUPABASE_ANON_KEY" ]; then
    echo "❌ SUPABASE_ANON_KEY is NOT set"
else
    echo "✅ SUPABASE_ANON_KEY is set (length: ${#SUPABASE_ANON_KEY})"
fi

echo ""
echo "To set them, run:"
echo "  export GEMINI_API_KEY=your_key_here"
echo "  export SUPABASE_URL=https://your-project.supabase.co"
echo "  export SUPABASE_ANON_KEY=your_anon_key_here"
