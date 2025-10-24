import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { imagesApi } from '../services/images';
import type { CaptionGenerateRequest } from '../types';

export const useImages = (projectId?: number) => {
  return useQuery({
    queryKey: ['images', projectId],
    queryFn: () => imagesApi.getAll(projectId),
  });
};

export const useImage = (id: number) => {
  return useQuery({
    queryKey: ['images', id],
    queryFn: () => imagesApi.getById(id),
    enabled: !!id,
  });
};

export const useUploadImage = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      file,
      projectId,
      style,
    }: {
      file: File;
      projectId: number;
      style?: string;
    }) => imagesApi.upload(file, projectId, style),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['images'] });
      queryClient.invalidateQueries({
        queryKey: ['images', variables.projectId],
      });
    },
  });
};

export const useGenerateCaption = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (request: CaptionGenerateRequest) =>
      imagesApi.generateCaption(request),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['images'] });
      queryClient.invalidateQueries({
        queryKey: ['images', variables.image_id],
      });
    },
  });
};

export const useDeleteImage = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: number) => imagesApi.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['images'] });
    },
  });
};
