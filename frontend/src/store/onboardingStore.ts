import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { OnboardingProgress } from '../types';

interface OnboardingState {
  progress: OnboardingProgress | null;
  currentStage: string;
  tutorialStep: number;
  checklist: Record<string, boolean>;
  setProgress: (progress: OnboardingProgress) => void;
  updateStage: (stage: string) => void;
  updateTutorialStep: (step: number) => void;
  updateChecklistItem: (key: string, completed: boolean) => void;
  resetOnboarding: () => void;
}

const initialChecklist = {
  project_created: false,
  image_uploaded: false,
  caption_generated: false,
  image_shared: false,
};

export const useOnboardingStore = create<OnboardingState>()(
  persist(
    (set) => ({
      progress: null,
      currentStage: 'landing',
      tutorialStep: 0,
      checklist: initialChecklist,
      setProgress: (progress) =>
        set({
          progress,
          currentStage: progress.stage,
          tutorialStep: progress.tutorial_step || 0,
          checklist: progress.checklist || initialChecklist,
        }),
      updateStage: (stage) =>
        set((state) => ({
          currentStage: stage,
          progress: state.progress
            ? { ...state.progress, stage: stage as any }
            : null,
        })),
      updateTutorialStep: (step) =>
        set((state) => ({
          tutorialStep: step,
          progress: state.progress
            ? { ...state.progress, tutorial_step: step }
            : null,
        })),
      updateChecklistItem: (key, completed) =>
        set((state) => ({
          checklist: { ...state.checklist, [key]: completed },
          progress: state.progress
            ? {
                ...state.progress,
                checklist: { ...state.progress.checklist, [key]: completed },
              }
            : null,
        })),
      resetOnboarding: () =>
        set({
          progress: null,
          currentStage: 'landing',
          tutorialStep: 0,
          checklist: initialChecklist,
        }),
    }),
    {
      name: 'onboarding-storage',
    }
  )
);
