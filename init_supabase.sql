-- Supabase SQL Schema
-- Run this in your Supabase SQL Editor to create the required tables

-- Table for storing system prompts (with versioning)
CREATE TABLE IF NOT EXISTS prompts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table for storing editor prompts (with versioning)
CREATE TABLE IF NOT EXISTS editor_prompt (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table for storing training examples
CREATE TABLE IF NOT EXISTS training_examples (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_sequence JSONB NOT NULL,
    chat_history JSONB NOT NULL,
    consultant_reply TEXT NOT NULL,
    ai_reply TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_prompts_created_at ON prompts(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_editor_prompt_created_at ON editor_prompt(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_training_examples_created_at ON training_examples(created_at DESC);

