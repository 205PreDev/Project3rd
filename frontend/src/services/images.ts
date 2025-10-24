import { api } from '../lib/api';
import type {
  Image,
  ImageUploadResponse,
  CaptionGenerateRequest,
  CaptionGenerateResponse,
} from '../types';

export const imagesApi = {
  getAll: async (projectId?: number): Promise<Image[]> => {
    const params = projectId ? `?project_id=${projectId}` : '';
    return api.get(`images${params}`).json();
  },

  getById: async (id: number): Promise<Image> => {
    return api.get(`images/${id}`).json();
  },

  upload: async (
    file: File,
    projectId: number,
    style?: string
  ): Promise<ImageUploadResponse> => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('project_id', projectId.toString());
    if (style) {
      formData.append('style', style);
    }

    return api.post('images/upload', { body: formData }).json();
  },

  generateCaption: async (
    request: CaptionGenerateRequest
  ): Promise<CaptionGenerateResponse> => {
    return api.post('images/caption/generate', { json: request }).json();
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`images/${id}`);
  },
};
