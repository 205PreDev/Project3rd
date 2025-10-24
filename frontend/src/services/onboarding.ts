import { api } from '../lib/api';
import type { OnboardingProgress, OnboardingProgressUpdate } from '../types';

export const onboardingApi = {
  getProgress: async (): Promise<OnboardingProgress> => {
    return api.get('onboarding/progress').json();
  },

  updateProgress: async (
    update: OnboardingProgressUpdate
  ): Promise<OnboardingProgress> => {
    return api.patch('onboarding/progress', { json: update }).json();
  },

  updateChecklistItem: async (
    itemKey: string,
    completed: boolean
  ): Promise<OnboardingProgress> => {
    return api
      .post('onboarding/checklist', {
        json: { item_key: itemKey, completed },
      })
      .json();
  },
};
