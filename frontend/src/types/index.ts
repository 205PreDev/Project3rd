// User Types
export interface User {
  id: number;
  email: string;
  full_name?: string;
  credits: number;
  created_at: string;
  updated_at: string;
}

// Project Types
export interface Project {
  id: number;
  user_id: number;
  name: string;
  description?: string;
  created_at: string;
  updated_at: string;
}

export interface ProjectCreate {
  name: string;
  description?: string;
}

// Image Types
export interface Image {
  id: number;
  project_id: number;
  user_id: number;
  original_url: string;
  processed_url?: string;
  style?: string;
  caption?: string;
  caption_metadata?: {
    tone?: string;
    length?: string;
    include_hashtags?: boolean;
    hashtags?: string[];
    generated_at?: string;
  };
  quality_score?: number;
  created_at: string;
  updated_at: string;
}

export interface ImageUploadResponse {
  image_id: number;
  original_url: string;
  message: string;
}

export interface CaptionGenerateRequest {
  image_id: number;
  tone?: 'formal' | 'casual' | 'friendly';
  length?: 'short' | 'medium' | 'long';
  include_hashtags?: boolean;
}

export interface CaptionGenerateResponse {
  image_id: number;
  caption: string;
  caption_metadata: Record<string, any>;
  message: string;
}

// Onboarding Types
export interface OnboardingProgress {
  user_id: number;
  stage: 'landing' | 'trial' | 'signup' | 'tutorial' | 'dashboard';
  tutorial_step?: number;
  checklist: Record<string, boolean>;
  completed_at?: string;
  created_at: string;
  updated_at: string;
}

export interface OnboardingProgressUpdate {
  stage?: string;
  tutorial_step?: number;
  checklist?: Record<string, boolean>;
  completed?: boolean;
}

// Trial Session Types
export interface TrialSession {
  session_id: string;
  original_image_url: string;
  processed_image_url?: string;
  style?: string;
  caption?: string;
  quality_score?: number;
  expires_at: string;
  created_at: string;
  updated_at: string;
}

export interface TrialSessionUploadResponse {
  session_id: string;
  original_image_url: string;
  message: string;
  expires_at: string;
}

// Credit Types
export interface CreditBalance {
  credits: number;
}

export interface CreditTransaction {
  success: boolean;
  new_balance: number;
  message: string;
}

// Prompt Validation Types
export interface PromptValidationRequest {
  prompt: string;
}

export interface PromptValidationResponse {
  is_valid: boolean;
  violation_type?: string;
  message: string;
  flagged_keywords?: string[];
}
