import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { onboardingApi } from '../services/onboarding';
import { useOnboardingStore } from '../store/onboardingStore';
import type { OnboardingProgressUpdate } from '../types';

export const useOnboardingProgress = () => {
  const setProgress = useOnboardingStore((state) => state.setProgress);

  return useQuery({
    queryKey: ['onboarding', 'progress'],
    queryFn: async () => {
      const progress = await onboardingApi.getProgress();
      setProgress(progress);
      return progress;
    },
  });
};

export const useUpdateOnboardingProgress = () => {
  const queryClient = useQueryClient();
  const setProgress = useOnboardingStore((state) => state.setProgress);

  return useMutation({
    mutationFn: (update: OnboardingProgressUpdate) =>
      onboardingApi.updateProgress(update),
    onSuccess: (data) => {
      setProgress(data);
      queryClient.invalidateQueries({ queryKey: ['onboarding', 'progress'] });
    },
  });
};

export const useUpdateChecklistItem = () => {
  const queryClient = useQueryClient();
  const updateChecklistItem = useOnboardingStore(
    (state) => state.updateChecklistItem
  );

  return useMutation({
    mutationFn: ({ itemKey, completed }: { itemKey: string; completed: boolean }) =>
      onboardingApi.updateChecklistItem(itemKey, completed),
    onSuccess: (data, variables) => {
      updateChecklistItem(variables.itemKey, variables.completed);
      queryClient.invalidateQueries({ queryKey: ['onboarding', 'progress'] });
    },
  });
};
