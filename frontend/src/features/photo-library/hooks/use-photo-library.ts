import { useState } from "react";
import { ApiClient } from "../api-client/api-client";

type PhotoLibraryResult = string;

export const usePhotoLibrary = () => {
  const [results, setResults] = useState<PhotoLibraryResult[]>([]);

  const search = async (query: string) => {
    setResults(await ApiClient.search(query));
  };

  const upload = async (file: File) => {
    await ApiClient.upload(file);
  };

  return { results, search, upload };
};
