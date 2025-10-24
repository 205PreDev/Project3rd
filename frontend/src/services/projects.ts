import { api } from '../lib/api';
import type { Project, ProjectCreate } from '../types';

export const projectsApi = {
  getAll: async (): Promise<Project[]> => {
    return api.get('projects').json();
  },

  getById: async (id: number): Promise<Project> => {
    return api.get(`projects/${id}`).json();
  },

  create: async (data: ProjectCreate): Promise<Project> => {
    return api.post('projects', { json: data }).json();
  },

  update: async (id: number, data: Partial<ProjectCreate>): Promise<Project> => {
    return api.patch(`projects/${id}`, { json: data }).json();
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`projects/${id}`);
  },
};
