import { api } from '../lib/api';
import type { TrialSession, TrialSessionUploadResponse } from '../types';

export const trialApi = {
  uploadImage: async (
    file: File,
    style?: string
  ): Promise<TrialSessionUploadResponse> => {
    const formData = new FormData();
    formData.append('file', file);
    if (style) {
      formData.append('style', style);
    }

    return api.post('trial/upload', { body: formData }).json();
  },

  getSession: async (sessionId: string): Promise<TrialSession> => {
    return api.get(`trial/${sessionId}`).json();
  },

  deleteSession: async (sessionId: string): Promise<void> => {
    await api.delete(`trial/${sessionId}`);
  },
};
