import { useEffect } from "react";
import { SearchBar } from "../components/search-bar";
import { usePhotoLibrary } from "../features/photo-library/hooks/use-photo-library";

function App() {
  const { results, search, upload } = usePhotoLibrary();

  useEffect(() => {
    search("");
  }, [search]);

  return (
    <div className="relative block m-auto w-full max-w-lg p-4">
      <SearchBar
        onSearch={async (query) => {
          await search(query);
        }}
        onUpload={async (file) => {
          await upload(file);
        }}
      />
      <div className="grid grid-cols-3 gap-4 mt-4">
        {results.map((url, i) => (
          <div
            key={i}
            className="aspect-square w-full rounded-md bg-center bg-cover"
            style={{ backgroundImage: `url(${url})` }}
          />
        ))}
      </div>
    </div>
  );
}

export default App;
