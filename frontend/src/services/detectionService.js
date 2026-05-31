import api from './api';

export const detectionService = {
  async detectEmotion(imageFile) {
    const formData = new FormData();
    formData.append('file', imageFile);
    
    const response = await api.post('/detect/emotion', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  async detectAge(imageFile) {
    const formData = new FormData();
    formData.append('file', imageFile);
    
    const response = await api.post('/detect/age', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },
};