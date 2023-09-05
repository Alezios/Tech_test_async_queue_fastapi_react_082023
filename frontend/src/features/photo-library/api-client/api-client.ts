export const ApiClient = {
  search: async (query: string) => {
    const response = await fetch(`https://localhost:8000/image/search?${query}`, {
      method: 'GET',
    })
    const data = await response.json()
    return data.items.map((item: any) => item.name);
  },

  upload: async (file: File) => {
    //TODO implement
  },
};
